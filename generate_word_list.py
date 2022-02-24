# takes a word list from local storage or the internet
# and creates a filtered list of words with a given length.

def generate_word_list(language: str, word_len: int) -> bool:

	sources: dict = {
		"English": "https://github.com/dwyl/english-words/raw/master/words_alpha.txt",
		"German": "https://gist.githubusercontent.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4/raw/36b70dd6be330aa61cd4d4cdfda6234dcb0b8784/wordlist-german.txt"
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
	f_out = open(short_filename, "x")  # create new file here

	print("Filtering ...")
	count = 0
	while True:
		# read next line:
		line = f_in.readline()
		if not line:  # reached end of file
			break
		word = line.strip().upper()  # cut off whitespace and convert to uppercase
		if len(word) == word_len:  # filter for word length
			f_out.write(f"{word}\n")
			count += 1

	f_in.close()
	f_out.close()

	# if the list is too short, it makes no sense to use it:

	if count <= word_len*2:
		print(f"found only {count} {language} words with {word_len} letters. That is not enough, sorry.")
		return False

	# if this part is reached, we have a useful word list:

	print(f"Created list of {count} {language} {word_len} letter words in file '{short_filename}'.")
	return True
