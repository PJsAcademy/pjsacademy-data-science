# 🐍 Phase 1 — Advanced Python Projects

10 projects that turn Python fundamentals into real, impressive tools. No frameworks needed — pure Python skill.

---

## 1. 🎨 ASCII Art Video Player
**Difficulty:** ⭐⭐ | **Skills:** OpenCV, threading, terminal manipulation, generators

Convert any video (or webcam feed) into live ASCII art playing in your terminal — with brightness-mapped characters and optional colour via ANSI codes.

- **v1:** Static image → ASCII
- **v2:** Video file → ASCII frames at 24fps
- **v3:** Live webcam → coloured ASCII with audio sync
- **Innovation:** Real-time frame throttling + character density mapping
- **Resume line:** *"Built a real-time video-to-ASCII renderer processing 24fps with dynamic brightness mapping."*

---

## 2. 🔐 Password Manager with Encryption
**Difficulty:** ⭐⭐ | **Skills:** cryptography (Fernet), file I/O, hashing, CLI design

A local, encrypted password vault. Master password → AES-encrypted store. Includes a password strength analyser and breach-style entropy checker.

- **v1:** Store/retrieve passwords in encrypted file
- **v2:** Master-password key derivation (PBKDF2), password generator
- **v3:** CLI with search, categories, clipboard auto-clear, export
- **Innovation:** Zero plaintext ever touches disk; memory-only decryption
- **Resume line:** *"Engineered an AES-256 encrypted CLI password manager with PBKDF2 key derivation."*

---

## 3. 🕸️ Multi-Threaded Web Scraper Engine
**Difficulty:** ⭐⭐⭐ | **Skills:** requests, BeautifulSoup, ThreadPoolExecutor, rate limiting

A polite, concurrent scraping framework with automatic retry, rate-limiting, robots.txt respect, and pluggable parsers.

- **v1:** Single-page scraper
- **v2:** Concurrent multi-page with thread pool
- **v3:** Full framework — queue, retry with backoff, CSV/JSON export, proxy rotation
- **Innovation:** Token-bucket rate limiter + graceful robots.txt compliance
- **Resume line:** *"Built a concurrent scraping engine with token-bucket rate limiting and exponential backoff retry."*

---

## 4. 📁 Smart File Organiser (AI-lite)
**Difficulty:** ⭐⭐ | **Skills:** os, shutil, regex, file-type detection, scheduling

Automatically organises a messy Downloads folder — by type, date, project, or content. Learns your patterns over time.

- **v1:** Sort by extension
- **v2:** Sort by date + rules engine (config file)
- **v3:** Content-based sorting (read PDFs/docs), duplicate detection via hashing, watch-folder daemon
- **Innovation:** MD5 duplicate detection + real-time folder watching
- **Resume line:** *"Automated file organisation with content-aware sorting and hash-based dedup, saving 2hrs/week."*

---

## 5. 🎮 Terminal Game Engine + 3 Games
**Difficulty:** ⭐⭐⭐ | **Skills:** curses, game loops, OOP, state machines, collision detection

A reusable terminal game engine, then build Snake, Tetris, and a Roguelike dungeon crawler on top of it.

- **v1:** Snake with the engine
- **v2:** Tetris with rotation + scoring
- **v3:** Procedurally-generated roguelike with fog of war
- **Innovation:** Shared engine architecture + procedural dungeon generation
- **Resume line:** *"Designed a reusable terminal game engine powering 3 games with procedural level generation."*

---

## 6. 💹 Personal Finance Tracker + Forecaster
**Difficulty:** ⭐⭐ | **Skills:** pandas, matplotlib, datetime, SQLite, simple forecasting

Parse bank statement CSVs (or UPI exports), auto-categorise transactions, and forecast next month's spending.

- **v1:** Parse + categorise transactions
- **v2:** Monthly reports + budget alerts
- **v3:** Spending forecast + savings goal tracker + SQLite backend
- **Innovation:** Rule + keyword auto-categorisation of UPI/Indian bank formats
- **Resume line:** *"Built a personal finance engine that auto-categorises UPI transactions and forecasts monthly spend."*

---

## 7. 🎵 Music Recommendation CLI (Audio Features)
**Difficulty:** ⭐⭐⭐ | **Skills:** librosa, numpy, audio DSP, similarity metrics

Analyse the actual audio (tempo, key, energy, MFCC) of your local music and recommend similar tracks — no streaming API needed.

- **v1:** Extract audio features from MP3s
- **v2:** Build a similarity index
- **v3:** "Find similar songs" + auto-playlist generator by mood
- **Innovation:** MFCC-based audio fingerprinting for offline recommendation
- **Resume line:** *"Implemented offline music recommendation using MFCC audio fingerprinting and cosine similarity."*

---

## 8. 🤖 Discord/Telegram Bot Framework
**Difficulty:** ⭐⭐⭐ | **Skills:** async/await, APIs, webhooks, plugin architecture

A modular bot framework with a plugin system — build commands as drop-in modules. Includes reminders, polls, and a mini trivia game.

- **v1:** Echo bot + basic commands
- **v2:** Plugin loader + persistent storage
- **v3:** Scheduled tasks, inline keyboards, admin panel
- **Innovation:** Hot-reloadable plugin architecture
- **Resume line:** *"Architected an async bot framework with a hot-reloadable plugin system for Telegram."*

---

## 9. 📊 CSV → Interactive Report Generator
**Difficulty:** ⭐⭐ | **Skills:** pandas, Jinja2, HTML/CSS generation, statistics

Point it at any CSV and it generates a full interactive HTML report — profiling, charts, correlations, outliers — no code needed by the end user.

- **v1:** Basic stats table → HTML
- **v2:** Auto-charts + correlation heatmap
- **v3:** Interactive filters, outlier flags, data-quality score, one-file export
- **Innovation:** Auto-detects column types and picks the right chart
- **Resume line:** *"Built an auto-EDA tool generating self-contained interactive HTML reports from any CSV."*

---

## 10. 🧩 Sudoku Solver + Generator + Vision
**Difficulty:** ⭐⭐⭐⭐ | **Skills:** backtracking, constraint propagation, OpenCV, OCR

Solve any Sudoku via backtracking, generate new puzzles of tunable difficulty, and **solve a Sudoku from a photo** using computer vision.

- **v1:** Backtracking solver
- **v2:** Puzzle generator with difficulty rating
- **v3:** Photo → grid detection → digit OCR → solve → overlay answer on image
- **Innovation:** Full CV pipeline (perspective transform + digit recognition)
- **Resume line:** *"Built a Sudoku solver that reads puzzles from photos using OpenCV perspective transform + OCR."*

---

## 🎯 Phase 1 Challenge
Complete **any 3** of these and you've proven you can build real tools with pure Python — the foundation for everything else.

---

*Course: [Data Science Mastery — PJ's Academy](https://pjsacademy.com)*
