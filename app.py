from flask import Flask, render_template, request, redirect, url_for, abort
import uuid 
import boto3
s3_client = boto3.client('s3')

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    # if request.method == "POST":
    #     if 'translate' in request.form:
    #         # initiate polly 
    #         # mp3 file is formed
    #         # playback mp3 file 
    return render_template('home.html')