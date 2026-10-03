"""CLI: python -m debrief generate --seed 1 --level 2 [--out item.json] | python -m debrief simulate"""
import argparse
import sys

from .core import coach_prompt, junior_prompt, make_item


def main(argv=None):
    ap = argparse.ArgumentParser(prog="debrief")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--seed", type=int, default=1)
    g.add_argument("--level", type=int, default=2, choices=[1, 2, 3])
    g.add_argument("--out")
    g.add_argument("--show-prompts", action="store_true")
    sub.add_parser("simulate")
    a = ap.parse_args(argv)
    if a.cmd == "simulate":
        from .simulate import main as sim
        return sim()
    item = make_item(a.seed, a.level)
    if a.out:
        open(a.out, "w").write(item.to_json())
    print(item.spec)
    if a.show_prompts:
        print("\n=== JUNIOR PRACTICE PROMPT ===\n" + junior_prompt(item, item.practice, None))
        print("\n=== COACH PROMPT (with oracle answers as placeholder log) ===\n" + coach_prompt(item, item.practice_key))


if __name__ == "__main__":
    sys.exit(main())
