"""Check the static homepage: python3 tests/check_site.py."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
VOID = set("area base br col embed hr img input link meta param source track wbr".split())


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, f"Unbalanced tag: {tag}"


page = Page()
html = (ROOT / "index.html").read_text()
page.feed(html)
page.close()
assert not page.stack, f"Unclosed tags: {page.stack}"
ids = [a["id"] for _, a in page.tags if "id" in a]
assert len(ids) == len(set(ids)), "Duplicate IDs"
assert sum(tag == "h1" for tag, _ in page.tags) == 1
assert any(tag == "meta" and a.get("name") == "viewport" for tag, a in page.tags)
assert (ROOT / "CNAME").read_text().strip() == "huaiwen.me"
for tag, attrs in page.tags:
    if tag == "img":
        assert "alt" in attrs, "Missing image alt attribute"
    for key in ("href", "src"):
        if key not in attrs:
            continue
        value = attrs[key]
        assert value and value != "#", "Placeholder link"
        url = urlsplit(value)
        assert url.scheme != "http", f"Insecure URL: {value}"
        if url.scheme or url.netloc:
            continue
        if url.path:
            assert (ROOT / url.path).is_file(), f"Missing local file: {value}"
        elif url.fragment:
            assert url.fragment in ids, f"Missing anchor: {value}"
assert sum(a.get("class") == "select_pub" for _, a in page.tags) == 8
assert "Earlier publications" not in html
assert "https://ccs.imu.edu.cn/info/1023/2402.htm" in html
assert "https://immc.feishu.cn/wiki/W4apw2p39ilI4wkArhHcf74mnuy" in html
assert "Inner Mongolia University Developer Group of Elite Student (IMUDGES)" in html
assert 'href="https://github.com/huaiwen"' not in html
assert "Recent entries follow" not in html
assert "Profile and recent publications updated" not in html
assert "Inner Mongolia Association for Artificial Intelligence (IMAAI)" in html
print("PASS: HTML nesting, metadata, 8 publications, assets, anchors, and domain configuration")
