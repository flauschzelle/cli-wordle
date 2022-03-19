#!/usr/bin/env python3

"""
cli-wordle: a word guessing game for command line terminals.
Copyright (C) 2022 Kirstin Rohwer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from random import randint
from argparse import ArgumentParser

# ANSI escape codes for output formatting:

BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLACK = '\033[40m'
BG_GRAY = '\033[100m'

GRAY = '\033[90m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

END = '\033[0m'
BOLD = '\033[1m'


def load_word_list_from_url(language: str, url: str) -> bool:
    """
    Download a word list from the internet.
    
    :param language: The language to use for the filename
    :param url: url of a word list (must be a utf8-encoded .txt file)
    :return: True if the download was successful
    """
    
    lang_filename: str = f"words_{language}.txt"
    import requests
    import os.path
    print(f"Downloading {url} ...")
    r = requests.get(url)
    with open(lang_filename, "xb") as f:
        f.write(r.content)
    if not os.path.isfile(lang_filename):
        print(f"could not create '{lang_filename}'.",
              f"Please download it manually from {url}.")
        return False
    return True


def generate_word_list(
        language: str,
        word_len: int,
        filter_by_letters: bool = True,
        print_freq: bool = False
) -> bool:
    """
    Create a txt file with one word of the given length per line.

    :param language: The language to take the words from
    :param word_len: The length of words to be listed
    :param filter_by_letters: if True, words are removed if
    they contain rare letters
    :param print_freq: if True, a list of
    (letter n, freq(n), freq(n-1)/freq(n)) is printed
    :return: True if a list of more than 2*word_len words
    was successfully created
    """

    lang_filename: str = f"words_{language}.txt"
    short_filename: str = f"words_{language}_{word_len}.txt"

    # download the source word list if it's not already stored:

    import os.path
    if not os.path.isfile(lang_filename):
        print(f"Word list source file not found in local memory.")
        url: str = read_source_from_config(language)
        if not url:
            print(f"Found no source URL for {language} word list.")
            return False
        if not load_word_list_from_url(language, url):
            return False

    # create a filtered list of n letter words:

    print("Reading word list ...")
    word_list: list = []

    with open(lang_filename, "r") as f_in:  # read words from this file

        print("Filtering ...")

        letter_frequency: dict = {}

        for line in f_in:
            # cut off trailing whitespace and convert to uppercase:
            word = line.strip().upper()

            # convert spaces to underscores:
            while ' ' in word:
                lw = list(word)
                pos = lw.index(' ')
                lw[pos] = '_'
                word = ''.join(lw)

            # count letter frequencies in the source word list:
            for ltr in word:
                if ltr in letter_frequency:
                    letter_frequency[ltr] += 1
                else:
                    letter_frequency[ltr] = 1

            # filter for word length, discard duplicates:
            if len(word) == word_len and word not in word_list:
                word_list.append(word)

        # sort letter frequency list by frequency (descending):
        letter_list = list(letter_frequency.items())
        letter_list.sort(key=(lambda tup: tup[1]), reverse=True)

    # print letter frequencies:
    if print_freq:
        prev_freq: int = 0
        for (ltr, freq) in letter_list:
            if prev_freq > 0:
                print(f"{ltr} {freq} - {prev_freq / freq}")
            else:
                print(f"{ltr} {freq}")
            prev_freq = freq
        print("\n")

    if not word_list:
        print(f"No {language} words with {word_len} letters found, sorry.")
        return False
    elif filter_by_letters:
        # filter out words with rare letters:
        rare_letters = find_rare_letters(letter_list, 6)
        word_list = filter_words_by_letters(word_list, rare_letters)

    # if the list is too short, it makes no sense to use it:

    if len(word_list) <= word_len * 2:
        print(f"found only {len(word_list)} {language} words with {word_len}",
              "letters. That is not enough, sorry.")
        return False

    # write list to file:

    with open(short_filename, "w") as f_out:  # create new file here
        for w in word_list:
            f_out.write(f"{w}\n")

    # if this part is reached, a useful word list was created:

    print(f"Created list of {len(word_list)} {language} {word_len} letter",
          f"words in file '{short_filename}'.")
    return True


def read_source_from_config(language: str) -> str:
    """
    Read the source url for the given language from config.txt.

    :param language: the name of the language
    :return: the url of a word list, if present
    """

    from configparser import ConfigParser, Error
    from sys import exit

    config = ConfigParser()
    config.read("config.txt")

    url = ""
    try:
        url = config.get("word list sources", language)
    except Error as e:
        print(f"No source url found for language {language}. ({e})")
        print("Please check available languages in config.txt.")
        exit(1)

    return url


def list_all_languages() -> list:
    """
    Make a list of all languages that have sources in config.txt
    
    :return: a list of all available language names
    """

    from configparser import ConfigParser
    config = ConfigParser()
    config.read("config.txt")

    langs = []
    for k in config['word list sources']:
        langs.append(k)

    return langs


def find_rare_letters(letter_freq: list, cutoff: int) -> set:
    """
    Find a set of rare letters.

    The list of letters is cut off above the first letter that
    is at or below 1/cutoff as frequent as its predecessor.

    :param letter_freq: a list of (letter, frequency) tuples,
    sorted by descending frequency
    :param cutoff: the factor at which to cut off the letter list
    (recommended: somewhere between 3 and 10)
    :return: a set containing the rare letters
    """

    rare_letters: set = set()
    max_freq: int = 0

    prev_freq: int = letter_freq[0][1]
    for (ltr, freq) in letter_freq:
        if prev_freq / freq >= cutoff:
            max_freq = freq
            break
        else:
            prev_freq = freq

    for (ltr, freq) in letter_freq:
        if freq <= max_freq:
            rare_letters.add(ltr)
    return rare_letters


def filter_words_by_letters(words_list: list, forbidden_letters: set) -> list:
    """
    Remove words from a list if they contain any letter in a given set.
    
    :param words_list: the list to be filtered
    :param forbidden_letters: a set of letters that are not allowed
    :return: a list of the words in words without any forbidden letters
    """

    filtered_words: list = [w for w in words_list
                            if forbidden_letters.isdisjoint(w)]
    removed_word_count: int = len(words_list) - len(filtered_words)
    removed_words: set = set(words_list) - set(filtered_words)

    if forbidden_letters:
        print(f"Removed {removed_word_count} words containing letters",
              f"{' '.join(sorted(forbidden_letters))} from the word list:",
              f"{' '.join(sorted(removed_words))}")
    return filtered_words


def get_char():
    """
    Read a single character from standard input.

    :return: the character that is typed in
    """

    # the code for this function is mostly taken from here:
    # https://stackoverflow.com/a/36974338

    # figure out which function to use once, and store it in _func
    if "_func" not in get_char.__dict__:
        try:
            # for Windows-based systems
            import msvcrt  # If successful, we are on Windows
            get_char._func = msvcrt.getch

        except ImportError:
            # for POSIX-based systems (with termios & tty support)
            import tty
            import sys
            import termios
            # raises ImportError if unsupported

            def _tty_read():
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)

                try:
                    tty.setcbreak(fd)
                    answer = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

                return answer

            get_char._func = _tty_read

    return get_char._func()


def read_config() -> (int, str):
    """
    Read word length and language setting from config.txt file.
    
    :return: a tuple of word length and language name
    """
    from configparser import ConfigParser

    config = ConfigParser()
    config.read("config.txt")

    word_length = config.getint("wordle configuration", "word length", fallback=5)
    language = config.get("wordle configuration", "language", fallback="en")

    return word_length, language


def write_config(language: str, length: int, url: str = None):
    """
    Writes the given language, word length and url into config.txt.
    
    :param language: The language to be set
    :param length: The word length to be set
    :param url: (optional) source url to be set for the language
    :return: (no return value, just writes to the file)
    """

    from configparser import ConfigParser, Error
    from sys import exit
    config = ConfigParser()

    # read config from file
    config.read("config.txt")

    # if no new url is given, preserve the old one for this language
    if url is None:
        try:
            url = config.get("word list sources", language)
        except Error as e:
            print(f"{language} is not a valid language. ({e})")
            exit(1)

    config.set("wordle configuration", "word length", str(length))
    config.set("wordle configuration", "language", language)
    config.set("word list sources", language, url)

    # write modified list back into the file:
    with open("config.txt", "wt") as f:
        config.write(f)


def load_words(lang: str, length: int) -> list:
    """
    Create a list of n-letter words of a language.
    
    The list of words is either loaded from a pre-existing txt file
    or the file is generated before loading the list from it.
    
    :param lang: the language to load words from
    :param length: number of letters (n) in each word
    :return: a list of words with n letters
    """
    filename = f"words_{lang}_{length}.txt"
    import os
    if not os.path.isfile(filename):
        if not generate_word_list(lang, length):
            print("Could not generate word list file.")
            return []

    words = []
    with open(filename, "r") as file:
        for line in file:
            words.append(line.strip())
    return words


def list_letters(words: list) -> list:
    """
    List all letters that are allowed.
    
    :param words: a word list to extract the letters from
    :return: a sorted list of all letters in the word list
    """
    letters: list = []
    for w in words:
        for ltr in w:
            if ltr not in letters:
                letters.append(ltr)
    letters.sort()
    return letters


def bold_colored_letter(letter: str, color: str) -> str:
    """
    Apply bold, spacing and color to the given letter.
    
    :param letter: the text to be formatted
    :param color: background or text color (ANSI code)
    :return:
    """
    ctext: str = f"{BOLD}{color} {letter} {END}"
    return ctext


def color_code_hints(text: str, pattern: str) -> str:
    """
    Apply hint colors to the given word.
    
    :param text: the text to be colored
    :param pattern: the solution to derive the hints from
    :return: the given word in bold, spaced text with hint colors
    """
    ctext: str = ""
    hidden: list = []

    for i in range(len(pattern)):
        if text[i] != pattern[i]:
            hidden.append(pattern[i])

    for i in range(len(pattern)):
        if text[i] == pattern[i]:
            ctext += bold_colored_letter(text[i], BG_GREEN)
        elif text[i] in hidden:
            ctext += bold_colored_letter(text[i], BG_YELLOW)
            hidden.remove(text[i])
        else:
            ctext += bold_colored_letter(text[i], BG_GRAY)
    return ctext


def color_code_input(letter: str, place: int, pattern: str, prev_lines: list
                     ) -> str:
    """
    Apply input line hint color to a letter.
    
    :param letter: the letter to be checked
    :param place: position of the letter in the input line
    :param pattern: the solution to derive hints from
    :param prev_lines: words that were guessed before
    :return: a string of one bold letter with hint color and spacing
    """
    hint_color: str = ""

    for li in prev_lines:
        if letter not in li:
            # no hints for this letter
            continue
        elif letter in li and letter not in pattern:
            hint_color = GRAY
            break
        elif li[place - 1] == letter and pattern[place - 1] == letter:
            hint_color = GREEN
            break
        elif letter in li and letter in pattern:
            hint_color = YELLOW
            # next line might still have a green hint
            continue
    text = bold_colored_letter(letter, hint_color)
    return text


def display_guesses(
        word_length: int,
        from_line: int,
        max_rows: int,
        filled_rows: list,
        pattern: str
):
    """
    Print the grid of guesses and blank lines.
    
    Print the guessed word(s) with nice formatting,
    plus a blank line with black background for each try that is left.
    
    :param word_length: length of the words to guess
    :param from_line: where in filled_rows to start reading from
    :param max_rows: how many rows are there overall
    :param filled_rows: a list of the words guessed so far
    :param pattern: the solution to derive hints from
    :return: No return value, this is used for printing only
    """
    for i in range(from_line, max_rows):
        if i < len(filled_rows):
            print(" " + color_code_hints(filled_rows[i], pattern))
        else:
            print(f" {BG_BLACK}{' ' * 3 * word_length}{END}")


def display_input_char(
        ch: str, place: int, guessed_words: list, pattern: str):
    """
    Print the given char with nice formatting, or delete the last one.
    
    :param ch: any letter from the list of allowed letters,
    or '\x7f' for backspace
    :param place: position of the character in the input line
    :param guessed_words: previous guesses to derive hints from
    :param pattern: solution to derive hints from
    :return: No return value, this is used for printing only
    """
    # delete / backspace:
    if ch == '\x7f':
        print("\b\b\b\x1B[0K", end="", flush=True)
    # letters:
    else:
        input_letter: str = color_code_input(ch.upper(),
                                             place, pattern, guessed_words)
        print(input_letter, end="", flush=True)


def has_right_place(letter: str, word: str, pattern: str) -> bool:
    """
    Check if a letter is in the right place in the given word.
    
    :param letter: the letter in question
    :param word: the word to be checked
    :param pattern: the solution to compare with
    :return: True if the letter is in the same position
    in word and pattern
    """
    for i in range(len(word)):
        if word[i] == pattern[i] and word[i] == letter:
            return True
    return False


def display_alphabet(
        lang: str, letters: list, guessed_words: list, pattern: str) -> int:
    """
    Print a formatted list of the allowed letters with hint colors.
    
    :param lang: the name of the language
    :param letters: the list of letters to print
    :param guessed_words: guesses to derive hint colors from
    :param pattern: the solution to derive hint colors from
    :return: the number of lines that the printed output uses
    """
    line_max: int = 13
    line_len: int = 0
    line_br: str = ""
    line_count: int = 4

    print(f" The following letters are allowed for {lang}:\n ")

    for ltr in letters:
        hint_color: str = ""
        for g in guessed_words:
            if ltr not in g:
                # no hints for this letter
                continue
            elif ltr in g and ltr not in pattern:
                hint_color = GRAY
                break
            elif has_right_place(ltr, g, pattern):
                hint_color = GREEN
                break
            elif ltr in g and ltr in pattern:
                hint_color = YELLOW
                # next guess might still have a green hint
                continue
        line_len += 1
        if line_len > line_max:
            line_len = 1
            line_count += 1
            line_br = "\n "
        print(f" {line_br}{hint_color}{ltr}{END} ", end="")
        line_br = ""
    print("\n ")
    return line_count


def start_game(language: str = None, word_len: int = None):
    """
    Run the game with given settings or settings from the config file.
    
    :param language: the language of guessable words
    :param word_len: the length of guessable words
    :return: (no return value)
    """

    if not (language and word_len):
        (conf_len, conf_lang) = read_config()
        if not word_len:
            word_len = conf_len
        if not language:
            language = conf_lang

    all_words = load_words(language, word_len)

    if len(all_words) > 0:

        max_guesses: int = max(6, word_len + max(1, (word_len // 3)))
        guesses: int = 0
        guessed: list = []
        default_message: str = "Type a word and\n press ENTER to guess!"
        message: str = default_message
        message_lines: int = 4
        lines: int = max_guesses + message_lines

        # choose a random word from the word list as the solution:
        pick_number: int = randint(1, len(all_words))
        solution: str = all_words[pick_number - 1]

        allowed_letters: list = list_letters(all_words)

        print("\n Welcome to COMMAND LINE WORDLE!\n")
        print(f" Guess the {language} word\n with {word_len}",
              f"letters\n in {max_guesses} or less tries!\n")

        # start with showing the empty grid:

        display_guesses(word_len, 0, max_guesses, guessed, solution)
        print(f"\n {message}\n")
        lines = lines + display_alphabet(language, allowed_letters,
                                         guessed, solution)

        # start input on the first empty grid line:

        print(f"\x1B[{str(lines)}F\x1B[2K", end="")

        while guesses < max_guesses:

            print(" ", end="", flush=True)

            current_input: str = ""

            while len(current_input) <= word_len:
                c: str = get_char()

                # in an empty line, only letters are allowed:
                if len(current_input) == 0:
                    if c.isalpha() and c.upper() in allowed_letters:
                        current_input += c
                        display_input_char(c, len(current_input),
                                           guessed, solution)
                    elif (c.isalpha()
                          or c.upper() in allowed_letters
                          or c == '\x20'):
                        continue
                    elif c == '\x7f' or c == '\n':
                        continue
                    else:
                        break

                # in an incomplete line, space or backspace is also allowed:
                elif len(current_input) < word_len:
                    if (c in ' _' or c == '\x20') and '_' in allowed_letters:
                        c = '_'
                        current_input += c
                    elif c.upper() in allowed_letters:
                        current_input += c
                    elif c.isalpha():
                        continue
                    elif c == '\x7f':
                        current_input = current_input[0:-1]
                    elif c == '\n':
                        continue
                    else:
                        break
                    display_input_char(c, len(current_input),
                                       guessed, solution)

                # in a full line, only backspace or enter is allowed:
                elif len(current_input) == word_len:
                    if c == '\x7f':
                        current_input = current_input[0:-1]
                        display_input_char(c, len(current_input),
                                           guessed, solution)
                    elif c.isalpha():
                        continue
                    elif c == '\n':
                        break
                    else:
                        break

            # save the guess:
            guess = current_input.upper()

            # overwrite input line after entering:
            print("\x0D\x1B[0J", end="")

            current_line: int = guesses

            if guess in all_words:
                message = default_message
                guesses += 1
                guessed.append(guess)
            else:
                message = f"{guess} is not a valid word.\n Try again!"

            display_guesses(word_len, current_line, max_guesses,
                            guessed, solution)

            if guess == solution:
                print(f"\n Solved in {guesses}/{max_guesses} tries :)\n")
                break

            if guesses >= max_guesses:
                print("\n No more tries left, sorry :(")
                print(f" The solution was {solution}.\n")
                break

            print(f"\n {message}\n")
            display_alphabet(language, allowed_letters, guessed, solution)

            # set the cursor to start the input on the next empty line:
            print(f"\x1B[{str(lines - guesses)}F\x1B[2K", end="")

        # in case you want to look up the word in your text file later:
        print(f" (Random word number {pick_number} of {len(all_words)})\n")


if __name__ == '__main__':
    p = ArgumentParser(
        description="A word guessing game for command line terminals."
    )
    p.add_argument("-a", "--all-languages", action="store_true",
                   dest="show",
                   help="show a list of all available languages and exit")
    p.add_argument("-r", "--rules", action="store_true",
                   dest="rules",
                   help="show a description of the game's rules and exit")
    p.add_argument("-l", "--language", dest="language", type=str,
                   default=None, help="set the language of words to guess")
    p.add_argument("-n", "--length", dest="length", type=int,
                   default=None, help="set the length of words to guess")
    p.add_argument("-u", "--url", dest="url", type=str, default=None,
                   help="set the URL to download a word list from")
    p.add_argument("-s", "--save", action="store_true", dest="save",
                   help="remember settings for future uses")
    args = p.parse_args()

    if args.language:
        args.language = args.language.lower()  # or configparser will hate us later on

    if args.url:
        if not args.language:
            print("You need to specify a language name",
                  "for the word list to be downloaded")
        else:
            load_word_list_from_url(args.language, args.url)
    if args.save:
        write_config(args.language, args.length, args.url)
    if args.show:
        print("The following languages are currently available:\n")
        languages = list_all_languages()
        for lan in languages:
            print(lan)
    elif args.rules:
        print("\nGuess the secret word by typing in any word",
              "\nand using the hints for your next guess:\n\n",
              " * If a letter is not in the secret word,",
              f"\n    it will be marked in {BG_GRAY} gray {END}.\n\n",
              " * If a letter is in the right place,",
              f"\n    it will be marked in {BG_GREEN} green {END}.\n\n",
              " * If a letter is in the secret word,",
              "\n    but in a different place,",
              f"\n    it will be marked in {BG_YELLOW} yellow {END}.\n"
              )
    else:
        start_game(args.language, args.length)
