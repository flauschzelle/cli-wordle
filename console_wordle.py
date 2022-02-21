#!/usr/bin/env python3

# A wordle implementation for unix terminals. 
# This will probably not work correctly on Windows, sorry!


# some parameters and defaults:

word_len = 5
max_guesses = word_len + (word_len//4)
guesses = 0
guessed = []
message = "Type a word and press ENTER to guess!"
message_lines = 3
lines = max_guesses + message_lines

# load the list of allowed words to guess:
def load_words(word_len) -> list:
	filename = "words" + str(word_len) + ".txt"
	file = open(filename, "r")
	words = []
	while(True):
		line = file.readline()
		if not line:
			break
		words.append(line.strip().upper())
	file.close()
	return words

all_words = load_words(word_len)

solution = "WORLD"

# some colors etc for output formatting:

BGREEN = '\033[42m'
BYELLOW = '\033[43m'
BBLACK = '\033[40m'
BGRAY = '\033[100m' 

BLACK = '\033[30m'
WHITE = '\033[37m'

ENDC = '\033[0m'
BOLD = '\033[1m'

# helpful functions:

def bold_colored_text(text: str, color: str) -> str:
	ctext = f"{BOLD}{color} {text} {ENDC}"
	return ctext

def color_code_hints(text: str, pattern: str) -> str:
	ctext = ""
	hidden = []

	for i in range (len(pattern)):
		if text[i] != pattern[i]:
			hidden.append(pattern[i])

	for i in range (len(pattern)):
		if text[i] == pattern[i]:
			ctext += bold_colored_text(text[i], BGREEN)
		elif text[i] in hidden:
			ctext += bold_colored_text(text[i], BYELLOW)
			hidden.remove(text[i])
		else:
			ctext += bold_colored_text(text[i], BGRAY)
	return ctext

def display_guesses(from_line: int):
	for i in range (from_line, max_guesses):
		if i < guesses:
			print(" "+color_code_hints(guessed[i], solution))
		else:
			print(f" {BBLACK}{' '*3*word_len}{ENDC}")

# the actual game starts here:

print("\n Welcome to CONSOLE WORDLE!")
print(" Guess the secret", word_len, "letter word in", max_guesses, "or less tries!\n")

# start with showing the empty grid:

display_guesses(0)
print(f"\n {message}\n")

# start input on the first empty grid line:

print(f"\x1B[{str(lines)}F\x1B[2K", end="")

while guesses < max_guesses:

	# truncate input string and convert to uppercase:
	guess = str(input(" "))[0:word_len].upper()

	print("\x1B[1F\x1B[0J", end="") # overwrite input line after entering

	current_line = guesses

	if len(guess) == word_len and (guess in all_words):
		message = "Type a word and press ENTER to guess!"
		guesses += 1
		guessed.append(guess)
	else:
		message = f"{guess} is not a valid word. Try again!"

	display_guesses(current_line)
	
	if guess == solution:
		print(f"\n Solved in {guesses}/{max_guesses} tries :)\n")
		break

	if guesses >= max_guesses:
		print("\n No more tries left, sorry :(\n")
		break

	print(f"\n {message}\n")

	# set the cursor to start the input on the next empty line:
	print(f"\x1B[{str(lines-guesses)}F\x1B[2K", end="")

