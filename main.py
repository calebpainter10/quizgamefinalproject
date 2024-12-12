# ------ Imports ------
import random
import json
import os

# ------ Static Variables ------
prize_ladder = [
    "1,000",
    "2,000",
    "3,000",
    "4,000",
    "5,000",
    "10,000",
    "25,000",
    "50,000",
    "100,000",
    "250,000",
    "500,000",
    "1,000,000"
]


# ------ Question Classes ------
class Question:
    def __init__(self, title, answer, difficulty):
        self.title = title
        self.answer = [a.lower() for a in list(answer)]
        self.difficulty = difficulty
        self.next = None
    
    def __eq__(self, comparison): # == overloading
        return comparison in self.answer
    
    def __ne__(self, comparison): # != overliading
        return comparison not in self.answer

class MultipleChoice(Question):
    def __init__(self, title, answer, difficulty, options: dict):
        super().__init__(title, answer, difficulty)

        for a in answer:
            if a.lower() not in ["a", "b", "c", "d"]:
                raise ValueError("Unexpected answer") 

        self.options = options

class TrueFalse(Question):
    def __init__(self, title, answer, difficulty, options: dict):
        super().__init__(title, answer, difficulty)

        for a in answer:
            if a.lower() not in ["true", "false", "t", "f"]:
                raise ValueError("Unexpected answer")
        
        self.options = options

class QuizLinkedList:
    def __init__(self):
        self.length = 0
        self.head = None
    
    def add_question(self, node):
        node.next = self.head
        self.head = node
        self.length += 1
    
    def load_questions(self):
        with open("questions.json", "r") as qfile:
            qdata = json.load(qfile)
        
        diff_sort = lambda q: q.get("difficulty")

        questions = qdata.get("questions", [])
        selected_questions = random.sample(questions, 12)
        sorted_questions = sorted(selected_questions, key=diff_sort, reverse=True)
        
        for i, q in enumerate(sorted_questions):
            title = q["title"]
            qtype = q["type"]
            difficulty = q["difficulty"]
            answers = q["data"]
            answer = q["answer"]

            if qtype == "Multiple Choice":
                self.add_question(node=MultipleChoice(title, answer, difficulty, options=answers))
            elif qtype == "True/False":
                self.add_question(node=TrueFalse(title, answer, difficulty, options=answers))
            else:
                print("Unable to load unrecognized question.")
            
            print(f"${prize_ladder[i]} question loaded.")


    def start_game(self):
        current_question = self.head
        question_number = 1

        print("---------------------------")
        print("Welcome to:")
        print("--- Who Wants to be a Millionare? (Pi Edition) ---")

        while current_question: # While the question is current_question, current_question will be modified at the end
            question = current_question.title
            options = current_question.options
            difficulty = current_question.difficulty
            current_prize = prize_ladder[question_number - 1]

            print(f"Question #{question_number}, ${current_prize} | Difficulty: {difficulty}\n{question}")
            print("\nOptions:")

            for key,value in options.items():
                print(f"[{key.upper()}] - {value}") # Print choices

            print("---------------------------")

            while True: # Ensure correct input
                response = input("Your answer: ").lower()
            
                if response == current_question: # Correct
                    print("Correct!\n[Blinking Green LED]")
                    print("---------------------------")
                    break
                elif isinstance(current_question, MultipleChoice) and response not in ["a", "b", "c", "d"] or isinstance(current_question, TrueFalse) and response not in ["true", "false", "t", "f"]: # Response is not valid
                    print("Invalid input detected. If the question is multiple choice, make sure to reply with the correct letter choice (e.g. 'a')")
                else: # Incorrect
                    print("Incorrect!\n[Solid Red LED]")
                    print(f"Unfortunately, you have lost the game. You got to: ${prize_ladder[question_number - 1] if question_number != 1 else '0'}")
                    os._exit(0)
                
            question_number += 1
            current_question = current_question.next
    
        print("---------------------------")
        print("Congratulations!\nYou have won Who Wants to be a Millionare! (Pi Edition, of course)")
            

qll = QuizLinkedList()
qll.load_questions()
qll.start_game()