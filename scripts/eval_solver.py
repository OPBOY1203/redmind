#!/usr/bin/env python3
# A Simple infix infix evaluator

import ast
import operator as op
import re
import sys
from math import factorial

_ALLOWED_BINOPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod, ast.Pow: op.pow,
    ast.BitOr: op.or_, ast.BitXor: op.xor, ast.BitAnd: op.and_,
    ast.LShift: op.lshift, ast.RShift: op.rshift,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: op.pos, ast.USub: op.neg, ast.Invert: op.invert,
}

def _eval_ast(node):
    if isinstance(node, ast.Num):  # py<3.8
        return node.n
    if isinstance(node, ast.Constant):  # py3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant")
    if isinstance(node, ast.UnaryOp):
        if type(node.op) in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[type(node.op)](_eval_ast(node.operand))
        raise ValueError("Unsupported unary op")
    if isinstance(node, ast.BinOp):
        if type(node.op) in _ALLOWED_BINOPS:
            left = _eval_ast(node.left)
            right = _eval_ast(node.right)
            return _ALLOWED_BINOPS[type(node.op)](left, right)
        raise ValueError("Unsupported bin op")
    if isinstance(node, ast.Expr):
        return _eval_ast(node.value)
    if isinstance(node, ast.Paren):
        return _eval_ast(node.value)
    raise ValueError("Unsupported expression node")

_fact_pat = re.compile(r'(\d+)!')  # turn "5!" -> "factorial(5)"

def safe_eval_infix(expr: str):
    # Treat caret as XOR, not exponent
    # If challenge truly uses '^' as exponent, change this mapping.
    expr = expr.replace('^', '^')  # no change, just explicit
    # Translate n! into factorial(n)
    expr = _fact_pat.sub(r'factorial(\1)', expr)
    # Prevent names/calls except factorial
    tree = ast.parse(expr, mode='eval')

    def _guard(n):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name) and n.func.id == 'factorial':
                if len(n.args) != 1: raise ValueError("factorial takes 1 arg")
                val = _guard(n.args[0])
                if not isinstance(val, (int, float, ast.Num, ast.Constant)):
                    raise ValueError("factorial arg must be number")
                return ast.copy_location(ast.Num(n= factorial(int(eval(compile(ast.Expression(body=val), '', 'eval'))))), n)
            raise ValueError("Calls not allowed")
        elif isinstance(n, (ast.BinOp, ast.UnaryOp, ast.Expr, ast.Constant, ast.Num, ast.Paren)):
            return n
        elif isinstance(n, ast.Name):
            raise ValueError("Names not allowed")
        elif isinstance(n, ast.Subscript):
            raise ValueError("Subscripts not allowed")
        else:
            # Recurse children generically
            for child in ast.iter_child_nodes(n):
                _guard(child)
            return n

    _guard(tree.body)
    return _eval_ast(tree.body)

# Postfix and Prefix evaluators
_BINOPS = {
    '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
    '//': op.floordiv, '%': op.mod, '**': op.pow,
    '^': op.xor, '&': op.and_, '|': op.or_,
    '<<': op.lshift, '>>': op.rshift
}
_UNARY = {'~': lambda x: ~x}

def try_eval_postfix(tokens):
    stack = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in _UNARY:
            if not stack: raise ValueError("bad postfix")
            stack.append(_UNARY[t](stack.pop()))
        elif t in ('//', '**', '<<', '>>'):  # 2-char ops already tokenized
            b = stack.pop(); a = stack.pop()
            stack.append(_BINOPS[t](a, b))
        elif t in _BINOPS:
            b = stack.pop(); a = stack.pop()
            stack.append(_BINOPS[t](a, b))
        else:
            stack.append(int(t))
        i += 1
    if len(stack) != 1: raise ValueError("bad postfix")
    return stack[0]

def try_eval_prefix(tokens):
    # Reverse-scan stack eval
    stack = []
    for t in reversed(tokens):
        if t in _UNARY:
            if not stack: raise ValueError("bad prefix")
            stack[-1] = _UNARY[t](stack[-1])
        elif t in _BINOPS:
            if len(stack) < 2: raise ValueError("bad prefix")
            a = stack.pop(); b = stack.pop()
            stack.append(_BINOPS[t](a, b))
        else:
            stack.append(int(t))
    if len(stack) != 1: raise ValueError("bad prefix")
    return stack[0]

def tokenize_ops(s: str):
    # keep multi-char ops together
    s = s.replace('**', ' ** ').replace('//', ' // ')
    s = s.replace('<<', ' << ').replace('>>', ' >> ')
    return re.findall(r'\*\*|//|<<|>>|[\+\-\*/%\^\&\|\~]|\-?\d+', s.strip())

# Sequence extrapolation
def next_term_sequence(seq):
    # Try arithmetic / geometric quick checks
    if len(seq) >= 3 and all((seq[i]-seq[i-1]) == (seq[1]-seq[0]) for i in range(2, len(seq))):
        return seq[-1] + (seq[1]-seq[0])
    if len(seq) >= 3 and all(seq[i-1] != 0 for i in range(1, len(seq))):
        r1 = seq[1]/seq[0] if seq[0] != 0 else None
        if r1 is not None and all(abs((seq[i]/seq[i-1]) - r1) < 1e-12 for i in range(2, len(seq)) if seq[i-1] != 0):
            return seq[-1]*r1

    # Finite differences
    diffs = [seq[:]]
    while len(diffs[-1]) > 1:
        last = diffs[-1]
        diffs.append([last[i+1]-last[i] for i in range(len(last)-1)])
        if all(x == diffs[-1][0] for x in diffs[-1]):  # constant row
            break

    # Extrapolate by summing last values up the triangle
    nxt = diffs[-1][0]
    for level in range(len(diffs)-2, -1, -1):
        nxt = diffs[level][-1] + nxt
    return nxt

def parse_sequence_line(line: str):
    # Accept comma/space separated integers
    parts = re.findall(r'-?\d+', line)
    if not parts: raise ValueError("no ints")
    return list(map(int, parts))


# Auto-detect & solve a single line
def solve_line(line: str):
    s = line.strip()

    # Heuristic: iS iT??
    if re.fullmatch(r'[\s,\-\d]+', s) and re.search(r'-?\d', s):
        seq = parse_sequence_line(s)
        return str(int(next_term_sequence(seq)))

    # Otherwise, try postfix/prefix if it looks space-tokenized
    tokens = tokenize_ops(s)
    if tokens and '('.encode() not in s.encode() and ')'.encode() not in s.encode():
        # Try postfix
        try:
            return str(int(try_eval_postfix(tokens)))
        except Exception:
            pass
        # Try prefix
        try:
            return str(int(try_eval_prefix(tokens)))
        except Exception:
            pass

    # Fallback: infix 
    try:
        val = safe_eval_infix(s)
        # Print as int if it's integral
        if isinstance(val, float) and abs(val - round(val)) < 1e-12:
            val = int(round(val))
        return str(val)
    except Exception:
        # Last resort: attempt to coerce any remaining numeric
        nums = re.findall(r'-?\d+', s)
        if len(nums) == 1:
            return nums[0]
        raise

def main():
    data = sys.stdin.read().strip().splitlines()
    for line in data:
        if line.strip() == '':
            continue
        print(solve_line(line))

if __name__ == "__main__":
    main()
    