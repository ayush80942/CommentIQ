from flask import Flask, render_template, url_for, request, make_response
import googleapiclient.discovery
import numpy as np
import pandas as pd
import nltk
import pickle
from dotenv import load_dotenv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# Import functions for data preprocessing & data preparation
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import string
from string import punctuation
import nltk
import re

load_dotenv()
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("YT_API")

app = Flask(__name__)

def extract_video_id(youtube_link):
    if "v=" in youtube_link:
        return youtube_link.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in youtube_link:
        return youtube_link.split("youtu.be/")[-1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    url = ''
    if request.method == 'POST':
        url = request.form['url']
    videoID = extract_video_id(url)
    print(videoID)

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    yt_request = youtube.commentThreads().list(
        part="snippet",
        videoId = videoID,
        maxResults = 100
    )
    response = yt_request.execute()

    comments = []

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['updatedAt'],
            comment['likeCount'],
            comment['textDisplay']
        ])

    df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
    data1 = df.drop(['author','published_at','updated_at','like_count'],axis=1)
    data1.rename(columns = {'text':'Comment'}, inplace = True)
    totalComments = len(data1.index)
    print(data1.head())

    nltk.download("popular")
    nltk.download("vader_lexicon")
    nltk.download('omw-1.4')

    stop_words = stopwords.words('english')
    lzr = WordNetLemmatizer()

    def text_processing(text):
        text = text.lower()
        text = re.sub(r'\n',' ', text)
        text = re.sub('[%s]' % re.escape(punctuation), "", text)
        text = re.sub("^a-zA-Z0-9$,.", "", text)
        text = re.sub(r'\s+', ' ', text, flags=re.I)
        text = re.sub(r'\W', ' ', text)
        text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])
        text=' '.join([lzr.lemmatize(word) for word in word_tokenize(text)])
        return text

    data_copy = data1.copy()
    data_copy.Comment = data_copy.Comment.apply(lambda text: text_processing(text))

    corpus = []
    for sentence in data_copy.Comment:
        corpus.append(sentence)
    print(corpus[0:5])

    from sklearn.feature_extraction.text import CountVectorizer
    cv = pickle.load(open("vectorizer.pickle", 'rb'))

    # Use pickle.load() to deserialize and load the object
    loaded_data = pickle.load(open('classifier-pkl', 'rb'))
    final_result = loaded_data.predict(cv.transform(corpus).toarray())
    negativeComments = np.count_nonzero(final_result == 0)
    positiveComments = np.count_nonzero(final_result == 2)
    neutralComments = np.count_nonzero(final_result == 1)

    categories = ['Positive', 'Negative', 'Neutral']
    values = [positiveComments, negativeComments, neutralComments]  # Example values, you can replace these with your own data

    fig, ax = plt.subplots()
    ax.bar(categories, values, color=['green', 'red', 'blue'])

    ax.set_xlabel('Sentiments')
    ax.set_ylabel('Count')
    ax.set_title('Sentiment Analysis')

    # Save the plot to a BytesIO object
    png_image = io.BytesIO()
    fig.savefig(png_image, format='png')
    png_image.seek(0)

    # Convert the BytesIO object to a base64 string
    png_base64 = base64.b64encode(png_image.getvalue()).decode('ascii')
    
    # Ensure the base64 string is properly formatted
    response = f"data:image/png;base64,{png_base64}"
    
    # Print the response for debugging
    print(response[:100])

    return render_template("dashboard.html", 
                           totalComments = totalComments, 
                           negativeComments = negativeComments, 
                           positiveComments = positiveComments, 
                           neutralComments = neutralComments,
                           response = response)

if __name__ == '__main__':
    app.run(debug=True)