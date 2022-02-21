#!/usr/bin/env python3

# A wordle implementation for unix terminals. 
# This will not work correctly on Windows, sorry!

solution = "wordl"
guesses = 0
max_guesses = 6

print("Welcome to CONSOLE WORDLE!")
print("Can you guess the secret word in", max_guesses, "or less tries?\n")

while guesses < max_guesses:

	guess = str(input())
	
	print("\x1B[F\x1B[2K", end="") #overwrite input line after entering
	print(guess)

	guesses += 1
	
	if guess == solution:
		print("\nYou found the secret word",
			f"in {guesses}/{max_guesses} tries :)\n")
		break

	if guesses >= max_guesses:
		print("\nNo more tries left, sorry :(\n")
		break
