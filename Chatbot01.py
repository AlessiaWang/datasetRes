#import the ChatterBot library
from chatterbot import ChatBot

#import ListTrainer to train the bot based on pre-determined list data
from chatterbot.trainers import ListTrainer

#import logic adapter for matching responses
from chatterbot.logic import LogicAdapter

#import statement for defining user inputs
from chatterbot.conversation import Statement

#import the os module to enable interacting with the operating system
import os

#import yaml
import yaml

#load the flask framework to run web applications
from flask import Flask, render_template, request

#build my own logic adapter
class FixedAnswerLogicAdapter(LogicAdapter):
    def __init__(self, bot, **kwargs):
        super().__init__(bot, **kwargs)
        #define multiple fixed questions and responses
        self.fixed_responses = {
            'Find me local cafés': 'I found some information about local cafés. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">',
            'find me local café': 'I found some information about local cafés. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">',
            'find me local cafes': 'I found some information about local cafés. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">',
            'find me local cafe': 'I found some information about local cafés. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">',
            'which one do you recommend?':'Well, all of them are pretty good! You can choose any of them.',
        }

    def can_process(self, statement):
        #check if an input matches with any fixed questions
        return statement.text.lower() in [q.lower() for q in self.fixed_responses]

    def process(self, input_statement, additional_response_selection_parameters):
        #return fixed responses according to specific inputs
        response_text = self.fixed_responses.get(input_statement.text.lower(), "Sorry, I don't understand. Could you please say it again?")
        response = Statement(response_text)
        response.confidence = 1
        return response

#build and define the database's path of this chatbot
bot = ChatBot('Alex01',
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database1.db',logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "Sorry, I didn't get you. Could you please say it again?",
            'maximum_similarity_threshold': 0.65 
        }
    ])

#append my own logic adapter to the bot's logic adapters
fixed_answer_adapter = FixedAnswerLogicAdapter(bot)
bot.logic_adapters.append(fixed_answer_adapter)


#get the directory of the yaml files
yaml_directory = "./Corpus"

#train the chatbot with list data
trainer = ListTrainer(bot)

#the list data that I used to show my stimuli
trainer.train(['find me cafés in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find me café in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find me cafes in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find me cafe in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find cafés in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find café in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find cafes in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])
trainer.train(['find cafe in amsterdam', 'I found some information about the cafés in Amsterdam. \n <img src="https://github.com/AlessiaWang/myimage/blob/main/stimuli.png?raw=true" height="500">'])

#get all the yaml files in this directory
for filename in os.listdir(yaml_directory):
    if filename.endswith('.yml') or filename.endswith('.yaml'):
        filepath = os.path.join(yaml_directory, filename)

#read yaml files from my corpus
        with open(filepath, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

#train the chatbot with yaml files
        for conversation in data.get('conversations', []):
            trainer.train(conversation)
            