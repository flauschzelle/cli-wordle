#!/usr/bin/env python3

# A wordle implementation for command line terminals.

from random import randint
from get_char import get_char
from generate_word_list import generate_word_list

# some parameters:

word_len: int = 5
language: str = "English"  # for a list of supported languages, see generate_word_list.py

# ANSI escape codes for output formatting:

BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLACK = '\033[40m'
BG_GRAY = '\033[100m'

GRAY = '\033[90m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

END = '\033[0m'
BOLD = '\033[1m'


def load_words(lang: str, length: int) -> list:
	"""
	creates a list of n-letter words of a language
	:param lang: the language to load words from
	:param length: number of letters (n) in each word
	:return: a list of words with n letters
	"""
	filename = f"words_{lang.lower()}_{length}.txt"
	import os
	if not os.path.isfile(filename):
		if not generate_word_list(lang, length):
			print("Could not generate word list file.")
			return []

	file = open(filename, "r")
	words = []
	while True:
		line = file.readline()
		if not line:
			break
		words.append(line.strip())
	file.close()
	return words


def list_letters(words: list) -> list:
	"""
	lists all letters that are allowed
	:param words: a word list to extract the letters from
	:return: a sorted list of all letters in the word list
	"""
	letters: list = []
	for w in words:
		for ltr in w:
			if ltr not in letters:
				letters.append(ltr)
	letters.sort()
	return letters


def bold_colored_text(text: str, color: str) -> str:
	"""
	applies bold, spacing and color to the text
	:param text: the text to be formatted
	:param color: background or text color (ANSI code)
	:return:
	"""
	ctext: str = f"{BOLD}{color} {text} {END}"
	return ctext


def color_code_hints(text: str, pattern: str) -> str:
	"""
	applies hint colors to the given word
	:param text: the text to be colored
	:param pattern: the solution to derive the hints from
	:return: the given word in bold text with hint colors
	"""
	ctext: str = ""
	hidden: list = []

	for i in range(len(pattern)):
		if text[i] != pattern[i]:
			hidden.append(pattern[i])

	for i in range(len(pattern)):
		if text[i] == pattern[i]:
			ctext += bold_colored_text(text[i], BG_GREEN)
		elif text[i] in hidden:
			ctext += bold_colored_text(text[i], BG_YELLOW)
			hidden.remove(text[i])
		else:
			ctext += bold_colored_text(text[i], BG_GRAY)
	return ctext


def color_code_input(letter: str, place: int, pattern: str, prev_lines: list) -> str:
	"""
	applies input line hint colors to a letter
	:param letter: the letter to be checked
	:param place: position of the letter in the input line
	:param pattern: the solution to derive hints from
	:param prev_lines: words that were guessed before
	:return: a string of one letter in bold, with hint color and spacing
	"""
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
	text = bold_colored_text(letter, hint_color)
	return text


def display_guesses(word_length: int, from_line: int, max_rows: int, filled_rows: list, pattern: str):
	"""
	prints the guessed word(s) with nice formatting,
	plus a blank line with black background for each try that is left
	:param word_length: length of the words to guess
	:param from_line: where in filled_rows to start reading from
	:param max_rows: how many rows are there overall
	:param filled_rows: a list of the words guessed so far
	:param pattern: the solution to derive hints from
	:return: No return value, this is used for printing only
	"""
	for i in range(from_line, max_rows):
		if i < len(filled_rows):
			print(" "+color_code_hints(filled_rows[i], pattern))
		else:
			print(f" {BG_BLACK}{' '*3*word_length}{END}")


def display_input_char(ch: str, place: int, guessed_words: list, pattern: str):
	"""
	Prints the given char with nice formatting, or deletes the last one
	:param ch: any letter from the list of allowed letters, or '\x7f' for backspace
	:param place: position of the character in the input line
	:param guessed_words: previous guesses to derive hints from
	:param pattern: solution to derive hints from
	:return: No return value, this is used for printing only
	"""
	# delete / backspace:
	if ch == '\x7f':
		print("\b\b\b\x1B[0K", end="", flush=True)
	# letters:
	else:
		input_letter: str = color_code_input(ch.upper(), place, pattern, guessed_words)
		print(input_letter, end="", flush=True)


def has_right_place(letter: str, word: str, pattern: str) -> bool:
	"""
	checks if a letter is in the right place in the given word
	:param letter: the letter in question
	:param word: the word to be checked
	:param pattern: the solution to compare with
	:return: True if the letter is in the same position in word and pattern
	"""
	for i in range(len(word)):
		if word[i] == pattern[i] and word[i] == letter:
			return True
	return False


def display_alphabet(lang: str, letters: list, guessed_words: list, pattern: str) -> int:
	"""
	prints a formatted list of the allowed letters with hint colors
	and a line of text that explains it
	:param lang: the name of the language
	:param letters: the list of letters to print
	:param guessed_words: guesses to derive hint colors from
	:param pattern: the solution to derive hint colors from
	:return: the number of lines that the printed output uses
	"""
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
			line_len = 1
			line_count += 1
			line_br = "\n "
		print(f" {line_br}{hint_color}{ltr}{END} ", end="")
		line_br = ""
	print("\n ")
	return line_count


def start_game():
	"""
	runs the actual game
	:return: (no return value)
	"""
	all_words = load_words(language, word_len)

	if len(all_words) > 0:

		max_guesses: int = max(6, word_len + max(1, (word_len // 3)))
		guesses: int = 0
		guessed: list = []
		default_message: str = "Type a word and\n press ENTER to guess!"
		message: str = default_message
		message_lines: int = 4
		lines: int = max_guesses + message_lines

		# choose a random word from the word list as the solution:
		pick_number: int = randint(1, len(all_words))
		solution: str = all_words[pick_number-1]

		allowed_letters: list = list_letters(all_words)

		print("\n Welcome to COMMAND LINE WORDLE!\n")
		print(f" Guess the {language} word\n with {word_len} letters\n in {max_guesses} or less tries!\n")

		# start with showing the empty grid:

		display_guesses(word_len, 0, max_guesses, guessed, solution)
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
					if c.isalpha() and c.upper() in allowed_letters:
						current_input += c
						display_input_char(c, len(current_input), guessed, solution)
					elif c.isalpha() or c.upper() in allowed_letters or c == '\x20':
						continue
					elif c == '\x7f' or c == '\n':
						continue
					else:
						break

				# in an incomplete line, space and backspace is also allowed:
				elif len(current_input) < word_len:
					if (c in ' _' or c == '\x20') and '_' in allowed_letters:
						c = '_'
						current_input += c
					elif c.upper() in allowed_letters:
						current_input += c
					elif c.isalpha():
						continue
					elif c == '\x7f':
						current_input = current_input[0:-1]
					elif c == '\n':
						continue
					else:
						break
					display_input_char(c, len(current_input), guessed, solution)

				# in a full line, only backspace or enter is allowed:
				elif len(current_input) == word_len:
					if c == '\x7f':
						current_input = current_input[0:-1]
						display_input_char(c, len(current_input), guessed, solution)
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

			display_guesses(word_len, current_line, max_guesses, guessed, solution)

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
		print(f" (Random word number {pick_number} of {len(all_words)})\n")


if __name__ == '__main__':
	start_game()
