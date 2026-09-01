"""The page and the engine must agree, and this is how that is known.

The taxonomy lives in one table, but the sorting rule is written twice: once in
Python for the command line, once in JavaScript so the page can run offline with
no server. Two implementations of one rule is exactly the situation where a
document quietly stops matching its own tool.

So the rule is not trusted, it is checked. This runs both implementations over
several hundred generated answer sets, including every all-unknown and
all-decided extreme, and fails if a single case sorts differently.

A checker that has never been seen to fail proves nothing, so it also plants a
deliberate disagreement and fails if that is not caught.
"""

from __future__ import annotations

import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from eiron import build  # noqa: E402
from eiron.engine import classify  # noqa: E402
from eiron.kinds import QUESTIONS  # noqa: E402

NODE = shutil.which("node")


def cases(n: int = 300) -> list[dict]:
    keys = [k for k, _ in QUESTIONS]
    out = [{k: "U" for k in keys}, {k: 1 for k in keys}, {k: 0 for k in keys}]
    rng = random.Random(20260831)
    for _ in range(n):
        out.append({k: rng.choice([1, 0, "U"]) for k in keys})
    return out


def js_sort(script_body: str, batch: list[dict]) -> list[dict]:
    """Run the page's own classify() under node over every case."""
    runner = script_body + """
var BATCH = %s;
var OUT = BATCH.map(function(a){
  var r = classify(a);
  return { applies: r.applies.map(function(v){return v.k.key;}).sort(),
           undecided: r.undecided.map(function(v){return v.k.key;}).sort(),
           excluded: r.excluded.map(function(v){return v.k.key;}).sort() };
});
console.log(JSON.stringify(OUT));
""" % json.dumps(batch)
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "run.js"
        f.write_text(runner, encoding="utf-8")
        r = subprocess.run([NODE, str(f)], capture_output=True, text=True)
        if r.returncode != 0:
            raise AssertionError("node failed:\n" + r.stderr)
        return json.loads(r.stdout)


def py_sort(answers: dict) -> dict:
    r = classify(answers)
    return {k: sorted(v.key for v in r[k])
            for k in ("applies", "undecided", "excluded")}


def page_script() -> str:
    """The exact JavaScript the published page carries, minus the DOM call."""
    html = build.page()
    body = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    return body.replace("render();", "")


class PageMatchesEngine(unittest.TestCase):
    @unittest.skipIf(NODE is None, "node is not on PATH")
    def test_every_case_sorts_the_same_in_both(self):
        batch = cases()
        got = js_sort(page_script(), batch)
        self.assertEqual(len(got), len(batch))
        for answers, js in zip(batch, got):
            self.assertEqual(py_sort(answers), js,
                             "page and engine disagree on %r" % answers)

    @unittest.skipIf(NODE is None, "node is not on PATH")
    def test_the_comparison_can_fail(self):
        """Plant a real disagreement. If this passes, the test above is empty."""
        broken = page_script().replace(
            'else if (given !== k.signature[q] && failed === null)',
            'else if (false && given !== k.signature[q] && failed === null)')
        self.assertNotEqual(broken, page_script(), "the sabotage did not apply")
        got = js_sort(broken, cases(40))
        differs = any(py_sort(a) != j for a, j in zip(cases(40), got))
        self.assertTrue(differs, "a broken page still matched the engine")


class TheTableHolds(unittest.TestCase):
    def test_unknown_never_becomes_a_yes(self):
        keys = [k for k, _ in QUESTIONS]
        r = classify({k: "U" for k in keys})
        self.assertEqual(r["applies"], [], "all unknown produced a verdict")
        self.assertTrue(r["undecided"], "all unknown decided nothing at all")

    def test_lie_and_verbal_irony_part_on_one_answer(self):
        """The claim the paper rests on, checked rather than asserted."""
        base = dict(said_meant=1, stable=1, hostile=0)
        lie = classify({**base, "meant_caught": 0})
        iro = classify({**base, "meant_caught": 1})
        self.assertIn("lie", [v.key for v in lie["applies"]])
        self.assertNotIn("verbal", [v.key for v in lie["applies"]])
        self.assertIn("verbal", [v.key for v in iro["applies"]])
        self.assertNotIn("lie", [v.key for v in iro["applies"]])

    def test_generated_files_are_reproducible(self):
        self.assertEqual(build.book(), build.book())
        self.assertEqual(build.page(), build.page())

    def test_the_page_makes_no_network_call(self):
        """Check the code, not the prose.

        The first version of this test searched the whole file and failed,
        because the footer tells the reader to search for the very string it
        was banning. A page that says "you will not find fetch here" contains
        the characters "fetch". That is a false positive from grepping a
        document instead of reading its code, and it is the same trap the
        audit tool in the neighbouring project documents under "Why it is not
        grep". So this looks inside the script and the attributes, where a
        network call would actually have to live.
        """
        html = build.page()
        script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
        for banned in ("fetch(", "XMLHttpRequest", "localStorage",
                       "sendBeacon", "WebSocket", "import("):
            self.assertNotIn(banned, script, "script calls " + banned)
        external = re.findall(r'(?:src|href)\s*=\s*["\'](?!#)([^"\']+)', html)
        self.assertEqual(external, [], "page loads something external")


if __name__ == "__main__":
    unittest.main(verbosity=2)
