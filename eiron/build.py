"""Generate the book and the app from the tables in kinds.py and wisdom.py.

Nothing about the taxonomy is written twice. The paper and the page are both
outputs. Edit the table, run this, and the prose and the tool move together or
neither moves. A statement that can drift from its own evidence is the thing
this whole repository is arguing against.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import wisdom
from .engine import DISCRIMINATOR
from .kinds import KINDS, QUESTIONS

ROOT = Path(__file__).resolve().parent.parent

FACE_WORD = {1: "yes", 0: "no"}

OPENING = """A paper about feigned ignorance, which feigns nothing.

Lead is soft, and it is what you use when you want a thing to be heavy rather
than strong. This one is iron. Every claim below names its source, every
distinction is a question you can answer yourself, and the machine that sorts
them is in the same folder and will contradict this text if this text is wrong.

There is an obvious joke available here, that a document about irony ought to
mean the opposite of what it says. It declines. The joke is the point: the only
honest paper on this subject is one that says exactly what it means, because
the subject is what happens when people do not."""

TODAY = """Irony stopped being a device and became weather.

Booth in 1974 could still describe a stable kind, where you flip the sentence
and find the meaning waiting underneath, and an unstable kind where nothing is
waiting. Hutcheon in 1994 described the next stage, in which the quotation marks
never come off, and there is no original being quoted.

The cost is specific and it is not aesthetic. Stable irony is a way of telling
someone something. Saturated irony is a way of never being answerable for
anything, because nothing was ever asserted. That is why Wallace in 1993 called
it a cage rather than a liberation, and why the move that reads as radical now
is meaning it.

Which is the situation the last row of the table describes. Sincerity, in a room
where everyone is protected, is the only remaining way to be caught."""

INCIDENT = """The test suite for this repository includes one rule: the page
must make no network call. The first version of that rule searched the whole
file for the string fetch( and failed immediately.

It failed because the page's own footer invites the reader to search it for
fetch( and find nothing. The sentence denying the thing contained the thing.
The checker was reading a document and reporting on code, and those are not the
same object.

This is worth recording because it is the subject of this paper happening to the
paper. A claim was made in good faith, in plain language, with no intent to
mislead, and a literal reader still got the wrong answer, because the mention of
a word and the use of a word are different acts. Verbal irony depends on that
difference and so does every quotation, every joke, and every denial.

The fix was not to delete the sentence. The fix was to make the checker look
inside the script and the attributes, where a network call would have to live,
and leave the prose alone. A checker that cannot tell mention from use will
either miss the real thing or convict the honest one, and it does both for the
same reason."""

NOT_CLAIMED = """This paper does not claim that the table is complete. It claims
that each row in it is checkable.

It does not settle whether Socrates was honest. It marks that unknown, on
purpose, and the engine will keep marking it unknown until someone supplies the
answer rather than the confidence.

It does not claim that irony is bad. Two of the rows are how literature works.

It claims one thing only, and it is the line the engine enforces: the difference
between deceiving a person and telling them something is whether you meant the
gap to be found."""


def book() -> str:
    """The Iron Paper. One cohesive statement, generated from the tables."""
    L = ["# The Iron Paper", "",
         "*On eironeia, cleverness, and what is left when the joke stops.*", "",
         OPENING, "", "---", "",
         "## 1. The word began as an accusation", "",
         "Eironeia is not a compliment in Greek. An eiron is a dissembler, the one "
         "who understates what he is. His opposite is the alazon, the braggart who "
         "overstates, and Aristotle puts truthfulness between them as the mean "
         "(Nicomachean Ethics 1108a, and Book IV.7).",
         "",
         "When Thrasymachus throws the word at Socrates in Republic 337a he is not "
         "admiring a technique. He is saying: stop dodging. Every later sense of "
         "the word, including the flattering ones, is built on top of that insult.",
         "", "---", "",
         "## 2. The table", "",
         "Eleven rows, oldest first. The order is the argument: the word starts as "
         "an insult and ends as a condition of the age. Each row lists the answers "
         "that must hold, so each row is a claim you can test rather than a "
         "definition you must accept.", ""]

    for i, k in enumerate(KINDS, 1):
        sig = ", ".join("%s: %s" % (dict(QUESTIONS)[q].rstrip("."), FACE_WORD[v])
                        for q, v in k.signature.items())
        L += ["### 2.%d %s" % (i, k.name), "",
              "*%s* &middot; %s" % (k.greek, k.era), "",
              k.gloss, "",
              "**Not to be confused with:** %s" % k.not_this, "",
              "**Holds when:** %s" % sig, "",
              "**Source:** %s" % k.source, ""]

    L += ["---", "", "## 3. The distinction that does the work", "",
          DISCRIMINATOR, "",
          "This is the only place in the table where two rows share a shape and "
          "part on a single answer, and it is not a technicality. It is the whole "
          "ethical content of the subject. Everything else here is taxonomy.",
          "", "---", "",
          "## 4. Cleverness, money, and wisdom", "",
          "*%s*" % wisdom.THESIS, ""]
    for i, s in enumerate(wisdom.STEPS, 1):
        L += ["### 4.%d %s" % (i, s["head"]), "", s["body"], "",
              "> %s" % s["keep"], ""]
    L += [wisdom.CLOSING, "", "---", "",
          "## 5. Today", "", TODAY, "", "---", "",
          "## 6. What this paper does not claim", "", NOT_CLAIMED, "", "---", "",
          "## 7. One that happened while this was written", "", INCIDENT, "",
          "---", "", "## 8. Sources", ""]
    for k in KINDS:
        L.append("- **%s** &mdash; %s" % (k.name, k.source))
    L += ["", "Generated from `eiron/kinds.py` and `eiron/wisdom.py` by "
          "`python -m eiron build`. If the table and this paper ever disagree, "
          "the table is right and this file is stale.", ""]
    return "\n".join(L).replace("&mdash;", ",").replace("&middot;", "-")


PAGE_CSS = """
:root{--paper:#f7f4ef;--ink:#181320;--muted:#5f5870;--line:#ddd5ca;--hot:#b23a2e;--ok:#1f7a4d}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font:17px/1.55 Georgia,"Iowan Old Style",serif;padding:0 18px 80px}
main{max-width:44rem;margin:0 auto}
h1{font-size:clamp(30px,6vw,44px);margin:38px 0 4px;letter-spacing:-.5px}
h2{font-size:24px;margin:38px 0 8px;border-top:1px solid var(--line);padding-top:22px}
h3{font-size:18px;margin:24px 0 4px}
.sub{color:var(--muted);margin:0 0 8px;font-style:italic}
.q{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:8px 0;
 background:#fff;display:flex;gap:10px;align-items:center;justify-content:space-between}
.q p{margin:0;flex:1}
.faces{display:flex;gap:5px;flex:0 0 auto}
button{font:inherit;font-size:14px;border:1px solid var(--line);background:#fff;
 border-radius:7px;padding:5px 11px;cursor:pointer;color:var(--muted)}
button[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
#out{margin-top:16px}
.card{border:1px solid var(--line);border-left-width:5px;border-radius:9px;
 padding:11px 14px;margin:9px 0;background:#fff}
.yes{border-left-color:var(--ok)} .unk{border-left-color:#b8a13e} .no{border-left-color:var(--line);opacity:.62}
.card b{display:block;font-size:17px} .card small{color:var(--muted);display:block;margin-top:3px}
.verdict{background:var(--ink);color:var(--paper);border-radius:10px;padding:13px 16px;margin:14px 0}
.row{border-bottom:1px solid var(--line);padding:14px 0}
.row .sig{color:var(--muted);font-size:14px}
blockquote{margin:10px 0;padding:7px 0 7px 14px;border-left:3px solid var(--hot);
 color:var(--ink);font-style:italic}
.foot{color:var(--muted);font-size:14px;margin-top:44px;border-top:1px solid var(--line);padding-top:14px}
@media (prefers-color-scheme:dark){
 :root{--paper:#14121a;--ink:#efeaf5;--muted:#a49bb4;--line:#332c3e;--hot:#ff7a68;--ok:#4fd08a}
 .q,.card{background:#1b1824}
 button{background:#1b1824}
 .verdict{background:#efeaf5;color:#14121a}}
"""

PAGE_JS = """
// Same rule as eiron/engine.py. The data below is generated from the same
// table, and tests/test_agreement.py runs this file against the Python engine
// on hundreds of random inputs to prove the two cannot drift apart.
var A = {};
function setFace(key, face, btn){
  A[key] = face;
  var wrap = btn.parentNode;
  for (var i=0;i<wrap.children.length;i++) wrap.children[i].setAttribute("aria-pressed","false");
  btn.setAttribute("aria-pressed","true");
  render();
}
function classify(answers){
  var applies=[], undecided=[], excluded=[];
  for (var i=0;i<KINDS.length;i++){
    var k=KINDS[i], missing=[], failed=null;
    for (var q in k.signature){
      var given = answers[q];
      if (given === undefined || given === "U") missing.push(q);
      else if (given !== k.signature[q] && failed === null)
        failed = QT[q]+" is "+given+", this needs "+k.signature[q];
    }
    if (failed) excluded.push({k:k, why:failed});
    else if (missing.length) undecided.push({k:k, why:missing.map(function(q){return "unknown: "+QT[q];})});
    else applies.push({k:k});
  }
  return {applies:applies, undecided:undecided, excluded:excluded};
}
function render(){
  var r = classify(A), h = "";
  var line;
  if (!r.applies.length && !r.undecided.length)
    line = "No kind in the table fits. That is a real answer: not everything is irony.";
  else if (!r.applies.length)
    line = "Nothing decided. "+r.undecided.length+" kinds wait on an answer you left unknown.";
  else {
    line = r.applies.map(function(v){return v.k.name;}).join(", ");
    line += r.undecided.length ? ". And "+r.undecided.length+" more cannot be decided yet."
                               : ". Nothing left unknown.";
  }
  h += '<div class="verdict">'+line+'</div>';
  r.applies.forEach(function(v){
    h += '<div class="card yes"><b>'+v.k.name+'</b>'+v.k.gloss+
         '<small>Not: '+v.k.not_this+'</small><small>'+v.k.source+'</small></div>';});
  r.undecided.forEach(function(v){
    h += '<div class="card unk"><b>'+v.k.name+' &mdash; undecided</b><small>'+
         v.why.join('<br>')+'</small></div>';});
  r.excluded.forEach(function(v){
    h += '<div class="card no"><b>'+v.k.name+' &mdash; ruled out</b><small>'+v.why+'</small></div>';});
  document.getElementById("out").innerHTML = h;
}
"""


def page() -> str:
    kinds_js = json.dumps([dict(key=k.key, name=k.name, gloss=k.gloss,
                                not_this=k.not_this, source=k.source,
                                signature=k.signature) for k in KINDS])
    qt_js = json.dumps(dict(QUESTIONS))
    qs = "".join(
        '<div class="q"><p>%s</p><div class="faces">'
        '<button onclick="setFace(\'%s\',1,this)" aria-pressed="false">yes</button>'
        '<button onclick="setFace(\'%s\',0,this)" aria-pressed="false">no</button>'
        '<button onclick="setFace(\'%s\',\'U\',this)" aria-pressed="true">unknown</button>'
        "</div></div>" % (text, key, key, key)
        for key, text in QUESTIONS)

    rows = "".join(
        '<div class="row"><b>%s</b> <span class="sig">%s - %s</span><br>%s'
        '<br><span class="sig">Not: %s</span><br><span class="sig">%s</span></div>'
        % (k.name, k.greek, k.era, k.gloss, k.not_this, k.source) for k in KINDS)

    steps = "".join("<h3>%s</h3><p>%s</p><blockquote>%s</blockquote>"
                    % (s["head"], s["body"], s["keep"]) for s in wisdom.STEPS)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Iron Paper</title>
<meta name="description" content="A decision engine for irony, and a paper that means what it says. Offline, no network, no model.">
<style>{PAGE_CSS}</style></head><body><main>

<h1>The Iron Paper</h1>
<p class="sub">On eironeia, cleverness, and what is left when the joke stops.</p>
<p>Answer what you can. Leave the rest unknown. Unknown is a real answer here,
and the engine will not turn it into a yes.</p>

<h2>Sort a case</h2>
{qs}
<div id="out"></div>

<h2>The distinction that does the work</h2>
<p>{DISCRIMINATOR}</p>

<h2>The table</h2>
{rows}

<h2>Cleverness, money, and wisdom</h2>
<p class="sub">{wisdom.THESIS}</p>
{steps}
<p>{wisdom.CLOSING}</p>

<h2>Today</h2>
{"".join("<p>%s</p>" % p for p in TODAY.split(chr(10) + chr(10)))}

<h2>What this paper does not claim</h2>
{"".join("<p>%s</p>" % p for p in NOT_CLAIMED.split(chr(10) + chr(10)))}

<p class="foot">One file. No network, no storage, no model. Search it for
<code>fetch(</code> and you will not find one. Generated from
<code>eiron/kinds.py</code> by <code>python -m eiron build</code>.</p>
</main>
<script>var KINDS={kinds_js};var QT={qt_js};{PAGE_JS}render();</script>
</body></html>
"""


def write_all(root: Path | None = None) -> list[Path]:
    root = Path(root or ROOT)
    out = []
    p = root / "IRON-PAPER.md"
    p.write_text(book(), encoding="utf-8")
    out.append(p)
    p = root / "index.html"
    p.write_text(page(), encoding="utf-8")
    out.append(p)
    return out
