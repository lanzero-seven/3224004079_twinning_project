# test_step4.py
import random
from generator import generate_exercises
from utils import save_exercises, save_answers

random.seed(3)
exs = generate_exercises(5, 10)
save_exercises(exs, "Exercises.txt")
save_answers(exs, "Answers.txt")

print("Exercises.txt:")
print(open("Exercises.txt", encoding="utf-8").read())
print("Answers.txt:")
print(open("Answers.txt", encoding="utf-8").read())