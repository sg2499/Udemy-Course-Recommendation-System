# 📘 Udemy-Course-Recommendation-System with Flask & NLP

![GitHub repo size](https://img.shields.io/github/repo-size/sg2499/Udemy-Course-Recommendation-System)
![GitHub stars](https://img.shields.io/github/stars/sg2499/Udemy-Course-Recommendation-System?style=social)
![Last Commit](https://img.shields.io/github/last-commit/sg2499/Udemy-Course-Recommendation-System)
![Built with Flask](https://img.shields.io/badge/Built%20With-Flask-blue)

This repository contains a web-based **Udemy Course Recommendation System** built using **Flask**, **NLP**, **Pandas**, and **Scikit-learn**. It allows users to search for a course title or keyword and receive personalized recommendations based on course similarity. It also includes a visually rich **EDA Dashboard** and a detailed narrative report summarizing the insights.

---

## 📁 Project Folder Structure

```
📦Udemy-Course-Recommendation-System/
├── SG_app.py                              # Main Flask app with search and dashboard routes
├── dashboard.py                           # Backend analytics functions for the dashboard
├── udemy_course_data.csv                  # Cleaned Udemy dataset
├── requirements.txt                       # All required Python libraries
├── templates/
│   ├── index.html                         # Homepage with course search input
│   └── dashboard.html                     # Dashboard view for EDA visualizations
├── Course Recommendation System - SG.ipynb  # Jupyter notebook for building recommendation logic
├── EDA on Udemy Dataset.ipynb             # EDA notebook with plots and analysis
├── Udemy_EDA_Narrative_Report.txt         # Written summary of EDA and findings
├── README.md                              # Project documentation
```

---

## 🔍 1. Key Features

- 🔎 **Search-based Recommendations**: Input a course title or keyword and receive the top 6 related courses based on title similarity.
- 📊 **Interactive Dashboard**: Shows subject distributions, yearly trends, course levels, subscribers, pricing, and more.
- 🧠 **NLP Text Processing**: Cleans and vectorizes course titles using `neattext` and `CountVectorizer`.
- 🧪 **Similarity Matching**: Uses cosine similarity for course recommendation logic.
- 📄 **Narrative EDA Summary**: Easy-to-understand insights extracted from Udemy dataset included in `Udemy_EDA_Narrative_Report.txt`.

---

## 📚 2. What’s Inside the EDA?

Insights covered in the EDA report and dashboard include:

- 🔤 **Course Titles**: Most frequent words, longest/shortest titles, keyword-based course discovery.
- 🗂️ **Subjects**: Most popular subjects, number of courses by subject/year, and subscriber interest by category.
- 📆 **Published Year**: Course release trends and year-wise growth.
- 🎓 **Course Levels**: Beginner vs Intermediate vs Expert breakdown and popularity.
- ⏱️ **Duration**: Duration vs subscribers, top longest-running courses.
- 💰 **Pricing**: Free vs Paid distribution, average prices, most profitable courses.
- 📈 **Correlations**: Relationships between price, reviews, lectures, duration, and number of subscribers.

---

## 💻 3. Setup Instructions

### 🔧 Clone the Repository

```bash
git clone https://github.com/sg2499/Udemy-Course-Recommendation-System.git
cd Udemy-Course-Recommendation-System
```

### 🐍 Create a Virtual Environment

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

### ✅ Option 1: Using Flask CLI

```bash
# For Windows CMD
set FLASK_APP=SG_app.py

# For PowerShell
$env:FLASK_APP = "SG_app.py"

# For macOS/Linux
export FLASK_APP=SG_app.py

flask run
```

### ✅ Option 2: Run Directly

```bash
python SG_app.py
```

---

## 📝 Dataset Overview

- **Source**: Udemy course data (CSV)
- **Columns**: Title, Price, URL, Level, Subject, Duration, Number of Subscribers
- **Preprocessing**: Stopword and special character removal for clean analysis and recommendations

---

## ✅ Requirements

Major packages used:

- `Flask==2.3.3`
- `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`
- `neattext` for NLP
- Full list in `requirements.txt`

---

## 📬 Author

Created with ❤️ by **Shailesh Gupta**  
🔗 GitHub: [sg2499](https://github.com/sg2499)  
📩 Email: shaileshgupta841@gmail.com

---

> Powered by Flask · Informed by Udemy · Explained through EDA ✨
