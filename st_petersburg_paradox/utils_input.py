import curses


def format_number_with_commas(number: int) -> str:
    return "{:,}".format(number)


def input_int_with_commas(prompt, default: int = 0) -> int:
    def curses_input(stdscr):
        curses.echo()
        input_str = str(default)
        while True:
            stdscr.clear()
            formatted_input = format_number_with_commas(int(input_str))
            stdscr.addstr(0, 0, f"{prompt}{formatted_input}")

            char: str = stdscr.get_wch()
            if char == "\n":
                break
            elif char == 263 or char == 330:  # backspace or delete
                if len(input_str) > 1:
                    input_str = input_str[:-1]
                elif len(input_str) == 1:
                    input_str = "0"
                else:
                    raise Exception()
            elif char.isdigit():
                if input_str == "0":
                    input_str = char
                else:
                    input_str += char

        return int(input_str.replace(",", ""))

    return curses.wrapper(curses_input)
