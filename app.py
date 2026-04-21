from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts(file_path:str):
    """Loads JSON file"""
    with open(file_path, "r") as handle:
        return json.load(handle)


@app.route('/')
def index():
    blog_posts = load_posts("data/blog_posts.json")
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods= ['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts("data/blog_posts.json")
        new_post = {}

        new_post["id"] = len(blog_posts) + 1
        new_post["author"] = request.form["author"]
        new_post["title"] = request.form["title"]
        new_post["content"] = request.form["content"]
        blog_posts.append(new_post)

        with open("data/blog_posts.json", "w") as handle:
            json.dump(blog_posts, handle)

        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)