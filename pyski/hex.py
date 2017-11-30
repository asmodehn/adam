import curses
from curses import wrapper
import asyncio

"""
Using the wrapper function is much cleaner, as you can see. From now on, we'll
just modify what's inside the function `main`, and assume we have the import and
the wrapper set up as above.
Now we can learn how to handle user input.

When the user presses a key, we want to be able to handle that action. The first
step in doing so is discovering which key was pressed. The function `getch` does
this for us. It returns a value that we can compare like so:
c = stdscr.getch()
c == ord('a') # Do this to check for a letter key
c == curses.KEY_UP # Do this to check for special keys
See https://docs.python.org/3.5/library/curses.html#constants for all special
key values.
"""

"""
What's stdscr.addstr? That's curses' way of printing. Later, we'll see that it
can also take arguments like y and x positions, which tell it where to print
the string on the terminal. For now, it just prints wherever the cursor is.
It's important to note that stdscr.clear, which is called in the block above,
not only clears the terminal, but also moves the cursor back to the top left.

You may have noticed that the program waits at stdscr.getch for the user to
press a key. We call this behavior "blocking", and would say that stdscr.getch
blocks the flow of the program. For some programs, this is useful. For others,
often in the case of games, this is not the desired behavior. Thankfully, curses
allows non-blocking key input as well.
"""

def drawbar(stdscr, line, direction, count, width):
    try:
        # Draw a springy bar
        stdscr.addstr(0, 0, "#" * count)
        count += direction
        if count == width:
            direction = -1
        elif count == 0:
            direction = 1
        return direction, count
    except asyncio.CancelledError:
        print("draw cancelled. this can happen if the terminal HW access is slow...")

def drawprompt(stdscr, line, str):
    return

def print_raw(stdscr, str):
    stdscr.addstr(str)


async def parseinput(stdscr, input):
    # tokenize
    tkns = input.split(' ')
    # build AST
    return tkns

async def printWT(stdscr, wordlist):
    stdscr.addstr(' '.join(wordlist))


async def interpWT(stdscr, wordlist):
    return


async def parsestk(stdscr, stk):
    # return current stack
    return []


def update_loop(el, stdscr):
    c = None
    width = curses.COLS
    direction = 1
    count = 0
    while c != ord('q'):  # use q for quit
        # TODO : special Ctrl-D for EOF ?? or some ASCII or UTF code ? we want a terminal|IRC feeling...
        now = el.time()

        c = stdscr.getch()
        # manage control commands
        # TODO

        # get user input
        input = stdscr.getstr()

        # Clear out anything else the user has typed in
        curses.flushinp()

        if input:
            # parse it
            #parse_task= asyncio.ensure_future(parseinput(stdscr=stdscr, input=input))

            # draw it immediately
            print_raw(input)

        # schedule complex stuff for later

        # anyway move the bar...
        #draw_task = asyncio.ensure_future(drawbar(stdscr=stdscr,line=3, direction=direction, count=count, width=width))

        # cleaning the window completely for simple dynamic display
        stdscr.clear()

        drawbar(stdscr=stdscr, line=3, direction=direction, count=count, width=width)


        # wait until 1/30 of a second has passed (trying to keep constant 30 fps as much as possible, even under load)
        await asyncio.sleep(0.03 - loop.time() + now)

        #if draw_task.done():
        #    direction, count = draw_task.result()  # will raise exception if there is any.
        #else:
        #    # cancel if we still have a drawing pending...
        #    draw_task.cancel()

        # refresh screen
        stdscr.refresh()

    else:
        return 0  # normal exit


def main(stdscr):
    import logging
    import warnings

    # Make stdscr.getch non-blocking
    stdscr.nodelay(True)
    stdscr.clear()

    event_loop = asyncio.get_event_loop()

    #for debug
    event_loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)
    warnings.filterwarnings("default", message='', category=Warning, module='', lineno=0, append=False)

    # schedule main task :
    event_loop.call_soon(update_loop(el=event_loop, stdscr=stdscr))

    try:
        return_value = event_loop.run_forever()
        print('return value: {!r}'.format(return_value))
    finally:
        event_loop.run_until_complete(event_loop.shutdown_asyncgens())
        event_loop.close()








"""
Calling stdscr.nodelay(True) made stdscr.getch() non-blocking. If Python gets to
that line and the user hasn't typed anything since last time, getch will return
-1, which doesn't match any key.

What if the user managed to type more than one character since the last time
getch was called? All of those characters will start to build up, and getch will
return the value for each one in the order that they came. This can cause
delayed reactions if you're writing a game. After getch, you can call
curses.flushinp to clear out the rest of the characters that the user typed.

This is a good place to talk more about getch.

Every time the user presses a key, that key's value gets stored in a list. When
getch is called, it goes to that list and pops that value. If the user manages
to press several keys before getch is called, getch will pop the least recently
added value (the oldest key pressed). The rest of the keys remain in the list!
The process continues like this. So there's a problem if there is a delay
between calls to getch: Key values can build up. If you don't want this to
happen, curses.flushinp() clears the list of inputted values. This ensures that
the next key the user presses after curses.flushinp() is what getch will return
next time it is called.
"""

"""
To continue learning about curses, checkout the addstr method to see how you can
print strings at certain y, x coordinates. You can start here:
https://docs.python.org/3/library/curses.html#window-objects
"""


# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)
