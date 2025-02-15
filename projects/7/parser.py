class Parser:

    def __init__(self, path=None):
        self.file = self.open_input_file(path)
        self.current_command = None
        self.translation_table = dict.fromkeys(map(ord, " @)("), None)
        self.commandTypeDict = {
            "call": "C_CALL",
            "pop": "C_POP",
            "push": "C_PUSH",
            "label": "C_LABEL",
            "goto": "C_GOTO",
            "if-goto": "C_IF",
            "function": "C_FUNCTION",
            "return": "C_RETURN",
        }

    def open_input_file(self, path: str):
        """Opens the file specified by path"""
        file = open(path, "r")
        return file

    def hasMoreCommands(self):
        """Checks if the current line is EOF or not
        but does not advance a line in the file. Skips
        comments and newlines."""
        pos = self.file.tell()  # current position of file
        line = self.file.readline()
        line_split = line.split()
        while line == "\n" or len(line_split) > 0 and "//" in line_split[0]:
            pos = self.file.tell()
            line = self.file.readline()
            line_split = line.split()
        self.file.seek(pos)  # go back to previous position
        if line:
            return True
        else:
            return False

    def advance(self):
        """Advances by reading the current line and
        jumping to the next line"""
        self.current_command = self.file.readline()

    def commandType(self):
        """Returns which command type the current command
        is."""
        for key, value in dict.items():
            if key in self.current_command:
                return value
        return "C_ARITHMETIC"

    def arg(self, idx: int):
        lst = []
        for args in self.current_command:
            lst.append(args)
        return lst[idx]

    def arg1(self):
        """Returns the 1st arg of the
        current commands"""
        return self.arg(0)

    def arg2(self):
        """Returns the 2nd arg of the
        current commands"""
        return self.arg(1)


if __name__ == "__main__":
    print("Hello world!")
