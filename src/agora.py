import whisper
import openai
import os
import dotenv
import time

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Agora:

    def __init__(self):
        self.filepath = None
        self.whisper_model = whisper.load_model("base")

        self.generator_counter = 0
        self.initial_text = None
        self.output_text = None


    def transcribe_audio(self, filepath):
        """
        The user only needs to call this method to transcribe 
        speech to generated output.
        """
        self.filepath = filepath
        self.initial_text = self.whisper_model.transcribe(self.filepath)["text"]
        return self.generate_output(self.initial_text)


    def generate_output(self, current_text):
        """
        Generates output based on current_text that is fed to this function
        """
        print(f"current iteration: {self.generator_counter}")

        print(current_text)

        if not self.contains_hate_speech(current_text) or self.generator_counter>10:
            self.output_text = current_text
            return self.generate_return_dict()
        else:
            response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Paraphrase the following phrase in a non-offensive way: \"{current_text}\"",
                    temperature=0.5,
                    max_tokens=250,
                    top_p=1.0,
                    frequency_penalty=0.8,
                    presence_penalty=0.0
                )
            new_text = response["choices"][0]["text"].replace("\n", "")
            self.generator_counter += 1
            self.generate_output(new_text)

    def contains_jigsaw_hate_speech(self, text):
        """
        Checks if the current text contains hate speech based on the Jigsaw criteria
        """
        openai_prompt = f"Does the following text contain one or more of toxic, severe toxic, obscene, threat, insult or identity hate: \"{text}\""

        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=openai_prompt,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.8,
                presence_penalty=0.0
                )
        
        text_response = response["choices"][0]["text"]
 
        return_dict = {
                "toxic": False,
                "severe toxic": False,
                "obscene": False,
                "threat": False,
                "insult": False,
                "identity hate": False
                }

        if text_response[0:2].lower() == "no":
            return return_dict

        list_of_items = text_response.split(",")

        for item in list_of_items:
            item = item.strip().lower()
            if item in return_dict.keys():
                return_dict[item] = True
        
        # the time.sleep(3) acts as a rate-limiting function (20 requests/minute) as supported
        # by OpenAI with the free tier
        time.sleep(3)

        return return_dict


    def contains_hate_speech(self, text):
        """
        Checks if the current text contains hate speech
        """
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Does the following prompt contain offensive language: \"{text}\"",
                temperature=0.5,
                max_tokens=250,
                top_p=1.0,
                frequency_penalty=0.8,
                presence_penalty=0.0
                )
    
        decision = response["choices"][0]["text"].replace("\n", "").lower()
        if decision[0:3] == "yes":
            return True
        elif decision[0:2] == "no":
            return False
        else:
            print(response)
            raise ValueError(f"GPT-3 cannot determine whether the current prompt contains offensive language: \"{text}\"") 


    def generate_return_dict(self):
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
