import importlib.util, json, os, re, subprocess, sys, unittest
from importlib.machinery import SourceFileLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "cc-panel")
_loader = SourceFileLoader("cc_panel", SCRIPT)
panel = importlib.util.module_from_spec(importlib.util.spec_from_loader("cc_panel", _loader))
_loader.exec_module(panel)


def plain(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


class PanelTest(unittest.TestCase):
    def rows(self, now=1_800_000_000):
        j, d, (first, tool), busy, fable_at = panel.demo()
        return plain(panel.render(j, d, first, tool, busy, fable_at, now)).split("\n")

    def test_columns_align(self):
        rows = self.rows()
        self.assertEqual(len(rows), 3)
        for a, b in (("CTX", "CACHE"), ("CACHE", "TTL"), ("5H", "WK"), ("WK", "FABLE"), ("OUT", "TTFT"),
                     ("TTFT", "TOOL"), ("TOK", "ID")):
            ra = next(r for r in rows if re.search(rf"\b{a}\b", r))
            rb = next(r for r in rows if re.search(rf"\b{b}\b", r))
            self.assertEqual(re.search(rf"\b{a}\b", ra).start(), re.search(rf"\b{b}\b", rb).start(), (a, b))
        self.assertEqual(rows[0].index("Opus"), rows[1].index("$"))
        self.assertTrue(all(r == r.rstrip() for r in rows))

    def test_heat_colors(self):
        self.assertEqual(panel.heat("69%", "X"), "X")
        self.assertEqual(panel.heat("70%", "X"), panel.AMBER)
        self.assertEqual(panel.heat("90%", "X"), panel.RED)

    def test_countdown_format(self):
        self.assertEqual(panel.left(59), "0m59s")
        self.assertEqual(panel.left(3700), "1h01m")
        self.assertEqual(panel.left(90000), "1d1h")

    def test_missing_ccstatusline_still_renders(self):
        env = {**os.environ, "CC_PANEL_CCSTATUSLINE": "/nonexistent", "HOME": os.path.join(ROOT, ".test-home")}
        out = subprocess.run([sys.executable, SCRIPT], input=json.dumps({"session_id": "t"}), env=env,
                             capture_output=True, text=True, timeout=20)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(len(plain(out.stdout).strip("\n").split("\n")), 3)


if __name__ == "__main__":
    unittest.main()
