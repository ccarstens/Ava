import pyttsx3


class Output:
    def __init__(self):
        self.synthesizer = pyttsx3.init(debug=True)
        self.voice = list(filter(lambda sv: ('Tracy' in sv.name),
                                 self.synthesizer.getProperty('voices')))[0]
        self.synthesizer.setProperty('voice', self.voice.id)
        self.synthesizer.setProperty('rate', 175)

        self.setup_callbacks()


    def setup_callbacks(self):
        self.synthesizer.connect('finished-utterance', self.on_finished_utterance)
        self.synthesizer.connect('started-word', self.on_started_word)

    def speak(self, utterance, name=""):
        pass

    def on_finished_utterance(self, name, completed):
        pass

    def on_started_word(self, name, location, length):
        pass





# for i, v in enumerate(voices):
#     if 'en' in v.languages[0]:
#         print(i, v.name, v.languages)
# engine.say("Ciao bella! Como va. Ma che freddo fa")
# engine.say("#LAUGH01# Lauren want's to have dinner with you! What do you say?")
# engine.say("#LAUGH01# Okay! I'll go ahead and ask! Is there anything else?")
tracy.say("Sally sells seashells by the seashore.", "shells")
START = datetime.now()
tracy.startLoop()
print("there")