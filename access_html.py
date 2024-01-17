<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <h1>Users</h1>
    <ul>
        {% for user in users %}
            <li>{{ user.username }} - {{ user.email }}</li>
        {% endfor %}
    </ul>

    <h1>Posts</h1>
    <ul>
        {% for post in posts %}
            <li>{{ post.title }} - {{ post.content }}</li>
        {% endfor %}
    </ul>
</body>
</html>




from flask import render_template
from app import app, db
from models import User, Post

@app.route('/')
def home():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('home.html', users=users, posts=posts)
