---
name: instagram-auto-upload
description: Automate Instagram Reels/Posts uploads via Meta Graph API.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [instagram, reels, upload, automation, meta-graph-api, social-media]
    related_skills: [youtube-full-access, ig-reel, ig-caption, ig-viral]
---

# Instagram Auto Upload

Real posting to Instagram (not just content drafting). The 13 `ig-*` skills in this library (ig-reel, ig-caption, etc.) are content-only — they write text, they don't post. This skill covers the actual uploader.

## TL;DR Recommendation

| Need | Best option | Setup time |
|---|---|---|
| Post reels/photos/carousels from script | **instapost** PyPI lib | 5 min |
| Full control, custom workflows | Meta Graph API direct | 30-60 min |
| YouTube → IG pipeline | AWS S3 + Flask + Meta API + n8n | 2-3 hours |
| Schedule + cross-post | Buffer/Hootsuite/Typefully | 5 min |

**For this user (Termux + trading bot + YouTube)**: `instapost` PyPI is the correct default. It handles local file upload (via Catbox relay), transcodes HEVC to H.264, and posts with one method call.

## Meta App Setup (required for all paths)

1. **Create App**: https://developers.facebook.com/apps/create → type "For Everything Else"
2. **Add Instagram product**
3. **Business verification** required for public-facing use; Development Mode works for personal account
4. **App Roles > Roles**: assign yourself as **Instagram Tester**
5. **Instagram → API Setup with Instagram Login** → add your IG account → **Generate token**
6. **Link Facebook Page** to Instagram (mandatory for API posting even with IG-only content)

Required permissions:
- `instagram_basic`
- `instagram_content_publish`
- `pages_read_engagement`
- `pages_show_list`

Credential values needed:
- `APP_ID` + `APP_SECRET` (for token exchange)
- `IG_USER_ID` (get from `/me` with a token)
- `PAGE_ACCESS_TOKEN` (long-lived, not short-lived user token)
- `PAGE_ID` (needed for Facebook CDN relay when posting videos)

**Do NOT use short-lived user tokens** — they expire in 1 hour. Exchange for long-lived:
```bash
curl -G "https://graph.facebook.com/v15.0/oauth/access_token" \
  --data-urlencode "grant_type=fb_exchange_token" \
  --data-urlencode "client_id=$APP_ID" \
  --data-urlencode "client_secret=$APP_SECRET" \
  --data-urlencode "fb_exchange_token=$SHORT_LIVED_TOKEN"
```
Long-lived tokens last 60 days — for permanent access, use a **Page Access Token** (never expires as long as the Page exists), obtained by posting to a Page.

## Path 1: instapost (Recommended)

Install:
```bash
pip install instapost
```

Basic usage:
```python
from instapost import InstagramPoster

poster = InstagramPoster(
    access_token="$PAGE_ACCESS_TOKEN",
    ig_user_id="$IG_USER_ID"
)

# Post reel
poster.post_reel(
    video="~/Hermes_Almari/03_UPLOADS/pending/reel.mp4",
    caption="New reel 🎬 #hashtags",
    share_to_feed=True
)

# Post image
poster.post_image(image="photo.jpg", caption="Caption")

# Post carousel (2-10 items, mixed image+video)
poster.post_carousel(
    media_items=[
        {"media": "photo1.jpg", "type": "IMAGE"},
        {"media": "video.mp4", "type": "VIDEO"},
    ],
    caption="Swipe through 👉"
)

# Verify
print(poster.verify()['username'])
```

How it works: local files auto-upload to Catbox (temporary relay), then sent to Meta API as URL. This is required because Meta requires the video to be publicly URL-accessible, not local.

## Path 2: Meta Graph API Direct (Full control)

Two-phase post:

### Phase 1: Create media container
```python
import requests

API = "https://graph.facebook.com/v21.0"

def create_container(ig_user_id, token, video_url, caption, thumb_offset=2000):
    r = requests.post(
        f"{API}/{ig_user_id}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "thumb_offset": thumb_offset,
            "access_token": token,
        },
        timeout=300
    )
    r.raise_for_status()
    return r.json()["id"]  # container_id
```

### Phase 2: Poll status, then publish
```python
def check_status(ig_user_id, token, container_id):
    r = requests.get(
        f"{API}/{container_id}?fields=status_code,status",
        params={"access_token": token},
        timeout=30
    )
    return r.json()  # wait for status_code == FINISHED

def publish(ig_user_id, token, container_id):
    r = requests.post(
        f"{API}/{ig_user_id}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": token,
        },
        timeout=120
    )
    return r.json()
```

**Always poll with retry** — Meta often returns `PUBLISH_IN_PROGRESS` or `media not ready` on first publish attempt. Retry 10 times with 10s delay (total ~100s).

## Video specs (Meta requirements)

Non-compliant files silently fail or error. Verify before upload:

| Requirement | Spec |
|---|---|
| Container | MP4, no edit lists, moov atom at front |
| Video codec | H.264 (mandatory — HEVC must be transcoded) |
| Audio codec | AAC, 48kHz, mono or stereo |
| Aspect | 9:16 for reels (1080x1920) |
| Duration | 3-90 sec for reels, 15 min max total |
| Bitrate | VBR 25Mbps video, 128kbps audio |
| File size | ≤ 1GB |

**Transcode HEVC → H.264 before upload:**
```bash
ffmpeg -i input_hevc.mp4 -c:v libx264 -preset slow -crf 23 \
  -c:a aac -b:a 128k -pix_fmt yuv420p -profile:v high -level 4.0 \
  -movflags +faststart output.mp4
```

Use `-movflags +faststart` to move moov atom to front (Meta rejects fastseek-into-middle files).

## Rate limits

- **50 posts/hour** per IG account
- **200 posts/day** per IG account
- **25 concurrent media upload requests** per app
- **1000 queries/hour** per app for Graph API overall

If hitting `code: 32` (rate limit), back off 60s.

## Pitfalls

- **Business verification is REQUIRED for public accounts** — Development Mode works for personal IG, but any posting outside your tester list will fail with `code: 200` after verification is required.
- **Facebook Page must be linked** — IG-only posting is impossible; you always need a Page connected to your IG Business/Creator account.
- **Do not use short-lived tokens** — they expire in 1 hour and posting pipelines silently break overnight. Always long-lived Page Access Tokens.
- **Catbox relay for instapost** — if instapost uses Catbox and Catbox is down or rate-limits, use a public URL host (S3 bucket, GitHub release asset, R2) instead.
- **Do not post from an unverified phone region** — Meta geo-blocks API posting for accounts that don't have phone verification in a supported region.
- **Do not schedule reels to `share_to_feed=false`** — the default is `false` (story-only), which hides reels from the profile grid. Always pass `share_to_feed=true` explicitly.
- **H.264 transcode check** — Instagram's docs say "HEVC or H264" for some parameters but the API silently rejects HEVC on most accounts. Transcode to H.264 unconditionally.
- **`thumb_offset` is in milliseconds**, not frames — default 2000ms = 2 seconds. Set to where the visual is sharpest.
- **Caption has no hard character limit** but Instagram truncates at ~2200 chars in the feed before the "more" button. Use the 125-char preview from `ig-caption` skill.
- **Do NOT use old Graph API versions** — pin to `v21.0` or newer. v17/v18 endpoints are being retired.
- **Cross-posting from other platforms** — Instagram blocks `instagram_content_publish` on unverified apps posting content from other users' channels. Only post to YOUR own linked account.
- **Never use the deprecated Instagram API v1** — Graph API v19+ is only path.

## Storage locations (this user's convention)

- **Credentials**: `~/.ig_env` alongside `~/.youtube_env`, `~/.google_env` — chmod 600
- **Upload script**: `~/Hermes_Almari/01_STRATEGY/code/ig_uploader/ig_uploader.py` (matches existing youtube uploader layout)
- **Pending uploads**: `~/Hermes_Almari/03_UPLOADS/pending/` (filename rules: `Name.mp4` public, `Name[PRIV].mp4` private)
- **Uploaded logs**: `~/Hermes_Almari/99_COLLABORATION/hermes_output/YYYY-MM-DD_ig_post.json`

## Verification checklist

After setup:
- [ ] `instagram_basic` + `instagram_content_publish` + `pages_*` permissions granted
- [ ] Long-lived Page Access Token generated (not short-lived user token)
- [ ] Page linked to IG Business account
- [ ] `poster.verify()` returns correct username
- [ ] One test reel posted successfully
- [ ] Video is H.264 (not HEVC)
- [ ] Video is 9:16 aspect for reels
- [ ] `share_to_feed=true` set explicitly
- [ ] Credentials in `~/.ig_env`, not in scripts

## Not this skill for

- Content drafting (captions, reels scripts, hooks) — use ig-reel, ig-caption, ig-viral
- Instagram scraping / reading — use xurl-style or public scraping
- Cross-posting to X/LinkedIn/TikTok — separate skills
- Community management — use ig-comment, ig-reply, ig-dm
