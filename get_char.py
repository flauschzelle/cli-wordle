# taken from here: https://stackoverflow.com/a/36974338

def get_char():
    """
    reads a single character from standard input
    :return: the character that is typed in
    """
    # figure out which function to use once, and store it in _func
    if "_func" not in get_char.__dict__:
        try:
            # for Windows-based systems
            import msvcrt # If successful, we are on Windows
            get_char._func = msvcrt.getch

        except ImportError:
            # for POSIX-based systems (with termios & tty support)
            import tty, sys, termios  # raises ImportError if unsupported

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