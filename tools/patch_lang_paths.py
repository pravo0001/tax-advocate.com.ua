"""
Fix language attributes, canonical / alternate URLs, and lang switcher
after copying /uk to /ru and /en. Run from repo: python tools/patch_lang_paths.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rel_prefix(lang_path: Path) -> str:
    parts = lang_path.parts
    depth = len(parts) - 1
    return "../" * depth


def sibling(lang_path: Path, target_lang: str) -> str:
    parts = list(lang_path.parts)
    parts[0] = target_lang
    return "/".join(parts)


def build_switcher(lang_path: Path, active: str) -> str:
    pre = rel_prefix(lang_path)
    parts = list(lang_path.parts)
    tail = "/".join(parts[1:])  # e.g. index.html or blog/foo.html
    aria = {"uk": "Мова сайту", "ru": "Язык сайта", "en": "Site language"}[active]
    if active == "uk":
        block = f"""        <div class="lang-switch" aria-label="{aria}">
          <a class="is-active" href="{pre}uk/{tail}" hreflang="uk">UA</a>
          <a href="{pre}ru/{tail}" hreflang="ru">RU</a>
          <a href="{pre}en/{tail}" hreflang="en">EN</a>
        </div>"""
    elif active == "ru":
        block = f"""        <div class="lang-switch" aria-label="{aria}">
          <a href="{pre}uk/{tail}" hreflang="uk">UA</a>
          <a class="is-active" href="{pre}ru/{tail}" hreflang="ru">RU</a>
          <a href="{pre}en/{tail}" hreflang="en">EN</a>
        </div>"""
    else:
        block = f"""        <div class="lang-switch" aria-label="{aria}">
          <a href="{pre}uk/{tail}" hreflang="uk">UA</a>
          <a href="{pre}ru/{tail}" hreflang="ru">RU</a>
          <a class="is-active" href="{pre}en/{tail}" hreflang="en">EN</a>
        </div>"""
    return block


SWITCH_RE = re.compile(r'<div class="lang-switch"[^>]*>.*?</div>', re.DOTALL)


def patch_file(path: Path, active: str) -> None:
    text = path.read_text(encoding="utf-8")
    web_lang = {"uk": "uk", "ru": "ru", "en": "en"}[active]
    canon_from = {"uk": "/uk/", "ru": "/uk/", "en": "/uk/"}  # replaced below
    _ = canon_from
    text = re.sub(r'<html lang="uk">', f'<html lang="{web_lang}">', text, count=1)
    if active == "ru":
        text = text.replace("https://taxlawyer.com.ua/uk/", "https://taxlawyer.com.ua/ru/")
        text = text.replace('"og:locale" content="uk_UA"', '"og:locale" content="ru_UA"')
        text = text.replace('"inLanguage": "uk"', '"inLanguage": "ru"')
    elif active == "en":
        text = text.replace("https://taxlawyer.com.ua/uk/", "https://taxlawyer.com.ua/en/")
        text = text.replace('"og:locale" content="uk_UA"', '"og:locale" content="en_US"')
        text = text.replace('"inLanguage": "uk"', '"inLanguage": "en"')
    lang_path = Path(path.relative_to(ROOT)).as_posix()
    switch = build_switcher(Path(lang_path), active)
    text, n = SWITCH_RE.subn(switch.strip(), text, count=1)
    if n != 1:
        raise RuntimeError(f"lang-switch not patched: {path}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for lang in ("ru", "en"):
        d = ROOT / lang
        for html in d.rglob("*.html"):
            patch_file(html, lang)
    print("patched:", ROOT)


if __name__ == "__main__":
    main()
