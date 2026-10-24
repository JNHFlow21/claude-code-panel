"""Renders the README media from `cc-panel` demo data: python3 docs/render.py

Each animation tick becomes an HTML frame, headless Chrome screenshots it and ffmpeg
joins the frames into docs/demo.gif; docs/screenshot.png is the first frame.
"""
import html, os, re, shutil, subprocess, tempfile, time
import importlib.util
from importlib.machinery import SourceFileLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_loader = SourceFileLoader("cc_panel", os.path.join(ROOT, "cc-panel"))
panel = importlib.util.module_from_spec(importlib.util.spec_from_loader("cc_panel", _loader))
_loader.exec_module(panel)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, FRAMES = 1330, 236, 10


def to_html(ansi):
    out, style = [], {}
    for part in re.split(r"(\x1b\[[0-9;]*m)", ansi):
        m = re.fullmatch(r"\x1b\[([0-9;]*)m", part)
        if not m:
            css = ";".join(f"{k}:{v}" for k, v in style.items())
            text = html.escape(part).replace(  # draw the side bar as a block so rows join up
                "▌", f'<span style="display:inline-block;width:.45em;height:1.55em;vertical-align:top;'
                     f'background:{style.get("color", "#D97757")}"></span>')
            out.append(f'<span style="{css}">{text}</span>' if part else "")
            continue
        codes = [int(c) for c in m.group(1).split(";") if c]
        while codes:
            c = codes.pop(0)
            if c == 0:
                style = {}
            elif c == 1:
                style["font-weight"] = "700"
            elif c == 22:
                style.pop("font-weight", None)
            elif c == 38 and codes[:1] == [2]:
                r, g, b = codes[1:4]; codes = codes[4:]
                style["color"] = f"rgb({r},{g},{b})"
            elif c == 39:
                style.pop("color", None)
    return "".join(out)


PAGE = """<!doctype html><meta charset="utf-8"><style>
html,body{{margin:0;background:#141318}}
.win{{margin:14px;border-radius:12px;background:#1B1A20;box-shadow:0 0 0 1px #2c2b31;overflow:hidden}}
.bar{{height:30px;display:flex;gap:8px;align-items:center;padding-left:14px}}
.bar i{{width:12px;height:12px;border-radius:50%;display:block}}
pre{{margin:0;padding:6px 22px 20px;font:15px/1.55 "SF Mono",Menlo,monospace;color:#D6D2C4}}
.rule{{color:#3a3940}}</style>
<div class="win"><div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div>
<pre><span class="rule">{rule}</span>
<span style="color:#87867F">❯</span>
<span class="rule">{rule}</span>
{panel}</pre></div>"""


def main():
    tmp = tempfile.mkdtemp()
    j, d, (first, tool), busy, fable_at = panel.demo()
    start = int(time.time()) // 10 * 10 + panel.SPIN.index("✻")  # first frame shows ✻
    for i in range(FRAMES):
        page = PAGE.format(rule="─" * 130, panel=to_html(panel.render(j, d, first, tool, busy, fable_at, start + i)))
        src = os.path.join(tmp, f"{i:02d}.html")
        open(src, "w").write(page)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        f"--window-size={W},{H}", f"--screenshot={tmp}/{i:02d}.png", f"file://{src}"],
                       check=True, capture_output=True)
    shutil.copy(f"{tmp}/00.png", os.path.join(ROOT, "docs/screenshot.png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", f"{tmp}/%02d.png", "-vf",
                    f"scale={W}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse",
                    "-loop", "0", os.path.join(ROOT, "docs/demo.gif")], check=True)


if __name__ == "__main__":
    main()
