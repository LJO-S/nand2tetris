


class SymbolTable:

    def __init__(self):
        self.hash_table = {
            ("R0","SP",)   : "0",
            ("R1","LCL",)  : "1",
            ("R2","ARG",)  : "2",
            ("R3","THIS",) : "3",
            ("R4","THAT",) : "4",
            ("R5",)        : "5",
            ("R6",)        : "6",
            ("R7",)        : "7",
            ("R8",)        : "8",
            ("R9",)        : "9",
            ("R10",)       : "10",
            ("R11",)       : "11",
            ("R12",)       : "12",
            ("R13",)       : "13",
            ("R14",)       : "14",
            ("R15",)       : "15",
            ("SCREEN",)    : "16384",
            ("KBD",)       : "24576"
        }

    def __str__(self):
        pass

    def addEntry(self, symbol: str, address: str):
        """Add key:value pair {symbol}:{address} to
        hash table"""
        self.hash_table[symbol] = address
        return None

    def contains(self, symbol: str):
        """Checks if hash table contains {symbol}"""
        contain_bool = False
        for key_group, binary in self.hash_table.items():
            if symbol.strip() in key_group:
                contain_bool = True
        return contain_bool
    
    def getAddress(self, symbol: str):
        """Returns the {address} bound to {symbol}"""
        return self.hash_table[symbol]


if __name__ == "__main__":
    pass
