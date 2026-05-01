"""Repair canonical / hreflang / og:url after language copies. Primary x-default → Ukrainian."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://taxlawyer.com.ua"


def page_url(lang: str, segments: list[str]) -> str:
    if segments == ["index.html"] or segments == []:
        return f"{BASE}/{lang}/"
    if segments == ["blog", "index.html"]:
        return f"{BASE}/{lang}/blog/"
    tail = "/".join(segments)
    return f"{BASE}/{lang}/{tail}"


def og_locale(lang: str) -> str:
    return {"uk": "uk_UA", "ru": "ru_UA", "en": "en_US"}[lang]


def html_lang(lang: str) -> str:
    return {"uk": "uk", "ru": "ru", "en": "en"}[lang]


def patch(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    parts = rel.split("/")
    lang = parts[0]
    segs = parts[1:]
    if not segs:
        segs = ["index.html"]
    u = page_url(lang, segs)
    uk_u = page_url("uk", segs)
    ru_u = page_url("ru", segs)
    en_u = page_url("en", segs)
    t = path.read_text(encoding="utf-8")
    t = re.sub(r'<link rel="canonical" href="[^"]+"\s*/>', f'<link rel="canonical" href="{u}" />', t, count=1)
    t = re.sub(
        r'<link rel="alternate" hreflang="uk" href="[^"]+"\s*/>',
        f'<link rel="alternate" hreflang="uk" href="{uk_u}" />',
        t,
        count=1,
    )
    t = re.sub(
        r'<link rel="alternate" hreflang="ru" href="[^"]+"\s*/>',
        f'<link rel="alternate" hreflang="ru" href="{ru_u}" />',
        t,
        count=1,
    )
    t = re.sub(
        r'<link rel="alternate" hreflang="en" href="[^"]+"\s*/>',
        f'<link rel="alternate" hreflang="en" href="{en_u}" />',
        t,
        count=1,
    )
    if 'hreflang="x-default"' not in t:
        t = t.replace(
            f'<link rel="alternate" hreflang="en" href="{en_u}" />',
            f'<link rel="alternate" hreflang="en" href="{en_u}" />\n    <link rel="alternate" hreflang="x-default" href="{uk_u}" />',
            1,
        )
    else:
        t = re.sub(
            r'<link rel="alternate" hreflang="x-default" href="[^"]+"\s*/>',
            f'<link rel="alternate" hreflang="x-default" href="{uk_u}" />',
            t,
            count=1,
        )
    t = re.sub(r'<meta property="og:url" content="[^"]+"\s*/>', f'<meta property="og:url" content="{u}" />', t, count=1)
    if 'property="og:locale"' not in t and 'property="og:url"' in t:
        t = t.replace(
            f'<meta property="og:url" content="{u}" />',
            f'<meta property="og:url" content="{u}" />\n    <meta property="og:locale" content="{og_locale(lang)}" />',
            1,
        )
    if "<html " in t:
        t = re.sub(r'<html lang="[^"]+"', f'<html lang="{html_lang(lang)}"', t, count=1)
    path.write_text(t, encoding="utf-8")


def main() -> None:
    for lang in ("uk", "ru", "en"):
        d = ROOT / lang
        for html in d.rglob("*.html"):
            patch(html)


if __name__ == "__main__":
    main()
    print("fixed canonical/hreflang in", ROOT)
