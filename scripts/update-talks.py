#!/usr/bin/env python3
"""Add new YouTube uploads to the top of the UX Talks row on the home page.

Run by .github/workflows/update-talks.yml. Reads the channel's public RSS feed
(no API key needed), and for every video published after CUTOFF that is not
already on the page, inserts a card at the start of the list. Existing cards
are never moved or removed. Shorts are skipped.

  python3 scripts/update-talks.py            # update index.html
  python3 scripts/update-talks.py --dry-run  # only print what would change
"""
import html
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "index.html"

# Only videos published after this moment are added, so older uploads that
# were left off the site on purpose stay off.
CUTOFF = datetime(2026, 10, 20, 0, 0, tzinfo=timezone.utc)

# Leave empty to look the channel up from the first video on the page.
CHANNEL_ID = ""

TRACK_MARK = "data-scroller-track>"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}
UA = {"User-Agent": "Mozilla/5.0 (site updater)", "Accept-Language": "en"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def channel_id(page_ids):
    if CHANNEL_ID:
        return CHANNEL_ID
    for vid in page_ids:
        try:
            m = re.search(r'"channelId":"(UC[\w-]{22})"', fetch(f"https://www.youtube.com/watch?v={vid}"))
        except urllib.error.URLError:
            continue
        if m:
            return m.group(1)
    sys.exit("Could not find the channel id. Set CHANNEL_ID in scripts/update-talks.py.")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def is_short(vid):
    # /shorts/<id> answers 200 for a Short and redirects for a normal video.
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(urllib.request.Request(f"https://www.youtube.com/shorts/{vid}", headers=UA), timeout=30) as r:
            return r.status == 200
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False


def card(vid, title):
    t = html.escape(title, quote=True)
    return (
        '\n          <div class="talk">\n'
        f'            <div class="yt" data-yt="{vid}" data-title="{t}"></div>\n'
        f'            <h3 class="talk__title">{t}</h3>\n'
        '          </div>'
    )


def main():
    dry = "--dry-run" in sys.argv
    page = PAGE.read_text(encoding="utf-8")
    on_page = re.findall(r'data-yt="([\w-]{11})"', page)
    cid = channel_id(on_page)
    print(f"Channel: {cid}")

    feed = ET.fromstring(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
    new = []
    for e in feed.findall("a:entry", NS):  # newest first
        vid = e.findtext("yt:videoId", namespaces=NS)
        title = e.findtext("a:title", namespaces=NS) or "YouTube video"
        published = datetime.fromisoformat(e.findtext("a:published", namespaces=NS).replace("Z", "+00:00"))
        status = "on page" if vid in on_page else "older than cutoff" if published <= CUTOFF else None
        if status is None and is_short(vid):
            status = "short, skipped"
        print(f"  {published:%Y-%m-%d} {vid} {title!r}: {status or 'NEW'}")
        if status is None:
            new.append((vid, title))

    if not new:
        print("Nothing to add.")
        return
    if dry:
        print(f"Dry run: would add {len(new)} video(s).")
        return
    i = page.index(TRACK_MARK) + len(TRACK_MARK)
    page = page[:i] + "".join(card(v, t) for v, t in new) + page[i:]
    PAGE.write_text(page, encoding="utf-8")
    print(f"Added {len(new)} video(s).")


if __name__ == "__main__":
    main()
