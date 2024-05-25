from flask import Flask, render_template, url_for, request
import googleapiclient.discovery
import pandas as pd

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyD4ewMWP_BoxjLTG_zgMbRlycPvYs7vaZs"

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
        maxResults=100
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
    df = df.drop(['author','published_at','updated_at','like_count'],axis=1)
    df.rename(columns = {'text':'Comment'}, inplace = True)
    print(df.head())

    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)