# CommentIQ

CommentIQ is a sentiment analysis tool designed to evaluate YouTube video comments. Using a Gaussian Naive Bayes model and the Natural Language Toolkit (nltk), CommentIQ classifies comments as positive, negative, or neutral. The model is integrated into a Flask web application that accepts the URL of a YouTube video, scrapes the comments using the YouTube Data API, processes the comments through the sentiment analysis model, and returns the results to the frontend.

## Features

- **YouTube Comment Scraping**: Fetches comments from YouTube videos using the YouTube Data API.
- **Sentiment Analysis**: Classifies comments into positive, negative, or neutral using a GaussianNB model.
- **Web Interface**: User-friendly frontend for inputting YouTube video URLs and displaying results.
- **Real-time Analysis**: Processes and returns sentiment analysis results quickly.

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/CommentIQ.git
    cd CommentIQ
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the YouTube Data API**
    - Obtain an API key from the [Google Developers Console](https://console.developers.google.com/).
    - Create a `.env` file in the root directory and add your API key:
        ```
        YOUTUBE_API_KEY=your_api_key_here
        ```

## Usage

1. **Run the Flask application**
    ```bash
    flask run
    ```

2. **Access the web interface**
    - Open your web browser and navigate to `http://127.0.0.1:5000`.
    - Enter the URL of a YouTube video and submit.
    - View the sentiment analysis results.

## Project Structure

```
CommentIQ/
│
├── app.py                 # Main application file
├── ML.ipynb               # Sentiment analysis model
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── .env                   # Environment variables
└── README.md              # Project readme file
```

## Dependencies

- Flask
- nltk
- scikit-learn
- requests
- python-dotenv

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any enhancements or bug fixes.

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Contact

For questions or support, please open an issue or contact [ayushaggarwal8094@gmail.com](mailto:ayushaggarwal8094@gmail.com).

---

Happy coding! 🚀
