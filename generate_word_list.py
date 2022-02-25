# takes a word list from local storage or the internet
# and creates a filtered list of words with a given length.

def generate_word_list(language: str, word_len: int) -> bool:

	sources: dict = {
		"English": "https://github.com/lorenbrichter/Words/raw/master/Words/en.txt",
		"German": "https://github.com/lorenbrichter/Words/raw/master/Words/de.txt",
		"French": "https://github.com/lorenbrichter/Words/raw/master/Words/fr.txt",
		"Spanish": "https://github.com/lorenbrichter/Words/raw/master/Words/es.txt"
		}

	lang_filename: str = f"words_{language.lower()}.txt"
	short_filename: str = f"words_{language.lower()}_{word_len}.txt"

	# download the source word list if it's not already stored:

	url: str = sources[language]
	import requests
	import os
	if not os.path.isfile(lang_filename):
		print(f"Word list source file not found in local memory.\nDownloading {url} ...")
		r = requests.get(url)
		f = open(lang_filename, "xb")
		f.write(r.content)
		f.close()
		if not os.path.isfile(lang_filename):
			print(f"could not create '{lang_filename}'. Please download it manually from {url}.")
			return False

	# create a filtered list of n letter words:

	print("Reading word list ...")
	f_in = open(lang_filename, "r")  # read words from this file

	word_list: list = []

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
	f_in.close()

	# count letter frequency:
	# for (ltr, freq) in count_letter_frequency(word_list)[0]: print(f"{ltr} {freq}")

	# filter out words with rare letters:
	word_list = filter_rare_words(word_list)

	# if the list is too short, it makes no sense to use it:

	if len(word_list) <= word_len*2:
		print(f"found only {len(word_list)} {language} words with {word_len} letters. That is not enough, sorry.")
		return False

	# write list to file:

	f_out = open(short_filename, "x")  # create new file here
	for w in word_list:
		f_out.write(f"{w}\n")
	f_out.close()

	# if this part is reached, a useful word list was created:

	print(f"Created list of {len(word_list)} {language} {word_len} letter words in file '{short_filename}'.")
	return True


def count_letter_frequency(words: list) -> (list, dict):
	letter_frequency: dict = {}
	for w in words:
		for l in w:
			if l in letter_frequency:
				letter_frequency[l] += 1
			else:
				letter_frequency[l] = 1
	letter_list = list(letter_frequency.items())
	letter_list.sort(key=(lambda tup: tup[1]), reverse=True)

	return letter_list, letter_frequency


def filter_rare_words(words: list) -> list:
	lf = count_letter_frequency(words)
	max_letter_freq: int = lf[0][0][1]
	cutoff: int = 200
	min_letter_freq: int = max_letter_freq // cutoff

	rare_letters: set = set()
	for (ltr, freq) in lf[0]:
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
