builtins_whitelist = set((
        # exceptions
        'ArithmeticError', 'AssertionError', 'AttributeError', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError',
        'EnvironmentError', 'Exception', 'FloatingPointError','FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
        'ImportWarning', 'IndentationError', 'IndexError', 'KeyError','LookupError', 'MemoryError', 'NameError', 'NotImplemented',
        'NotImplementedError', 'OSError', 'OverflowError','PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
        'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'TabError', 'TypeError',
        'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError','UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning',
        # constants
        'False', 'None', 'True', '__doc__', '__name__', '__package__', 'copyright', 'license', 'credits',
        # types
        'basestring', 'bytearray', 'bytes', 'complex', 'dict', 'float', 'frozenset', 'int', 'list', 'long', 'object', 'set', 'str',
        'tuple', 'unicode',
        # functions
        '__import__', 'abs', 'all', 'any', 'apply', 'bin', 'bool', 'buffer', 'callable', 'chr', 'classmethod', 'cmp', 'coerce',
        'compile', 'delattr', 'dir', 'divmod', 'enumerate', 'filter', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
        'isinstance', 'issubclass', 'iter', 'len', 'locals', 'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'property',
        'range', 'reduce', 'repr', 'reversed', 'round', 'setattr', 'slice', 'sorted', 'staticmethod', 'sum', 'super', 'type', 'unichr',
        'vars', 'xrange', 'zip', 'exec', '__build_class__'
        ))

from ctypes import pythonapi, POINTER, py_object
_get_dict = pythonapi._PyObject_GetDictPtr
_get_dict.restype = POINTER(py_object)
_get_dict.argtypes = [py_object]
del pythonapi, POINTER, py_object
def dictionary_of(ob):
    dptr = _get_dict(ob)
    return dptr.contents.value

def varni_import(__import__, module_whitelist):
    def safe_import(module_name, globals={}, locals={}, fromList=[], level=0):
        if module_name in module_whitelist:
            return __import__(module_name, globals, locals, fromList, level)
        else:
            raise ImportError("Blocked import " + module_name)
    return safe_import

class readOnlyList(dict):
    def popitem(self):
        raise RuntimeError("Popping not allowed!")
    def setdefault(self, key, *defValue):
        raise RuntimeError("Editing not allowed!")
    def pop(self, key, *value):
        raise RuntimeError("Popping not allowed!")
    def update(self, other):
        raise RuntimeError("Editing not allowed")
    def __setitem__(self, key, value):
        raise RuntimeError("Editing not allowed")
    def __setattr__(self, key, value):
        raise RuntimeError("Editing not allowed")
    def clear(self):
        raise RuntimeError("Editing not allowed")

class Sandbox(object):
    def __init__(self):
        builtins = sys.modules["__main__"].__dict__["__builtins__"].__dict__.copy()

        for builtin in builtins.keys():
            if builtin not in builtins_whitelist:
                del sys.modules["__main__"].__dict__["__builtins__"].__dict__[builtin]

        ## builtins so pythonove vgrajene funkcije in __import__ se klice kadar
        ## klicemo "import x", zato ga zej spremenimo v novo varno funkcijo
        module_whitelist = ["math", "string", "re"]
        builtins["__import__"] = varni_import(__import__, module_whitelist)
        safe_builtins = readOnlyList(builtins)

        sys.modules["__main__"].__dict__["__builtins__"] = safe_builtins

    def execute(self, code_string):
        exec(code)

#exec("""print("123")""")
    
code = """
import math
#import stats
print("Hello world!")
#open("test.txt", "r")
x = 1 + 2
print(x)
y = [1,2,3,10,12]
for i in y:
    print(i)

print("Drevo:")
class Node:
    def __init__(self, l, r, v):
        self.left = l
        self.right = r
        self.value = v
    
    def printTree(self):
        print(self.value)
        if not (self.left == None):
            self.left.printTree()
        if not (self.right == None):
            self.right.printTree()

n1 = Node(None, None, 1) 
n2 = Node(None, None, 2)
n3 = Node(None, None, 3)
n4 = Node(None, None, 4)
n5 = Node(n1, n2, 5)
n6 = Node(n4, n3, 6)
n7 = Node(n5, n6, 7)
n7.printTree()
"""

from types import FunctionType
import sys


def foo():
    print("meov")

def evil_function():
    print("EVIL!")

#print(dir(foo))
#print(dir(foo.__code__))
#print(foo.__code__.co_code)
#foo.__code__ = evil_function.__code__
#foo()
#function_dict = dictionary_of(FunctionType)
#del function_dict["__code__"]
#foo.__code__ = evil_function.__code__
#foo()



#print(__builtins__.__dict__.keys())

"""
print([].__class__)
print([].__class__.__bases__[0])
#print([].__class__.__bases__[0].__subclasses__())
"""

"""
obj_class = [].__class__.__bases__[0].__subclasses__()
i = 0
k = 0
for o in obj_class:
    #print(o.__name__)
    if o.__name__ == "Sandbox":
        k = i
    i = i + 1
s1 = obj_class[k]()
print(s1)
"""

print(dir(dict))

s2 = Sandbox()
print(s2)
s2.execute(code)