#!/usr/bin/env python3

# this makes a list of english words with a given number of letters
# using the word list from
# https://github.com/dwyl/english-words/blob/master/words_alpha.txt

word_len = 5

fin = open("words_alpha.txt", "r")
fout = open(f"words{word_len}.txt", "x")

while(True):
	#read next line
	line = fin.readline()
	#if line is empty, you are done with all lines in the file
	if not line:
		break
	#do things with the line
	word = line.strip()
	if len(word) == word_len:
		fout.write(f"{word}\n")
		
fin.close()
fout.close()
