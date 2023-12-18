import requests
from curses import *

board = ""

# Fixes the shitty html and gives it in a nice readable format.
def clean_up_comments(comment) -> str:
    n = comment.replace("<br>","\n").replace("&#039;t", "'").replace("&#039;d", "'").replace("&gt;", ">").replace("&#039;m", "'").replace('<span class="quote">', ">").replace("</span>", "").replace("<s>","~~").replace("</s>", "~~").replace("&#039;", "'").replace("&quot;", "\"")
    return n

## Request data for the threads
h = {'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT'}

def main():
    # start up curses
    stdscr = initscr()

    ## Step 1: ask the user for the board they want
    stdscr.addstr("What board do you want? ")

    c = 0
    global board
    while c != 10:
       c = stdscr.getch()
       board += chr(c)


    # We have the board now :)
    stdscr.erase() # clear window
    stdscr.refresh()
    # Request threads
    board = board.replace("\n", "")

    
    r = requests.get(f"https://a.4cdn.org/{board}/threads.json", headers=h)
    _r = r.json() # first page
    threads = _r[0]['threads']

    thread_no = 0
    running = True
    while running:
        stdscr.addstr(f"<{thread_no}/{len(threads)}>\n")

        thread_id = threads[thread_no]['no']
        stdscr.addstr(f"Thread id: {thread_id}\n")

        # Get info about the thread
        new_r = requests.get(f"https://a.4cdn.org/{board}/thread/{thread_id}.json",
                               headers=h)

        __r = new_r.json()
        posts = __r['posts']

        # Print OP's post. Then ask to go to the next post or view replies
        name = posts[0]['name']
        date = posts[0]['now']
        fixed_content = clean_up_comments(posts[0]['com'])
        stdscr.addstr(f"{name} {date}\n")
        try:
            stdscr.addstr(f"{fixed_content}\n\n")
        except: pass

        stdscr.addstr("View replies (V), exit (E) or next (N)/ prev (P) post?") 
        c = stdscr.getch()
        if c == 101: running = False
        elif c == 112:
            if thread_no != 0: thread_no -= 1
            stdscr.erase()
            stdscr.refresh()
        elif c == 110:
            thread_no += 1
            stdscr.erase()
            stdscr.refresh()
    endwin()

if __name__ == "__main__":
    main()
