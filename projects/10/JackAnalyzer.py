#!/usr/bin/python

import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path
import JackTokenizer
import CompilationEngine

# This module is the top file
# 1. Creates a JackTokenizer
# 2. Create output xml file
# 3. Drive JackTokenizer. Use JackTokenizer to feed CompilationEngine


def xmlOutput(tokenizer: JackTokenizer):
    """Handles XML file writing"""

    root = ET.Element("tokens")
    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        # if tokenizer.tokenType() == "STRING_CONST":
        #    pass
        # elif tokenizer.tokenType() == "SYMBOL":
        #    pass
        # elif tokenizer.tokenType() == "INT_CONST":
        #    pass
        # elif tokenizer.tokenType() == "KEYWORD":
        #    pass
        # elif tokenizer.tokenType() == "IDENTIFIER":
        #    pass


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
        # TODO let CompilationEngine kick in here
    else:
        # Directory (multiple files)
        outputDir = inputPath
        for jackFile in inputPath.glob("*.jack"):
            outputFile = str(outputDir) + "/" + f"{jackFile.stem}T_user.xml"
            tokenizer = JackTokenizer(jackFile)
            xmlOutput(tokenizer, outputFile)
            tokenizer.close_input_file()
            # TODO let CompilationEngine kick in here
