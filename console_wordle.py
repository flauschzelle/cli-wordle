#!/usr/bin/env python3

solution = "wordl"
guesses = 0
max_guesses = 6

print("Welcome to CONSOLE WORDLE!")
print("Can you guess the secret word in", max_guesses, "or less tries?\n\n")

while guesses < max_guesses:

	guess = str(input())
	print(guess)

	guesses += 1
	
	if guess == solution:
		print("You found the secret word in", guesses, "tries :)")
		break

	if guesses >= max_guesses:
		print("No more tries lief, sorry :(")
		break
