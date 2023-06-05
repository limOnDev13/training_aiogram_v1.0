def read_token_from_txt() -> str:
    with open("TOKEN.txt") as token_file:
        token = token_file.readline()
        return token