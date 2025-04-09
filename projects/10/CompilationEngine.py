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

    def __init__(self, tokenizer: JackTokenizer, outputFile: str):
        self.outputFile = outputFile
        self.tokenizer = tokenizer
        self.depth = 0  # incr for {, decr for }
        self.depthStack = []  # append for {, pop for }
        self.compileClass()

    def compileClass(self):
        self.depthStack.append(ET.Element("class"))
        while self.tokenizer.hasMoreTokens():
            # =========================================================
            self.tokenizer.advance()
            # =========================================================
            if self.tokenizer.tokenType() == "KEYWORD":
                # --------------------------------------------------
                if self.tokenizer.keyWord() == "class":
                    ET.SubElement(self.depthStack[-1], "keyword").text = (
                        self.tokenizer.keyWord()
                    )
                # --------------------------------------------------
                elif (
                    self.tokenizer.keyWord() == "constructor"
                    or self.tokenizer.keyWord() == "method"
                    or self.tokenizer.keyWord() == "function"
                ):
                    self.compileSubroutine()
                # --------------------------------------------------
                elif (
                    self.tokenizer.keyWord() == "int"
                    or self.tokenizer.keyWord() == "boolean"
                    or self.tokenizer.keyWord() == "char"
                ):
                    # TERMINAL BOYS!!
                    ET.SubElement(self.depthStack[-1], "keyword").text = (
                        self.tokenizer.keyWord()
                    )
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "VOID":
                    pass
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "VAR":
                    pass
                # --------------------------------------------------
                elif (
                    self.tokenizer.keyWord() == "static"
                    or self.tokenizer.keyWord() == "field"
                ):
                    self.compileClassVarDec()
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "LET":
                    pass
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "DO":
                    pass
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "IF":
                    pass
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "ELSE":
                    pass
                # --------------------------------------------------
                elif self.tokenizer.keyWord() == "WHILE":
                    pass
                elif self.tokenizer.keyWord() == "RETURN":
                    pass
                elif self.tokenizer.keyWord() == "TRUE":
                    pass
                elif self.tokenizer.keyWord() == "FALSE":
                    pass
                elif self.tokenizer.keyWord() == "NULL":
                    pass
                elif self.tokenizer.keyWord() == "THIS":
                    pass
            # =========================================================
            elif self.tokenizer.tokenType() == "SYMBOL":
                # TODO:
                # this feels like an append with {
                # this feels like a .pop() with ; and }
                # also gotta handle , and shit
                ET.SubElement(self.depthStack[-1], "symbol").text = (
                    self.tokenizer.symbol()
                )
                if (
                    self.tokenizer.symbol() == ";" or self.tokenizer.symbol() == "}"
                ) and len(self.depthStack > 1):
                    # done with whatever statement we were parsing
                    self.depthStack.pop()
                elif self.tokenizer.symbol() == "(":
                    # This may symbolize many things, such as parameterList, expression, expressionList
                    # What determines this? Surely the previous state which called upon a (_)
                    # If inside "subroutineDec" --> "parameterList"
                    # If inside
                    pass

            # =========================================================
            elif self.tokenizer.tokenType() == "INT_CONST":
                pass
            # =========================================================
            elif self.tokenizer.tokenType() == "STRING_CONST":
                pass
            # =========================================================
            elif self.tokenizer.tokenType() == "IDENTIFIER":
                ET.SubElement(self.depthStack[-1], "identifier").text = (
                    self.tokenizer.identifier()
                )
            # =========================================================

        tree = ET.ElementTree(self.depthStack[-1])
        ET.indent(tree, "")
        tree.write(self.outputFile)

    def compileClassVarDec(self):
        self.depthStack.append(ET.SubElement(self.depthStack[-1], "classVarDec"))
        # i.e. field // static
        ET.SubElement(self.depthStack[-1], "keyword").text = self.tokenizer.keyWord()

    def compileSubroutine(self):
        # non-terminal
        self.depthStack.append(ET.SubElement(self.depthStack[-1], "subroutineDec"))
        # i.e. constructor // function // method
        ET.SubElement(self.depthStack[-1], "keyword").text = self.tokenizer.keyWord()

    def compileParameterList(self):
        # non-terminal
        # This can only occur inside a SubroutineDec
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


if __name__ == "__main__":
    pass
