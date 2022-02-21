#!/usr/bin/env python3

# A wordle implementation for unix terminals. 
# This will not work correctly on Windows, sorry!

solution = "WORDL"
word_len = 5
guesses = 0
max_guesses = 6

BGREEN = '\033[42m'
BYELLOW = '\033[43m'
BBLACK = '\033[40m'
BGRAY = '\033[100m' 

BLACK = '\033[30m'
WHITE = '\033[37m'

ENDC = '\033[0m'
BOLD = '\033[1m'

print("Welcome to CONSOLE WORDLE!")
print("Can you guess the secret", word_len, "letter word in", max_guesses, "or less tries?\n")

def bold_colored_text(text: str, color: str) -> str:
	ctext = f"{BOLD}{color}{text}{ENDC}"
	return ctext

def color_code_hints(text: str, pattern: str) -> str:
	ctext = ""
	for i in range (len(pattern)):
		if text[i] == pattern[i]:
			ctext += bold_colored_text(text[i], BGREEN)
		elif text[i] in pattern:
			ctext += bold_colored_text(text[i], BYELLOW)
		else :
			ctext += bold_colored_text(text[i], BGRAY)
	return ctext
	
while guesses < max_guesses:

	# truncate input string and convert to uppercase:
	guess = str(input())[0:word_len].upper()

	print("\x1B[F\x1B[2K", end="") # overwrite input line after entering

	if len(guess) < word_len:
		print(f"      {guess} is too short.",
			 f"Words must be {word_len} letters long!")
		continue

	if not guess.isalpha():
		print(f"      {guess} contains invalid characters.",
			 "Only letters are allowed!")
		continue

	print(color_code_hints(guess, solution))

	guesses += 1
	
	if guess == solution:
		print("\nYou found the secret word",
			f"in {guesses}/{max_guesses} tries :)\n")
		break

	if guesses >= max_guesses:
		print("\nNo more tries left, sorry :(\n")
		break
