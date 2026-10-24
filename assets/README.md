# Profile artwork

Original SVG artwork built for Vj Mabansag's GitHub profile. The diagram is a conceptual illustration of applied-AI interests, not a live model visualization or a claim that every linked project uses a transformer internally.

- `workbench-*`: the profile introduction. Normal versions contain one 4.8-second CSS animation; `*-still.svg` files contain no animation. The README selects still artwork for reduced-motion preferences and links a separate still profile.
- `hydralab-*`: document-to-evidence-to-review workflow illustration.
- `workflow-*`: the source-review and human-judgment sign-off.
- Each figure has light/dark and desktop/mobile layouts, a title/description and an explicit background. No scripts, external fonts, trackers, remote resources or API keys.

Rebuild SVG files with Python 3 and the standard library:

```sh
python3 tools/build_profile.py
```

Professional copy remains ordinary Markdown, so it can be read and updated without running the generator. Update `README.md` and `PROFILE-STILL.md` together when changing copy.
