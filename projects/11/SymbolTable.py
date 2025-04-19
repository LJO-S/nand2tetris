# The purpose of the symboltable:
# - Every identifier found starting with 'var', 'static'... is added to symbol table with type, kind, and run index
# - When we run the code and find a non-hashed identifier, we can assume this is a class/subroutine name
#   ... We can then peek to see if class/subroutine; if 'subroutine', we find '.' or '(', else 'class'.

import copy

class SymbolTable:

    def __init__(self):
        self.classScope = {}
        self.subroutineScope = {}
        self._idxTracker = {}

    def startSubroutine(self) -> None:
        """
        Starts a new subroutine scope by clearing current
        subroutine scope. Clears 'var' & 'arg' running idx from
        _idxTracker if they exist

            Parameters:
                None
            Returns:
                None
        """
        # Clear scope
        self.subroutineScope.clear()
        # Clear _idxTracker for subroutine
        self._idxTracker.pop("var", None)
        self._idxTracker.pop("arg", None)

    def define(self, name: str, type: str, kind: str) -> None:
        """
        Defines a new ID of a given name, type, and kind.
        Assigns it a running index. 'static' & 'field' have 
        CLASS scope. 'var' & 'arg' have SUBROUTINE scope.
        
            Parameters:
                name (str): __name__
                type (str): int, char, string etc...
                kind (str): static / field / var / arg
            Returns:
                None
        """
        idx = 0
        temp_dict = {}
        isClass = False
        # Note: using {} to create a set which compares hashes to get O(1) iteration speed
        # Note: temp_dict is a reference to the *scope, so it changes them straight away
        if (kind in {'static', 'field'}):
            temp_dict = self.classScope
            isClass = True
        else:
            temp_dict = self.subroutineScope

        # Error if identifier already exists
        if name in temp_dict.keys():
            raise KeyError("Tried defining '" + name + "' but already defined in " + 
                            ("Class" if isClass else "Subroutine") + " Symbol Table\r\n")
        
        # Return running index if it exists else set to 0
        idx = self._idxTracker.get(kind, -1) + 1
        self._idxTracker[kind] = idx

        # Create new dict element
        temp_dict[name] = {
                "type" : type, 
                "kind" : kind, 
                "idx"  : idx 
                }

    def varCount(self, kind: str)  -> int:
        """
        Returns the number of variables of the given 'kind' 
        already defined in the current scope.

            Parameters:
                kind (str): static / field / var / arg 
            Returns:
                count (int): the number of variables declared in the current scope
        """
        if kind in {'static', 'field', 'arg', 'var'}:
            return self._idxTracker[kind] + 1
        else:
            raise ValueError(f"Illegal 'kind'! Tried varCount({kind}).")

    def kindOf(self, name: str) -> str | None:
        """
        Returns the 'kind' of the identifier 'name' in the current 
        scope.
        If the identifier is unknown, returns None.
            
            Parameters:
                name (str): name of the identifier
            Returns:
                kind (str, None): static / field / arg / var / None
        """
        if name in self.subroutineScope:
            return self.subroutineScope[name]["kind"]
        elif name in self.classScope:
            return self.classScope[name]["kind"]
        # if none, then probably a func call?
        return None
            
    def typeOf(self, name: str) -> str:
        """
        Returns the 'type' of the named identifier in the
        current scope.

            Parameters:
                name (str): identifier
            Returns:
                type (str): type of named identifier
        """
        if name in self.subroutineScope:
            return self.subroutineScope[name]["type"]
        elif name in self.classScope:
            return self.classScope[name]["type"]
        else:
            raise KeyError(f"typeOf() failed! '{name}' not defined in either scope.")

    def indexOf(self, name: str) -> int:
        """
        Returns the running index of the named identifier
        in the current scope.

            Parameters:
                name (str): identifier
            Returns:
                idx (int): running index of named identifier
        """
        if name in self.subroutineScope:
            return self.subroutineScope[name]["idx"]
        elif name in self.classScope:
            return self.classScope[name]["idx"]
        else:
            raise KeyError(f"indexOf() failed! '{name}' not defined in either scope.")

if __name__ == "__main__":
    symbolTable = SymbolTable()

    input = [("A", "int", "static"),
            ("B", "int", "static"),
            ("C", "char", "field"),
            ("D", "int", "arg"),
            ("E", "bool", "field"),
            ("F", "int", "arg"),
            ("G", "int", "static"),
            ("H", "int", "var"),
            ("I", "bool", "var"),
            ]

    for elem in input:
        symbolTable.define(elem[0], elem[1], elem[2])
    
    print(symbolTable._idxTracker)
    print()
    print(symbolTable.classScope)
    print()
    print(symbolTable.subroutineScope)
