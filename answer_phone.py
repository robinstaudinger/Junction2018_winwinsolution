from flask import Flask, request
from twilio.twiml.voice_response import Record, VoiceResponse
from twilio.rest import Client
from speechAPI import speechAPI
from urllib.request import urlopen
from text_summarizer import text_summarizer
import requests
from google.cloud import speech_v1 as speech
import io


# Your Account Sid and recording sid from twilio.com/console
account_sid = 'AC8b9fbab7141ecb52cdd3460f0ff8668f'
rid = 'RE8ff24766b309a6525bce1de700ff0240'

app = Flask(__name__)


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Hello, unfortunately all our customer service agents are busy right now. I am SAP0, a friendly assistant ready to help you with all your problems. Feel free to describe your problem to me while waiting for one of our customer service agents.", voice='alice')

    #record the answer
    resp.record(timeout = 4, action =  "/recording", method = "POST")


    #process the audio file
    #recording.uri

    return str(resp)

@app.route("/recording", methods=['GET', 'POST'])
def process_recording():
    # Start our TwiML response
    resp = VoiceResponse()
    resp.say("Thank you, I'm processing your problem. Hang on!")
    #rid = request.args.get('RecordingSid')



    url = 'https://api.twilio.com/2010-04-01/Accounts/'+ account_sid +'/Recordings/'+ rid
    r = requests.get(url, allow_redirects=True)
    open('rec.wav', 'wb').write(r.content)
    #process the audio file

    t = speechAPI()

    #text = t.start_transcribing('rec.wav')

    #speech-text with automatic punctuation
    sc = speech.SpeechClient()
    with io.open('rec.wav', 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True)

    #choose the best punctuation
    transcript = []
    text = sc.recognize(config, audio)
    for i, result in enumerate(text.results):
        alternative = result.alternatives[0]
        transcript.append(alternative.transcript)
        #break

    transcript = ' '.join(transcript)
    ts = text_summarizer()
    #text = 'Hi. My name is Paul. I am quite new to using SAP ERP products. Actually our company acquired SAP products last month. We were using a product from another vendor before. Alirght, so my question, is how do I implement planning phases inside the software. It has lots of features so it is difficult for me to go through each and every one of them and trying to find out what I need. Please refer to a specific page of the user guide or inuitive navigation guide. Thanks for the help.'
    summary = ts.summarize(transcript)

    resp.say("Thanks for your patience, unfortunately, I cannot help you in this matter. I will now redirect you to one of our experts and brief them on your problem.")
    #resp.redirect()
    render = '<div><h3> Service request </h3><p>'+transcript+'</p><h3> Summary </h3><p>'+summary+'</p></div>'

    return str(render)




if __name__ == "__main__":
    app.run(debug=True)
