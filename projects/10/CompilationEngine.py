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
            self.writexml(self.root)
        while (self.token.tag != "symbol") and (self.token.text != "{"):
            self.advance()
            self.writexml(self.root)
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
        self.writexml(self.root)

        # Write output file
        tree = ET.ElementTree(self.root)
        ET.indent(tree, "   ")
        tree.write(self.outputFile)

    def compileClassVarDec(self):
        branch = ET.SubElement(self.root, "classVarDec")
        self.writexml(branch)
        while (self.token.tag != "symbol") and (self.token.text != ";"):
            self.advance()
            self.writexml(branch)

    def compileSubroutine(self):
        branchDec = ET.SubElement(self.root, "subroutineDec")
        self.writexml(branchDec)
        while (self.token.tag != "symbol") and (self.token.text != "("):
            self.advance()
            self.writexml(branchDec)
        self.verify("symbol", "(")
        self.writexml(branchDec)  # (
        self.advance()
        self.compileParameterList(branchDec)
        self.writexml(branchDec)  # )
        # subroutineBody
        branchBody = ET.SubElement(self.root, "subroutineBody")
        self.advance()
        self.verify("symbol", "{")
        self.writexml(branchBody)  # {
        self.advance()
        ## varDec*
        while (self.token.tag == "keyword") and (self.token.text == "var"):
            self.compileVarDec(branchBody)
        ## statements
        while (self.token.tag != "symbol") and (self.token.text != "}"):
            self.compileStatements(branchBody)
        # '}'
        self.verify("symbol", "}")
        self.writexml(branchBody)

    def compileParameterList(self, branchName):
        branch = ET.SubElement(branchName, "parameterList")
        while (self.token.tag != "symbol") and (self.token.text != ")"):
            self.writexml(branch)
            self.advance()

    def compileVarDec(self, branchName):
        branch = ET.SubElement(branchName, "varDec")
        self.writexml(branch)  # var
        while (self.token.tag != "symbol") and (self.token.text != ";"):
            self.advance()
            self.writexml(branch)
        # Last advance to get 'var' again
        self.advance()

    def compileStatements(self, branch):
        # EACH CASE WILL HAVE 1 LAST ADVANCE()
        # let
        if (self.token.tag == "keyword") and (self.token.text == "let"):
            self.compileLet(ET.SubElement(branch, "letStatement"))
        # if
        elif (self.token.tag == "keyword") and (self.token.text == "if"):
            self.compileIf(ET.SubElement(branch, "ifStatement"))
        # while
        elif (self.token.tag == "keyword") and (self.token.text == "while"):
            self.compileWhile(ET.SubElement(branch, "whileStatement"))
        # do
        elif (self.token.tag == "keyword") and (self.token.text == "do"):
            # TODO
            self.compileDo(ET.SubElement(branch, "doStatement"))
        # return
        elif (self.token.tag == "keyword") and (self.token.text == "return"):
            # TODO
            self.compileReturn(ET.SubElement(branch, "returnStatement"))
        else:
            self.verify("keyword", "ANY")

    def compileDo(self, branch):
        # do
        self.writexml(branch)
        # id
        self.advance()
        self.writexml(branch)
        # symbol
        self.advance()
        self.writexml(branch)
        if (self.token.tag == "symbol") and (self.token.text == "("):
            # function/method of current class
            self.compileExpressionList(ET.SubElement(branch, "expressionList"))
            self.verify("symbol", ")")
            self.writexml(branch)
        elif (self.token.tag == "symbol") and (self.token.text == "."):
            # function/method of other class
            self.advance()
            self.writexml(branch)  # sub-id
            self.advance()
            self.verify("symbol", "(")
            self.writexml(branch)
            self.compileExpressionList(ET.SubElement(branch, "expressionList"))
            self.verify("symbol", ")")
            self.writexml(branch)
        self.advance()

    def compileLet(self, branch):
        # let
        self.writexml(branch)
        # varName
        self.advance()
        self.writexml(branch)
        # '[' or '='
        self.advance()
        self.writexml(branch)
        if (self.token.tag == "symbol") and (self.token.text == "["):
            # Expression
            branchExpression = ET.SubElement(branch, "expression")
            self.compileExpression(branchExpression)
            self.verify("symbol", "]")
            self.writexml(branch)  # ']'
            # '='
            self.advance()
            self.verify("symbol", "=")
            self.writexml(branch)
            self.compileExpression(branchExpression)
        elif (self.token.tag == "symbol") and (self.token.text == "="):
            branchExpression = ET.SubElement(branch, "expression")
            self.compileExpression(branchExpression)
        self.verify("symbol", ";")
        self.writexml(branch)
        self.advance()

    def compileWhile(self, branch):
        # while
        self.writexml(branch)
        # symbol
        self.advance()
        self.verify("symbol", "(")
        self.writexml(branch)
        # expression
        self.compileExpression(ET.SubElement(branch, "expression"))
        # symbol
        self.verify("symbol", ")")
        self.writexml(branch)
        # symbol
        self.advance()
        self.verify("symbol", "{")
        self.writexml(branch)
        # statements
        self.advance()
        self.compileStatements(ET.SubElement(branch, "statements"))
        self.verify("symbol", "}")
        self.writexml(branch)
        self.advance()

    def compileReturn(self, branch):
        # return
        self.writexml(branch)
        if (self.peek().tag != "symbol") and (self.peek().text != ";"):
            self.compileExpression(ET.SubElement(branch, "expression"))
            self.verify("symbol", ";")
            self.writexml(branch)
        else:
            self.advance()
            self.verify("symbol", ";")
            self.writexml(branch)
        self.advance()

    def compileIf(self, branch):
        # if
        self.writexml(branch)
        # symbol
        self.advance()
        self.verify("symbol", "(")
        self.writexml(branch)
        # expression
        self.compileExpression(ET.SubElement(branch, "expression"))
        # symbol
        self.verify("symbol", ")")
        self.writexml(branch)
        # symbol
        self.advance()
        self.verify("symbol", "{")
        self.writexml(branch)
        # statements
        # TODO: probably one advance here
        self.advance()
        self.compileStatements(ET.SubElement(branch, "statements"))
        self.verify("symbol", "}")
        self.writexml(branch)
        self.advance()
        if (self.token.tag == "keyword") and (self.token.text == "else"):
            # 'else' '{'
            for _ in range(2):
                self.writexml(branch)
                self.advance()
            self.compileStatements(ET.SubElement(branch, "statements"))
            self.verify("symbol", "}")
            self.writexml(branch)
            self.advance()

    def compileExpression(self, branch):
        self.advance()  # term
        branchTerm = ET.SubElement(branch, "term")
        self.compileTerm(branchTerm)
        if self.token.text in ("+", "-", "*", "/", "&", "|", "<", ">", "="):
            self.writexml(branch)
            self.compileExpression(branch)

    def compileTerm(self, branch):
        if self.token.tag == "integerConstant":
            self.writexml(branch)
        elif self.token.tag == "stringConstant":
            self.writexml(branch)
        elif (self.token.tag == "keyword") and (
            (self.token.text) in ("true", "false", "null", "this")
        ):
            self.writexml(branch)
        elif self.token.tag == "identifier":
            # LOOKAHEAD!!! need to diff between varName, varName[], and varName.xxx()
            lookaheadToken = self.peek()
            if (lookaheadToken.tag == "symbol") and (lookaheadToken.text == "["):
                # array
                self.writexml(branch)
                self.advance()
                self.verify("symbol", "[")
                self.writexml(branch)
                self.compileExpression(branch)
                self.verify("symbol", "]")
                self.writexml(branch)
            elif (lookaheadToken.tag == "symbol") and (lookaheadToken.text == "("):
                # function/method of current class
                self.writexml(branch)  # id
                self.advance()
                self.verify("symbol", "(")
                self.writexml(branch)
                self.compileExpressionList(ET.SubElement(branch, "expressionList"))
                self.verify("symbol", ")")
                self.writexml(branch)
            elif (lookaheadToken.tag == "symbol") and (lookaheadToken.text == "."):
                # function/method of other class
                self.writexml(branch)  # id
                self.advance()
                self.verify("symbol", ".")
                self.writexml(branch)  # '.'
                self.advance()
                self.writexml(branch)  # sub-id
                self.advance()
                self.verify("symbol", "(")
                self.writexml(branch)
                self.compileExpressionList(ET.SubElement(branch, "expressionList"))
                self.verify("symbol", ")")
                self.writexml(branch)
            else:
                # varName
                self.writexml(branch)
        elif (self.token.tag == "symbol") and (self.token.text == "("):
            # '(' expression ')'
            self.writexml(branch)
            self.advance()
            self.compileExpression(branch)
            self.verify("symbol", ")")
            self.writexml(branch)
        elif (self.token.tag == "symbol") and (
            (self.token.text == "~") or (self.token.text == "-")
        ):
            # UNARY OP
            self.writexml(branch)
            self.advance()
            branchTerm = ET.SubElement(branch, "term")
            self.compileTerm(branchTerm)
        # Last advance
        self.advance()

    def compileExpressionList(self, branch):
        """Compiles a list of 0 or more expressions. \n
        Grammar: (expression (',' expression)*)?"""
        branchExpression = ET.SubElement(branch, "expression")
        self.compileExpression(branchExpression)
        if (self.token.tag == "symbol") and (self.token.text == ","):
            self.writexml(branch)
            self.compileExpression(branchExpression)

    ## Helper functions ##

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

    def writexml(self, branch):
        ET.SubElement(branch, self.token.tag).text = self.token.text

    def verify(self, expectedTag: str, expectedText: str):
        if (self.token.tag != expectedTag) or (self.token.text != expectedText):
            raise Exception(
                f"Expected '<"
                + expectedTag
                + "> "
                + expectedText
                + " </"
                + expectedTag
                + ">' but got '<"
                + self.token.tag
                + "> "
                + self.token.text
                + " </"
                + self.token.tag
                + ">'"
            )

    def peek(self):
        if self.hasMoreTokens():
            return self.tokens[self.idx + 1]
        return None


if __name__ == "__main__":
    pass
