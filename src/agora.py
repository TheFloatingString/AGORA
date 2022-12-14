import whisper

class Agora:

    def __init__(self):
        self.filepath = None
        self.whisper_model = whisper.load_model("base")
        self.generator_counter = 0
        self.initial_text = None
        self.output_text = None


    def transcribe(self, filepath):
        """
        The user only needs to call this method to transcribe 
        speech to generated output.
        """
        self.filepath = filepath
        self.initial_text = self.whisper_model.transcribe(self.filepath)
        return generate_output(self.initial_text)

    def generate_output(self, current_text):
        """
        Generates output based on current_text that is fed to this function
        """
        if not contains_hate_speech:
            self.output_text = current_text
            return generate_return_dict()

    def contains_hate_speech(self, text):
        """
        Checks if the current text contains hate speech
        """
        return False

    def genrate_return_dict(self):
        """
        Generates a return dict based on current class attributes
        """
        return_dict = {
                "inputFile": self.filepath,
                "initialText": self.initial_text,
                "outputText": self.output_text,
                "containsHateSpeech": None,
                "status": None,
                "error": None
                }

        return return_dict

    def __reinitialize_class(self):
        """
        Internal function that reinitalizes the class parameters after 
        completing speech to generated text procedure for each individual
        .transcribe() call
        """
        self.filepath = None
        self.generator_counter = 0
