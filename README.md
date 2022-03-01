# cli-wordle

A word guessing game implementation for command line terminals. Because everyone loves making wordle clones right now :)

I mostly made this project for practice - I'm learning Python for a new job, so I made something fun and simple to start getting used to the new language. This is the first usable thing I've ever written in Python, so don't judge me too hard, please.

## How to play

Just open this directory in your terminal and run `./cli_wordle.py`. The basic rules are the same as in most of the other countless wordle clones out there:

Guess the secret word by typing in any word and using the hints for your next guess. 
- If a letter is not in the secret word, it will be marked in gray
- If a letter is in the right place, it will be marked in green 🟩 
- If a letter is in the secret word, but in a different place, it will be marked in yellow 🟨

## System Requirements

I'm only testing this on **Linux**. It should also work on **macOS** (thanks to [Lena](https://github.com/lenaschimmel/) for testing).  

On **Windows**, it *might* work if your system is newer than 2016 and if you start the game from the *cmd.exe* terminal. If you tried it, let me know how it went :)

Obviously, you need to have **Python 3** installed.

In addition to the files in this repo, the game needs a **word list** to choose words from. I didn't include word lists directly in here to keep them from bloating the size of this repo, but the game will automatically download a word list when you run it for the first time. This will use between 3 and 30 MB per language.

## (Optional:) Run the game in Docker

To be independent of your local python environment, you can also run the game in a docker container. To do so, open this directory in a terminal and enter the following two commands:

```commandline
docker build -t cli-wordle .
docker run -it cli-wordle
```

## Word length and language
The default word length is 5 letters and the default language is English. 

To change one or both of these, edit the `config.txt` file.

Currently, sources are included for the following languages:

- English
- French
- German
- Spanish
- Toki Pona

If you want to use one of these, you can just set the language name in line 5 of `config.txt`.

If you want to use any other language, add the name of the language and the url of a word list (utf8-encoded _.txt_ file) to the list of sources at the end of `config.txt`.

Feel free to let me know where to find a good word list for any language you like, so I can include it for everyone.

If your word list is not available online, you can also manually put it in a file named `words_<language>.txt` and change the `language` value in `config.txt` without adding a line to the source list.