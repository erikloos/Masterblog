from flask import Flask, render_template
import json

app = Flask(__name__)

def load_posts(file_path:str):
    """Loads JSON file"""
    with open(file_path, "r") as handle:
        return json.load(handle)

blog_posts = load_posts("data/blog_posts.json")

@app.route('/')
def index():
    return render_template('index.html', blog_posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)