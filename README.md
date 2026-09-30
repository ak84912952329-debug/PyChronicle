# PyChronicle: AST-Powered Time-Travel Debugger

PyChronicle is a Python debugging prototype that records program
execution states and allows developers to inspect the execution history.

## 🎯 Project Objective

The main objective of PyChronicle is to make debugging easier by
maintaining a history of program execution.

Instead of checking only the current state of a program, developers
can inspect previously recorded execution states.

## 🏗️ Architecture

```text
Python Source Code
        ↓
   AST Analyzer
        ↓
Execution Tracer
        ↓
 State Recording
        ↓
 History Manager
        ↓
Previous / Next / Jump
