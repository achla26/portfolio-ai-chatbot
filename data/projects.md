# My Projects

Here are the projects I'm most proud of — a mix of production apps, AI systems, and personal experiments.

---

## 1. Shaky Isles — NZ Quake Data Pipeline

**One-liner:** An hourly earthquake pipeline: GeoNet API to bronze JSON to dbt marts, fully tested and scheduled.

**Tech Stack:** `Python`, `DuckDB`, `dbt`, `Airflow`, `GitHub Actions`

**What I built:**
- Hourly GeoNet API ingestion into timestamped bronze JSON (raw, as-is)
- Idempotent DuckDB loads deduped on quake ID (run twice, same count)
- dbt staging (JSON parsing + casts) plus daily-counts mart, **5/5 tests passing**
- Scheduled green runs on GitHub Actions (55s) plus an Airflow DAG version
- Written debugging record (LEARNED.md) for every bug and fix

**Why it's cool:**
A real end-to-end data pipeline with testing, CI and orchestration — not a notebook demo. Shows how I think about idempotency, data quality and automation.

**Links:**
- 🔗 [GitHub Source](https://github.com/achla26/shaky-isles)

---

## 2. SQL Data Warehouse — Bronze to Gold

**One-liner:** A PostgreSQL warehouse with Bronze→Silver→Gold layers, star schema and ETL procedures.

**Tech Stack:** `PostgreSQL`, `SQL`, `ETL`, `Star Schema`, `Docker`

**What I built:**
- Bronze/Silver/Gold layered architecture with documented load order
- Star schema with dimension and fact tables
- ETL stored procedures with incremental loads
- Data-quality checks at Silver and Gold layers

**Why it's cool:**
My first warehouse end-to-end — and the foundation I'm now rebuilding with dbt and Airflow (see Shaky Isles above).

**Links:**
- 🔗 [GitHub Source](https://github.com/achla26/sql-warehouse)

---

## 3. Fixaddo — Home Services Marketplace (In Progress)

**One-liner:** A React Native mobile app connecting homeowners with local service providers.

**Tech Stack:** `React Native`, `Laravel`, `MySQL`, `REST API`, `JWT Auth`

**What I built:**
- Cross-platform mobile app with booking workflows and service listings
- Laravel REST API backend with JWT-based authentication
- Provider profile management, service categories, and reviews
- Real-time booking status updates

**Why it's cool:**
This is a real client project for an active freelance engagement. It required me to think end-to-end — from mobile UI/UX to API design, database architecture, and deployment. Currently in active development.

**Links:**
- 🔗 [GitHub Source](https://github.com/achla26/fixaddo)

---

## 4. AI Handbook Q&A System (RAG) — Production RAG

**One-liner:** A production-grade RAG system that answers questions from a large handbook with 100% accuracy on test queries.

**Tech Stack:** `Python`, `FastAPI`, `LangChain`, `Qdrant`, `Groq API`

**What I built:**
- Complete RAG pipeline: document ingestion → chunking → embedding → retrieval → generation
- **Hallucination detection** — flags responses when confidence is low
- **Confidence scoring** — every answer comes with a reliability score
- Achieved **1.01s average query latency** (fast enough for real-time)
- 100% accuracy on test query set

**Why it's cool:**
This isn't a toy RAG demo. It has production-grade features like hallucination detection and confidence scoring — the kind of things that separate "cool prototype" from "actually usable in production."

**Links:**
- 🔗 [GitHub Source](https://github.com/achla26/ai-handbook-qa)

---

## 5. Pulse — AI-Native Mobile Command Center (In Progress)

**One-liner:** A mobile-first productivity app that replaces 5+ apps by unifying notes, tasks, reminders, links, and ideas into one AI-powered inbox.

**Tech Stack:** `React Native`, `Expo`, `Node.js`, `Fastify`, `PostgreSQL`, `Prisma`, `Groq LLM`, `Turborepo`

**What I built:**
- **Unified Item model** — one data model for note/task/reminder/link/list/idea
- **Zero-friction AI:** Groq LLM auto-classifies captures, extracts tasks from notes, summarizes URLs, generates checklists
- **PostgreSQL full-text search** with tsvector ranking
- **Smart resurface algorithm** — surfaces forgotten items intelligently
- **Type-safe monorepo** using Turborepo, Fastify, Prisma, Zod, TanStack Query

**Why it's cool:**
This is my personal daily-driver app — solving my own productivity problem with AI. The architecture (monorepo + type safety end-to-end) is production-grade.

**Links:**
- 🔗 [GitHub Source](https://github.com/achla26/pulse)

---

## 6. AI Resume Matcher — Live Web Tool

**One-liner:** A deployed tool where users paste their resume and a job description to get a match score and actionable improvement suggestions.

**Tech Stack:** `Python`, `Streamlit`, `Groq API`

**What I built:**
- Simple, focused UI for pasting resume + JD
- LLM-powered analysis using Groq's fast inference
- Actionable, specific suggestions (not generic advice)
- Live and deployed for public use

**Why it's cool:**
Built end-to-end in a weekend. Solves a real problem I faced during my own job search. Fast, focused, and useful.

**Links:**
- 🔗 [GitHub Source](https://github.com/achla26/ai-resume-matcher)

---

## 7. Catking.in — EdTech Platform (Production)

**One-liner:** A course registration and management platform for a real EdTech client.

**Tech Stack:** `Laravel`, `React`, `MySQL`

**What I built:**
- Course catalog with search, filters, and categories
- Student registration and enrollment workflows
- Admin dashboard for course/instructor management
- Payment integration and receipts

**Why it's cool:**
Production app serving real students. Taught me how to handle real-world edge cases — payment failures, concurrent enrollments, data integrity.

---

## 8. Walmart Sales Performance Analysis

**One-liner:** Data analysis project uncovering revenue trends and holiday uplift patterns across 45 Walmart stores.

**Tech Stack:** `Python`, `Pandas`, `SQL`, `Matplotlib`

**What I did:**
- Analyzed **6,400+ weekly sales records** across 45 stores
- Identified revenue trends by store, category, and season
- Quantified holiday uplift patterns worth **$54M annually**; top store earns **8.1x** the bottom one

**Why it's cool:**
Shows I can work with real datasets and derive actionable business insights, not just build apps.

---

## Other Notable Projects

- **Brew My Idea** — Idea validation platform (Laravel + React)
- **Whispering Shouts** — Content platform
- **Original Rides** — E-commerce platform

---

## Want to See More?

Check out my [GitHub](https://github.com/achla26) — I regularly push code and experiments there.