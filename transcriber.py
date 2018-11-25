import speech_recognition as sr

class transcriber():
	def __init__(self):
		self.temp = []
		self.BING_KEY = "918c6d85f1ed4cbbb5c3c9508a071198"
		self.GOOGLE_KEY = "3f3adc032e8cecc2bc74801ce7067a5b16880eba"
	def transcribe_audio(self, audio_file):
		transcribed_text = None
		r = sr.Recognizer()
		cur_recording = sr.AudioFile(audio_file)
		with cur_recording as source:
			audio = r.record(source)
			print (type(audio))

		try:
			transcribed_text = r.recognize_google(audio, key =self.GOOGLE_KEY, language=('en-US'))
			print (transcribed_text)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
		return transcribed_text
