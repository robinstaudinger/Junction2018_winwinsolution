import argparse
import base64
import sys, os

from googleapiclient import discovery
import httplib2, sys

from oauth2client.client import GoogleCredentials

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="api-key.json"

class speechAPI():

	def __init__(self):
		self.DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
			'version={apiVersion}')

	def get_speech_service(self):
	    credentials = GoogleCredentials.get_application_default().create_scoped(['https://www.googleapis.com/auth/cloud-platform'])
	    http = httplib2.Http()
	    credentials.authorize(http)
	    return discovery.build('speech', 'v1beta1', http=http, discoveryServiceUrl=self.DISCOVERY_URL)


	def start_transcribing(self, speech_file):
	    """Transcribe the given audio file.

	    Args:
	        speech_file: the name of the audio file.
	    """
	    with open(speech_file, 'rb') as speech:
	        speech_content = base64.b64encode(speech.read())


	    service = self.get_speech_service()

	    service_request = service.speech().syncrecognize(
	        body={
	            'config': {
	                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
	                'sampleRate': 8000,  # 16 khz
	                'languageCode': 'en-US',  # a BCP-47 language tag
	            },
	            'audio': {
	                'content': speech_content.decode('UTF-8')
	                }
	            })
	    response = service_request.execute()
	    output_str = response['results'][0]['alternatives'][0]['transcript']

	    return output_str

if __name__ == '__main__':

    audio_file = 'self_test_mono.wav'
    google_speech_api = speech_API()
    transcribed_text = google_speech_api.start_transcribing(audio_file)
    print ('google thinks, you have said: \n')
    print (transcribed_text)
