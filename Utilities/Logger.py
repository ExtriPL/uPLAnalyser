class Logger:
    def __init__(self, prefix: str):
        self.__prefix: str = prefix

    def log(self, text: str) -> None:
        prefix = self.__text_prefix()
        print(prefix + " " + text)

    def __text_prefix(self) -> str:
        return "[" + self.__prefix + "]"
