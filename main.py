import math
import operator


from util import parse, to_string


class Env(dict):
    """
    変数の名前空間
    """

    def __init__(self, params=(), args=(), outer=None) -> None:
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        """
        ローカルの名前空間で見つからなければ外側を探索
        """
        return self if var in self else self.outer.find(var)


def add_globals(env: dict) -> dict:
    # mathの関数を一括追加
    env.update(vars(math))
    env.update(
        {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.__truediv__,
            "=": operator.eq,
            "not": operator.not_,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "equal?": operator.eq,
            "eq?": operator.is_,
            "length": len,
            "cons": lambda x, y: [x] + y,
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "append": operator.add,
            "list": lambda *x: list(x),
            "list?": lambda x: isinstance(x, list),
            "null?": lambda x: not x,
            "symbol?": lambda x: isinstance(x, str),
        }
    )
    return env


def eval(x, env):
    """
    構文解析器
    """
    if isinstance(x, str):
        return env.find(x)[x]

    elif not isinstance(x, list):
        return x

    # quoteは解釈せずに出力
    elif x[0] == "quote":
        _, exp = x
        return exp

    # (if test conseq, alt)
    # testを評価してTrueであればconseq, Falseであればalt
    elif x[0] == "if":
        _, test, conseq, alt = x
        return eval((conseq if eval(test, env) else alt), env)

    # (set! var exp)
    # expを評価して結果をvarに代入
    elif x[0] == "set!":
        _, var, exp = x
        env.find(var)[var] = eval(exp, env)

    # (define var exp)
    # 現在の環境でexpの結果をvarに代入
    elif x[0] == "define":
        _, var, exp = x
        env[var] = eval(exp, env)

    # (lambda (var...) exp)
    # 引数var..を取り、式expに代入
    elif x[0] == "lambda":
        _, vars, exp = x
        return lambda *args: eval(exp, Env(vars, args, env))

    # (begin exp...)
    # expを逐次的に評価していく
    elif x[0] == "begin":
        val = None
        for exp in x[1:]:
            val = eval(exp, env)
        return val

    # (proc exp)
    # その他のシンボルは手続き処理として扱う
    else:
        exps = [eval(exp, env) for exp in x]
        proc = exps.pop(0)
        return proc(*exps)


if __name__ == "__main__":
    global_env = add_globals(Env())
    while True:
        val = eval(parse(input()), global_env)
        if val is not None:
            print(to_string(val))
