# cli-wordle

A word guessing game implementation for command line terminals. Because everyone loves making wordle clones right now :)

I mostly made this project for practice - I'm learning Python for a new job, so I made something fun and simple to start getting used to the new language. This is the first usable thing I've ever written in Python, so don't judge me too hard, please.

## How to play

Just open this directory in your terminal and run `./cli_wordle.py`. The basic rules are the same as in most of the other countless wordle clones out there.

## System Requirements

I'm only testing this on **Linux**. It should also work on **macOS** (thanks to [Lena](https://github.com/lenaschimmel/) for testing).  

On **Windows**, it *might* work if your system is newer than 2016 and if you start the game from the *cmd.exe* terminal. If you tried it, let me know how it went :)

Obviously, you need to have **Python 3** installed.

In addition to the files in this repo, the game needs a **word list** to choose words from. I didn't include word lists directly in here to keep them from bloating the size of this repo, but the game will automatically download a word list when you run it for the first time. This will use between 3 and 30 MB per language.

## Word length
The default word length is 5 letters, but it can easily be changed if you want to try something else.

To set the new word length in the game, change the value of `word_len` in `cli_wordle.py` (line 11) before playing.

## Language

The default language is English. 

If you want to guess German, French, Spanish, or Toki Pona words instead, change the value of `language` in `cli_wordle.py` (line 12) to `"German"`, `"French"`, `"Spanish"` or `"Toki Pona"`.

If you want to use any other language, add the name of the language and the url of a word list (utf8-encoded _.txt_ file) to `sources` in `generate_word_list.py` (line 6) and change the value of `language` in `cli_wordle.py` (line 12) to the new language name.

Feel free to let me know where to find a good word list for any language you like, so I can include it in the game.

If your word list is not available online, you can also manually put it in a file named `words_<language>.txt` and change the `language` value in `cli_wordle.py` without adding a URL anywhere.