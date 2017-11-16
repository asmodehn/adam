import sys
import cmd
import types
from inspect import signature

from svm import stk_set, stk_get, dup, drop, swap, over, rot

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

    def prompt_refresh(self):
        # note : we need the reversed stack for a left prompt
        self.prompt = '[ ' + " ".join(reversed(tuple(stk_get()))) + ' < '

    def do_dup(self, arg):
        """duplicates its argument and push it up to the stack.
        Extra arguments are treated before, following stack semantics.
        This might seem a bit confusing and might be improved by switching prefix/postfix input semantics and repl design...
        """
        stk_set(*dup(*stk_get()))

    def do_drop(self, arg):
        stk_set(*drop(*stk_get()))

    def do_swap(self, arg):
        stk_set(*swap(*stk_get()))

    def do_over(self, arg):
        stk_set(*over(*stk_get()))

    def do_rot(self, arg):
        stk_set(*rot(*stk_get()))

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        This method automatically adds the command as undefined word, and recurse on argument (until one known command is found).
        """
        # lets extract the command
        cmd, arg, line = self.parseline(line)
        # an add it to the stack (PUSH)
        stk_set(cmd, *stk_get())

    def emptyline(self):
        """
        Called when the input line is empty
        This executes one computation on the existing stack
        :return:
        """
        self.onecmd(" ".join(stk_get()))

    # def parseline(self, line):
    #     """Parse the line into a command name and a string containing
    #     the arguments.  Returns a tuple containing (command, args, line).
    #     'command' and 'args' may be None if the line couldn't be parsed.
    #
    #     Note this is the reverse as the default cmd implementation : the last word is the command.
    #     """
    #     line = line.strip()
    #     if not line:
    #         return None, None, line
    #     elif line[-1] == '?':
    #         line = line[:-1] + ' help'
    #     elif line[-1] == '!':
    #         if hasattr(self, 'do_shell'):
    #             line = line[:-1] + ' shell'
    #         else:
    #             return None, None, line
    #     i, n = 0, len(line)
    #     while i < n and line[-i] in self.identchars: i = i + 1
    #     cmd, arg = line[-i:].strip(), line[:-i]
    #
    #     return cmd, arg, line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        cmd, arg, line = self.parseline(line)
        if arg:  # keep rest of the line in cmdqueue, and execute it in cmdloop.
            self.cmdqueue.append(arg)
        # update prompt
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
