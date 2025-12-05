"""
Name: Luke Reicherter
Student ID: 3135060
Class: EECS 510
Final Project: R-Type Turing Machine
"""

#import networkx as nx 
#import matplotlib.pyplot as plt

class RTypeTM:
    def __init__(self, tape, initial_state='op0', blank='_'):
        self.tape = tape
        self.head = 0
        self.state = initial_state
        self.blank = blank
        self.steps = 0
        self.isValid = 0
        self.alphabet = ['0', '1', '#', 'A', 'B', 'C', 'D', 'E', 'X', 'Y', 'Z', ':', '+', '_', 'd']
        self.transitions = {
            # Transistion Structure: (Current State, Read): (Write, Direction, Next State)
            # Reads the opcode bits
            ('op0', '0'): ('_', 'R', 'op1'),
            ('op1', '0'): ('_', 'R', 'op2'),
            ('op2', '0'): ('_', 'R', 'op3'),
            ('op3', '0'): ('_', 'R', 'op4'),
            ('op4', '0'): ('_', 'R', 'op5'),
            ('op5', '0'): ('_', 'R', 'rs0'),

            # Finds the register that RS refers to
            ('rs0', '0'): ('_', 'R', 'rs1'),
            ('rs0', '1'): ('_', 'R', 'regE0blank0'),
            ('rs1', '0'): ('_', 'R', 'rs2'),
            ('rs1', '1'): ('_', 'R', 'regD0blank0'),
            ('rs2', '0'): ('_', 'R', 'rs3'),
            ('rs2', '1'): ('_', 'R', 'regC0blank0'),
            ('rs3', '0'): ('_', 'R', 'rs4'),
            ('rs3', '1'): ('_', 'R', 'regB0blank0'),
            ('rs4', '1'): ('_', 'R', 'regA0'),

            # Goes to Reg A
            ('regA0', '0'): ('0', 'R', 'regA0'),
            ('regA0', '1'): ('1', 'R', 'regA0'),
            ('regA0', '#'): ('#', 'R', 'regA0'),
            ('regA0', 'A'): ('A', 'R', 'passColon0'),

            # Goes to Reg B
            ('regB0blank0', '0'): ('_', 'R', 'regB0'),
            ('regB0', '0'): ('0', 'R', 'regB0'),
            ('regB0', '1'): ('1', 'R', 'regB0'),
            ('regB0', '#'): ('#', 'R', 'regB0'),
            ('regB0', 'A'): ('A', 'R', 'regB0'),
            ('regB0', ':'): (':', 'R', 'regB0'),
            ('regB0', 'B'): ('B', 'R', 'passColon0'),
            
            # Goes to Reg C
            ('regC0blank0', '0'): ('_', 'R', 'regC0blank1'),
            ('regC0blank1', '0'): ('_', 'R', 'regC0'),
            ('regC0', '0'): ('0', 'R', 'regC0'),
            ('regC0', '1'): ('1', 'R', 'regC0'),
            ('regC0', '#'): ('#', 'R', 'regC0'),
            ('regC0', 'A'): ('A', 'R', 'regC0'),
            ('regC0', ':'): (':', 'R', 'regC0'),
            ('regC0', 'B'): ('B', 'R', 'regC0'),
            ('regC0', 'C'): ('C', 'R', 'passColon0'),
            
            # Goes to Reg D
            ('regD0blank0', '0'): ('_', 'R', 'regD0blank1'),
            ('regD0blank1', '0'): ('_', 'R', 'regD0blank2'),
            ('regD0blank2', '0'): ('_', 'R', 'regD0'),
            ('regD0', '0'): ('0', 'R', 'regD0'),
            ('regD0', '1'): ('1', 'R', 'regD0'),
            ('regD0', '#'): ('#', 'R', 'regD0'),
            ('regD0', 'A'): ('A', 'R', 'regD0'),
            ('regD0', ':'): (':', 'R', 'regD0'),
            ('regD0', 'B'): ('B', 'R', 'regD0'),
            ('regD0', 'C'): ('C', 'R', 'regD0'),
            ('regD0', 'D'): ('D', 'R', 'passColon0'),

            # Goes to Reg E
            ('regE0blank0', '0'): ('_', 'R', 'regE0blank1'),
            ('regE0blank1', '0'): ('_', 'R', 'regE0blank2'),
            ('regE0blank2', '0'): ('_', 'R', 'regE0blank3'),
            ('regE0blank3', '0'): ('_', 'R', 'regE0'),
            ('regE0', '0'): ('0', 'R', 'regE0'),
            ('regE0', '1'): ('1', 'R', 'regE0'),
            ('regE0', '#'): ('#', 'R', 'regE0'),
            ('regE0', 'A'): ('A', 'R', 'regE0'),
            ('regE0', ':'): (':', 'R', 'regE0'),
            ('regE0', 'B'): ('B', 'R', 'regE0'),
            ('regE0', 'C'): ('C', 'R', 'regE0'),
            ('regE0', 'D'): ('D', 'R', 'regE0'),
            ('regE0', 'E'): ('E', 'R', 'passColon0'),

            # Passes the colon, then starts the moving of the register value to the workspace
            ('passColon0', ':'): (':', 'R', 'RegtoWorkspace0'),
            ('RegtoWorkspace0', '0'): ('X', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0', '1'): ('Y', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0', 'B'): ('B', 'R', 'FinishedRegtoWorkspace0'),
            ('RegtoWorkspace0', 'C'): ('C', 'R', 'FinishedRegtoWorkspace0'),
            ('RegtoWorkspace0', 'D'): ('D', 'R', 'FinishedRegtoWorkspace0'),
            ('RegtoWorkspace0', 'E'): ('E', 'R', 'FinishedRegtoWorkspace0'),
            ('RegtoWorkspace0', '#'): ('#', 'R', 'FinishedRegtoWorkspace0'),

            # Steps for moving a 0
            ('RegtoWorkspace0Copy0Step1', '0'): ('0', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', '1'): ('1', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', 'B'): ('B', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', ':'): (':', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', 'C'): ('C', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', 'D'): ('D', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', 'E'): ('E', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', '#'): ('#', 'R', 'RegtoWorkspace0Copy0Step1'),
            ('RegtoWorkspace0Copy0Step1', '_'): ('0', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', '0'): ('0', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', '1'): ('1', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', '#'): ('#', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', ':'): (':', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', 'E'): ('E', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', 'D'): ('D', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', 'C'): ('C', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', 'B'): ('B', 'L', 'RegtoWorkspace0Copy0Step2'),
            ('RegtoWorkspace0Copy0Step2', 'X'): ('X', 'R', 'RegtoWorkspace0'),

            # Steps for moving a 1
            ('RegtoWorkspace0Copy1Step1', '0'): ('0', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', '1'): ('1', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', 'B'): ('B', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', ':'): (':', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', 'C'): ('C', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', 'D'): ('D', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', 'E'): ('E', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', '#'): ('#', 'R', 'RegtoWorkspace0Copy1Step1'),
            ('RegtoWorkspace0Copy1Step1', '_'): ('1', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', '0'): ('0', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', '1'): ('1', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', '#'): ('#', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', ':'): (':', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', 'E'): ('E', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', 'D'): ('D', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', 'C'): ('C', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', 'B'): ('B', 'L', 'RegtoWorkspace0Copy1Step2'),
            ('RegtoWorkspace0Copy1Step2', 'Y'): ('Y', 'R', 'RegtoWorkspace0'),
            
            # Finished moving register value, starts to find next register
            ('FinishedRegtoWorkspace0', 'X'): ('0', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', 'Y'): ('1', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', ':'): (':', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', 'E'): ('E', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', 'D'): ('D', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', 'C'): ('C', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', 'B'): ('B', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', 'A'): ('A', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', '#'): ('#', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', '0'): ('0', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', '1'): ('1', 'R', 'FinishedRegtoWorkspace0'),
            ('FinishedRegtoWorkspace0', '_'): ('#', 'L', 'FinishedRegtoWorkspace1'),

            # Determines if next step is rt or rd decode
            ('FinishedRegtoWorkspace1', 'X'): ('0', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'Y'): ('1', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', ':'): (':', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'E'): ('E', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'D'): ('D', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'C'): ('C', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'B'): ('B', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'A'): ('A', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', '#'): ('#', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', '0'): ('0', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', '1'): ('1', 'L', 'FinishedRegtoWorkspace1'),
            ('FinishedRegtoWorkspace1', 'd'): ('_', 'R', 'rd0'),
            ('FinishedRegtoWorkspace1', '_'): ('_', 'R', 'rt0'),
            
            # Finds the register rt refers to
            ('rt0', '0'): ('_', 'R', 'rt1'),
            ('rt0', '1'): ('_', 'R', 'regE1blank0'),
            ('rt1', '0'): ('_', 'R', 'rt2'),
            ('rt1', '1'): ('_', 'R', 'regD1blank0'),
            ('rt2', '0'): ('_', 'R', 'rt3'),
            ('rt2', '1'): ('_', 'R', 'regC1blank0'),
            ('rt3', '0'): ('_', 'R', 'rt4'),
            ('rt3', '1'): ('_', 'R', 'regB1blank0'),
            ('rt4', '1'): ('d', 'R', 'regA1'),

            # Goes to Reg A
            ('regA1', '0'): ('0', 'R', 'regA1'),
            ('regA1', '1'): ('1', 'R', 'regA1'),
            ('regA1', '#'): ('#', 'R', 'regA1'),
            ('regA1', 'A'): ('A', 'R', 'passColon0'),

            # Goes to Reg B
            ('regB1blank0', '0'): ('d', 'R', 'regB1'),
            ('regB1', '0'): ('0', 'R', 'regB1'),
            ('regB1', '1'): ('1', 'R', 'regB1'),
            ('regB1', '#'): ('#', 'R', 'regB1'),
            ('regB1', 'A'): ('A', 'R', 'regB1'),
            ('regB1', ':'): (':', 'R', 'regB1'),
            ('regB1', 'B'): ('B', 'R', 'passColon0'),

            # Goes to Reg C
            ('regC1blank0', '0'): ('_', 'R', 'regC1blank1'),
            ('regC1blank1', '0'): ('d', 'R', 'regC1'),
            ('regC1', '0'): ('0', 'R', 'regC1'),
            ('regC1', '1'): ('1', 'R', 'regC1'),
            ('regC1', '#'): ('#', 'R', 'regC1'),
            ('regC1', 'A'): ('A', 'R', 'regC1'),
            ('regC1', ':'): (':', 'R', 'regC1'),
            ('regC1', 'B'): ('B', 'R', 'regC1'),
            ('regC1', 'C'): ('C', 'R', 'passColon0'),

            # Goes to Reg D
            ('regD1blank0', '0'): ('_', 'R', 'regD1blank1'),
            ('regD1blank1', '0'): ('_', 'R', 'regD1blank2'),
            ('regD1blank2', '0'): ('d', 'R', 'regD1'),
            ('regD1', '0'): ('0', 'R', 'regD1'),
            ('regD1', '1'): ('1', 'R', 'regD1'),
            ('regD1', '#'): ('#', 'R', 'regD1'),
            ('regD1', 'A'): ('A', 'R', 'regD1'),
            ('regD1', ':'): (':', 'R', 'regD1'),
            ('regD1', 'B'): ('B', 'R', 'regD1'),
            ('regD1', 'C'): ('C', 'R', 'regD1'),
            ('regD1', 'D'): ('D', 'R', 'passColon0'),
            
            # Goes to Reg E
            ('regE1blank0', '0'): ('_', 'R', 'regE1blank1'),
            ('regE1blank1', '0'): ('_', 'R', 'regE1blank2'),
            ('regE1blank2', '0'): ('_', 'R', 'regE1blank3'),
            ('regE1blank3', '0'): ('d', 'R', 'regE1'),
            ('regE1', '0'): ('0', 'R', 'regE1'),
            ('regE1', '1'): ('1', 'R', 'regE1'),
            ('regE1', '#'): ('#', 'R', 'regE1'),
            ('regE1', 'A'): ('A', 'R', 'regE1'),
            ('regE1', ':'): (':', 'R', 'regE1'),
            ('regE1', 'B'): ('B', 'R', 'regE1'),
            ('regE1', 'C'): ('C', 'R', 'regE1'),
            ('regE1', 'D'): ('D', 'R', 'regE1'),
            ('regE1', 'E'): ('E', 'R', 'passColon0'),

            # Finds the register rd refers to
            ('rd0', '0'): ('_', 'R', 'rd1'),
            ('rd0', '1'): ('_', 'R', 'markregEblank0'),
            ('rd1', '0'): ('_', 'R', 'rd2'),
            ('rd1', '1'): ('_', 'R', 'markregDblank0'),
            ('rd2', '0'): ('_', 'R', 'rd3'),
            ('rd2', '1'): ('_', 'R', 'markregCblank0'),
            ('rd3', '0'): ('_', 'R', 'rd4'),
            ('rd3', '1'): ('_', 'R', 'markregBblank0'),
            ('rd4', '1'): ('_', 'R', 'markregA'),

            # Moves to Reg A for marking
            ('markregA', '0'): ('0', 'R', 'markregA'),
            ('markregA', '1'): ('1', 'R', 'markregA'),
            ('markregA', '#'): ('#', 'R', 'markregA'),
            ('markregA', 'A'): ('A', 'R', 'markdestreg'),
            
            # Moves to Reg B for marking
            ('markregBblank0', '0'): ('_', 'R', 'markregB'),
            ('markregB', '0'): ('0', 'R', 'markregB'),
            ('markregB', '1'): ('1', 'R', 'markregB'),
            ('markregB', '#'): ('#', 'R', 'markregB'),
            ('markregB', 'A'): ('A', 'R', 'markregB'),
            ('markregB', ':'): (':', 'R', 'markregB'),
            ('markregB', 'B'): ('B', 'R', 'markdestreg'),
            
            # Moves to Reg C for marking
            ('markregCblank0', '0'): ('_', 'R', 'markregCblank1'),
            ('markregCblank1', '0'): ('_', 'R', 'markregC'),
            ('markregC', '0'): ('0', 'R', 'markregC'),
            ('markregC', '1'): ('1', 'R', 'markregC'),
            ('markregC', '#'): ('#', 'R', 'markregC'),
            ('markregC', 'A'): ('A', 'R', 'markregC'),
            ('markregC', ':'): (':', 'R', 'markregC'),
            ('markregC', 'B'): ('B', 'R', 'markregC'),
            ('markregC', 'C'): ('C', 'R', 'markdestreg'),

            # Moves to Reg D for marking
            ('markregDblank0', '0'): ('_', 'R', 'markregDblank1'),
            ('markregDblank1', '0'): ('_', 'R', 'markregDblank2'),
            ('markregDblank2', '0'): ('_', 'R', 'markregD'),
            ('markregD', '0'): ('0', 'R', 'markregD'),
            ('markregD', '1'): ('1', 'R', 'markregD'),
            ('markregD', '#'): ('#', 'R', 'markregD'),
            ('markregD', 'A'): ('A', 'R', 'markregD'),
            ('markregD', ':'): (':', 'R', 'markregD'),
            ('markregD', 'B'): ('B', 'R', 'markregD'),
            ('markregD', 'C'): ('C', 'R', 'markregD'),
            ('markregD', 'D'): ('D', 'R', 'markdestreg'),
            
            # Moves to Reg E for marking
            ('markregEblank0', '0'): ('_', 'R', 'markregEblank1'),
            ('markregEblank1', '0'): ('_', 'R', 'markregEblank2'),
            ('markregEblank2', '0'): ('_', 'R', 'markregEblank3'),
            ('markregEblank3', '0'): ('_', 'R', 'markregE'),
            ('markregE', '0'): ('0', 'R', 'markregE'),
            ('markregE', '1'): ('1', 'R', 'markregE'),
            ('markregE', '#'): ('#', 'R', 'markregE'),
            ('markregE', 'A'): ('A', 'R', 'markregE'),
            ('markregE', ':'): (':', 'R', 'markregE'),
            ('markregE', 'B'): ('B', 'R', 'markregE'),
            ('markregE', 'C'): ('C', 'R', 'markregE'),
            ('markregE', 'D'): ('D', 'R', 'markregE'),
            ('markregE', 'E'): ('E', 'R', 'markdestreg'),

            # Marks the destination register
            ('markdestreg', ':'): (':', 'R', 'markdestreg'),
            ('markdestreg', '0'): ('Z', 'R', 'markdestreg'),
            ('markdestreg', '1'): ('Z', 'R', 'markdestreg'),
            ('markdestreg', 'B'): ('B', 'L', 'gotoshamt'),
            ('markdestreg', 'C'): ('C', 'L', 'gotoshamt'),
            ('markdestreg', 'D'): ('D', 'L', 'gotoshamt'),
            ('markdestreg', 'E'): ('E', 'L', 'gotoshamt'),
            ('markdestreg', '#'): ('#', 'L', 'gotoshamt'),
            
            # Goes the the shamt
            ('gotoshamt', 'Z'): ('Z', 'L', 'gotoshamt'),
            ('gotoshamt', ':'): (':', 'L', 'gotoshamt'),
            ('gotoshamt', 'A'): ('A', 'L', 'gotoshamt'),
            ('gotoshamt', 'B'): ('B', 'L', 'gotoshamt'),
            ('gotoshamt', 'C'): ('C', 'L', 'gotoshamt'),
            ('gotoshamt', 'D'): ('D', 'L', 'gotoshamt'),
            ('gotoshamt', 'E'): ('E', 'L', 'gotoshamt'),
            ('gotoshamt', '0'): ('0', 'L', 'gotoshamt'),
            ('gotoshamt', '1'): ('1', 'L', 'gotoshamt'),
            ('gotoshamt', '#'): ('#', 'L', 'gotoshamt'),
            ('gotoshamt', '_'): ('_', 'R', 'shamt0'),

            # Reads the shamt
            ('shamt0', '0'): ('_', 'R', 'shamt1'),
            ('shamt1', '0'): ('_', 'R', 'shamt2'),
            ('shamt2', '0'): ('_', 'R', 'shamt3'),
            ('shamt3', '0'): ('_', 'R', 'shamt4'),
            ('shamt4', '0'): ('_', 'R', 'funct0'),
            
            # Determines the operation
            ('funct0', '0'): ('_', 'R', 'funct1'),
            ('funct1', '0'): ('_', 'R', 'funct2'),
            ('funct2', '0'): ('_', 'R', 'funct3'),
            ('funct3', '0'): ('_', 'R', 'funct4'),
            ('funct4', '0'): ('_', 'R', 'funct5'),
            ('funct4', '1'): ('_', 'R', 'addgotoworkspace0blank0'),
            ('funct5', '1'): ('_', 'R', 'subgotoworkspace0'),
            
            # Start of process of finding the first operand for addition
            ('addgotoworkspace0blank0', '0'): ('_', 'R', 'addgotoworkspace0blank0'),
            ('addgotoworkspace0blank0', '#'): ('#', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', '#'): ('#', 'R', 'addgotoworkspace1'),
            ('addgotoworkspace0', 'A'): ('A', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', ':'): (':', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', 'Z'): ('Z', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', 'B'): ('B', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', 'C'): ('C', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', 'D'): ('D', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', 'E'): ('E', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', '0'): ('0', 'R', 'addgotoworkspace0'),
            ('addgotoworkspace0', '1'): ('1', 'R', 'addgotoworkspace0'),

            # Finds the next bit in the first operand
            ('addgotoworkspace1', '0'): ('X', 'R', 'addgotoworkspace1'),
            ('addgotoworkspace1', '1'): ('Y', 'R', 'addgotoworkspace1'),
            ('addgotoworkspace1', 'X'): ('X', 'R', 'addgotoworkspace1'),
            ('addgotoworkspace1', 'Y'): ('Y', 'R', 'addgotoworkspace1'),
            ('addgotoworkspace1', '#'): ('#', 'L', 'startAdd'),
            ('addgotoworkspace1', '_'): ('_', 'L', 'startAdd'),

            # Starts the Add, goes to finish state if complete
            ('startAdd', 'X'): ('_', 'R', 'add0+unknown0'),
            ('startAdd', 'Y'): ('_', 'R', 'add1+unknown0'),
            ('startAdd', '#'): ('#', 'R', 'Finish'),

            # For 0+ some bit
            ('add0+unknown0', '_'): ('_', 'R', 'add0+unknown0'),
            ('add0+unknown0', '#'): ('#', 'R', 'add0+unknown1'),

            # For 1 + some bit
            ('add1+unknown0', '_'): ('_', 'R', 'add1+unknown0'),
            ('add1+unknown0', '#'): ('#', 'R', 'add1+unknown1'),

            # Helps find the end of the string
            ('add0+unknown1', '1'): ('1', 'R', 'add0+unknown1'),
            ('add0+unknown1', '0'): ('0', 'R', 'add0+unknown1'),
            ('add0+unknown1', '#'): ('_', 'L', 'add0+unknown2'),
            ('add0+unknown1', '_'): ('_', 'L', 'add0+unknown2'),

            # Helps find the end of the string
            ('add1+unknown1', '1'): ('1', 'R', 'add1+unknown1'),
            ('add1+unknown1', '0'): ('0', 'R', 'add1+unknown1'),
            ('add1+unknown1', '#'): ('_', 'L', 'add1+unknown2'),
            ('add1+unknown1', '_'): ('_', 'L', 'add1+unknown2'),
            
            # Detemines if 0+1 or 0+0
            ('add0+unknown2', '_'): ('_', 'L', 'add0+unknown2'),
            ('add0+unknown2', '0'): ('_', 'L', 'add0+0'),
            ('add0+unknown2', '1'): ('_', 'L', 'add0+1'),

            # Determines if 1+0 or 1+1
            ('add1+unknown2', '_'): ('_', 'L', 'add1+unknown2'),
            ('add1+unknown2', '0'): ('_', 'L', 'add0+1'),
            ('add1+unknown2', '1'): ('_', 'L', 'add1+1'),

            # For 0+0
            ('add0+0', '0'): ('0', 'L', 'add0+0'),
            ('add0+0', '1'): ('1', 'L', 'add0+0'),
            ('add0+0', '_'): ('_', 'L', 'add0+0'),
            ('add0+0', 'Y'): ('Y', 'L', 'add0+0'),
            ('add0+0', 'X'): ('X', 'L', 'add0+0'),
            ('add0+0', '#'): ('#', 'L', 'add0+0'),
            ('add0+0', ':'): (':', 'L', 'add0+0'),
            ('add0+0', 'E'): ('E', 'L', 'add0+0'),
            ('add0+0', 'D'): ('D', 'L', 'add0+0'),
            ('add0+0', 'C'): ('C', 'L', 'add0+0'),
            ('add0+0', 'B'): ('B', 'L', 'add0+0'),
            ('add0+0', '+'): ('1', 'L', 'addgotoworkspace0'),
            ('add0+0', 'Z'): ('0', 'L', 'addgotoworkspace0'),

            # For 0+1 or 1+0
            ('add0+1', '0'): ('0', 'L', 'add0+1'),
            ('add0+1', '1'): ('1', 'L', 'add0+1'),
            ('add0+1', '_'): ('_', 'L', 'add0+1'),
            ('add0+1', 'Y'): ('Y', 'L', 'add0+1'),
            ('add0+1', 'X'): ('X', 'L', 'add0+1'),
            ('add0+1', '#'): ('#', 'L', 'add0+1'),
            ('add0+1', ':'): (':', 'L', 'add0+1'),
            ('add0+1', 'E'): ('E', 'L', 'add0+1'),
            ('add0+1', 'D'): ('D', 'L', 'add0+1'),
            ('add0+1', 'C'): ('C', 'L', 'add0+1'),
            ('add0+1', 'B'): ('B', 'L', 'add0+1'),
            ('add0+1', '+'): ('0', 'L', 'movecarry'),
            ('add0+1', 'Z'): ('1', 'L', 'addgotoworkspace0'),

            # For 1+1
            ('add1+1', '0'): ('0', 'L', 'add1+1'),
            ('add1+1', '1'): ('1', 'L', 'add1+1'),
            ('add1+1', '_'): ('_', 'L', 'add1+1'),
            ('add1+1', 'Y'): ('Y', 'L', 'add1+1'),
            ('add1+1', 'X'): ('X', 'L', 'add1+1'),
            ('add1+1', '#'): ('#', 'L', 'add1+1'),
            ('add1+1', ':'): (':', 'L', 'add1+1'),
            ('add1+1', 'E'): ('E', 'L', 'add1+1'),
            ('add1+1', 'D'): ('D', 'L', 'add1+1'),
            ('add1+1', 'C'): ('C', 'L', 'add1+1'),
            ('add1+1', 'B'): ('B', 'L', 'add1+1'),
            ('add1+1', '+'): ('1', 'L', 'movecarry'),
            ('add1+1', 'Z'): ('0', 'L', 'movecarry'),
            
            # Moves the carry but if needed
            ('movecarry', 'Z'): ('+', 'R', 'addgotoworkspace0'),
            ('movecarry', ':'): (':', 'R', 'addgotoworkspace0'),
            
            # Starts the finding of the first bit of the first operand
            ('subgotoworkspace0', '#'): ('#', 'R', 'subgotoworkspace1'),

            # Continues to move to workspace
            ('subgotoworkspace1', 'A'): ('A', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', ':'): (':', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', '0'): ('0', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', '1'): ('1', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', 'Z'): ('Z', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', 'B'): ('B', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', 'C'): ('C', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', 'D'): ('D', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', 'E'): ('E', 'R', 'subgotoworkspace1'),
            ('subgotoworkspace1', '#'): ('#', 'R', 'subgotoworkspace2'),

            # Moves to next bit in first operand
            ('subgotoworkspace2', '0'): ('X', 'R', 'subgotoworkspace2'),
            ('subgotoworkspace2', '1'): ('Y', 'R', 'subgotoworkspace2'),
            ('subgotoworkspace2', 'X'): ('X', 'R', 'subgotoworkspace2'),
            ('subgotoworkspace2', 'Y'): ('Y', 'R', 'subgotoworkspace2'),
            ('subgotoworkspace2', '#'): ('#', 'L', 'startSub'),
            ('subgotoworkspace2', '_'): ('_', 'L', 'startSub'),

            # Starts the subtraction process
            ('startSub', 'X'): ('_', 'R', 'sub0-unknown0'),
            ('startSub', 'Y'): ('_', 'R', 'sub1-unknown0'),
            ('startSub', '#'): ('#', 'R', 'Finish'),

            # For 0- some bit
            ('sub0-unknown0', '_'): ('_', 'R', 'sub0-unknown0'),
            ('sub0-unknown0', '#'): ('#', 'R', 'sub0-unknown1'),
            
            # For 1 - some bit
            ('sub1-unknown0', '_'): ('_', 'R', 'sub1-unknown0'),
            ('sub1-unknown0', '#'): ('#', 'R', 'sub1-unknown1'),

            # Goes right to find first bit second operand
            ('sub0-unknown1', '0'): ('0', 'R', 'sub0-unknown1'),
            ('sub0-unknown1', '1'): ('1', 'R', 'sub0-unknown1'),
            ('sub0-unknown1', '#'): ('#', 'L', 'sub0-unknown2'),
            ('sub0-unknown1', '_'): ('_', 'L', 'sub0-unknown2'),

            # Goes right to find first bit second operand
            ('sub1-unknown1', '0'): ('0', 'R', 'sub1-unknown1'),
            ('sub1-unknown1', '1'): ('1', 'R', 'sub1-unknown1'),
            ('sub1-unknown1', '#'): ('#', 'L', 'sub1-unknown2'),
            ('sub1-unknown1', '_'): ('_', 'L', 'sub1-unknown2'),
            
            # Determines second operand next bit
            ('sub0-unknown2', '_'): ('_', 'L', 'sub0-unknown2'),
            ('sub0-unknown2', '0'): ('_', 'L', 'sub0-0'),
            ('sub0-unknown2', '1'): ('_', 'L', 'sub0-1findborrow1'),
            
            # Determines second operand next bit
            ('sub1-unknown2', '_'): ('_', 'L', 'sub1-unknown2'),
            ('sub1-unknown2', '0'): ('_', 'L', 'sub0-1write1'),
            ('sub1-unknown2', '1'): ('_', 'L', 'sub0-0'),
            
            # For 0-0 and 1-1
            ('sub0-0', '0'): ('0', 'L', 'sub0-0'),
            ('sub0-0', '1'): ('1', 'L', 'sub0-0'),
            ('sub0-0', '#'): ('#', 'L', 'sub0-0'),
            ('sub0-0', 'X'): ('X', 'L', 'sub0-0'),
            ('sub0-0', 'Y'): ('Y', 'L', 'sub0-0'),
            ('sub0-0', ':'): (':', 'L', 'sub0-0'),
            ('sub0-0', 'E'): ('E', 'L', 'sub0-0'),
            ('sub0-0', 'C'): ('C', 'L', 'sub0-0'),
            ('sub0-0', 'D'): ('D', 'L', 'sub0-0'),
            ('sub0-0', 'B'): ('B', 'L', 'sub0-0'),
            ('sub0-0', '_'): ('_', 'L', 'sub0-0'),
            ('sub0-0', 'Z'): ('0', 'R', 'subgotoworkspace1'),

            # Finds the borrow in case of 0-1
            ('sub0-1findborrow1', '0'): ('0', 'L', 'sub0-1findborrow1'),
            ('sub0-1findborrow1', '1'): ('1', 'L', 'sub0-1findborrow1'),
            ('sub0-1findborrow1', '#'): ('#', 'L', 'sub0-1findborrow2'),

            # Inverts bits in first operand for carry
            ('sub0-1findborrow2', '_'): ('_', 'L', 'sub0-1findborrow2'),
            ('sub0-1findborrow2', 'X'): ('Y', 'L', 'sub0-1findborrow2'),
            ('sub0-1findborrow2', 'Y'): ('X', 'L', 'sub0-1write1'),
            ('sub0-1findborrow2', '#'): ('#', 'L', 'sub0-1write1'),

            # Writes 1 to destination 
            ('sub0-1write1', '0'): ('0', 'L', 'sub0-1write1'),
            ('sub0-1write1', '1'): ('1', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'X'): ('X', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'Y'): ('Y', 'L', 'sub0-1write1'),
            ('sub0-1write1', '#'): ('#', 'L', 'sub0-1write1'),
            ('sub0-1write1', ':'): (':', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'E'): ('E', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'D'): ('D', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'C'): ('C', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'B'): ('B', 'L', 'sub0-1write1'),
            ('sub0-1write1', '_'): ('_', 'L', 'sub0-1write1'),
            ('sub0-1write1', 'Z'): ('1', 'R', 'subgotoworkspace1'),

        }
    """Performs a single step of the Turing machine."""
    def step(self):
        if self.head < 0:
            # Extends tape to the left
            self.tape.insert(0, self.blank)
            self.head = 0
        elif self.head >= len(self.tape):
            # Extends tape to the right
            self.tape.append(self.blank)

        symbol = self.tape[self.head]
        key = (self.state, symbol)

        if key not in self.transitions:
            # Halt Condition
            return False

        write_symbol, move, next_state = self.transitions[key]
        self.tape[self.head] = write_symbol
        print(self.state)
        self.state = next_state

        # Moves the head
        if move == 'R':
            self.head += 1
        elif move == 'L':
            self.head -= 1
        else:
            raise ValueError(f"Invalid move: {move}")

        # Adds one to step count
        self.steps += 1
        return True
    
    """Runs the machine until step count reaches 0 or a halt occurs"""
    def run(self, max_steps=100000):
        # Runs while step count less than max_steps, and move is valid
        while self.steps < max_steps and self.step():
            self.print_tape()
            pass
        print(self.state)
        "Checks if the final state was Finish (means string is valid)"
        if self.state == 'Finish':
            self.isValid = 1
        return ''.join(self.tape)
    
    """Prints the tape"""
    def print_tape(self):
        tape_str = ''.join(self.tape)
        head_marker = ' ' * self.head + '^'
        print(tape_str)
        print(head_marker)

    """Converts TM to graph, stored in tm.png"""
    def tm_to_graph(self):
        G = nx.DiGraph()

        for (state, symbol), (write, move, next_state) in self.transitions.items():
            label = f"{symbol}/{write},{move}"
            G.add_edge(state, next_state, label=label)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'label')

        plt.figure(figsize=(60, 60))
        nx.draw(G, pos, with_labels=True, arrows=True, node_size=2500)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.savefig("tm.png", dpi=300)

    """Coverts TM to unrestricted Grammar"""
    def tm_to_unrestricted_grammar(self):
        grammar = []

        grammar.append(f"S -> op0")

        for (state, read), (write, direction, next_state) in self.transitions.items():
            if direction == "R":
                grammar.append(f"{state}{read} -> {write}{next_state}")

            elif direction == "L":
                for c in self.alphabet:
                    grammar.append(f"{c}{state}{read} -> {next_state}{c}{write}")

            else:
                raise ValueError("Direction must be 'L' or 'R'.")


        grammar.append(f"Finish -> λ")

        return grammar

"""Start of program, where user input is collected"""
def main():
    tape = list(input("Input the starting tape (MIPS Intruction + Registers): "))
    #tape = list("00000000001000100000100000000010#A:00111110B:00010101C:11111111D:00000100E:00100000#")
    while True:
        tm = RTypeTM(tape, initial_state='op0', blank='_')

        # Run the machine
        final_tape = tm.run(max_steps=50000)
        clean_final_tape = (final_tape.replace('#', '')).replace('_', '')
        if tm.isValid == 1:
            print("String is valid")
            print(f"Final tape output: {clean_final_tape}")
        else:
            print("String is not valid")
            break

        instruction = input("Input the next instruction to compute on same registers:")
        tape = list(instruction + '#' + clean_final_tape + '#')

    # Used to print the unrestricted grammar of the tm
    #print(tm.tm_to_unrestricted_grammar())

    # Used to create the graph of the turing machine
    #tm.tm_to_graph()  
main()
