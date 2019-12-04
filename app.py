from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/')
def home():
    """Display home page"""
    return render_template("home.html")


@app.route('/library')
def library():
    """Display's all dnd info, according to homebrew, like a wiki"""
    return render_template("library.html")


@app.route('/sheets')
def sheets():
    """Displays Character sheets"""
    return render_template("sheets.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
