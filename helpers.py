from datetime import datetime
import builtins


# noinspection PyShadowingBuiltins
def print(*args):
    print_string = "[" + datetime.now().strftime('%H:%M:%S.%f') + "] " + " ".join(map(str, args))
    builtins.print(print_string)

