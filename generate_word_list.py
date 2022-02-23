# takes a word list from local memory or from
# https://github.com/dwyl/english-words/raw/master/words_alpha.txt
# and creates a filtered list of words with a given length.

def generate_word_list(word_len: int) -> bool:

	# download the source word list if it's not already stored:

	url: str = "https://github.com/dwyl/english-words/raw/master/words_alpha.txt"
	import requests
	import os
	if not os.path.isfile("words_alpha.txt"):
		print(f"Word list source file not found in local memory.\nDownloading {url} ...")
		r = requests.get(url)
		f = open("words_alpha.txt", "xb")
		f.write(r.content)
		f.close()
		if not os.path.isfile("words_alpha.txt"):
			print(f"could not create 'words_alpha.txt'. Please download it manually from {url}.")
			return False

	# create a filtered list of n letter words:

	print("Reading word list ...")
	f_in = open("words_alpha.txt", "r")  # read words from this file
	f_out = open(f"words{word_len}.txt", "x")  # create new file here

	print("Filtering ...")
	count = 0
	while True:
		# read next line:
		line = f_in.readline()
		if not line:  # reached end of file
			break
		word = line.strip()  # cut off whitespaces and newlines
		if len(word) == word_len:  # filter for word length
			f_out.write(f"{word}\n")
			count += 1

	f_in.close()
	f_out.close()

	# if the list is too short, it makes no sense to use it:

	if count <= word_len*2:
		print(f"found only {count} words with {word_len} letters. That is not enough, sorry.")
		return False

	# if this part is reached, we have a useful word list:

	print(f"Created list of {count} words with {word_len} letters in file 'words{word_len}.txt'.")
	return True
