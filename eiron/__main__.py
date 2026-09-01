"""CLI. build the paper and the page, print the table, or sort one case."""
from __future__ import annotations

import sys

from . import build
from .engine import DISCRIMINATOR, classify, summary
from .kinds import KINDS, QUESTIONS


def ask() -> int:
    print("Answer y, n, or press enter for unknown.\n")
    answers = {}
    for key, text in QUESTIONS:
        answers[key] = input("  %s [y/n/enter] " % text).strip() or "U"
    r = classify(answers)
    print("\n" + summary(r) + "\n")
    for v in r["applies"]:
        print("  APPLIES   %s" % v.name)
    for v in r["undecided"]:
        print("  UNDECIDED %s" % v.name)
        for why in v.because:
            print("              %s" % why)
    return 0


def table() -> int:
    for k in KINDS:
        print("%-28s %s" % (k.name, k.gloss))
        print("%-28s not: %s" % ("", k.not_this))
    print("\n" + DISCRIMINATOR)
    return 0


def main(argv=None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    cmd = args[0] if args else "build"
    if cmd == "build":
        for p in build.write_all():
            print("wrote", p)
        return 0
    if cmd == "ask":
        return ask()
    if cmd == "table":
        return table()
    print(__doc__)
    print("usage: python -m eiron [build|ask|table]")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
