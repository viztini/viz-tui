import requests
import time
import readchar
from bs4 import BeautifulSoup
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.live import Live

BASE_URL = "https://viztini.github.io/"
ABOUT_URL = "https://viztini.github.io/about.html"
POSTS_URL = "https://viztini.github.io/posts.json"
console = Console()

def fetch_data():
    posts, about = [], {}
    try:
        r = requests.get(POSTS_URL, timeout=10)
        r.raise_for_status()
        raw_posts = r.json()
        raw_posts.sort(key=lambda p: (not p.get("pinned", False), p.get("date", "")), reverse=False)
        for p in raw_posts:
            posts.append({
                "title": p["title"],
                "date": p["date"],
                "content": p["content"],
                "tags": p.get("tags", [])
            })
        ra = requests.get(ABOUT_URL, timeout=10)
        ra.raise_for_status()
        soupa = BeautifulSoup(ra.text, "html.parser")
        terminal_pre = soupa.select_one(".terminal-content pre")
        bio_paragraphs = [p.get_text(strip=True) for p in soupa.select("#tab-general p") if p.get_text(strip=True)]
        about = {
            "terminal": terminal_pre.get_text(strip=True) if terminal_pre else "SYSTEM OFFLINE",
            "text": bio_paragraphs
        }
    except Exception as e:
        posts = [{"title": "Connection Error", "date": "---", "content": str(e), "tags": []}]
        about = {"terminal": "OFFLINE", "text": ["Check your connection."]}
    return posts, about

def boot_sequence():
    boot_msg = Text("""> SYSTEM BOOT...
> LOADING PROTOCOLS...
> CONNECTING TO THE WIRED...
> CONNECTION ESTABLISHED
> WELCOME, USER

"No matter where you go, everyone's connected."

STATUS: ONLINE""", style="bold green")
    console.clear()
    console.print("\n")
    console.print(Align.center(Panel(boot_msg, border_style="green", padding=(1, 5), expand=False)))
    time.sleep(3)

def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="sidebar", size=45),
        Layout(name="content", ratio=1)
    )
    return layout

def main():
    boot_sequence()
    posts, about = fetch_data()
    selected, page = 0, "home"
    layout = make_layout()

    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            nav = Text(" viztini's tech blog ", style="bold black on cyan")
            nav.append("  ")
            nav.append(" [ HOME ] ", style="bold green" if page == "home" else "dim white")
            nav.append(" [ ABOUT ] ", style="bold green" if page == "about" else "dim white")
            layout["header"].update(Align.left(nav))
            layout["footer"].update(Panel(Align.center(Text("[TAB] Toggle View  |  [ARROWS] Navigate  |  [Q] Quit", style="bold green")), border_style="green"))

            if page == "home":
                t_list = Text()
                for i, p in enumerate(posts):
                    style = "reverse" if i == selected else ""
                    t_list.append(f"{p['date']} ", style=f"{style} yellow")
                    t_list.append(f"{p['title']}\n", style=f"{style} white")
                layout["sidebar"].update(Panel(t_list, title="Index", border_style="magenta"))

                curr = posts[selected]
                t_cont = Text()
                t_cont.append(f"{curr['title']}\n", style="bold cyan")
                t_cont.append(f"{curr['date']}\n", style="italic yellow dim")
                t_cont.append("─" * 30 + "\n\n", style="dim")
                t_cont.append(f"{curr['content']}\n\n")
                if curr['tags']:
                    t_cont.append(" ".join(curr['tags']), style="bold magenta")
                layout["content"].update(Panel(t_cont, title="Post Viewer", border_style="green", padding=(1, 2)))
            else:
                layout["sidebar"].update(Panel("SYSTEM PROFILE\n\nIdentity: viztini\nLocation: the wired\nStatus: Online", border_style="magenta"))
                t_about = Text(f"{about['terminal']}\n\n", style="green")
                for p in about['text']:
                    if "> printf" in p or "Hello, World!" in p:
                        t_about.append(p + "\n\n", style="bold green")
                    else:
                        t_about.append(p + "\n\n", style="white")
                layout["content"].update(Panel(t_about, title="User Profile", border_style="green", padding=(1, 2)))

            key = readchar.readkey()
            if key.lower() == "q": 
                break
            elif key == readchar.key.TAB:
                page = "about" if page == "home" else "home"
            if page == "home":
                if key in (readchar.key.DOWN, "j"):
                    selected = min(selected + 1, len(posts) - 1)
                elif key in (readchar.key.UP, "k"):
                    selected = max(selected - 1, 0)

    console.clear()
    exit_msg = Text("\nthank you for visiting viztini's tech blog <3", style="bold magenta")
    console.print(Align.center(exit_msg))
    print("\n")

if __name__ == "__main__":
    main()
