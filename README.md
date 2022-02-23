# cli-wordle

A word guessing game implementation for unix command line. Because everyone loves making wordle clones right now :)

I mostly made this project for practice - I'm learning Python for a new job, so I made something fun and simple to start getting used to the new language. This is the first usable thing I've ever written in Python, so don't judge me too hard, please.

## How to play

Just open this directory in your terminal and run `./cli_wordle.py`. The basic rules are the same as in most of the other countless wordle clones out there.

## Installation and Requirements

I've only tested this on **Linux**. It should also work on **macOS** (thanks to [Lena](https://github.com/lenaschimmel/) for testing), but probably not on Windows. If you'd like to try it anyway, let me know how it went :)

Obviously, you need to have **Python 3** installed.

In addition to the files in this repo, you need a source for the **word list** to choose words from. I didn't include a word list in here to keep it from bloating the size of this repo.

If you don't change anything in the source code, it will automatically use [words_alpha.txt](https://github.com/dwyl/english-words/raw/master/words_alpha.txt) from [dwyl/english-words](https://github.com/dwyl/english-words/). That list contains a lot of obscure words I've never seen before, so if you know a better one (maybe sorted by frequency), feel free to let me know :)

If you want to use a different word list source, you can either change the value of `url` in `generate_word_list.py` or name your manually created/downloaded word list `words_alpha.txt` and put it in the same directory.

## Word length
The default word length is 5 letters, but it can easily be changed if you want to try something else.

To set the new word length in the game, change the value of `word_len` in `cli_wordle.py` before playing.