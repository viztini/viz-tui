import requests
import time
import readchar
import os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.live import Live

BASE_URL = "https://viztini.github.io/"
ABOUT_URL = "https://viztini.github.io/about.html"
console = Console()

def fetch_data():
    posts, about = [], {}
    try:
        r = requests.get(BASE_URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for post in soup.select("article.blog-post"):
            raw_tags = [t.get_text(strip=True) for t in post.select(".tag")]
            clean_tags = [tag if tag.startswith("#") else f"#{tag}" for tag in raw_tags]
            
            posts.append({
                "title": post.select_one(".post-header h3").get_text(strip=True),
                "date": post.select_one(".post-date").get_text(strip=True),
                "content": post.select_one(".post-content").get_text("\n", strip=True),
                "tags": clean_tags
            })
        
        ra = requests.get(ABOUT_URL, timeout=10)
        soupa = BeautifulSoup(ra.text, "html.parser")
        about = {
            "terminal": soupa.select_one(".terminal-content pre").get_text(strip=True),
            "text": [p.get_text(strip=True) for p in soupa.select(".content-box .text-content p")]
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
            # --- Header / Nav Bar ---
            nav = Text(" viztini's tech blog ", style="bold black on cyan")
            nav.append("  ")
            nav.append(" [ HOME ] ", style="bold green" if page == "home" else "dim white")
            nav.append(" [ ABOUT ] ", style="bold green" if page == "about" else "dim white")
            layout["header"].update(Align.left(nav))

            # --- Footer ---
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

    # --- Shutdown Sequence ---
    console.clear()
    exit_msg = Text("\nthank you for visiting viztini's tech blog <3", style="bold magenta")
    console.print(Align.center(exit_msg))
    print("\n")

if __name__ == "__main__":
    main()
