import requests
import json
import hashlib, uuid
import jwt
import random

from flask import Flask, request, render_template, jsonify

from report import HashReport

hash_report = HashReport()
hash_report.insert_difficulty(5)

app = Flask(__name__, template_folder='template')

secret = "Noia"

@app.route('/send-email', methods = ['POST'])
def send_email():

    # Get data sent in request body
    data = request.get_json()

    user_db = hash_report.df_user.loc[hash_report.df_user['username'] == data['username']]
    if user_db is None:
        return "Não cadastrado"

    password_hash = str(hashlib.sha256(str(data["password"]).encode('utf-8')).hexdigest())

    password_hash_db = str(user_db[-1:]['password'].values[0])

    if password_hash != password_hash_db:
        return "401 - Unauthorized"

    if (hash_report.df_time["time"].mean() > data['time']):
        hash_report.insert_difficulty(int(hash_report.df_difficulty.iloc[-1]["difficulty"]) + 1)
        hash_report.insert_time(data['time'])

    else:
        if int(hash_report.df_difficulty.iloc[-1]["difficulty"]) >= 2:
            hash_report.insert_difficulty(int(hash_report.df_difficulty.iloc[-1]["difficulty"]) - 1)
            hash_report.insert_time(data['time'])
        else:
            hash_report.insert_time(data['time'])
            hash_report.insert_difficulty(int(hash_report.df_difficulty.iloc[-1]["difficulty"]))

    access_token = jwt.encode({"id": hash_report.df_difficulty.iloc[-2]["id"]}, secret, algorithm='HS256')

    return jsonify({"token": access_token, "difficulty": hash_report.df_difficulty.iloc[-2]["difficulty"]})

@app.route('/register', methods = ['POST'])
def register():
    data = request.get_json()

    hash_report.insert_user(data['username'], hashlib.sha256(str(data["password"]).encode('utf-8')).hexdigest(), None)
    return "200 - User added"

@app.route('/authenticate', methods = ['POST'])
def autenticate():
    data = request.get_json()
    difficulty_object = jwt.decode(data['token'], secret, algorithms=['HS256'])
    difficulty_slice = hash_report.df_difficulty[hash_report.df_difficulty["id"]==difficulty_object['id']]

    if difficulty_slice.empty:
        return "401 - Unauthorized"
    else:
        return difficulty_slice['difficulty'].values[0]

@app.route('/get-difficulty', methods = ['GET'])
def get_difficulty():
    return hash_report.df_difficulty.iloc[-1]["difficulty"]

@app.route('/time', methods = ["GET"])
def df_time_to_html():
    return render_template('time.html', tables=[hash_report.df_time.to_html(classes='data')], titles=hash_report.df_time.columns.values)

@app.route('/difficulty', methods = ["GET"])
def df_difficulty_to_html():
    return render_template('difficulty.html', tables=[hash_report.df_difficulty.to_html(classes='data')], titles=hash_report.df_difficulty.columns.values)

@app.route('/user', methods = ["GET"])
def df_user_to_html():
    return render_template('user.html', tables=[hash_report.df_user.to_html(classes='data')], titles=hash_report.df_user.columns.values)

if __name__ == '__main__':
    app.run()