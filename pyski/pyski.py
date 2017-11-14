import sys
import cmd
import types
from inspect import signature

stk = []

# Forth - like stack operators
# the needed arguments are retrieve from the top of the stack (reversed) is passed as arguments
def dup(a):  # ( a -- a a )
    return [a, a]

def drop(s):  # ( a --  )
    return s[1:]

def swap(s):  # ( a b -- b a )
    return s[1] + s[0] + s[2:]

def over(s):  # ( a b -- a b a )
    return s[0:1] + s[0] + s[2:]

def rot(s):  # ( a b c -- b c a )
    return s[1:2] + s[0] + s[3:]

#TODO : unify interface using list of args.
# combinators
# Note how we apply only the immediate composition for B.
def B(x, y, z):
    return x, y(z)

def C(x, y, z):
    return x, z, y

def K(x, y):
    return x

def W(x, y):
    return x, y, y



class StackREPL(cmd.Cmd):
    """
    Design notes. Cmd is based on the usual model of command + params, or function + arguments.
    We want to have a stack based concatenative language, so we need to find the middle ground here...

    Each time the user type return, one computation is effectuated
    First computation is the current input line (command style) if there is one otherwise current stack (last first)
    Any unknown word will be added to the stack and only considered as (unknown symbolic) param, not command.
    """
    intro = 'Welcome to pyski.   Type help or ? to list commands.\n'
    prompt = '[ < '
    file = None

    # defining basic combinators with the host language features
    env = {
        'B': lambda *args: args,
        'C': lambda x, y, z: x(y)(z),
        'K': lambda x: x,
        'W': lambda x: x,
    }



    # interpreter with the host language features
    def evl(self, xpr):
        for c in xpr:
            try:
                yield StackREPL.cmb[c]
            except Exception:
                raise  # TODO : proper handling...

    def push(self, *arg):
        for a in arg:
            stk.append(a)
        # TODO : check for max size

    def pop(self, n=1):
        res = []
        for i in range(n):
            res += stk.pop()
        return res

    def prompt_refresh(self):
        self.prompt = '[ ' + " ".join(stk) + ' < '


    def do_dup(self, arg):
        """duplicates its argument and push it up to the stack.
        Extra arguments are treated before, following stack semantics. This might seem a bit confusing and might be improved by switching prefix/postfix input semantics and repl design
        """
        # for stack semantics on args
        args = stk + arg.split()[::-1]
        #finding number of args of the command
        argsnb = len(signature(dup).parameters)
        # removing them from the stack
        self.pop(argsnb)
        # doing the computation
        newargs = dup(*args[-argsnb:])
        # pushing result onto the stack
        self.push(*newargs)

    def do_drop(self, arg):
        drop(reversed(arg.split())[0])
        self.push(*['drop'] + arg.split())

    def do_swap(self, arg):
        self.stack(*['swap'] + arg.split())
        self.prompt_refresh()

    def do_over(self, arg):
        self.stack(*['over'] + arg.split())
        self.prompt_refresh()

    def do_rot(self, arg):
        self.stack(*['rot'] + arg.split())
        self.prompt_refresh()

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        This method automatically adds the command as undefined word, and recurse on argument (until one known command is found).
        """
        # lets extract the command
        cmd, arg, line = self.parseline(line)
        # an add it to the stack
        self.push(cmd)
        # recurse if string not empty
        if arg: self.onecmd(arg)

    def emptyline(self):
        """
        Called when the input line is empty
        This executes one computation on the existing stack
        :return:
        """
        self.onecmd(" ".join(stk))

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.

        Note this is the reverse as the default cmd implementation : the last word is the command.
        """
        line = line.strip()
        if not line:
            return None, None, line
        elif line[-1] == '?':
            line = line[:-1] + ' help'
        elif line[-1] == '!':
            if hasattr(self, 'do_shell'):
                line = line[:-1] + ' shell'
            else:
                return None, None, line
        i, n = 0, len(line)
        while i < n and line[-i] in self.identchars: i = i + 1
        cmd, arg = line[-i:].strip(), line[:-i]

        return cmd, arg, line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""

        self.prompt_refresh()
        return stop

    # basic REPL commands

    # def do_help(self, arg):
    #    ""

    # def do_shell(self, arg):
    #    ""

    def do_eof(self, arg):
        'Stop recording, close the pyski window, and exit.'
        print('Thank you for using pyski')
        self.close()
        return True

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')

    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    StackREPL().cmdloop()
