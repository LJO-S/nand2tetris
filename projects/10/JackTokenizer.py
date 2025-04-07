#!/usr/bin/python

import xml.etree.ElementTree as ET
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

        self.keywordTable = [
            "class",
            "constructor",
            "function",
            "method",
            "field",
            "static",
            "var",
            "int",
            "char",
            "boolean",
            "void",
            "true",
            "false",
            "null",
            "this",
            "let",
            "do",
            "if",
            "else",
            "while",
            "return",
        ]

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
        # while line == "\n" or (
        while line.isspace() or (
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
            # 1. Find everything that starts and ends with ". It is not allowed with new space and " inside
            # 2. Find all word characters (a-z, 0-9) that occur at least once
            # 3. Find all non-whitespace and non-word i.e. symbols.
            self.tokens = re.findall(r'"[^"\n]*"|[\w]+|[^\s\w]', line_no_comments)
        self.currentToken = self.tokens.pop(0)

    def tokenType(self):
        """Returns the type of the current token"""

        if re.search(r'"[^"\n]*"', self.currentToken):
            return "STRING_CONST"

        elif re.search(r"[^\w]", self.currentToken):
            return "SYMBOL"

        elif re.search(r"[0-9]+", self.currentToken):
            return "INT_CONST"

        elif self.currentToken in self.keywordTable:
            return "KEYWORD"

        elif re.search(r"\w", self.currentToken):
            return "IDENTIFIER"
        else:
            raise Exception("Unknown token: " + self.currentToken)

    def keyWord(self):
        return self.currentToken.lower()

    def symbol(self):
        return self.currentToken

    def identifier(self):
        return self.currentToken

    def intVal(self):
        return self.currentToken

    def stringVal(self):
        stringVal = self.currentToken.split('"')
        return stringVal[1]


def xmlOutput(tokenizer: JackTokenizer, outputFile=None):
    """Handles XML file writing"""

    root = ET.Element("tokens")
    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        if tokenizer.tokenType() == "STRING_CONST":
            ET.SubElement(root, "stringConstant").text = (
                " " + tokenizer.stringVal() + " "
            )
        elif tokenizer.tokenType() == "SYMBOL":
            ET.SubElement(root, "symbol").text = tokenizer.symbol()
        elif tokenizer.tokenType() == "INT_CONST":
            ET.SubElement(root, "integerConstant").text = tokenizer.intVal()
        elif tokenizer.tokenType() == "KEYWORD":
            ET.SubElement(root, "keyword").text = tokenizer.keyWord()
        elif tokenizer.tokenType() == "IDENTIFIER":
            ET.SubElement(root, "identifier").text = tokenizer.identifier()

    tree = ET.ElementTree(root)
    ET.indent(tree, "")
    tree.write(outputFile)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python JackTokenizer.py [input_dir/input_filename.vm] or [input_dir]"
        )
        sys.exit(1)
    # Get filename from cmd line
    inputPath = sys.argv[1]
    inputPath = Path(inputPath)

    if "jack" in str(inputPath).split("."):
        # Single file
        outputDir = inputPath.parent
        outputName = inputPath.stem
        outputFile = str(outputDir) + "/" + f"{outputName}T_user.xml"
        tokenizer = JackTokenizer(inputPath)
        xmlOutput(tokenizer, outputFile)
        tokenizer.close_input_file()
    else:
        # Directory (multiple files)
        outputDir = inputPath
        for jackFile in inputPath.glob("*.jack"):
            outputFile = str(outputDir) + "/" + f"{jackFile.stem}T_user.xml"
            tokenizer = JackTokenizer(jackFile)
            xmlOutput(tokenizer, outputFile)
            tokenizer.close_input_file()
