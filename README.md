
# 🧠 Unstop AI Quiz App (Flask + Streamlit Versions)

This repository contains **two different implementations** of an AI-based Quiz Generator using **Google Gemini API**:

1. 🎯 **Flask App**: A structured web app similar to Unstop platform, deployed using PythonAnywhere.
2. ⚡ **Streamlit App**: An interactive quiz app with a live progress bar and animations, deployed on Streamlit Cloud.

---

## 📁 Project Structure

```

.
├── Unstop_AI_Quiz/
│   └── app.py                # Flask backend
│   └── static/               # HTML files for UI
│   └── templates/ 
├── generate_quiz.py          # Streamlit frontend logic
└── README.md                 # This file

````

---

## 🔧 1. Flask Version – `flask_quiz_app/`

### 🌐 What It Does

- Generates quizzes automatically using Gemini API.
- Different pages for Aptitude, Grammar, Reasoning, etc.
- 5-question quiz dynamically created for selected topic.
- Deployed at: [vachaspathi.pythonanywhere.com](https://vachaspathi.pythonanywhere.com/)

---

### 🚀 How to Run (Flask)

#### 1️⃣ Install Python and dependencies

```bash
pip install flask google-generativeai
````

#### 2️⃣ Clone the Repository

```bash
git clone https://github.com/vachaspathi6/Unstop-AI-Quiz-.git
cd unstop-ai-quiz/flask_quiz_app
```

#### 3️⃣ Set API Key

In your terminal:

```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```

(Or add it in `.env` and load with `python-dotenv`)

#### 4️⃣ Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

### 🌍 Deployment (PythonAnywhere)

1. Sign up on [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload files inside `flask_quiz_app/`
3. Configure `app.py` as the WSGI file
4. Set environment variable `GEMINI_API_KEY` under **Web > Environment**
5. Reload the web app

---

## ⚡ 2. Streamlit Version – `streamlit_quiz_app/`

### 🤖 What It Does

* Lets users choose a topic and number of questions
* Auto-generates quiz with Gemini
* Shows one question at a time
* Keeps track of score and shows results at the end
* Nice UI with animations, progress bar, answer review
* Deployed at: [unstopai.streamlit.app](https://unstopai.streamlit.app/)

---

### 🚀 How to Run (Streamlit)

#### 1️⃣ Install Requirements

```bash
pip install streamlit google-generativeai
```

#### 2️⃣ Clone the Repository

```bash
git clone https://github.com/vachaspathi6/Unstop-AI-Quiz-.git
cd unstop-ai-quiz/streamlit_quiz_app
```

#### 3️⃣ Set API Key

In your terminal:

```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```

#### 4️⃣ Run the App

```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`

---

### 🌐 Deployment (Streamlit Cloud)

1. Push `streamlit_quiz_app/` folder to a GitHub repo
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Link your GitHub repo and choose `app.py`
4. Set `GEMINI_API_KEY` in **Secrets**
5. Deploy 🚀

---

## 🤝 Credits

* Gemini Pro API by Google
* [Streamlit](https://streamlit.io)
* [Flask](https://flask.palletsprojects.com/)
* UI inspired by [Unstop](https://unstop.com)

---

## 📬 Contact

For queries or collaboration, contact: **[2100032473cseh@gmail.com](mailto:2100032473cseh@gmail.com)**

```
