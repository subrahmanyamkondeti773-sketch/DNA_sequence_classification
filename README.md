# 🧬 AI DNA Sequence Classification System

A production-ready Django 5 web application for classifying DNA sequences using trained machine learning models, enriched with **GPT-4o-powered biological explanations** and a premium interactive UI.

---

## 🚀 Features

- **ML Classification** – Predicts DNA sequence class using `scikit-learn` models (vectorizer + classifier + label encoder)
- **AI Explanation** – GPT-4o-mini generates biological context, gene type, health implications
- **AI Suggestions** – Research directions, mutation insights, experimental recommendations
- **Color-coded DNA Display** – A/T/G/C bases colored for visual analysis
- **Confidence Scoring** – Probability scores with progress bar visualization
- **Analytics Dashboard** – Chart.js pie chart + 7-day activity bar chart
- **PDF Export** – Download full analysis reports (ReportLab)
- **Search & History** – Paginated, searchable prediction history
- **User Auth** – Register, login, profile management
- **Admin Panel** – Custom dashboard + Django admin for user/record management

---

## 📁 Project Structure

```
dna_classification_project/
├── dna_classification_project/   # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                        # User auth & profiles
│   ├── models.py, views.py, forms.py, urls.py, admin.py
├── dna_classifier/               # DNA classification app
│   ├── models.py                 # DNASequence, APILog
│   ├── predictor.py              # Singleton ML model loader
│   ├── utils.py                  # Sequence validation & stats
│   ├── ai_helper.py              # OpenAI integration
│   ├── views.py                  # All views
│   ├── urls.py, admin.py
├── templates/                    # HTML templates
│   ├── base.html, home.html, dashboard.html
│   ├── dna_input.html, result.html, history.html
│   ├── admin_dashboard.html
│   └── users/ (login, register, profile)
├── static/
│   ├── css/styles.css            # Premium glassmorphism CSS
│   └── js/main.js               # Dark mode, animations
├── models/                       # ML model files
│   ├── dna_classifier.pkl
│   ├── vectorizer.pkl
│   └── label_encoder.pkl
├── .env                          # Environment variables
├── requirements.txt
└── manage.py
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Edit .env file:
SECRET_KEY=your-django-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-api-key
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000**

---

## 🔑 Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/users/register/` | Register |
| `/users/login/` | Login |
| `/dashboard/` | User dashboard |
| `/dna/classify/` | DNA input & classification |
| `/dna/result/<id>/` | Classification result |
| `/dna/history/` | Prediction history |
| `/dna/export/<id>/` | PDF export |
| `/admin/` | Django admin panel |
| `/admin-dashboard/` | Custom analytics dashboard |
| `/api/analytics/` | JSON analytics API |

---

## 🧬 DNA Validation Rules

- Characters: **A, T, G, C only** (case-insensitive)
- Minimum length: **10** characters
- Maximum length: **5000** characters

---

## 🤖 ML Model Files

Place in `models/` directory:
- `dna_classifier.pkl` – Trained classifier
- `vectorizer.pkl` – Feature vectorizer
- `label_encoder.pkl` – Class label encoder

---

## 🛡️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5, DRF |
| ML | scikit-learn, joblib |
| AI | OpenAI GPT-4o-mini |
| Frontend | Bootstrap 5.3, Chart.js |
| Auth | Django built-in |
| PDF | ReportLab |
| Static | WhiteNoise |
