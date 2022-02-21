#!/usr/bin/env python3

# A wordle implementation for unix terminals. 
# This will probably not work correctly on Windows, sorry!

solution = "WORDL"
word_len = 5
guesses = 0
max_guesses = 6
guessed = []
message = "Type a word and press ENTER to guess!"

BGREEN = '\033[42m'
BYELLOW = '\033[43m'
BBLACK = '\033[40m'
BGRAY = '\033[100m' 

BLACK = '\033[30m'
WHITE = '\033[37m'

ENDC = '\033[0m'
BOLD = '\033[1m'

print("\n Welcome to CONSOLE WORDLE!")
print(" Can you guess the secret", word_len, "letter word in", max_guesses, "or less tries?\n")

def bold_colored_text(text: str, color: str) -> str:
	ctext = f"{BOLD}{color} {text} {ENDC}"
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

def display_guesses(from_line: int):
	for i in range (from_line, max_guesses):
		if i < guesses:
			print(" "+color_code_hints(guessed[i], solution))
		else:
			print(f" {BBLACK}{' '*3*word_len}{ENDC}")

# start with showing the empty grid:
display_guesses(0)
print(f"\n {message}\n")

# set the cursor to start the input on the first empty grid line:
print("\x1B[9F\x1B[2K", end="")

while guesses < max_guesses:

	# truncate input string and convert to uppercase:
	guess = str(input(" "))[0:word_len].upper()

	print("\x1B[1F\x1B[0J", end="") # overwrite input line after entering

	current_line = guesses

	if guess.isalpha() and len(guess) == word_len:
		message = "Type a word and press ENTER to guess!"
		guesses += 1
		guessed.append(guess)
	else:
		message = f"{guess} is not a valid word. Try again!"

	display_guesses(current_line)
	
	if guess == solution:
		print("\n You found the secret word",
			f"in {guesses}/{max_guesses} tries :)\n")
		break

	if guesses >= max_guesses:
		print("\n No more tries left, sorry :(\n")
		break

	print(f"\n {message}\n")

	# set the cursor to start the input on the next empty line:
	print(f"\x1B[{str(9-guesses)}F\x1B[2K", end="")

