"""Module that runs the application"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

def load_posts():
    """Loads blog posts from JSON file"""
    try:
        with open("data/blog_posts.json", "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_posts(blog_posts: list):
    """Save the blog posts in the JSON file"""
    os.makedirs("data", exist_ok=True)
    with open("data/blog_posts.json", "w", encoding="utf-8") as handle:
        json.dump(blog_posts, handle)

@app.route('/')
def index():
    """Renders the index page with all posts"""
    blog_posts = load_posts()
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods= ['GET', 'POST'])
def add():
    """Render the add.html and add a post to the JSON file
    with all blog posts and redirects to the index.html"""
    new_post = {}
    if request.method == 'POST':
        blog_posts = load_posts()
        if len(blog_posts) == 0:
            new_post["id"] = 1
        else:
            new_post["id"] = max(post["id"] for post in blog_posts) + 1

        new_post["author"] = request.form["author"]
        new_post["title"] = request.form["title"]
        new_post["content"] = request.form["content"]
        blog_posts.append(new_post)

        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id: int):
    """Delete a post with the specific 'post_id' in the JSON file.
     Redirects to the main page with all blog posts."""
    blog_posts = load_posts()
    new_blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_posts(new_blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int):
    """Render the update.html and update a post in the JSON file
    and redirects to the index.html"""
    blog_posts = load_posts()
    post = fetch_post_by_id(blog_posts, post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        updated_post = {
        "id": post_id,
        "author": request.form["author"],
        "title": request.form["title"],
        "content": request.form["content"]
        }

        new_blog_posts = []
        for post in blog_posts:
            if post_id == post['id']:
                new_blog_posts.append(updated_post)
            else:
                new_blog_posts.append(post)

        save_posts(new_blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


def fetch_post_by_id(blog_posts: list, post_id: int):
    """Return a post with a specific post id or None if no post with this post id was found"""
    for post in blog_posts:
        if post_id == post['id']:
            return post
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
