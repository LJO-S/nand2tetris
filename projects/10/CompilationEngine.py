#!/usr/bin/python

import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path


# Let JackAnalyzer feed the JackTokenizer into the CompilationEngine, no xml_T needed...
# The CompilationEngine will then be the master, handling .advance() and so on.
# Terminals: keyword, symbol, integerConst, strinGconstant, indetifier


class CompilationEngine:

    def __init__(self, inputPath=None, outputPath=None):
        pass

    def compileClass(self):
        # non-terminal
        pass

    def compileClassVarDec(self):
        # non-terminal
        pass

    def compileSubroutine(self):
        # non-terminal
        pass

    def compileParameterList(self):
        # non-terminal
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
