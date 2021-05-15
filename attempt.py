from challenge import MathChallenge

class Attempt:
    def __init__(self,input,challenge):
        self.input = input
        self.challenge = challenge
        self.success = True if input == challenge.problem['answer'] else False


#y = MathChallenge('subtraction')
#a = Attempt(60,y)
#print(a.success)