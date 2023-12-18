def clean_up_comments(comment) -> str:
    n = comment.replace("<br>","\n").replace("&#039;t", "'").replace("&#039;d", "'").replace("&gt;", ">").replace("&#039;m", "'").replace('<span class="quote">', ">").replace("</span>", "").replace("<s>","~~").replace("</s>", "~~").replace("&#039;", "'").replace("&quot;", "\"")
    return n

def clear_scr(stdscr):
    stdscr.erase()
    stdscr.refresh()
