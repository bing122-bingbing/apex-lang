#!/usr/bin/env python3

import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Apex Language Interpreter")
        print("Usage: python main.py <filename>")
        print("       python main.py -i (interactive mode)")
        sys.exit(1)
    
    if sys.argv[1] == '-i':
        interactive_mode()
    else:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        
        with open(filename, 'r') as f:
            source = f.read()
        
        run_code(source)

def run_code(source: str):
    """Run Apex code"""
    try:
        # Tokenization
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpretation
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except (NameError, TypeError, AttributeError, IndexError, RuntimeError) as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def interactive_mode():
    """Interactive REPL mode"""
    print("Apex Language Interpreter - Interactive Mode")
    print("Type 'exit' to quit")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            source = input("apex> ")
            
            if source.lower() == 'exit':
                break
            
            if not source.strip():
                continue
            
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            result = interpreter.interpret(ast)
            
            if result is not None:
                print(result)
        
        except (SyntaxError, NameError, TypeError, AttributeError, IndexError, RuntimeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break

if __name__ == '__main__':
    main()
