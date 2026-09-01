"""The decision procedure. Deterministic, no model, no network.

Give it answers, get back which names apply, which are blocked by something you
do not know, and which are ruled out and by exactly which answer.

The rule that matters: an answer of U does not become a guess. If a kind's
signature needs an answer you have marked unknown, that kind comes back
UNDECIDED and says which question would settle it. A verdict this engine cannot
reach is reported as unreached, never as a no.
"""

from __future__ import annotations

from dataclasses import dataclass

from .kinds import KINDS, QUESTION_TEXT

TRUE, FALSE, UNKNOWN = 1, 0, "U"
FACES = (TRUE, FALSE, UNKNOWN)


def parse_face(value) -> int | str:
    """Accept 1/0/U in the shapes a person actually types."""
    if value in (1, "1", True, "y", "yes", "t", "true"):
        return TRUE
    if value in (0, "0", False, "n", "no", "f", "false"):
        return FALSE
    if value in ("U", "u", None, "", "?", "unknown"):
        return UNKNOWN
    raise ValueError("A face is 1, 0, or U. Got: %r" % (value,))


@dataclass(frozen=True)
class Verdict:
    key: str
    name: str
    face: int | str          # 1 applies, 0 excluded, U undecided
    because: tuple           # the questions that decided it


def _check(kind, answers: dict) -> Verdict:
    missing, failed = [], []
    for question, required in kind.signature.items():
        given = answers.get(question, UNKNOWN)
        if given == UNKNOWN:
            missing.append(question)
        elif given != required:
            failed.append((question, given, required))
    if failed:
        q, given, required = failed[0]
        return Verdict(kind.key, kind.name, FALSE,
                       ("%s is %s, this needs %s" % (QUESTION_TEXT[q], given, required),))
    if missing:
        return Verdict(kind.key, kind.name, UNKNOWN,
                       tuple("unknown: " + QUESTION_TEXT[q] for q in missing))
    return Verdict(kind.key, kind.name, TRUE,
                   tuple("%s is %s" % (QUESTION_TEXT[q], v)
                         for q, v in kind.signature.items()))


def classify(answers: dict) -> dict:
    """Return every kind sorted into applies, undecided, and excluded."""
    clean = {k: parse_face(v) for k, v in answers.items()}
    verdicts = [_check(k, clean) for k in KINDS]
    return {
        "applies": [v for v in verdicts if v.face == TRUE],
        "undecided": [v for v in verdicts if v.face == UNKNOWN],
        "excluded": [v for v in verdicts if v.face == FALSE],
        "answers": clean,
    }


def summary(result: dict) -> str:
    """One honest line about what was reached."""
    applies, undecided = result["applies"], result["undecided"]
    if not applies and not undecided:
        return "No kind in the table fits. That is a real answer: not everything is irony."
    if not applies:
        return ("Nothing decided. %d kinds are waiting on an answer you marked "
                "unknown." % len(undecided))
    names = ", ".join(v.name for v in applies)
    if undecided:
        return ("%s. And %d more cannot be decided until you answer what you "
                "left unknown." % (names, len(undecided)))
    return names + ". Nothing left unknown."


# The distinction that does the most work in this whole table, kept where the
# code can see it and not only the prose.
DISCRIMINATOR = (
    "A lie and verbal irony have the same shape: said one thing, meant another. "
    "They differ by one answer only. The lie needs the gap to go unnoticed. The "
    "irony needs it noticed. Intent to be caught is the whole boundary between "
    "deceiving someone and telling them something."
)
