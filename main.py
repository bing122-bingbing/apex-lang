#!/usr/bin/env python3

import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from error_handler import ErrorHandler, ApexException, SyntaxException, RuntimeException
from autocomplete import Autocomplete
import readline

def main():
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("  Apex Language Interpreter (Advanced Edition)")
        print("="*60)
        print("\nUsage: python main.py <filename>")
        print("       python main.py -i (interactive mode)\n")
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
        
        run_code(source, filename)

def run_code(source: str, filename: str = "<stdin>"):
    """Run Apex code with comprehensive error handling"""
    error_handler = ErrorHandler()
    
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
        exc = SyntaxException(
            message=str(e),
            suggestion="Check syntax carefully. Common mistakes: missing semicolon, unclosed bracket."
        )
        error_handler.handle_error(exc)
    except ApexException as e:
        error_handler.handle_error(e)
    except (NameError, TypeError, AttributeError, IndexError, RuntimeError) as e:
        exc = RuntimeException(message=str(e))
        error_handler.handle_error(exc)
    except Exception as e:
        error_handler.handle_exception(e)

def interactive_mode():
    """Interactive REPL mode with auto-complete and error handling"""
    print("\n" + "="*60)
    print("  Apex Language Interpreter - Interactive Mode")
    print("="*60)
    print("\nCommands:")
    print("  exit          - Quit interpreter")
    print("  help          - Show help")
    print("  clear         - Clear screen")
    print("  symbols       - Show defined symbols")
    print("  history       - Show command history\n")
    
    interpreter = Interpreter()
    error_handler = ErrorHandler()
    autocomplete = Autocomplete()
    command_history = []
    
    # Configure readline for better auto-complete
    readline.set_completer(lambda text, state: completer(text, state, autocomplete))
    readline.parse_and_bind("tab: complete")
    
    while True:
        try:
            source = input("\n⚡ apex> ").strip()
            
            if not source:
                continue
            
            command_history.append(source)
            
            # Handle special commands
            if source.lower() == 'exit':
                print("\n👋 Goodbye!\n")
                break
            elif source.lower() == 'help':
                show_help()
                continue
            elif source.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                continue
            elif source.lower() == 'symbols':
                show_symbols(autocomplete)
                continue
            elif source.lower() == 'history':
                show_history(command_history)
                continue
            elif source.lower().startswith('?'):
                # Auto-complete help
                partial = source[1:].strip()
                completions = autocomplete.get_completions(partial)
                print(autocomplete.format_completions(completions))
                continue
            
            # Extract symbols for auto-complete
            autocomplete.extract_symbols(source)
            
            # Run code
            try:
                lexer = Lexer(source)
                tokens = lexer.tokenize()
                
                parser = Parser(tokens)
                ast = parser.parse()
                
                result = interpreter.interpret(ast)
                
                if result is not None:
                    print(f"\n📤 Result: {result}")
            
            except SyntaxError as e:
                exc = SyntaxException(
                    message=str(e),
                    suggestion=error_handler.suggest_keyword(source.split()[0] if source.split() else '')
                )
                error_handler.handle_error(exc)
            except ApexException as e:
                error_handler.handle_error(e)
            except (NameError, TypeError, AttributeError, IndexError, RuntimeError) as e:
                exc = RuntimeException(message=str(e))
                error_handler.handle_error(exc)
            except Exception as e:
                error_handler.handle_exception(e)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            continue
        except EOFError:
            print("\n\n👋 Goodbye!\n")
            break

def completer(text, state, autocomplete):
    """Tab completion function for readline"""
    completions = autocomplete.get_completions(text)
    if state < len(completions):
        return completions[state]['text']
    return None

def show_help():
    """Display help information"""
    help_text = """
    ╔════════════════════════════════════════════════════════════╗
    ║          Apex Language - Interactive Mode Help             ║
    ╚════════════════════════════════════════════════════════════╝
    
    SYNTAX:
      • var name: type = value;     - Variable declaration
      • def func(param: type) -> type { ... }  - Function definition
      • class ClassName { ... }     - Class definition
      • if (condition) { ... }      - Conditional
      • while (condition) { ... }   - Loop
      • for item in list { ... }    - Iterator
    
    TYPES:
      • int, float, string, bool    - Primitive types
      • list, dict, set, tuple      - Collection types
      • any, void, optional         - Special types
    
    AUTO-COMPLETE:
      • Press TAB to auto-complete
      • Type '? keyword' to see suggestions
    
    SPECIAL COMMANDS:
      • exit              - Exit interpreter
      • help              - Show this help
      • clear             - Clear screen
      • symbols           - Show defined symbols
      • history           - Show command history
    
    EXAMPLES:
      var x: int = 42;
      print(x);
      
      def greet(name: string) -> void {
          print("Hello, ");
          print(name);
      }
    """
    print(help_text)

def show_symbols(autocomplete):
    """Show defined symbols"""
    print("\n📊 Defined Symbols:\n")
    
    if autocomplete.user_variables:
        print(f"  Variables: {', '.join(sorted(autocomplete.user_variables))}")
    else:
        print("  Variables: (none)")
    
    if autocomplete.user_functions:
        print(f"  Functions: {', '.join(sorted(autocomplete.user_functions))}")
    else:
        print("  Functions: (none)")
    
    if autocomplete.user_classes:
        print(f"  Classes: {', '.join(sorted(autocomplete.user_classes))}")
    else:
        print("  Classes: (none)")
    print()

def show_history(history):
    """Show command history"""
    print("\n📜 Command History:\n")
    for i, cmd in enumerate(history[-20:], 1):
        print(f"  {i:2}. {cmd}")
    print()

if __name__ == '__main__':
    main()
