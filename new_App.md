📚 Project Overview: Smart Exam Question Generator System
🎯 Goal
To develop a full-stack educational web application where users can upload learning materials (PDF, DOCX, or TXT), set up generation parameters, and generate Multiple Choice Questions (MCQs) or Written Questions automatically.

This solution is aimed at teachers, students, and institutions for:

Fast exam preparation

Self-testing

Assignment creation

Assessment automation

✨ Key Features
✅ Main Features (User Portal)
File Upload Interface

Supports PDF, Word (.docx), and plain text (.txt) files

Drag-and-drop or browse upload

Question Setup Form

Question Type:

MCQ

Written (short/long answer)

Mixed

Difficulty Level:

Easy

Medium

Hard

Number of Questions: (e.g. 5–50)

Custom Instructions (Optional):

e.g., “Focus only on biology definitions” or “Include question numbers”

Smart Generation Logic

Text extracted from uploaded files

Based on input settings, questions are generated

Instructions are interpreted and applied where possible

Results Viewer

Nicely formatted questions shown on-screen

Option to download as Word or PDF

Print button

Option to save result in user's dashboard (if user login is added in future)

🔒 Admin Dashboard
Professional, sidebar-based dashboard for monitoring and managing system usage.

Login screen (admin-only)

Sidebar Navigation:

Dashboard Overview

Uploaded Files Log

Question Generator (Manual Input)

Question Review / Edit

Settings

Manual Text Input Generator

Admin can paste content and generate MCQs or written questions

User Activity Logs (optional)

API Status Panel (for checking if AI API is active or fallback is used)

🏗️ Technology Stack
Area	Tool/Language
Frontend	HTML + CSS + JavaScript (Bootstrap for UI)
Backend	Python + Flask
Templating	Jinja2 (for dynamic HTML pages)
Document Parsing	PyMuPDF, python-docx, pdfplumber
Database	SQLite (can scale to PostgreSQL later)
Authentication	Flask-Login (for admin login)
AI Question Generation	

Primary: Admin manually generates (if no API key available)

Optional Fallback: Plug in OpenAI, Cohere, or free-tier APIs later using a config file
| Hosting | Replit (All-in-one dev + hosting environment) |

🧠 Intelligence Logic (AI or Manual)
If no AI API key is set: system uses admin backend for manual generation.

If a free or paid API key is added: user requests are processed by GPT or Cohere to generate questions automatically based on selected parameters.

Questions should match type, difficulty, and user instructions.

Admin can edit or filter generated questions before publishing (if moderation is enabled).

🔒 Fallback Plan
Scenario	What Happens
No API key available	Admin generates questions manually
API quota exceeded	Notify admin, system switches to manual
Upload failure	Show friendly error + retry button
High traffic	Queue requests or scale later to Render or VPS

📌 Ready-to-Use Instructions for Replit AI (Prompt)
Build a full-stack Flask web application named SmartExamGen.
Key features:

User file upload (PDF, DOCX, TXT)

Form to select:

Question type: MCQ, Written, Mixed

Difficulty level: Easy, Medium, Hard

Number of questions (5–50)

Optional instructions (textarea)

Extract text using PyMuPDF and python-docx

Display generated questions nicely in HTML (with download/print option)

Admin panel with login, sidebar, manual generator, and upload log

AI generation should be optional (support config.py with API key fallback)

Use SQLite for now