# Contributing

Thanks for helping! Issues and pull requests are welcome.

1. Fork and clone.
2. Run the tests; they are offline and need no Claude Code session:

   ```sh
   python3 -m unittest discover -s tests
   ```

3. Preview layout changes with `python3 cc-panel --demo`. If the look changes, regenerate the demo with `python3 docs/render.py` (needs Chrome and ffmpeg) and include the new `docs/demo.gif`, kept under 3 MB.
4. Keep `cc-panel` a single dependency-free script that works on Python 3.10+.
5. Never commit real session IDs, transcripts, tokens or personal paths in tests or screenshots; use synthetic data.
