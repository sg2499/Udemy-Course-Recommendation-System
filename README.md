# 📘 Udemy Course Recommendation System with Flask & NLP

![GitHub repo size](https://img.shields.io/github/repo-size/sg2499/Udemy_Course_Recommendation_System)
![GitHub stars](https://img.shields.io/github/stars/sg2499/Udemy_Course_Recommendation_System?style=social)
![Last Commit](https://img.shields.io/github/last-commit/sg2499/Udemy_Course_Recommendation_System)
![Built with Flask](https://img.shields.io/badge/Built%20With-Flask-blue)

This repository contains a web-based **Course Recommendation System** built using **Flask, NLP, Pandas, and Scikit-learn**. It allows users to input a course title or keyword and get personalized recommendations from Udemy’s dataset. A separate dashboard displays insightful data visualizations using Matplotlib and Seaborn.

---

## 📁 Project Folder Structure

```
📦Udemy_Course_Recommendation_System/
├── SG_app.py                        # Main Flask app with search and dashboard routes
├── dashboard.py                     # Dashboard helper functions (EDA logic)
├── udemy_course_data.csv            # Udemy course dataset (cleaned & preprocessed)
├── requirements.txt                 # Required Python libraries
├── templates/
│   ├── index.html                   # Main HTML template for search & results
│   └── dashboard.html               # Dashboard HTML for data insights
├── Course Recommendation System - SG.ipynb   # Notebook to build recommender logic
├── EDA on Udemy Dataset.ipynb                # Notebook for exploratory data analysis
├── README.md                        # Project documentation
```

---

## 🔎 1. What It Does

- **Search by Exact Title** – Get highly similar courses using cosine similarity on cleaned text.
- **Search by Keyword** – If title match fails, fall back to partial keyword search.
- **Course Details Shown** – Title, URL, Price, Subscriber Count.
- **Dashboard** – Interactive data analysis: level-wise count, subjects per level, year-wise profits, and more.

---

## 🧠 2. How It Works

- **Text Cleaning** – Uses `neattext` to remove stopwords and special characters.
- **Vectorization** – Converts cleaned titles into vectors using `CountVectorizer`.
- **Similarity Calculation** – Uses `cosine_similarity` to compare courses.
- **Fallback Logic** – If no exact match, uses substring search for popularity-based results.
- **Dashboard** – Aggregates dataset insights via Pandas grouping and Matplotlib plots.

---

## 💻 3. Setup Instructions

### 🔧 Clone the Repository

```bash
git clone https://github.com/sg2499/Udemy_Course_Recommendation_System.git
cd Udemy_Course_Recommendation_System
```

### 🐍 Create a Virtual Environment (Recommended)

```bash
conda create -n course_recommender python=3.11
conda activate course_recommender
```

### 📦 Install All Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 4. Run the App

### ✅ Option 1: Using Flask

```bash
set FLASK_APP=SG_app.py       # For Windows CMD
$env:FLASK_APP="SG_app.py"    # For PowerShell
export FLASK_APP=SG_app.py    # For macOS/Linux

flask run
```

### ✅ Option 2: Direct Python Run

```bash
python SG_app.py
```

---

## 📊 5. Dataset

The dataset used is `udemy_course_data.csv`, containing:

- Course Title
- URL
- Price
- Number of Subscribers
- Subject
- Published Date
- Course Level

> All text cleaning, visualization, and recommendations are built on top of this dataset.

---

## ✅ 6. Requirements

Refer to `requirements.txt`. Major packages used:

- `Flask==2.3.3`
- `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`
- `neattext` (for NLP preprocessing)

```txt
See full list in requirements.txt →
```

---

## 📬 Author

Developed with ❤️ by **Shailesh Gupta**  
🔗 [GitHub – sg2499](https://github.com/sg2499)  
📩 shaileshgupta841@gmail.com

---

> Powered by Flask, Pandas, and Scikit-learn · Inspired by Udemy’s course data
