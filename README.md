# cli-wordle

A word guessing game implementation for unix command line. Because everyone loves making wordle clones right now :)

I mostly made this project for practice - I'm learning Python for a new job, so I made something fun and simple to start getting used to the new language. This is the first usable thing I've ever written in Python, so don't judge me too hard, please.

## How to play

After you've created a word list (see below for more info), just open this directory in your terminal and run `./cli_wordle.py`. The basic rules are the same as in most of the other countless wordle clones out there.

## Installation and Requirements

I've only tested this on **Linux**. It might also work on MacOS, but probably not on Windows. If you tried it, let me know how it went :)

Obviously, you need to have **Python 3** installed.

In addition to the files in this repo, you need a source for the **word list** to choose words from. I didn't include a word list in here to keep it from bloating the size of this repo.

So far, I've used `words_alpha.txt` from [this source](https://github.com/dwyl/english-words/). It contains a lot of obscure words I've never seen before, so if you know a better one (maybe sorted by frequency), feel free to let me know :)

After cloning this repo and downloading a word list source file (just put it in the same folder and name it `words_alpha.txt`), generate your smaller word list file by running `./generate_word_list.py`.  
After that, you can delete the large word list file to keep it from cluttering up your disk space.

## Word length
The default word length is 5 letters, but it can easily be changed if you want to try something else. If you do, remember that you need to generate a separate word list file for each length - just change the value of `word_len` in `generate_word_list.py` before running it.

To set the new word length in the game, change the value of `word_len` in `cli_wordle.py` before playing.