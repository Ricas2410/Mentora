
# 📘 Educational Learning Platform Overview
### Helping Underprivileged Learners Rebuild Their Dreams

---

## 🎯 Goal
To provide an online learning platform for underprivileged learners (especially school dropouts and late learners) to **study GES-aligned subjects** from the basics upward, with **English as the foundation**, using structured lessons, quizzes, and level-based progression — all in a private, supportive environment.

---

## 🏗️ Core System Structure

### 1. 🧑‍🎓 Target Users
- Youth and adults who missed formal education
- Learners with low literacy and confidence
- People looking to build up from middle school or earlier levels

---

### 2. 📚 Subjects Covered
International K-12 curriculum subjects:
- **English Language Arts** (Reading, writing, grammar, literature, communication)
- **Mathematics** (Numbers, algebra, geometry, statistics, problem-solving)
- **Science** (Biology, chemistry, physics, earth sciences)
- **Social Studies** (History, geography, civics, cultural studies)
- **Life Skills** (Health, safety, values, practical life skills)

Each subject will be broken down into:
- **Grade levels** (Grades 1-12: Elementary, Middle School, High School)
- **Topics** within each grade
- **Learning content** (notes, media)
- **Quizzes**, **tests**, and **exams**

---

## 🔄 Learning Flow & Level Progression

1. **Learner chooses or is assigned a starting level** (e.g., Class 1 English)
2. For each topic in that level:
   - 📖 Study notes
   - ❓ Practice quiz (multiple choice, fill-in-the-blank)
   - 🧪 Topic test and quizzes
3. After completing all topics in a level:
   - 📝 Final exam (auto-generated or curated)
4. If they pass (e.g., 70%+; should be handled by admin), they are promoted to the next class 
5. If they fail, they can **retake with new shuffled questions**

✅ The system tracks learner progress and unlocks new content accordingly.

---

## 🧠 Learning Features

- **Multiple choice and fill-in-the-blank** question types
- **Instant feedback** on every quiz question (with explanations)
- **Shuffled answers** and randomized questions
- **Study notes** in simple language, supported by images/audio
- **Progress tracking** (bars, scores, badges)
- **Offline reading** support for downloaded notes

---

## 🔐 Authentication System

- Custom **user registration**
- **Email verification** before full access
- Optional: password reset via email
- Login system with session management

Each learner will have a **dashboard** showing:
- Current level and subject
- Goals or personal targets
- Progress (quizzes/tests completed, pass/fail record)

---

## 📊 Admin Panel (Backend)

Admin(s) can:
- Add/edit/delete:
  - Subjects
  - Levels (Class 1, 2, etc.)
  - Topics and study notes
  - Questions (with correct answers + feedback)
- Define pass mark per test/exam
- View learner progress and performance

---

## ⚙️ Technical Stack

| Component       | Technology                        |
|----------------|------------------------------------|
| Backend         | Python (Django preferred)         |
| Frontend        | Tailwind CSS + DaisyUI            |
| Auth            | Django Auth + Email Verification  |
| Database        | SQLite                            |
| UI Framework    | Responsive design for mobile/desktop |

---

## 📁 Suggested App Modules

- `users` – registration, login, profile, progress
- `subjects` – subject list, levels, topics
- `content` – notes, media, quizzes, tests, exams
- `admin_panel` – content and learner management
- `core` – system-wide settings, promotions logic, pass/fail rules

---

## 🚀 MVP Milestone Features

1. User registration + email verification
2. Subject and class-level selection
3. Study notes with progress bar
4. Quizzes with explanations
5. Auto test generation + exam result tracking
6. Class promotion logic
7. Simple admin dashboard for content creation


## default email config:
SMTP Host: smtp.gmail.com
SMTP Port: 587
TLS: Enable
SMTP Username: skillnetservices@gmail.com
SMTP Password: tdms ckdk tmgo fado
Email Settings: skillnetservices@gmail.com
