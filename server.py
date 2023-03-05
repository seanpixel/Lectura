from flask import Flask, jsonify, request, render_template, make_response,send_file
from model import Model
from flask_cors import CORS
from pytube import YouTube
from pydub import AudioSegment
from moviepy.editor import AudioFileClip
from urllib.parse import urlparse, parse_qs
import numpy as np
import os
import requests

app = Flask(__name__)
cors = CORS(app)

ffmpeg_folder = '/opt/homebrew/bin'
os.environ['PATH'] += ':' + ffmpeg_folder

# cors = CORS(app, resources={"/": {"origins": "*"}})

model = Model()

@app.route('/audio', methods=['POST'])
def audio():
    # Get the audio file from the request
    file = request.files['mp3']

    # transcribe the audio and set it
    model.setTranscription(file)
    transcription = model.getTranscription()

    # summarize the transcription and set it
    model.setSummary()
    summary = model.getSummary()

    # Return the transcription as a JSON response
    return jsonify({'transcription': transcription, 'summary': summary})

@app.route('/question', methods=['POST'])
def text_output():
    # Get the text input from the form
    question = request.form['text']

    answer = model.answerQuestion(question)

    # Return the processed text as a JSON response
    return jsonify({'answer': answer})
    
@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    youtube_link = data['link']
    # Download the YouTube video.
    youtube_video = YouTube(youtube_link)
    video_file = youtube_video.streams.get_highest_resolution().download()
    # Convert the video file to MP3.
    audio_clip = AudioFileClip(video_file)
    audio_file = audio_clip.write_audiofile('audio.mp3')
    # Pass the MP3 file to another API.
    mp3_file = open('audio.mp3', 'rb')
    files = {'mp3': mp3_file}
    response = requests.post('http://127.0.0.1:5000/audio', files=files)
    mp3_file.close()
    os.remove('audio.mp3')
    os.remove(video_file)
    # Return the response from the other API.
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
    
