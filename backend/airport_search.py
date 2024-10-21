def parse_between_chars(string: str, start_char: str, end_char: str) -> str:
    start_index = string.index(start_char) + 1
    end_index = string.index(end_char)
    return string[start_index:end_index]


def get_airport_by_code(airport_code: str):
    with open("../resources/airport_codes.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line[0:3] == airport_code:
                return parse_between_chars(line, '"', ",").title()
