from flask import Flask, render_template, request, redirect, url_for, abort
import boto3
from contextlib import closing

app = Flask(__name__)
request = 0

@app.route('/', methods=['POST', 'GET'])
def home():
    item_requested = "none"
    if request.method == 'POST':
        item_requested = request.form['submit']
        request = 1
        eng_to_cn_audio("Item has been ordered!") 
    else
        request = 0

    return render_template('home.html')

@app.route('/staff', methods=['POST', 'GET'])
def staff():
    return render_template('staff.html')

def eng_to_cn_audio(str):
    translate = boto3.client('translate', region_name='us-east-1')
    polly = boto3.client('polly')

    translated = translate.translate_text(
        Text=str,
        SourceLanguageCode='en',
        TargetLanguageCode='zh'
    )
    translated_text = translated["TranslatedText"]
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=translated_text,
        VoiceId='Zhiyu',
        LanguageCode='cmn-CN'
    )
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = "polly-boto.mp3"

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
