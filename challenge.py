import random


class MathChallenge():
    def __init__(self,operation):
        self.problem = self.get_problem(operation)


    def get_problem(self,operation):
        if operation == 'subtraction':
            return self.subtraction_problem()
        elif operation == 'addition':
            return self.addition_problem()

    def subtraction_problem(self):
        first_num = random.randint(50,100)
        second_num = random.randint(0,first_num)
        answer = first_num - second_num
        return ({'question':f'What is {first_num} - {second_num}?','answer':answer})

    def addition_problem(self):
        first_num = random.randint(0,50)
        second_num = random.randint(0,50)
        answer = first_num + second_num
        return ({'question':f'What is {first_num} + {second_num}?','answer':answer})


