"""
A very basic stack based VM. This helps to define simple operational semantics by experimenting.
"""

_stk = ()

# reverse order for extended tuple, for FILO semantics
def stk_get():
    return reversed(_stk)

def stk_set(*n):
    global _stk
    _stk = n[::-1]

# TODO dont we have a comonad here somewhere ??


# Forth - like stack operators
# the needed arguments are retrieve from the top of the stack that is passed as arguments tuple
#
# The API chosen here is for compatibility between clarity in python, stack operational semantics,
# and purity of denotational semantics. The list of arguments is just the existing stack.
def dup(a, *s):  # ( a -- a a )
    """
    DUPlicates the top of the stack
    :param a:
    :param s:
    :return:

    >>> dup(1, 2, 3)
    (1, 1, 2, 3)
    """
    return (a, a) + s


def drop(a, *s):  # ( a --  )
    """
    DROPs the top of the stack
    :param a:
    :param s:
    :return:
    >>> drop(1, 2, 3)
    (2, 3)
    """
    return s


def swap(a, b, *s):  # ( a b -- b a )
    """
    SWAPs the top of the stack with the second most top element
    :param a:
    :param b:
    :param s:
    :return:
    >>> swap(1, 2, 3)
    (2, 1, 3)
    """
    return (b, a) + s


def over(a, b, *s):  # ( a b -- a b a )
    """

    :param a:
    :param b:
    :param s:
    :return:
    """
    return (a, b, a) + s


def rot(a, b, c, *s):  # ( a b c -- b c a )
    """

    :param a:
    :param b:
    :param c:
    :param s:
    :return:
    """
    return (b, c, a) + s


# TODO : given its functional nature, decorator can be used for function composition (concatenation) ?

# TODO : look into kernel as a way to implement quotations (like Cat or Joy)

# TODO : look into cactus/spaghetti stack to implement delimited continuations to allow interpreter reflection and program control

#TODO : since these are pure functions, we should memoize them and detect computation errors. ZAP.
# Idea : use doctest for this... somehow...
# Note : Cat has a similar concept with YAML text

