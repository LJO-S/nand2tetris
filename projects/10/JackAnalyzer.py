#!/usr/bin/python

import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

# This module is the top file
# 1. Creates a JackTokenizer
# 2. Create output xml file
# 3. Drive JackTokenizer. Use JackTokenizer to feed CompilationEngine


def TokenizerHandler(tokenizer: JackTokenizer):
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
    return root


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python JackAnalyzer.py [input_dir/input_filename.vm] or [input_dir]"
        )
        sys.exit(1)
    # Get filename from cmd line
    inputPath = sys.argv[1]
    inputPath = Path(inputPath)

    if "jack" in str(inputPath).split("."):
        # Single file
        outputDir = inputPath.parent
        outputName = inputPath.stem
        outputFile = str(outputDir) + "/" + f"{outputName}_user.xml"
        tokenizer = JackTokenizer(inputPath)
        tokens = TokenizerHandler(tokenizer)
        tokenizer.close_input_file()
        compilator = CompilationEngine(tokens, outputFile)
    else:
        # Directory (multiple files)
        outputDir = inputPath
        for jackFile in inputPath.glob("*.jack"):
            outputFile = str(outputDir) + "/" + f"{jackFile.stem}_user.xml"
            tokenizer = JackTokenizer(jackFile)
            tokens = TokenizerHandler(tokenizer)
            tokenizer.close_input_file()
            compilator = CompilationEngine(tokens, outputFile)
