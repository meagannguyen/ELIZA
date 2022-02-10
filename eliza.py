# Name: Meagan Nguyen
# CMSC 416: Introduction to NLP
# Date: February 08, 2022
# Programming Assignment 1: ELIZA

# This project utilizes the fundamentals of Natural Language Processing such as regular expressions,
# word spotting and transform rules to reimplement a form of ELIZA, a Rogerian psychotherapist chatbot.

# Example input/output:
#   Hello, I'm Eliza, your interactive psychotherapist. Who am I speaking with today?
#   Hi, I'm Meagan.
#   Hi Meagan, what's been on your mind?
#   [Meagan]: I am sad
#   You are feeling sad?
#   [Meagan]: Yes
#   I see.
#   [Meagan]: My life is in shambles
#   Why do you think your life is in shambles?
#   [Meagan]: My mother hates me
#   How do you feel about that?
#   [Meagan]: I feel lonely
#   When do you usually feel lonely?
#   [Meagan]: I am lonely most of the time
#   What are your thoughts on feeling lonely most of the time?
#   [Meagan]: Goodbye
#   Have a great day! I'll always be here if you need me. :)

# Algorithm:
#   1. Define a list of common Rogerian regexes with sublists of responses for that regex
#   2. Define a list dictionary of common complementary pronouns and helping verbs
#   3. Define a class elizaProcessing that:
#       a. Initialize keys (inp => regexes) and values (outp => sublists of responses)
#       b. Define a function replace() that tokenizes the user input and finds matching keys to replace for output
#       c. Define a function converse() that finds, compiles and generates a response for ELIZA to print
#   4. Define a function eliza() that:
#       a. Prints out ELIZA's salutation and asks for name as user input
#       b. Transforms entire input to lowercase and tokenizes word-by-word
#       c. Assigns the last word of the input as the user's name
#       d. Removes period at end of name, capitalizes it and adds it to start of user prompt
#       e. If user input is not an "exit" phrase, continue conversation
#           i. Otherwise, output ELIZA's concluding phrase and end program

# Usage:
#   python eliza.py

import random
import re

responseList = [
    # Regex for a phrase that starts with "I am"
    [r"I am (.*)",
     ["Sorry to hear you are feeling %1.",
      "Why do you feel %1?",
      "What are your thoughts on feeling %1?",
      "You are feeling %1?"
      ]
     ],

    # Regex for a phrase that starts with "I think"
    [r"I think (.*)",
     ["Do you really think %1?",
      "Why do you think so?"]
     ],

    # Regex for a phrase that starts with "I want"
    [r"I want (.*)",
     ["Why do you want %1?",
      "What would you do if you got %1?"]
     ],

    # Regex for a phrase that starts with "I feel"
    [r"I feel (.*)",
     ["Tell me more about these feelings.",
      "When do you usually feel %1?"]
     ],

    # Regex for a phrase that starts with "I don't"
    [r"I don\'?t (.*)",
     ["Why don't you %1?",
      "Are you sure you don't %1?",
      "Please elaborate more on why you don't %1."]
     ],

    # Regex for a phrase that starts with "I have"
    [r"I have (.*)",
     ["Since you have %1, tell me more about it.",
      "Why do you have %1?"]
     ],

    # Regex for a phrase that starts with "My"
    [r"My (.*)",
     ["I see, your %1.",
      "How do you feel about that?",
      "Why do you think your %1?"]
     ],

    # Regex for a phrase that starts with "You"
    [r"You (.*)",
     ["Don't worry about me, this time is about you.",
      "I don't want to discuss me, I want to discuss you.",
      "I'm here to talk about you, not me."]
     ],

    # Regex for the word "Yes"
    [r"Yes",
     ["I see.",
      "Are you sure?",
      "I admire your confidence.",
      "Please tell me more."]
     ],

    # Regex for when a phrase contains the word "mother"
    [r"(.*) mother(.*)",
     ["Tell me more about your mother.",
      "What is your relationship with your mother like?",
      "How do you feel about your mother?"]
     ],

    # Regex for when a phrase contains the word "father"
    [r"(.*) father(.*)",
     ["Tell me more about your father.",
      "What is your relationship with your father like?",
      "How do you feel about your father?"]
     ],

    # Regex for "Goodbye" or "bye"
    [r"(Good)*bye",
     ["Have a great day! I'll always be here if you need me. :)"]
     ],

    # Regex for the word "quit"
    [r"quit",
     ["Have a great day! I'll always be here if you need me. :)"]
     ],

    # Regex for the word "exit"
    [r"exit",
     ["Have a great day! I'll always be here if you need me. :)"]
     ],

    # Regex for any other word or phrase
    [r"(.*)",
     ["Interesting.",
      "I'm not sure how to respond.",
      "I see.",
      "Please tell me more."]
     ]
]

complements = {
    "i": "you",
    "you": "me",
    "me": "you",
    "my": "your",
    "your": "my",
    "am": "are",
    "are": "am",
    "was": "were",
    "were": "was",
}

class elizaProcessing:
    # initializes keys (user input) and values (program output) in list of responses
    def __init__(self):
        self.inp = list(map(lambda x: re.compile(x[0]), responseList))
        self.outp = list(map(lambda x: x[1], responseList))

    # translates the tokenized user input to corresponding ELIZA responses
    def replace(self, userInput, responses):
        s = ' '
        tokens = userInput.lower().split()
        dictKeys = responses.keys()
        # finds tokenized input as key in list of responses
        for i in range(0, len(tokens)):
            if tokens[i] in dictKeys:
                tokens[i] = responses[tokens[i]]
        return s.join(tokens)

    # finds and generates a response for ELIZA to print
    def converse(self, userInput):
        for i in range(0, len(self.inp)):
            # checks if user input matches keywords
            if self.inp[i].search(userInput):
                # randomly chooses from list of responses
                rand = random.choice(self.outp[i])
                # searches for a % delimiter to substitute for rest of ELIZA output
                x = rand.find('%')
                while x >= 0:
                    index = float(rand[x+1:x+2])
                    index2 = int(index)
                    rand = rand[:x] + self.replace(self.inp[i].search(userInput).group(index2), complements) + rand[x+2:]
                    x = rand.find('%')
                return rand
        return None

# Sets up ELIZA chatbot for conversation with user
def eliza():
    inputName = input("Hello, I'm Eliza, your interactive psychotherapist. Who am I speaking with today?\n")
    nameInput = inputName.lower()
    splitNameInput = nameInput.split()
    name = splitNameInput[-1]
    # Removes period at end of name if found
    if '.' in name:
        name = name.removesuffix('.')
    print("Hi " + name.capitalize() + ", what's been on your mind?")
    string = ""
    doc = elizaProcessing()
    while string != 'goodbye':
        string = input('[' + name.capitalize() + ']: ' )
        print(doc.converse(string))
        # ends program if ELIZA responds with this phrase
        if doc.converse(string) == "Have a great day! I'll always be here if you need me. :)":
            break

eliza()