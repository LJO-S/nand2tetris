import re
import sys
from pathlib import Path


class JackTokenizer:
    """The Jack Tokenizer's purpose is to read
    a .jack file (or directory) and strip all
    white space & comments, and break the
    Jack code into Jack-language tokens. The output
    is an .xml containing all tokens."""

    def __init__(self, inputFile=None):
        self.file = self.open_input_file(inputFile)
        self.currentToken = None
        self.tokens = None

    def open_input_file(self, path: str):
        """Opens the file specified by path"""
        file = open(path, "r")
        return file

    def close_input_file(self):
        """Closes input file"""
        self.file.close()

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
            and ((longComment) or ("//" in line_split[0]) or ("/**" in line_split[0]))
        ):
            if (len(line_split) > 0) and "/**" in line_split[0]:
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
        """Advances by reading the first word in currentLine and
        popping that word"""
        if self.tokens == None or len(self.tokens) == 0:
            line = self.file.readline()
            # Substitute // and all following characters with  using Regular Expression
            line_no_comments = re.sub(r"//.*", " ", line)
            # Find all word characters (a-z, 0-9) that occur at least once or...
            # ... all non-whitespace and non-word i.e. symbols.
            self.tokens = re.findall(r"\w+|[^\s\w]", line_no_comments)
        self.currentToken = self.tokens.pop(0)

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
    # TODO modify this to handle .xml files
    if len(sys.argv) < 2:
        print(
            "Usage: python JackTokenizer.py [input_dir/input_filename.vm] or [input_dir]"
        )
        sys.exit(1)
    # Get filename from cmd line
    input_path = sys.argv[1]
    input_path = Path(input_path)
    if "jack" in str(input_path).split("."):
        # Single file
        tokenizer = JackTokenizer(input_path)
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            print(tokenizer.currentToken)
        tokenizer.close_input_file()
    else:
        # Directory (multiple files)
        for vm_file in input_path.glob("*.jack"):
            tokenizer = JackTokenizer(vm_file)
            while tokenizer.hasMoreTokens():
                tokenizer.advance()
                print(tokenizer.currentToken)
            tokenizer.close_input_file()
