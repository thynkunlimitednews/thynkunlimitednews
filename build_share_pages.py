import json
import os
import re

SITE_URL = "https://thynkunlimitednews.github.io/thynkunlimitednews/"
DEFAULT_IMAGE = SITE_URL + "social/home.jpg"

def esc_attr(val):
    return (
        str(val)
        .replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

def resolve_abs_url(path):
    if not path:
        return DEFAULT_IMAGE
    if re.match(r"^https?://", path, re.I):
        return path
    return SITE_URL + path.lstrip("./")

with open("data/articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

for art in articles:
    slug = art["slug"]
    title = f"{art['title']} | Thynk Unlimited"
    deck = art["deck"]
    img_url = resolve_abs_url(art.get("image"))
    canonical_url = f"{SITE_URL}story/{slug}/"
    target_app_url = f"{SITE_URL}?story={slug}"

    story_dir = os.path.join("story", slug)
    os.makedirs(story_dir, exist_ok=True)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc_attr(title)}</title>
  <meta name="description" content="{esc_attr(deck)}" />
  <meta name="author" content="{esc_attr(art.get('author', 'Jay Altaf'))}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{esc_attr(canonical_url)}" />

  <meta property="og:site_name" content="Thynk Unlimited" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc_attr(title)}" />
  <meta property="og:description" content="{esc_attr(deck)}" />
  <meta property="og:url" content="{esc_attr(canonical_url)}" />
  <meta property="og:image" content="{esc_attr(img_url)}" />
  <meta property="og:image:secure_url" content="{esc_attr(img_url)}" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{esc_attr(art['title'])}" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc_attr(title)}" />
  <meta name="twitter:description" content="{esc_attr(deck)}" />
  <meta name="twitter:image" content="{esc_attr(img_url)}" />
  <meta name="twitter:image:alt" content="{esc_attr(art['title'])}" />

  <meta http-equiv="refresh" content="0; url={esc_attr(target_app_url)}" />
  <script>window.location.replace({json.dumps(target_app_url)});</script>
</head>
<body>
  <p>Redirecting to <a href="{esc_attr(target_app_url)}">{esc_attr(art['title'])}</a>&hellip;</p>
</body>
</html>
"""
    with open(os.path.join(story_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

print(f"Generated static share pages for {len(articles)} article(s).")
