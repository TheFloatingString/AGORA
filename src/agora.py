import whisper
import openai
import os
import dotenv
import time
from openai import OpenAI
import pandas as pd

dotenv.load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

class Agora:
    def __init__(self):
        self.filepath = None
        self.whisper_model = whisper.load_model("base")
        self.generator_counter = 0
        self.initial_text = None
        self.output_text = None
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_AGORA"))
        self.dict_to_pandas = dict()

    def config_pandas_dict(self, true_label, true_label_detail, true_transcript):
        self.dict_to_pandas["true_label"] = true_label
        self.dict_to_pandas["true_label_detail"] = true_label_detail
        self.dict_to_pandas["true_transcript"] = true_transcript

    def export_pandas_dict(self):
        self.dict_to_pandas["n_iterations"] = self.generator_counter
        if self.generator_counter == 0:
            self.dict_to_pandas["predict_label"] = "non-toxic"
        elif self.generator_counter > 0:
            self.dict_to_pandas["predict_label"] = "toxic"
        self.dict_to_pandas["initial_whisper_text"] = self.initial_text
        self.dict_to_pandas["output_text"] = self.output_text
        return self.dict_to_pandas

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
        # print(current_text)
        if not self.contains_hate_speech(current_text) or self.generator_counter>10:
            self.output_text = current_text
            return self.generate_return_dict()
        else:
            response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    # model="gpt-4-0125-preview",
                    messages=[
                        {"role":"user", "content": f"Paraphrase the following phrase in a non-offfensive way: \"{current_text}\" Only provide the rephrased text with nothing else."}
                        ]
                    )
            new_text = response.choices[0].message.content
            '''
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
            '''
            self.generator_counter += 1
            self.generate_output(new_text)

    def contains_jigsaw_hate_speech(self, text):
        """
        Checks if the current text contains hate speech based on the Jigsaw criteria
        """
        # openai_prompt = f"Does the following text prompt contain one or several of toxic, severe toxic, obscene, threat, insult or identity hate: \"{text}\"Provide a single answer: \"yes\" or \"no\"."
        openai_prompt = f"Does the following text prompt contain toxic or offensive language: \"{text}\" Provide a single answer: \"yes\" or \"no\"."
        # openai_prompt = f"Does the following text contain harmful content: \"{text}\" Provide a singel answer: \"yes\" or \"no\"."
        print(openai_prompt)
        response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                # model="gpt-4-0125-preview",
                messages=[
                    {"role":"user", "content":openai_prompt}
                    ]
                )
        text_response = response.choices[0].message.content
        '''
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=openai_prompt,
                temperature=0.5,
                top_p=1.0,
                frequency_penalty=0.8,
                presence_penalty=0.0
                )
        text_response = response["choices"][0]["text"]
        '''
        return_dict = {
                "toxic": False,
                "severe toxic": False,
                "obscene": False,
                "threat": False,
                "insult": False,
                "identity hate": False
                }
        
        if text_response.lower() == "no":
            return False
        else:
            return True

        # print(text_response)
        # if text_response[0:2].lower() == "no":
        #     return return_dict
        # list_of_items = text_response.split(",")
        # for item in list_of_items:
        #     item = item.strip().lower()
        #     if item in return_dict.keys():
        #         return_dict[item] = True
        
        # the time.sleep(3) acts as a rate-limiting function (20 requests/minute) as supported
        # by OpenAI with the free tier
        time.sleep(3)

        return return_dict


    def contains_hate_speech(self, text):
        """
        Checks if the current text contains hate speech
        """
        jigsaw_pred = self.contains_jigsaw_hate_speech(text)
        # print(jigsaw_pred.values())
        # if True in jigsaw_pred.values():
        if jigsaw_pred:
            return True
        else:
            return False


        # archived code
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
    """

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
