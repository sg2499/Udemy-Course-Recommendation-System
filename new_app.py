import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import plotly.express as px

# ----------------- CONFIG & STYLING -------------------
st.set_page_config(page_title="🎓 Udemy Course Recommendation", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    h1, h2, h3 { color: #1f4068; font-family: 'Segoe UI', sans-serif; }
    .stButton button {
        background-color: #1f4068; color: white; padding: 0.5em 1em; border-radius: 6px;
        border: none; font-size: 1em; font-weight: bold;
    }
    .stButton button:hover {
        background-color: #30475e;
    }
    </style>
""", unsafe_allow_html=True)

st.image("udemy_banner_streamlit.png", use_column_width=True)

# ----------------- DATA LOAD & UTILS -------------------
@st.cache_data
def readdata():
    return pd.read_csv("udemy_course_data.csv")

def clean_titles(df):
    df['Clean_Title'] = df['course_title'].apply(nfx.remove_stopwords).apply(nfx.remove_special_characters)
    return df

def get_cosine_matrix(df):
    vect = CountVectorizer()
    mat = vect.fit_transform(df['Clean_Title'])
    return cosine_similarity(mat)

def recommend_courses(df, title, cosine_mat, numrec=6):
    course_index = pd.Series(df.index, index=df['course_title']).drop_duplicates()
    if title not in course_index:
        return None
    index = course_index[title]
    scores = list(enumerate(cosine_mat[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    selected_index = [i[0] for i in sorted_scores[1:numrec+1]]
    recommended_df = df.iloc[selected_index].copy()
    recommended_df['Similarity_Score'] = [i[1] for i in sorted_scores[1:numrec+1]]
    return recommended_df[['course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']]

def fallback_search(df, term):
    result_df = df[df['course_title'].str.contains(term, case=False)]
    return result_df.sort_values(by='num_subscribers', ascending=False).head(6)

# ----------------- DASHBOARD CHARTS -------------------
def dashboard_charts(df):
    df['price'] = df['price'].astype(str).str.replace('Free|TRUE', '0', regex=True).astype(float)
    df['profit'] = df['price'] * df['num_subscribers']
    df['published_date'] = pd.to_datetime(df['published_timestamp'], errors='coerce')
    df.dropna(subset=['published_date'], inplace=True)

    df['year'] = df['published_date'].dt.year
    df['month'] = df['published_date'].dt.month_name()

    tabs = st.tabs(["📊 Domain-wise Subscribers", "📈 Courses by Level", "📅 Yearly Trends", "📆 Monthly Stats", "🔍 Category-Wise"])

    with tabs[0]:
        data = df.groupby("subject")["num_subscribers"].sum().reset_index()
        fig = px.pie(data, names='subject', values='num_subscribers', title="Subscribers by Domain")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        data = df['level'].value_counts().reset_index()
        data.columns = ['level', 'count']
        fig = px.pie(data, names='level', values='count', title="Courses by Level", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        sub = df.groupby('year')['num_subscribers'].sum().reset_index()
        profit = df.groupby('year')['profit'].sum().reset_index()
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(sub, x='year', y='num_subscribers', title="Subscribers per Year")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(profit, x='year', y='profit', title="Profit per Year")
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        sub = df.groupby('month')['num_subscribers'].sum().reset_index()
        profit = df.groupby('month')['profit'].sum().reset_index()
        month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
        sub['month'] = pd.Categorical(sub['month'], categories=month_order, ordered=True)
        profit['month'] = pd.Categorical(profit['month'], categories=month_order, ordered=True)
        sub = sub.sort_values('month')
        profit = profit.sort_values('month')
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(sub, x='month', y='num_subscribers', title="Monthly Subscribers")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(profit, x='month', y='profit', title="Monthly Profit")
            st.plotly_chart(fig, use_container_width=True)

    with tabs[4]:
        combo = df.groupby(['subject', 'level'])['num_subscribers'].sum().reset_index()
        combo['label'] = combo['subject'] + " - " + combo['level']
        fig = px.bar(combo, x='label', y='num_subscribers', title="Subscribers by Category", color='subject')
        st.plotly_chart(fig, use_container_width=True)

# ----------------- MAIN APP -------------------
df = readdata()
df = clean_titles(df)
cosine_mat = get_cosine_matrix(df)

menu = st.sidebar.radio("🚀 Go To", ["🔍 Recommend Courses", "📊 View Dashboard"])

if menu == "🔍 Recommend Courses":
    st.subheader("Type a course title to get smart recommendations")
    user_input = st.text_input("🔎 Course Title", "")
    if st.button("Recommend"):
        if user_input:
            recdf = recommend_courses(df, user_input, cosine_mat)
            if recdf is not None:
                st.success(f"Showing recommendations for: **{user_input}**")
                cols = st.columns(3)
                for i, row in recdf.iterrows():
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div style='background:#fff;padding:15px;border-radius:10px;
                                    border:1px solid #ddd;box-shadow:2px 2px 6px rgba(0,0,0,0.05)'>
                            <h4 style='color:#1f4068'>{row['course_title']}</h4>
                            <p>💸 <b>${row['price']}</b> &nbsp; 👥 <b>{row['num_subscribers']}</b></p>
                            <a href="{row['url']}" target="_blank">
                                <button style='padding:6px 12px;background-color:#1f4068;color:#fff;
                                               border:none;border-radius:5px'>🔗 View Course</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background-color:#fff3cd;border-left:5px solid #ffa502;
                                padding:10px 16px;border-radius:6px;margin-bottom:20px;">
                      <span style="color:#856404;font-weight:500;font-size:15px;">
                        ⚠️ Exact match not found. Showing related courses instead.
                      </span>
                    </div>
                """, unsafe_allow_html=True)
                fallback = fallback_search(df, user_input)
                cols = st.columns(3)
                for i, row in fallback.iterrows():
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div style='background:#fff;padding:15px;border-radius:10px;
                                    border:1px solid #ddd;box-shadow:2px 2px 6px rgba(0,0,0,0.05)'>
                            <h4 style='color:#1f4068'>{row['course_title']}</h4>
                            <p>💸 <b>${row['price']}</b> &nbsp; 👥 <b>{row['num_subscribers']}</b></p>
                            <a href="{row['url']}" target="_blank">
                                <button style='padding:6px 12px;background-color:#1f4068;color:#fff;
                                               border:none;border-radius:5px'>🔗 View Course</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

elif menu == "📊 View Dashboard":
    st.subheader("📊 Course Analytics Dashboard")
    dashboard_charts(df)