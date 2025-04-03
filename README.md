# nand2tetris repo

These are my solutions to the different nand2tetris tasks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

See User Guide at:

```
/User Guide.pdf
```

## nand2tetris Tools
* Assembler - Compiles .vm files into .asm files to be run on the CPUEmulator.
* HardwareSimulator - Simulates chip component behaviour and can be used to test output of chip implementation.
* VMEmulator - used to emulate virtual machine environment. Executes .vm files and throws errors when encountering bugs.
* CPUEmulator - Emulates CPU (ALU, registers, PC, RAM, ROM...) by running an .asm program on it. Throws errors when encountering bugs.
* JackCompiler - Compiles files in the .jack language into .vm files to be run on a VMEmulator.
* TextComparer - haven't used in project.

## nand2tetris Goals
* Learn how a digital computer works and how software executes on it.
* Get familiar with high-level code transformation into machine code, along with execution of it.
* Implement the Harvard architecture CPU on a Artix-family FPGA using VHDL.

## Authors
**Ludvig**

## Acknowledgments

* Nisan and Schocken, and the nand2tetris community.
