from flask import Flask, jsonify, request, render_template
from model import Model

app = Flask(__name__)

model = Model()

@app.route('/audio', methods=['POST'])
def audio():
    # Get the audio file from the request
    file = request.form['mp3']

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)