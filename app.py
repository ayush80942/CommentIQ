from flask import Flask, render_template, url_for, request

app = Flask(__name__)

def extract_video_id(youtube_link):
    index = youtube_link.index('=')
    video_id = youtube_link[index + 1:]
    return video_id

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
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)