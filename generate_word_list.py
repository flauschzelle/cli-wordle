# takes a word list from local storage or the internet
# and creates a filtered list of words with a given length.

def generate_word_list(language: str, word_len: int) -> bool:
	"""
	creates a txt file with one word of the given length per line
	:param language: The language to take the words from
	:param word_len: The length of words to be listed
	:return: True if a list of more than 2*word_len words was successfully created
	"""

	lang_filename: str = f"words_{language.lower()}.txt"
	short_filename: str = f"words_{language.lower()}_{word_len}.txt"

	# download the source word list if it's not already stored:

	import requests
	import os
	if not os.path.isfile(lang_filename):
		print(f"Word list source file not found in local memory.")
		url: str = read_source_from_config(language)
		if url == "":
			return False
		print(f"Downloading {url} ...")
		r = requests.get(url)
		with open(lang_filename, "xb") as f:
			f.write(r.content)
		if not os.path.isfile(lang_filename):
			print(f"could not create '{lang_filename}'. Please download it manually from {url}.")
			return False

	# create a filtered list of n letter words:

	print("Reading word list ...")
	word_list: list = []

	with open(lang_filename, "r") as f_in:  # read words from this file

		print("Filtering ...")
		while True:
			# read next line:
			line = f_in.readline()
			if not line:  # reached end of file
				break
			word = line.strip().upper()  # cut off trailing whitespace and convert to uppercase

			# convert spaces to underscores:
			while ' ' in word:
				lw = list(word)
				pos = lw.index(' ')
				lw[pos] = '_'
				word = ''.join(lw)

			if len(word) == word_len:  # filter for word length
				word_list.append(word)

	# count letter frequency:
	# for (ltr, freq) in count_letter_frequency(word_list): print(f"{ltr} {freq}")

	if len(word_list) == 0:
		print(f"No {language} words with {word_len} letters found, sorry.")
		return False
	else:
		# filter out words with rare letters:
		word_list = filter_rare_words(word_list)

	# if the list is too short, it makes no sense to use it:

	if len(word_list) <= word_len*2:
		print(f"found only {len(word_list)} {language} words with {word_len} letters. That is not enough, sorry.")
		return False

	# write list to file:

	with open(short_filename, "x") as f_out:  # create new file here
		for w in word_list:
			f_out.write(f"{w}\n")

	# if this part is reached, a useful word list was created:

	print(f"Created list of {len(word_list)} {language} {word_len} letter words in file '{short_filename}'.")
	return True


def read_source_from_config(language: str) -> str:
	"""
	reads the source url for the given language from config.txt
	:param language: the name of the language
	:return: the url of a word list, if present
	"""
	url: str = ""
	with open("config.txt", "r") as conf:
		while True:
			line: str = conf.readline()
			if line[0:len(language)] == language:
				url = line[len(language)+2:].strip()
				break
	if url == "":
		print(f"No source url found for {language}, please check available languages in config.txt")
	return url


def count_letter_frequency(words: list) -> list:
	"""
	counts the frequency of any letters in a list of words
	:param words: a list of words
	:return: a list of (letter, freq) tuples, sorted by frequency
	"""
	letter_frequency: dict = {}
	for w in words:
		for ltr in w:
			if ltr in letter_frequency:
				letter_frequency[ltr] += 1
			else:
				letter_frequency[ltr] = 1
	letter_list = list(letter_frequency.items())
	letter_list.sort(key=(lambda tup: tup[1]), reverse=True)

	return letter_list


def filter_rare_words(words: list) -> list:
	"""
	removes words from a list if they contain any letter that is 200 times less frequent that the most frequent letter
	:param words: the list to be filtered
	:return: the list without the rare-letter-containing words
	"""
	lf = count_letter_frequency(words)
	max_letter_freq: int = lf[0][1]
	cutoff: int = 200
	min_letter_freq: int = max_letter_freq // cutoff

	rare_letters: set = set()
	for (ltr, freq) in lf:
		if freq <= min_letter_freq:
			rare_letters.add(ltr)

	filtered_words: list = [w for w in words if rare_letters.isdisjoint(w)]
	removed_word_count: int = len(words) - len(filtered_words)
	removed_words: set = set(words) - set(filtered_words)

	if len(rare_letters) > 0:
		text: str = f"Removed {removed_word_count} words containing rare letters " + \
					f"{' '.join(rare_letters)} from the word list: {' '.join(removed_words)}"
		print(text)
	return filtered_words
