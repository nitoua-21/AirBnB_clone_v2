#!/usr/bin/python3
"""
This module starts a Flask web application with multiple routes.

Routes:
    /: Displays 'Hello HBNB!'
    /hbnb: Displays 'HBNB'
    /c/<text>: Displays 'C ' followed by the value of the text variable
    /python/(<text>): Displays 'Python ' + {text} + (default: 'is cool')
    /number/<n>: Displays '<n> is a number' only if n is an integer
    /number_template/<n>: Displays an HTML page only if n is an integer
    /number_odd_or_even/<n>: display HTML page; display odd/even info
"""
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """Hello HBNB"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """HBNB"""
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """C is fun!"""
    return "C " + text.replace('_', ' ')


@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_text(text):
    """Displays 'Python ' + {text} + 'is cool'"""
    return "Python " + text.replace('_', ' ')


@app.route('/number/<int:n>')
def number(n):
    """Displays '<n> is a number' only if n is an integer"""
    return f"{n} is a number"


@app.route('/number_template/<int:n>')
def number_template(n):
    """Displays an HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def html_odd_or_even(n):
    """display html page only if int given
       place given int into html template
       substitute text to display if int is odd or even
    """
    odd_or_even = "even" if (n % 2 == 0) else "odd"
    return render_template('6-number_odd_or_even.html',
                           n=n, odd_or_even=odd_or_even)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
