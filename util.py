from typing import Union


def tokenize(s: str) -> list:
    """
    構文のトークン化
    """
    return s.replace("(", " ( ").replace(")", " ) ").split()


def atom(token: str) -> Union[str, int, float]:
    """
    トークンの型を推論
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)


def read_from(tokens: list) -> Union[list, str, int, float]:
    """
    トークンを式単位に分割
    """
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF while reading")

    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from(tokens))
        tokens.pop(0)
        return L

    elif token == ")":
        raise SyntaxError("unexpected)")
    else:
        return atom(token)


def parse(s: str) -> list:
    return read_from(tokenize(s))


def to_string(exp):
    return (
        "(" + "".join(map(to_string, exp)) + ")" if isinstance(exp, list) else str(exp)
    )
