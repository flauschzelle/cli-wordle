#!/usr/bin/env python3

# A wordle implementation for unix command line.
# This will probably not work correctly on Windows, sorry!

import random
from get_char import get_char
from generate_word_list import generate_word_list

# some parameters and defaults:

word_len: int = 5
language: str = "English"  # for a list of supported languages, see generate_word_list.py

max_guesses: int = max(6, word_len + max(1, (word_len//3)))
guesses: int = 0
guessed: list = []
default_message: str = "Type a word and\n press ENTER to guess!"
message: str = default_message
message_lines: int = 4
lines: int = max_guesses + message_lines


def load_words(lang: str, length: int) -> list:
	# loads the list of allowed words to guess
	filename = f"words_{lang.lower()}_{length}.txt"
	import os
	if not os.path.isfile(filename):
		if not generate_word_list(lang, length):
			print("Could not generate word list file.")
			# TODO: proper error handling
			return [""]

	file = open(filename, "r")
	words = []
	while True:
		line = file.readline()
		if not line:
			break
		words.append(line.strip())
	file.close()
	return words


all_words = load_words(language, word_len)

# choose a random word from the word list as the solution:

pick_number = random.randint(0, len(all_words))
solution = all_words[pick_number]

# make a list of all letters that are allowed:


def list_letters(words: list) -> list:

	letters: list = []
	for w in words:
		for l in w:
			if l not in letters:
				letters.append(l)
	letters.sort()
	return letters


allowed_letters: list = list_letters(all_words)

# some colors etc. for output formatting:

BGREEN = '\033[42m'
BYELLOW = '\033[43m'
BBLACK = '\033[40m'
BGRAY = '\033[100m' 

# BLACK = '\033[30m'
# WHITE = '\033[37m'
GRAY = '\033[90m'
GREEN = '\033[32m'
YELLOW = '\033[33m'


ENDC = '\033[0m'
BOLD = '\033[1m'

# helpful functions:


def bold_colored_text(text: str, color: str) -> str:
	ctext: str = f"{BOLD}{color} {text} {ENDC}"
	return ctext


def color_code_hints(text: str, pattern: str) -> str:
	ctext: str = ""
	hidden: list = []

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


def color_code_input(letter: str, place: int, pattern: str, prev_lines: list) -> str:

	hint_color: str = ""

	for li in prev_lines:
		if letter not in li:
			# no hints for this letter
			continue
		elif letter in li and letter not in pattern:
			hint_color = GRAY
			break
		elif li[place-1] == letter and pattern[place-1] == letter:
			hint_color = GREEN
			break
		elif letter in li and letter in pattern:
			hint_color = YELLOW
			# next line might still have a green hint
			continue

	if hint_color == "":
		text = f"{BOLD}{letter}{ENDC}"
	else:
		text = f"{BOLD}{hint_color}{letter}{ENDC}"
	return text


def display_guesses(from_line: int):
	for i in range (from_line, max_guesses):
		if i < guesses:
			print(" "+color_code_hints(guessed[i], solution))
		else:
			print(f" {BBLACK}{' '*3*word_len}{ENDC}")


def display_input_char(ch: str, place: int):
	# letters:
	if ch.isalpha():
		letter: str = color_code_input(ch.upper(), place, solution, guessed)
		print(f" {letter} ", end="", flush=True)
	# delete / backspace:
	elif ch == '\x7f':
		print("\b\b\b\x1B[0K", end="", flush=True)


def has_right_place(letter: str, word: str, pattern: str) -> bool:
	for i in range(len(word)):
		if word[i] == pattern[i] and word[i] == letter:
			return True
	return False


def display_alphabet(lang: str, letters: list, guessed_words: list, pattern: str) -> int:

	line_max: int = 13
	line_len: int = 0
	line_br: str = ""
	line_count: int = 4

	print(f" The following letters are allowed for {lang}:\n ")

	for ltr in letters:
		hint_color: str = ""
		for g in guessed_words:
			if ltr not in g:
				# no hints for this letter
				continue
			elif ltr in g and ltr not in pattern:
				hint_color = GRAY
				break
			elif has_right_place(ltr, g, pattern):
				hint_color = GREEN
				break
			elif ltr in g and ltr in pattern:
				hint_color = YELLOW
				# next guess might still have a green hint
				continue
		line_len += 1
		if line_len > line_max:
			line_len = 0
			line_count += 1
			line_br = "\n "
		print(f" {line_br}{hint_color}{ltr}{ENDC} ", end="")
		line_br = ""
	print("\n ")
	return line_count


# the actual game starts here:

print("\n Welcome to COMMAND LINE WORDLE!\n")
print(f" Guess the {language} word\n with {word_len} letters\n in {max_guesses} or less tries!\n")

# start with showing the empty grid:

display_guesses(0)
print(f"\n {message}\n")
lines = lines + display_alphabet(language, allowed_letters, guessed, solution)

# start input on the first empty grid line:

print(f"\x1B[{str(lines)}F\x1B[2K", end="")

while guesses < max_guesses:

	print(" ", end="", flush=True)

	current_input: str = ""

	while len(current_input) <= word_len:
		c: str = get_char()

		# in an empty line, only letters are allowed:
		if len(current_input) == 0:
			if c.isalpha():
				current_input += c
				display_input_char(c, len(current_input))
			elif c == '\x7f' or c == '\n':
				continue
			else:
				break

		# in an incomplete line, backspace is also allowed:
		elif len(current_input) < word_len:
			if c.isalpha():
				current_input += c
			elif c == '\x7f':
				current_input = current_input[0:-1]
			elif c == '\n':
				continue
			else:
				break
			display_input_char(c, len(current_input))

		# in a full line, only backspace or enter is allowed:
		elif len(current_input) == word_len:
			if c == '\x7f':
				current_input = current_input[0:-1]
				display_input_char(c, len(current_input))
			elif c.isalpha():
				continue
			elif c == '\n':
				break
			else:
				break

	# save the guess:
	guess = current_input.upper()

	# overwrite input line after entering:
	print("\x0D\x1B[0J", end="")

	current_line: int = guesses

	if guess in all_words:
		message = default_message
		guesses += 1
		guessed.append(guess)
	else:
		message = f"{guess} is not a valid word.\n Try again!"

	display_guesses(current_line)
	
	if guess == solution:
		print(f"\n Solved in {guesses}/{max_guesses} tries :)\n")
		break

	if guesses >= max_guesses:
		print("\n No more tries left, sorry :(\n")
		break

	print(f"\n {message}\n")
	display_alphabet(language, allowed_letters, guessed, solution)

	# set the cursor to start the input on the next empty line:
	print(f"\x1B[{str(lines-guesses)}F\x1B[2K", end="")

# in case you want to look up the word in your text file later:
print(f" (Random word number {pick_number+1} of {len(all_words)})\n")
