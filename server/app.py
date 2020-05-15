import requests
import json

from flask import Flask, request, render_template
from report import HashReport

hash_report = HashReport()

app = Flask(__name__, template_folder='template')

@app.route('/send-email', methods = ['POST'])
def send_email():
    data = request.get_json()
    if (hash_report.df_difficulty.empty):
        hash_report.insert_difficulty(5)
        hash_report.insert_time(data['time'])
        
    elif (hash_report.df_time["time"].mean() > data['time']):
        hash_report.insert_difficulty(int(hash_report.df_difficulty.iloc[-1]["difficulty"]) + 1)
    else:
        if int(hash_report.df_difficulty.iloc[-1]["difficulty"]) >= 1:
            hash_report.insert_difficulty(int(hash_report.df_difficulty.iloc[-1]["difficulty"]) - 1)
    
    return "Submitted new time"

@app.route('/get-difficulty', methods = ['GET'])
def get_difficulty():
    return hash_report.df_difficulty.iloc[-1]["difficulty"]

@app.route('/time', methods = ["GET"])
def df_time_to_html():
    return render_template('simple.html', tables=[hash_report.df_time.to_html(classes='data')], titles=hash_report.df_time.columns.values)

@app.route('/difficulty', methods = ["GET"])
def df_difficulty_to_html_():
    return render_template('simple.html', tables=[hash_report.df_difficulty.to_html(classes='data')], titles=hash_report.df_difficulty.columns.values)

if __name__ == '__main__':
    app.run()