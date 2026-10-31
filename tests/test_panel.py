import importlib.util, json, os, re, subprocess, sys, unittest, unittest.mock
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
        j, d, (first, tool), busy, fable_at, q = panel.demo()
        return plain(panel.render(j, d, first, tool, busy, fable_at, now, q)).split("\n")

    def test_columns_align(self):
        rows = self.rows()
        self.assertEqual(len(rows), 8)  # Claude block, hairline, GPT, Grok, Google, DeepSeek
        for a, b in (("CTX", "CACHE"), ("CACHE", "TTL"), ("WK", "FABLE"), ("OUT", "TTFT"),
                     ("TTFT", "TOOL"), ("TOK", "ID"), ("CTX", "BAL")):
            ra = next(r for r in rows if re.search(rf"\b{a}\b", r))
            rb = next(r for r in rows if re.search(rf"\b{b}\b", r))
            self.assertEqual(re.search(rf"\b{a}\b", ra).start(), re.search(rf"\b{b}\b", rb).start(), (a, b))
        self.assertEqual(rows[0].index("Opus"), rows[1].index("$"))
        bars = {m.start() for r in rows[4:7] for m in [re.search(r"[▰▱]{8}", r)]}
        self.assertEqual(bars, {re.search(r"[▰▱]{8}", rows[0]).start()})  # GPT / Grok / Google bars line up with CTX
        self.assertEqual(rows[4].index("RESET"), rows[5].index("Bot"))
        self.assertEqual(rows[5].index("Bot"), rows[6].index("Gemini"))
        self.assertTrue(all(r == r.rstrip() for r in rows))

    def test_ctx_follows_compact_window(self):
        j = {"cwd": "/nonexistent", "context_window": {"context_window_size": 1_000_000, "current_usage": {
            "input_tokens": 2, "cache_creation_input_tokens": 4_998, "cache_read_input_tokens": 320_000}}}
        for env, want in (("650000", "50%"), ("2000000", "32%"), ("100000", "100%")):
            d = {}
            with unittest.mock.patch.dict(os.environ, {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": env}):
                panel.ctx_value(d, j)
            self.assertEqual(d["ctx"], want, env)
        d = {"ctx": "7%"}
        panel.ctx_value(d, {})
        self.assertEqual(d["ctx"], "7%")  # no usage yet: keep ccstatusline's value

    def test_heat_colors(self):
        self.assertEqual(panel.heat("69%", "X"), "X")
        self.assertEqual(panel.heat("70%", "X"), panel.AMBER)
        self.assertEqual(panel.heat("90%", "X"), panel.RED)

    def test_countdown_format(self):
        self.assertEqual(panel.left(59), "0m59s")
        self.assertEqual(panel.left(3700), "1h01m")
        self.assertEqual(panel.left(90000), "1d1h")

    def test_missing_ccstatusline_still_renders(self):
        env = {**os.environ, "CC_PANEL_CCSTATUSLINE": "/nonexistent", "HOME": os.path.join(ROOT, ".test-home"),
               "CC_PANEL_QUOTAS": "0"}
        out = subprocess.run([sys.executable, SCRIPT], input=json.dumps({"session_id": "t"}), env=env,
                             capture_output=True, text=True, timeout=20)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(len(plain(out.stdout).strip("\n").split("\n")), 3)


if __name__ == "__main__":
    unittest.main()
