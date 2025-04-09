#!/usr/bin/python

import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path
import JackTokenizer

# This will be the master, handling .advance() and so on.
# Only .advance() if .hasMoreTokens() is true
# Terminals: keyword, symbol, integerConst, strinGconstant, indetifier


# TODO
# ParameterList or varDec


class CompilationEngine:

    def __init__(self, tokenizedInput: ET.Element, outputFile: str):
        self.outputFile = outputFile
        self.tokens = list(tokenizedInput)
        self.idx = 0
        self.token = self.tokens[0]
        # Creating a seed to be grown into an XML
        self.root = ET.Element("class")

        # Heading to compile class which is recursive in itself
        self.compileClass()

    def compileClass(self):
        if (self.token.tag != "keyword") or (self.token.text != "class"):
            raise Exception(
                "Token list does not start with '<keyword> class </keyword>'!"
            )
        else:
            # <keyword> class </keyword>
            ET.SubElement(self.root, self.token.tag).text = self.token.text
        while (self.token.tag != "symbol") and (self.token.text != "{"):
            self.advance()
            ET.SubElement(self.root, self.token.tag).text = self.token.text
        ### =============================
        # Recursive Part!!!
        while (self.token.tag == "keyword") and (
            (self.token.text in ("static", "field"))
        ):
            self.compileClassVarDec()
            self.advance()
        while (self.token.tag == "keyword") and (
            (self.token.text in ("constructor", "function", "method"))
        ):
            self.compileSubroutine()
            self.advance()
        ### =============================
        # Write <symbol> } </symbol>
        ET.SubElement(self.root, self.token.tag).text = self.token.text

        # Write output file
        tree = ET.ElementTree(self.root)
        ET.indent(tree, "   ")
        tree.write(self.outputFile)

    def compileClassVarDec(self):
        branch = ET.SubElement(self.root, "classVarDec")
        ET.SubElement(branch, self.token.tag).text = self.token.text
        while (self.token.tag != "symbol") and (self.token.text != ";"):
            self.advance()
            ET.SubElement(branch, self.token.tag).text = self.token.text

    def compileSubroutine(self):
        branch = ET.SubElement(self.root, "subroutineDec")
        ET.SubElement(branch, self.token.tag).text = self.token.text
        while (self.token.tag != "symbol") and (self.token.text != "("):
            self.advance()
            ET.SubElement(branch, self.token.tag).text = self.token.text
        if (self.token.tag == "symbol") and (self.token.text == "("):
            ET.SubElement(branch, self.token.tag).text = self.token.text
            self.advance()
            self.compileParameterList(branch)
        else:
            raise Exception(
                f"Expected ' <symbol> ( </symbol>' but got '<"
                + self.token.tag
                + "> "
                + self.token.text
                + " </"
                + self.token.tag
                + ">'"
            )

    def compileParameterList(self, branchName):
        branch = ET.SubElement(branchName, "parameterList")
        pass

    def compileVarDec(self):
        # non-terminal
        pass

    def compileStatements(self):
        # non-terminal
        pass

    def compileDo(self):
        # non-terminal
        pass

    def compileLet(self):
        # non-terminal
        pass

    def compileWhile(self):
        # non-terminal
        pass

    def compileReturn(self):
        # non-terminal
        pass

    def compileIf(self):
        # non-terminal
        pass

    def compileExpression(self):
        # non-terminal
        pass

    def compileTerm(self):
        # non-terminal
        # Lookahead!!
        pass

    def compileExpressionList(self):
        # non-terminal
        pass

    ## Helper functions
    def hasMoreTokens(self):
        """Checks if more tokens are available.
        Returns true if current idx is smaller than length of
        tokens list."""
        return self.idx < len(self.tokens)

    def advance(self):
        if self.hasMoreTokens():
            self.idx += 1
            self.token = self.tokens[self.idx]
        else:
            self.token = None

    def peek(self):
        if self.hasMoreTokens():
            return self.tokens[self.idx + 1]
        return None


if __name__ == "__main__":
    pass
