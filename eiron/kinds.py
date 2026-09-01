"""The taxonomy. One table, and everything else is generated from it.

Each kind of irony is defined by a signature: the answers that must hold for
that name to apply. A signature is not a vibe. It is a set of yes/no conditions
a person can check, which is the only reason a machine can decide anything here.

Faces are 1 (yes), 0 (no), U (not known). U is a real answer, not a missing one.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Question keys. Each one is a thing a person can answer about a case.
QUESTIONS = [
    ("said_meant", "The words said differ from what was meant."),
    ("expect_out", "What happened differs from what was expected."),
    ("observer_knows", "Someone watching knows what a participant does not."),
    ("meant_caught", "The gap is meant to be noticed."),
    ("professed_ign", "The speaker claims not to know."),
    ("asks", "The method is questioning, not asserting."),
    ("stable", "One real meaning can be recovered underneath."),
    ("self_aware", "The work shows that it knows it is a work."),
    ("hostile", "The aim includes wounding."),
    ("saturated", "It answers an age already soaked in irony."),
]

QUESTION_TEXT = dict(QUESTIONS)


@dataclass(frozen=True)
class Kind:
    key: str
    name: str
    greek: str
    era: str
    source: str
    gloss: str
    not_this: str
    signature: dict = field(default_factory=dict)


# Ordered oldest first. The order is the argument: the word starts as an insult
# and ends as a condition.
KINDS = [
    Kind(
        key="lie",
        name="A lie",
        greek="pseudos",
        era="always",
        source="the boundary case, not a kind of irony",
        gloss="Says one thing, means another, and needs the gap to stay unseen.",
        not_this="Verbal irony. The lie wants to be believed; irony wants to be caught.",
        signature=dict(said_meant=1, meant_caught=0),
    ),
    Kind(
        key="eironeia",
        name="Eironeia, the old insult",
        greek="eironeia",
        era="5th to 4th c. BC",
        source="Aristophanes, Clouds; Plato, Republic 337a, where Thrasymachus "
               "spits the word at Socrates as an accusation of dodging",
        gloss="Dissembling. Understating what you are and what you know, to win.",
        not_this="Socratic method. Here the ignorance is a costume, worn to conceal.",
        signature=dict(said_meant=1, professed_ign=1, meant_caught=0),
    ),
    Kind(
        key="socratic",
        name="Socratic irony",
        greek="eironeia, reclaimed",
        era="5th c. BC, argued over ever since",
        source="Plato, Apology 21d and Symposium 216e; Vlastos, "
               "Socrates: Ironist and Moral Philosopher, 1991",
        gloss="Professed ignorance plus a question, aimed at the other person's "
              "impasse rather than at your own victory.",
        not_this="Eironeia. The disagreement about which one Socrates was doing "
                 "is the oldest live question in this table.",
        signature=dict(professed_ign=1, asks=1, meant_caught=1),
    ),
    Kind(
        key="verbal",
        name="Verbal irony",
        greek="the trope",
        era="1st c. AD onward",
        source="Quintilian, Institutio Oratoria VIII.6.54, irony as a figure "
               "in which the opposite of what is said is understood",
        gloss="Says the opposite and expects you to flip it back.",
        not_this="A lie. This one hands you the key with the lock.",
        signature=dict(said_meant=1, meant_caught=1, stable=1),
    ),
    Kind(
        key="sarcasm",
        name="Sarcasm",
        greek="sarkazein, to tear flesh",
        era="the word carries its own violence",
        source="from Greek sarkazein, literally to strip off flesh",
        gloss="Verbal irony pointed at someone, meant to leave a mark.",
        not_this="Verbal irony in general, which need not wound.",
        signature=dict(said_meant=1, meant_caught=1, hostile=1),
    ),
    Kind(
        key="dramatic",
        name="Dramatic irony",
        greek="tragic irony",
        era="named 1833, practised since Sophocles",
        source="Connop Thirlwall, On the Irony of Sophocles, 1833",
        gloss="The watcher knows what the speaker does not. The speaker is sincere.",
        not_this="Verbal irony. Nobody on stage is being clever. That is the point.",
        signature=dict(observer_knows=1, said_meant=0),
    ),
    Kind(
        key="situational",
        name="Situational irony",
        greek="cosmic irony, irony of fate",
        era="19th c.",
        source="the modern sense, at home in Hardy; the one that needs no speaker",
        gloss="The outcome mocks the expectation. No one said anything.",
        not_this="Bad luck. Irony needs the outcome to answer the expectation, "
                 "not merely to disappoint it.",
        signature=dict(expect_out=1, said_meant=0),
    ),
    Kind(
        key="romantic",
        name="Romantic irony",
        greek="the work turns and looks at you",
        era="1797 onward",
        source="Friedrich Schlegel, Lyceum and Athenaeum fragments",
        gloss="The work admits it is a work, and keeps going anyway.",
        not_this="A mistake. The seam is shown on purpose.",
        signature=dict(self_aware=1),
    ),
    Kind(
        key="unstable",
        name="Unstable irony",
        greek="no floor",
        era="1974",
        source="Wayne Booth, A Rhetoric of Irony",
        gloss="The gap is real and there is nothing underneath to recover.",
        not_this="Verbal irony, which promises a stable meaning under the flip.",
        signature=dict(said_meant=1, stable=0),
    ),
    Kind(
        key="postmodern",
        name="Postmodern irony",
        greek="everything in quotation marks",
        era="late 20th c.",
        source="Linda Hutcheon, Irony's Edge, 1994",
        gloss="Irony as the default air, not a move made against a background "
              "of sincerity. Quotation with no original.",
        not_this="Unstable irony alone. This one is a condition, not a device.",
        signature=dict(stable=0, saturated=1),
    ),
    Kind(
        key="post_irony",
        name="Post-irony, new sincerity",
        greek="saying it straight, on purpose, now",
        era="1993 onward",
        source="David Foster Wallace, E Unibus Pluram, 1993; and the "
               "metamodern oscillation described by Vermeulen and "
               "van den Akker, 2010",
        gloss="Meaning it, in an age where meaning it reads as a move. "
              "Sincerity becomes the transgression.",
        not_this="Plain sincerity. This one is sincerity that knows the room.",
        signature=dict(said_meant=0, meant_caught=1, saturated=1),
    ),
]

BY_KEY = {k.key: k for k in KINDS}
