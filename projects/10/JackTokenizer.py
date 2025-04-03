class JackTokenizer:
    """The Jack Tokenizer's purpose is to read
    a .jack file (or directory) and strip all
    white space & comments, and break the
    Jack code into Jack-language tokens. The output
    is an .xml containing all tokens."""

    def __init__(self, inputFile=None):
        self.file = self.open_output_file(inputFile)
        self.currentToken = None

    def hasMoreTokens(self):
        """Checks if the current line is EOF or not
        but does not advance a line in the file. Skips
        comments and newlines."""
        longComment = False
        pos = self.file.tell()  # current position of file
        line = self.file.readline()
        line_split = line.split()
        while line == "\n" or (
            len(line_split) > 0
            and (longComment)
            or ("//" in line_split[0])
            or ("/**" in line_split[0])
        ):
            if "/**" in line_split[0]:
                longComment = True
            if "*/" in line_split:
                longComment = False
            pos = self.file.tell()
            line = self.file.readline()
            line_split = line.split()
        self.file.seek(pos)  # go back to previous position
        if line:
            return True
        else:
            return False

    def advance(self):
        pass

    def tokenType(self):
        pass

    def keyWord(self):
        pass

    def symbol(self):
        pass

    def identifier(self):
        pass

    def intVal(self):
        pass

    def stringVal(self):
        pass


if __name__ == "__main__":
    print("Hello world!\r\n")
