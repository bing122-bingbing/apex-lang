import re
from typing import List, Optional, Dict, Set
from lexer import Lexer, TokenType

class Autocomplete:
    """Intelligent auto-complete engine for Apex"""
    
    KEYWORDS = [
        'class', 'interface', 'trait', 'enum', 'struct',
        'def', 'async', 'await', 'match', 'case',
        'try', 'catch', 'finally', 'throw',
        'if', 'else', 'elif', 'while', 'do', 'for', 'in',
        'break', 'continue', 'return',
        'new', 'this', 'super', 'extends', 'implements',
        'var', 'immutable', 'static', 'private', 'public', 'protected', 'abstract', 'final',
        'lambda',
        'true', 'false', 'null',
        'and', 'or', 'not', 'xor',
    ]
    
    TYPES = [
        'int', 'float', 'string', 'bool', 'list', 'dict', 'set', 'tuple',
        'void', 'any', 'optional'
    ]
    
    BUILTINS = [
        'print', 'len', 'int', 'float', 'string', 'bool', 'list', 'dict',
        'range', 'map', 'filter', 'reduce', 'zip', 'enumerate',
        'typeof', 'instanceof', 'keys', 'values', 'items', 'push', 'pop', 'shift', 'unshift'
    ]
    
    SNIPPETS = {
        'class': 'class ${1:ClassName} {\n    ${2:// body}\n}',
        'def': 'def ${1:functionName}(${2:params}) -> ${3:type} {\n    ${4:// body}\n}',
        'if': 'if (${1:condition}) {\n    ${2:// body}\n}',
        'for': 'for ${1:item} in ${2:iterable} {\n    ${3:// body}\n}',
        'while': 'while (${1:condition}) {\n    ${2:// body}\n}',
        'try': 'try {\n    ${1:// body}\n} catch (${2:exception}) {\n    ${3:// handle}\n}',
        'lambda': 'lambda ${1:x} => ${2:x}',
    }
    
    def __init__(self):
        self.user_variables: Set[str] = set()
        self.user_functions: Set[str] = set()
        self.user_classes: Set[str] = set()
    
    def get_completions(self, text: str, context: Optional[Dict] = None) -> List[Dict]:
        """
        Get auto-complete suggestions based on partial input
        Returns list of dicts with 'text', 'type', 'description'
        """
        if not text:
            return []
        
        completions = []
        
        # Extract the word being completed
        word_match = re.search(r'\w+$', text)
        if not word_match:
            return completions
        
        partial = word_match.group()
        
        # Keywords
        for keyword in self.KEYWORDS:
            if keyword.startswith(partial):
                completions.append({
                    'text': keyword,
                    'type': 'keyword',
                    'description': f'Keyword: {keyword}',
                    'snippet': self.SNIPPETS.get(keyword)
                })
        
        # Types
        for type_name in self.TYPES:
            if type_name.startswith(partial):
                completions.append({
                    'text': type_name,
                    'type': 'type',
                    'description': f'Type: {type_name}'
                })
        
        # Built-in functions
        for builtin in self.BUILTINS:
            if builtin.startswith(partial):
                completions.append({
                    'text': builtin,
                    'type': 'function',
                    'description': f'Built-in function: {builtin}()'
                })
        
        # User-defined
        for var in self.user_variables:
            if var.startswith(partial):
                completions.append({
                    'text': var,
                    'type': 'variable',
                    'description': f'Variable: {var}'
                })
        
        for func in self.user_functions:
            if func.startswith(partial):
                completions.append({
                    'text': func,
                    'type': 'function',
                    'description': f'Function: {func}()'
                })
        
        for cls in self.user_classes:
            if cls.startswith(partial):
                completions.append({
                    'text': cls,
                    'type': 'class',
                    'description': f'Class: {cls}'
                })
        
        # Sort by relevance
        completions.sort(key=lambda x: (len(x['text']), x['text']))
        
        return completions[:15]  # Limit to 15 suggestions
    
    def get_signature_help(self, func_name: str) -> Optional[str]:
        """Get function signature help"""
        signatures = {
            'print': 'print(...args: any) -> void',
            'len': 'len(obj: any) -> int',
            'map': 'map(func: lambda, iterable: list) -> list',
            'filter': 'filter(func: lambda, iterable: list) -> list',
            'range': 'range(start: int, end: int, step?: int) -> list',
        }
        return signatures.get(func_name)
    
    def extract_symbols(self, source: str) -> None:
        """Extract variables, functions, and classes from source"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            i = 0
            while i < len(tokens):
                token = tokens[i]
                
                # Classes
                if token.type == TokenType.CLASS and i + 1 < len(tokens):
                    if tokens[i + 1].type == TokenType.IDENTIFIER:
                        self.user_classes.add(tokens[i + 1].value)
                        i += 2
                        continue
                
                # Functions
                if token.type == TokenType.DEF and i + 1 < len(tokens):
                    if tokens[i + 1].type == TokenType.IDENTIFIER:
                        self.user_functions.add(tokens[i + 1].value)
                        i += 2
                        continue
                
                # Variables
                if token.type == TokenType.VAR and i + 1 < len(tokens):
                    if tokens[i + 1].type == TokenType.IDENTIFIER:
                        self.user_variables.add(tokens[i + 1].value)
                        i += 2
                        continue
                
                i += 1
        except:
            pass  # Silently fail on incomplete code
    
    def format_completions(self, completions: List[Dict]) -> str:
        """Format completions for display in terminal"""
        if not completions:
            return "No suggestions"
        
        lines = ["\n🔍 Auto-complete suggestions:\n"]
        
        for i, comp in enumerate(completions, 1):
            type_icon = {
                'keyword': '🔑',
                'type': '📦',
                'function': '⚙️',
                'variable': '📝',
                'class': '🏗️',
            }.get(comp['type'], '•')
            
            lines.append(f"  {i}. {type_icon}  {comp['text']:<20} {comp['description']}")
        
        return '\n'.join(lines)
