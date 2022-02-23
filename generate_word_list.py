# this makes a list of english words with a given number of letters
# using the word list from
# https://github.com/dwyl/english-words/raw/master/words_alpha.txt

def generate_word_list(word_len: int) -> bool:

	import os
	if not os.path.isfile("words_alpha.txt"):
		# TODO: load file from the internet and proper error handling
		print("Word list source not found. Please download 'words_alpha.txt'.")
		return False

	print("Reading word list...")
	fin = open("words_alpha.txt", "r")  # read words from this file
	fout = open(f"words{word_len}.txt", "x")  # create new file here

	print("Filtering...")
	count = 0
	while True:
		# read next line:
		line = fin.readline()
		if not line:  # reached end of file
			break
		word = line.strip()  # cut off whitespaces and newlines
		if len(word) == word_len:  # filter for word length
			fout.write(f"{word}\n")
			count += 1

	fin.close()
	fout.close()
	print(f"Created list of {count} words with {word_len} letters in file 'words{word_len}.txt'.")
	return True
