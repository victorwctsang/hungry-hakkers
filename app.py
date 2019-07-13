from flask import Flask, render_template, request, redirect, url_for, abort

from contextlib import closing
import subprocess

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        item_requested = request.form['submit']
        print(item_requested)
        language = request.form['language']

        if language == "cn":
            eng_to_cn_audio(item_requested) 
        else:
            eng_to_es_audio(item_requested)

        subprocess.call(['./test.sh'])

    return render_template('home.html')

@app.route('/staff', methods=['POST', 'GET'])
def staff():
    return render_template('staff.html')

def eng_to_es_audio(str):
    translate = boto3.client('translate', region_name='us-east-1')
    polly = boto3.client('polly')

    translated = translate.translate_text(
        Text=str,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )
    translated_text = translated["TranslatedText"]
    print(translated_text)
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=translated_text,
        VoiceId='Miguel',
        LanguageCode='es-US'
    )
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            print("AUDIOOO")
            output = "polly-boto.mp3"

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    print("WRITING AUDIO")
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

def eng_to_cn_audio(str):
    translate = boto3.client('translate', region_name='us-east-1')
    polly = boto3.client('polly')

    translated = translate.translate_text(
        Text=str,
        SourceLanguageCode='en',
        TargetLanguageCode='zh'
    )
    translated_text = translated["TranslatedText"]
    print(translated_text)
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=translated_text,
        VoiceId='Zhiyu',
        LanguageCode='cmn-CN'
    )
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            print("AUDIOOO")
            output = "polly-boto.mp3"

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    print("WRITING AUDIO")
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
