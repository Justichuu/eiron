# eiron

A decision engine for irony, and the paper it generates.

Open `index.html`. One file, offline, no network, no storage, no model. Answer
what you can about a case, leave the rest unknown, and it tells you which names
apply, which are undecided, and which are ruled out and by exactly which answer.

Read `IRON-PAPER.md` for the cohesive version. Both are generated from the same
table, so they cannot drift apart.

## Why it exists

The word *eironeia* began as an insult. An *eiron* is a dissembler. When
Thrasymachus throws the word at Socrates in *Republic* 337a he is not admiring a
technique, he is saying stop dodging. Every flattering sense of the word is
built on top of that accusation, and most arguments about irony are really
arguments about which sense is in play.

So the point here is not to be clever about irony. It is to make the
distinctions checkable, so a person can answer eleven plain questions and find
out what they are actually looking at.

## Unknown is an answer

Faces are `1`, `0`, and `U`. If a kind's signature needs an answer you marked
unknown, that kind comes back **undecided**, naming the question that would
settle it. It never becomes a yes.

That is not a technicality, it is the argument. A system with only true and
false has to answer every question, so it answers some of them falsely.

## The one distinction that does the work

A lie and verbal irony have the same shape: said one thing, meant another. They
differ by a single answer. **The lie needs the gap to go unnoticed. The irony
needs it noticed.** Intent to be caught is the whole boundary between deceiving
someone and telling them something.

Everything else in the table is taxonomy. That line is the ethics.

## Use it

```
python -m eiron build     regenerate IRON-PAPER.md and index.html
python -m eiron ask       sort one case at the prompt
python -m eiron table     print the taxonomy
python -m pytest tests/   prove the page and the engine agree
```

## The tests are the interesting part

The taxonomy lives in one table, but the sorting rule is written twice: Python
for the command line, JavaScript so the page runs offline with no server. Two
implementations of one rule is exactly where a document quietly stops matching
its own tool.

So `tests/test_agreement.py` runs both over 303 generated answer sets and fails
if a single case sorts differently. Then it plants a deliberate bug in the
JavaScript and fails if that is **not** caught, because a checker never seen to
fail proves nothing.

One of those tests failed for a good reason and the story is in section 7 of the
paper. The rule "the page must contain no `fetch(`" failed on the page's own
footer, which invites the reader to search for `fetch(` and find nothing. The
sentence denying the thing contained the thing. Mention is not use, which is the
subject of the paper happening to the paper.

## Layout

```
eiron/kinds.py     the table. Everything else is generated from it.
eiron/engine.py    the decision procedure. 1 / 0 / U.
eiron/wisdom.py    cleverness, money, and what wisdom is.
eiron/build.py     writes the paper and the page.
tests/             proves the two implementations agree.
IRON-PAPER.md      generated
index.html         generated
```

Edit the table, run the build, and the prose and the tool move together or
neither moves.

MIT.
