import re
import requests
from config import GEMINI_API_KEY

# Comprehensive list of Python-related keywords
PYTHON_KEYWORDS = [
    # Core Python
    'python', 'variable', 'data type', 'operator', 'conditional', 'if', 'else', 'elif',
    'loop', 'while', 'for', 'break', 'continue', 'function', 'input', 'output',
    'print', 'type casting', 'int', 'str', 'float', 'bool', 'list', 'tuple',
    'set', 'dictionary', 'dict', 'array', 'stack', 'queue', 'linked list',
    'tree', 'graph', 'hash table', 'collection', 'sequence', 'mutable', 'immutable',
    
    # Programming concepts
    'class', 'object', 'instance', 'inheritance', 'polymorphism', 'encapsulation',
    'abstraction', 'method', 'attribute', 'property', 'static method', 'class method',
    'constructor', '__init__', 'self', 'super', 'abstract class', 'interface',
    'decorator', 'generator', 'iterator', 'context manager', 'descriptor',
    'metaclass', 'comprehension', 'async', 'await', 'coroutine',
    'multithreading', 'multiprocessing', 'gil', 'memory management',
    
    # Libraries and frameworks
    'django', 'flask', 'fastapi', 'pyramid', 'web2py', 'pandas', 'numpy',
    'matplotlib', 'seaborn', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
    'tkinter', 'PyQt', 'wxPython', 'kivy', 'pygame', 'SQLAlchemy', 'pymongo',
    'requests', 'beautiful soup', 'scrapy', 'pillow', 'opencv', 'scipy',
    
    # File and system operations
    'file', 'open', 'read', 'write', 'append', 'close', 'with', 'csv', 'json',
    'txt', 'binary file', 'text file', 'file pointer', 'seek', 'tell', 'flush',
    'os', 'sys', 'subprocess', 'threading', 'multiprocessing', 'file system',
    
    # Other technical terms
    'algorithm', 'sorting', 'searching', 'recursion', 'big o', 'complexity',
    'api', 'rest', 'http', 'websocket', 'middleware', 'orm', 'template',
    'route', 'view', 'model', 'database', 'sql', 'sqlite', 'postgresql',
    'mysql', 'mongodb', 'neural network', 'deep learning', 'machine learning',
    'regression', 'classification', 'clustering', 'model training', 'prediction',
    'testing', 'unittest', 'pytest', 'doctest', 'mock', 'debugging',
    'test cases', 'assertions', 'tdd', 'coverage', 'integration testing',
    'unit testing', 'security', 'cryptography', 'hashing', 'encryption',
    'ssl/tls', 'authentication', 'authorization'
]

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def is_python_question(text: str) -> bool:
    """
    Determine if the input text is a Python-related question using a two-step approach:
    1. First check against a comprehensive list of Python keywords
    2. If unsure, use Gemini API for final verification
    """
    text_low = text.lower()
    
    # Step 1: Check against our comprehensive keyword list
    if any(re.search(rf'\b{re.escape(kw)}\b', text_low) for kw in PYTHON_KEYWORDS):
        return True
    
    # Step 2: If no clear Python keywords found, use Gemini for verification
    try:
        resp = requests.post(
            GEMINI_URL,
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "Respond with only 'yes' or 'no'. "
                                    "Is the following question specifically about Python programming language?\n"
                                    f"Question: {text}\n"
                                    "Consider it Python-related only if it explicitly mentions Python, "
                                    "its syntax, libraries, or frameworks. "
                                    "General programming questions without Python context should be 'no'."
                                )
                            }
                        ]
                    }
                ],
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 1
                }
            }
        )
        resp.raise_for_status()
        content = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip().lower()
        return content == "yes"
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return False