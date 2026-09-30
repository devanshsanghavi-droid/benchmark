"""Child-process side of the Brackwater harness (public source).

Launched by harness.py as:  python3 bot_runner.py <path/to/bot.py> <move_cpu_seconds>
Protocol: one JSON object per line on stdin (from harness) / on the original stdout (to harness).
Anything your bot prints goes to stderr, never into the protocol.
"""
import importlib.util
import json
import os
import signal
import sys
import time
import traceback

PUBLIC_DIR = os.path.dirname(os.path.abspath(__file__))


class _MoveTimeout(BaseException):
    pass


def _on_sigprof(signum, frame):
    raise _MoveTimeout()


def _decode_obs(o):
    o["crews"] = {int(k): v for k, v in o["crews"].items()}
    o["enemy_crews"] = {int(k): v for k, v in o["enemy_crews"].items()}
    o["lost_crews"] = {int(k): v for k, v in o["lost_crews"].items()}
    return o


def _scalar(o):
    # numpy scalars (np.int64, np.bool_) -> Python scalars; anything else is an error
    if hasattr(o, "item") and not hasattr(o, "__len__"):
        return o.item()
    raise TypeError("object of type %s is not JSON serialisable" % type(o).__name__)


def _norm(action):
    if isinstance(action, dict) and isinstance(action.get("orders"), dict):
        orders = {}
        for k, v in action["orders"].items():
            if not isinstance(k, (str, int)) and hasattr(k, "__index__"):
                k = k.__index__()
            orders[k] = v
        action = dict(action)
        action["orders"] = orders
    return action


def _fmt(e):
    tb = traceback.extract_tb(e.__traceback__)
    where = ""
    if tb:
        fr = tb[-1]
        where = " at %s:%s" % (os.path.basename(fr.filename), fr.lineno)
    return "%s: %s%s" % (type(e).__name__, str(e)[:300], where)


def main():
    bot_path = os.path.abspath(sys.argv[1])
    move_cpu = float(sys.argv[2])
    fin = sys.stdin.buffer
    fout = os.fdopen(os.dup(1), "wb")
    os.dup2(2, 1)               # bot prints -> stderr
    sys.stdout = sys.stderr
    sys.stdin = open(os.devnull)

    def send(obj):
        fout.write((json.dumps(obj, separators=(",", ":")) + "\n").encode())
        fout.flush()

    def recv():
        line = fin.readline()
        if not line:
            sys.exit(0)
        return json.loads(line)

    signal.signal(signal.SIGPROF, _on_sigprof)
    try:
        sys.path.insert(0, os.path.dirname(bot_path))
        if PUBLIC_DIR not in sys.path:
            sys.path.insert(1, PUBLIC_DIR)
        spec = importlib.util.spec_from_file_location("submitted_bot", bot_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["submitted_bot"] = mod
        spec.loader.exec_module(mod)
        msg = recv()
        bot = mod.Bot(msg["player"], msg["game_info"])
    except BaseException as e:  # noqa
        send({"error": "startup failed: " + _fmt(e)})
        return
    send({"ok": True})
    while True:
        msg = recv()
        if msg.get("type") != "obs":
            return
        obs = _decode_obs(msg["obs"])
        t0 = time.process_time()
        try:
            signal.setitimer(signal.ITIMER_PROF, move_cpu)
            action = bot.act(obs)
            signal.setitimer(signal.ITIMER_PROF, 0)
        except _MoveTimeout:
            send({"error": "per-move CPU limit (%.3fs) exceeded" % move_cpu})
            return
        except BaseException as e:  # noqa
            signal.setitimer(signal.ITIMER_PROF, 0)
            send({"error": "act() raised " + _fmt(e)})
            return
        cpu = time.process_time() - t0
        if cpu > move_cpu:
            send({"error": "per-move CPU limit (%.3fs) exceeded (%.3fs)" % (move_cpu, cpu)})
            return
        try:
            payload = json.dumps({"action": _norm(action), "cpu": cpu}, separators=(",", ":"),
                                 default=_scalar)
        except (TypeError, ValueError) as e:
            send({"error": "action is not JSON-serialisable: " + _fmt(e)})
            return
        fout.write((payload + "\n").encode())
        fout.flush()


if __name__ == "__main__":
    main()
