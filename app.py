import requests
import json
import sqlite3
import os

from utils.query_augment import get_augment_data, get_highest
from flask import Flask, render_template, request, session, redirect, url_for
from bs4 import BeautifulSoup

app = Flask(__name__)
url = 'https://tactics.tools/augments'

app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query_data():
    conn = sqlite3.connect('data/tft.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == 'POST':
        user_input = request.form.get('championName')

        cur.execute("SELECT * FROM champion WHERE name LIKE ?", ('%' + user_input + '%',))
        results = cur.fetchall()

        conn.close()

        return render_template('results.html', results=results)
    
    return render_template('query.html')

@app.route('/augments', methods=['GET', 'POST'])
def augments():
    conn = sqlite3.connect('data/tft.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT name FROM champion")
    champions = cur.fetchall()

    if 'user_list' not in session:
        session['user_list'] = []

    if request.method == 'POST':
        selected_champion = request.form.get('selected_champion')
        session['user_list'].append(selected_champion)
        session.modified = True
    
    return render_template('augments.html', champions=champions, user_list=session['user_list'])

@app.route('/recommendations', methods=['GET', 'POST'])
def get_recommendation():

    if request.method == 'POST':
        stage = request.form.get('current_stage')
        first_augment = request.form.get('firstChoice')
        second_augment = request.form.get('secondChoice')
        third_augment = request.form.get('thirdChoice')

        response = requests.get(url)

        data_first = get_augment_data(first_augment, stage)
        data_second = get_augment_data(second_augment, stage)
        data_third = get_augment_data(third_augment, stage)

        highest_place = get_highest(data_first, data_second, data_third, 'place')
        highest_top4 = get_highest(data_first, data_second, data_third, 'top4')
        highest_won = get_highest(data_first, data_second, data_third, 'won')

        return render_template('winrate.html',
                               stage=stage, 
                               highest_place=highest_place,
                               highest_top4=highest_top4,
                               highest_won=highest_won,
                               data_first=data_first, 
                               data_second=data_second, 
                               data_third=data_third)

    return render_template('recommendations.html')

@app.route('/clear_list', methods=['POST'])
def clear_list():
    # Clear the user's list stored in the session
    session['user_list'] = []
    session.modified = True  # Notify Flask that the session has been modified

    # Redirect back to the augments page
    return redirect(url_for('augments'))

if __name__ == '__main__':
    app.run(debug=True)