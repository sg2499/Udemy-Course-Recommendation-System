# Importing necessary modules
from flask import Flask, request, render_template  # Flask core and form/rendering support
import pandas as pd  # For working with tabular data
import numpy as np  # For numerical operations
import neattext.functions as nfx  # For text cleaning: stopwords, special characters
from sklearn.feature_extraction.text import CountVectorizer  # Convert text to numbers
from sklearn.metrics.pairwise import cosine_similarity  # Measure similarity between vectors
from dashboard import getvaluecounts, getlevelcount, getsubjectsperlevel, yearwiseprofit  # Dashboard helper functions

# Initialize the Flask app
app = Flask(__name__)


# Function to create CountVectorizer matrix from cleaned course titles
def getcosinemat(df):
    countvect = CountVectorizer()
    cv_mat = countvect.fit_transform(df['Clean_Title'])  # Transforms text into a numerical matrix
    return cv_mat


# Function to clean course titles using neattext
def getcleantitle(df):
    # Remove stopwords like "the", "in", "and"
    df['Clean_Title'] = df['course_title'].apply(nfx.remove_stopwords)
    # Remove special characters like !, @, #
    df['Clean_Title'] = df['Clean_Title'].apply(nfx.remove_special_characters)
    return df


# Function to compute cosine similarity between course titles
def cosinesimmat(cv_mat):
    return cosine_similarity(cv_mat)


# Load the Udemy course dataset from a CSV file
def readdata():
    df = pd.read_csv(r'C:\Users\shail\OneDrive\Shailesh\Personal\Personal Learning\Udemy Projects\Course Recommendation System\udemy_course_data.csv')
    return df


# Main function to recommend similar courses using cosine similarity
def recommend_course(df, title, cosine_mat, numrec):
    # Create a Series to map course titles to their index
    course_index = pd.Series(df.index, index=df['course_title']).drop_duplicates()
    index = course_index[title]  # Find index of the input course

    scores = list(enumerate(cosine_mat[index]))  # Get similarity scores of this course with others
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)  # Sort courses by similarity

    selected_course_index = [i[0] for i in sorted_scores[1:]]  # Ignore the first (self-match)
    selected_course_score = [i[1] for i in sorted_scores[1:]]

    recommended_df = df.iloc[selected_course_index]  # Get course rows
    recommended_df['Similarity_Score'] = selected_course_score  # Add similarity scores

    # Return top 'numrec' recommended courses with relevant details
    recommended_courses = recommended_df[['course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']]
    return recommended_courses.head(numrec)


# If partial search term is entered, search courses using keyword match
def searchterm(term, df):
    # Filter course titles that contain the given term (case-insensitive)
    result_df = df[df['course_title'].str.contains(term, case=False)]
    # Sort results by number of subscribers and return top 6
    top6 = result_df.sort_values(by='num_subscribers', ascending=False).head(6)
    return top6


# Extracts only useful fields from a recommendation dataframe
def extractfeatures(recdf):
    course_url = list(recdf['url'])  # Get course URLs
    course_title = list(recdf['course_title'])  # Get course titles
    course_price = list(recdf['price'])  # Get course prices
    return course_url, course_title, course_price


# Home route: handles both GET (normal) and POST (form submission) requests
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # If user submits the form with a course title
    if request.method == 'POST':
        my_dict = request.form
        titlename = my_dict['course']  # Get the entered course name
        print("Entered Title:", titlename)

        try:
            # Load data and clean course titles
            df = readdata()
            df = getcleantitle(df)
            cvmat = getcosinemat(df)  # Convert cleaned titles into matrix
            cosine_mat = cosinesimmat(cvmat)  # Compute similarity between courses

            # Get top 6 recommendations
            recdf = recommend_course(df, titlename, cosine_mat, 6)
            course_url, course_title, course_price = extractfeatures(recdf)
            dictmap = dict(zip(course_title, course_url))  # Create dictionary for rendering

            if dictmap:
                return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)
            else:
                return render_template('index.html', showerror=True, coursename=titlename)

        except Exception as e:
            # If exact title match fails, try using keyword search
            print("Fallback due to error:", e)
            df = readdata()
            resultdf = searchterm(titlename, df)
            course_url, course_title, course_price = extractfeatures(resultdf)
            coursemap = dict(zip(course_title, course_url))

            if coursemap:
                return render_template('index.html', coursemap=coursemap, coursename=titlename, showtitle=True)
            else:
                return render_template('index.html', showerror=True, coursename=titlename)

    # For GET requests, show the empty search form
    return render_template('index.html')


# Dashboard route to display analytics from the course data
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    df = readdata()
    valuecounts = getvaluecounts(df)
    levelcounts = getlevelcount(df)
    subjectsperlevel = getsubjectsperlevel(df)
    yearwiseprofitmap, subscriberscountmap, profitmonthwise, monthwisesub = yearwiseprofit(df)

    # Render the dashboard.html template with all the computed data
    return render_template('dashboard.html',
                           valuecounts=valuecounts,
                           levelcounts=levelcounts,
                           subjectsperlevel=subjectsperlevel,
                           yearwiseprofitmap=yearwiseprofitmap,
                           subscriberscountmap=subscriberscountmap,
                           profitmonthwise=profitmonthwise,
                           monthwisesub=monthwisesub)


# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)  # Starts the Flask development server