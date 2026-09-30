"""Brackwater match harness (public source).  Used by run_local.py and score.py.

Submitted bots always run in a fresh child process per game (bot_runner.py) that never sees
the engine state.  The harness enforces the compute limits below; any crash, exception,
malformed/illegal action or limit breach forfeits the game for that bot.
"""
import importlib.util
import json
import multiprocessing as mp
import os
import resource
import select
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import brackwater_engine as bw  # noqa: E402  (compiled engine, shipped without source)

LIMITS = {
    "game_cpu": 3.0,      # total CPU seconds of the bot process per game (start-up, imports, __init__, all act calls)
    "move_cpu": 0.25,     # CPU seconds per act() call
    "startup_wall": 20.0,  # wall seconds to start, import and construct Bot
    "move_wall": 3.0,     # wall seconds per act() round trip (guards against sleeping/blocking)
    "memory_mb": 2048,    # address-space limit of the bot process
}

_CLK = os.sysconf("SC_CLK_TCK") if hasattr(os, "sysconf") else 100


def _proc_cpu(pid):
    try:
        with open("/proc/%d/stat" % pid) as fh:
            s = fh.read()
        rest = s[s.rindex(")") + 2:].split()
        return (int(rest[11]) + int(rest[12])) / _CLK
    except (OSError, ValueError, IndexError):
        return None


class Forfeit(Exception):
    pass


class _LineReader:
    def __init__(self, fd):
        self.fd = fd
        self.buf = b""

    def readline(self, timeout):
        deadline = time.monotonic() + timeout
        while b"\n" not in self.buf:
            rem = deadline - time.monotonic()
            if rem <= 0:
                raise Forfeit("wall-clock timeout (%.1fs)" % timeout)
            r, _, _ = select.select([self.fd], [], [], rem)
            if not r:
                raise Forfeit("wall-clock timeout (%.1fs)" % timeout)
            chunk = os.read(self.fd, 1 << 16)
            if not chunk:
                raise Forfeit("bot process exited unexpectedly")
            self.buf += chunk
        line, self.buf = self.buf.split(b"\n", 1)
        return line


class SubprocessBot:
    """A submitted bot running in its own process under the LIMITS."""

    def __init__(self, bot_path, player, game_info, limits=None, show_stderr=False):
        self.limits = dict(LIMITS, **(limits or {}))
        self.cpu_reported = 0.0
        self.max_move_cpu = 0.0
        self.proc = None
        env = dict(os.environ)
        env.update({"PYTHONHASHSEED": "0", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
                    "MKL_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"})
        mem = int(self.limits["memory_mb"]) * 1024 * 1024

        def _pre():
            try:
                resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
            except (ValueError, OSError):
                pass

        self.proc = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "bot_runner.py"), os.path.abspath(bot_path),
             repr(float(self.limits["move_cpu"]))],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=None if show_stderr else subprocess.DEVNULL,
            env=env, cwd=os.path.dirname(os.path.abspath(bot_path)), preexec_fn=_pre)
        self.reader = _LineReader(self.proc.stdout.fileno())
        self._send({"type": "init", "player": player, "game_info": game_info})
        msg = self._recv(self.limits["startup_wall"])
        if "error" in msg:
            raise Forfeit(msg["error"])
        self._check_game_cpu()

    def _send(self, obj):
        try:
            self.proc.stdin.write((json.dumps(obj, separators=(",", ":")) + "\n").encode())
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            raise Forfeit("bot process exited unexpectedly")

    def _recv(self, timeout):
        line = self.reader.readline(timeout)
        try:
            msg = json.loads(line)
        except ValueError:
            raise Forfeit("protocol error (bad JSON from bot process)")
        if not isinstance(msg, dict):
            raise Forfeit("protocol error")
        return msg

    def cpu(self):
        c = _proc_cpu(self.proc.pid)
        return self.cpu_reported if c is None else c

    def _check_game_cpu(self):
        c = self.cpu()
        if c > self.limits["game_cpu"]:
            raise Forfeit("per-game CPU budget (%.1fs) exceeded (%.2fs)" % (self.limits["game_cpu"], c))

    def send_obs(self, obs):
        self._c0 = self.cpu()
        self._send({"type": "obs", "obs": obs})

    def recv_action(self):
        msg = self._recv(self.limits["move_wall"])
        if "error" in msg:
            raise Forfeit(msg["error"])
        if "action" not in msg:
            raise Forfeit("protocol error (no action)")
        mc = float(msg.get("cpu", 0.0))
        self.cpu_reported += mc
        c1 = self.cpu()
        if c1 - self._c0 > self.limits["move_cpu"] + 0.05:  # /proc has 10 ms granularity
            raise Forfeit("per-move CPU limit (%.3fs) exceeded" % self.limits["move_cpu"])
        self.max_move_cpu = max(self.max_move_cpu, mc)
        self._check_game_cpu()
        return msg["action"]

    def close(self):
        if self.proc is not None:
            try:
                self.proc.kill()
            except OSError:
                pass
            try:
                self.proc.wait(timeout=5)
            except Exception:
                pass
            for f in (self.proc.stdin, self.proc.stdout):
                try:
                    f.close()
                except Exception:
                    pass
            self.proc = None


class InProcessBot:
    """A trusted bot class run inside the harness process (reference bots only)."""

    def __init__(self, cls, player, game_info):
        t0 = time.process_time()
        self.bot = cls(player, json.loads(json.dumps(game_info)))
        self.cpu_used = time.process_time() - t0
        self.max_move_cpu = 0.0
        self._pending = None

    def send_obs(self, obs):
        self._pending = obs

    def recv_action(self):
        t0 = time.process_time()
        try:
            a = self.bot.act(self._pending)
        except Exception as e:  # noqa
            raise Forfeit("act() raised %s: %s" % (type(e).__name__, e))
        dt = time.process_time() - t0
        self.cpu_used += dt
        self.max_move_cpu = max(self.max_move_cpu, dt)
        return a

    def cpu(self):
        return self.cpu_used

    def close(self):
        pass


_CLASS_CACHE = {}


def load_bot_class(path, class_name="Bot"):
    """Import a bot file (trusted, in-process) and return its Bot class."""
    path = os.path.abspath(path)
    key = (path, class_name)
    if key not in _CLASS_CACHE:
        d = os.path.dirname(path)
        if d not in sys.path:
            sys.path.insert(0, d)
        name = "inproc_%d" % len(_CLASS_CACHE)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        _CLASS_CACHE[key] = getattr(mod, class_name)
    return _CLASS_CACHE[key]


def _make_bot(spec, player, game_info, limits, show_stderr):
    kind, path = spec[0], spec[1]
    if kind == "inproc":
        return InProcessBot(load_bot_class(path), player, game_info)
    if kind == "subproc":
        return SubprocessBot(path, player, game_info, limits, show_stderr)
    raise ValueError(kind)


def play_game(map_data, seed, specs, limits=None, show_stderr=False, trace=None):
    """Play one game.  specs[p] = ("subproc", path) or ("inproc", path) for player p.
    Returns a result dict; forfeits are recorded per player."""
    match = bw.Match(map_data, seed)
    bots = [None, None]
    forfeit = [None, None]
    try:
        for p in (0, 1):
            try:
                bots[p] = _make_bot(specs[p], p, match.game_info(p), limits, show_stderr)
            except Forfeit as e:
                forfeit[p] = "startup: %s" % e
            except Exception as e:  # noqa
                forfeit[p] = "startup: %s: %s" % (type(e).__name__, e)
        while not match.done and forfeit == [None, None]:
            obs = [match.observe(0), match.observe(1)]
            for p in (0, 1):
                try:
                    bots[p].send_obs(obs[p])
                except Forfeit as e:
                    forfeit[p] = "turn %d: %s" % (match.turn, e)
            acts = [None, None]
            for p in (0, 1):
                if forfeit[p]:
                    continue
                try:
                    raw = bots[p].recv_action()
                    acts[p] = match.validate(p, raw)
                except Forfeit as e:
                    forfeit[p] = "turn %d: %s" % (match.turn, e)
                except bw.IllegalAction as e:
                    forfeit[p] = "turn %d: illegal action: %s" % (match.turn, e)
            if forfeit != [None, None]:
                break
            match.step(acts)
            if trace is not None:
                trace(match)
    finally:
        cpu = [None, None]
        mmc = [None, None]
        for p in (0, 1):
            if bots[p] is not None:
                try:
                    cpu[p] = bots[p].cpu()
                    mmc[p] = bots[p].max_move_cpu
                except Exception:
                    pass
                bots[p].close()
    res = match.result()
    if forfeit[0] and forfeit[1]:
        winner = None
    elif forfeit[0]:
        winner = 1
    elif forfeit[1]:
        winner = 0
    else:
        winner = res["winner"]
    return {"winner": winner, "grain": res["grain"], "turns": res["turns"], "forfeit": forfeit,
            "cpu": cpu, "max_move_cpu": mmc, "stats": res["stats"]}


# ---------------------------------------------------------------- batch running
def _job(args):
    job_id, map_data, seed, specs, limits = args
    t0 = time.time()
    r = play_game(map_data, seed, specs, limits)
    r["job"] = job_id
    r["wall"] = time.time() - t0
    return r


def run_jobs(jobs, workers=None, progress=True):
    """jobs: list of (job_id, map_data, seed, specs, limits).  Returns results in job order."""
    workers = workers or max(1, (os.cpu_count() or 2))
    out = {}
    n = len(jobs)
    t0 = time.time()
    if workers == 1:
        it = map(_job, jobs)
        pool = None
    else:
        pool = mp.get_context("fork").Pool(workers)
        it = pool.imap_unordered(_job, jobs, chunksize=1)
    try:
        for i, r in enumerate(it, 1):
            out[r["job"]] = r
            if progress and (i % 50 == 0 or i == n):
                el = time.time() - t0
                sys.stderr.write("  %d/%d games  (%.0fs elapsed, ~%.0fs left)\n" % (i, n, el, el / i * (n - i)))
                sys.stderr.flush()
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return [out[j[0]] for j in jobs]
