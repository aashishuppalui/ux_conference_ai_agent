# 🚀 UX Conference Intelligence Agent

An automated AI-powered system that discovers, verifies, and summarizes UX/UI conferences globally — without manual effort.

---

## 🧠 Overview

The **UX Conference Intelligence Agent** is a Python-based automation pipeline that:

- 🔍 Discovers UX/UI conferences from the internet
- 🤖 Uses AI to verify event relevance
- 🧠 Extracts structured event details from web pages
- 📊 Stores data in Google Sheets
- ✍️ Generates LinkedIn-ready content summaries
- ⚙️ Runs automatically via GitHub Actions

---

## 🎯 Project Goal

Build a **fully automated UX conference tracking system** that:

- Requires zero manual input
- Maintains a clean, verified dataset
- Generates actionable insights for designers

---

## 🏗️ Architecture

```
Internet (RSS Sources)
        ↓
Discovery Layer
        ↓
AI Verification Layer
        ↓
AI Extraction Layer
        ↓
Google Sheets Database
        ↓
Content Generation (OpenAI)
        ↓
LinkedIn Post Output
        ↓
GitHub Actions Automation
```

---

## ⚙️ Tech Stack

- **Python**
- **OpenAI (gpt-4o-mini)**
- **Google Sheets API (gspread)**
- **GitHub Actions (scheduler)**
- **RSS feeds (Google News)**

---

## 📂 Project Structure

```
ux_conference_ai_agent/
│
├── main.py                     # Main pipeline
├── generate_post.py           # LinkedIn content generator
├── requirements.txt
│
├── data/
│   └── seed_conferences.json
│
├── discovery/
│   └── rss_search.py
│
├── verification/
│   └── ai_verify_event.py
│
├── extraction/
│   └── extract_event_details.py
│
├── utils/
│   └── event_filter.py
│
└── .github/workflows/
    └── run.yml
```

---

## 🔄 Workflow

1. **Discover Events**
   - Uses RSS search queries:
     - "UX conference"
     - "UX meetup"
     - "design summit"

2. **Verify Events (AI)**
   - Classifies if an event is relevant to UX/design

3. **Extract Details (AI)**
   - Parses event pages to extract:
     - Name
     - Location
     - Date
     - Online/Offline
     - Price

4. **Store Data**
   - Saves structured data to Google Sheets

5. **Generate Content**
   - Creates LinkedIn-ready summaries

6. **Automation**
   - Runs every 14 days via GitHub Actions

---

## 📊 Example Output

### Google Sheet

| Name                    | Location | Date       | Price |
| ----------------------- | -------- | ---------- | ----- |
| UX Research Summit 2026 | Berlin   | March 2026 | €399  |

---

### LinkedIn Post

```
🌍 UX Conferences Recently Announced

• UX Research Summit 2026 (Berlin)
• UX Design Meetup Tokyo
• AI-Powered UX Conference

Great opportunities for designers to learn and connect.

#UXDesign #UXConference #DesignCommunity
```

---

## 🔐 Environment Variables

Set in GitHub Secrets:

- `GOOGLE_CREDENTIALS`
- `OPENAI_API_KEY`

---

## 💰 Cost Efficiency

- Uses **gpt-4o-mini (low-cost model)**
- Approx cost:
  - ₹0.05–₹0.15 per run

- Monthly limit can be capped at $1

---

## 🚀 Future Improvements

- 📍 Better event detail extraction (location/date parsing)
- 🧠 AI-based event classification (conference vs course)
- 🌍 Add new discovery sources:
  - Sessionize (CFP)
  - Meetup

- 📅 UX Conference Calendar view
- 📊 Dashboard for visualization
- 📩 Newsletter automation

---

## ⭐ Why This Project Matters

This project demonstrates:

- AI-powered automation pipelines
- Real-world use of LLMs for data processing
- End-to-end system design
- Scalable architecture for intelligence systems

---

## 🙌 Author

Built as an exploration into **AI-driven UX intelligence systems**.

---

## 📌 Note

This is an evolving project. Contributions and ideas for improving event discovery and accuracy are welcome.
