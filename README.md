# 📸 Instagram Agent Skill

Instagram Reels, Posts, captions, hashtags - complete Instagram workflow skills

**Repository by:** [Alpesh Makwana](https://github.com/makwanaalpesh811-a11y)

---

## 📦 What's Inside

16 Hermes Agent skills for instagram agent skill:

- `ig-audit` — Audit past Instagram posts to find what worked.
- `ig-caption` — Write Instagram captions that survive the 125-char cut.
- `ig-carousel` — Build Instagram carousel slides and cover copy.
- `ig-comment` — Write human-sounding comments on other posts.
- `ig-dm` — Write Instagram DMs that get replies.
- `ig-hashtag-strategist` — Size 3-5 hashtags to niche/mid/broad tiers.
- `ig-hook-extractor` — Reverse-engineer viral reel hooks into a template.
- `ig-human` — Strip AI-slop out of drafts and score the result.
- `ig-plan` — Plan the week of Instagram posts and engagement.
- `ig-profile` — Score and rewrite an Instagram profile bio.
- `ig-reel` — Write an Instagram Reel script with scored hooks.
- `ig-reply` — Draft replies to comments under your own posts.
- `ig-repurpose` — Turn one long asset into a week of reels.
- `ig-story` — Write a daily Instagram story sequence.
- `ig-viral` — Research viral reels in your niche into a swipe file.
- `instagram-auto-upload` — Automate Instagram Reels/Posts uploads via Meta Graph API.

---


## 🔐 SECURITY NOTICE

**This repo is safe to use publicly.** It contains only skill definitions (SKILL.md) and documentation - no live credentials.

### What NOT to commit:
- API keys (GitHub, YouTube, Gemini, OpenAI, etc.)
- AWS credentials (`~/.aws/credentials`)
- Telegram bot tokens
- Exchange API keys (Delta, Hyperliquid, etc.)
- Private keys or certificates

### Where to store secrets (on your machine):
```
~/.aws/credentials          # AWS
~/.youtube_token.json       # YouTube OAuth
~/.ig_env                   # Instagram/Gemini
~/.signal_bot_env           # Trading bot
~/.gh_token                 # GitHub token
```

All skills are designed to read secrets from your filesystem, not embed them.


## 🚀 Installation

### Option 1: Clone to Hermes skills directory
```bash
git clone https://github.com/makwanaalpesh811-a11y/instagram-agent-skill.git ~/.hermes/skills/instagram-agent-skill
```

### Option 2: Install individual skills
```bash
# Create skills dir if not exists
mkdir -p ~/.hermes/skills

# Clone only what you need
git clone --depth 1 --filter=blob:none https://github.com/makwanaalpesh811-a11y/instagram-agent-skill.git /tmp/instagram-agent-skill
cp -r /tmp/instagram-agent-skill/skills/* ~/.hermes/skills/
```

---

## ⚙️ Prerequisites

Check each skill's `SKILL.md` for specific dependencies. Common ones:
- **Termux** (Android terminal) or Linux/macOS
- **Python 3.11+**
- **Node.js + npm** (for CLI-based skills)
- **API keys** stored in `~/.<name>_env` or `~/.<name>_token.json` files

---

## 🔧 Setup Guide

1. **Install Hermes Agent:** `pip install hermes-agent` or see [Hermes docs](https://hermes-agent.nousresearch.com/docs)
2. **Clone this repo** into `~/.hermes/skills/`
3. **Configure credentials** in your environment (see each skill's SKILL.md)
4. **Use in chat:** Ask Hermes to use any skill by name

---

## 📚 Skill Documentation

Each skill lives in `skills/<skill-name>/SKILL.md` with:
- **YAML frontmatter:** name, description
- **Commands:** CLI/API references
- **Examples:** Ready-to-use snippets
- **Gotchas:** Real-world pitfalls

---

## 🛡️ Security

## 🔐 SECURITY NOTICE

**This repo is safe to use publicly.** It contains only skill definitions (SKILL.md) and documentation - no live credentials.

### What NOT to commit:
- API keys (GitHub, YouTube, Gemini, OpenAI, etc.)
- AWS credentials (`~/.aws/credentials`)
- Telegram bot tokens
- Exchange API keys (Delta, Hyperliquid, etc.)
- Private keys or certificates

### Where to store secrets (on your machine):
```
~/.aws/credentials          # AWS
~/.youtube_token.json       # YouTube OAuth
~/.ig_env                   # Instagram/Gemini
~/.signal_bot_env           # Trading bot
~/.gh_token                 # GitHub token
```

All skills are designed to read secrets from your filesystem, not embed them.

---

## 📜 License

MIT License - see [LICENSE](./LICENSE)

---

## 👨‍💻 Author

**Alpesh Makwana** — Trading, content, and Hermes Agent enthusiast.

- **GitHub:** [makwanaalpesh811-a11y](https://github.com/makwanaalpesh811-a11y)
- **Telegram:** @alpeshalgobot

---

## 🤝 Contributing

Issues and PRs welcome. Follow the SKILL.md format conventions.

## 🏷️ Topics
`instagram` `reels` `social-media` `content` 
