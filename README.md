# viz-tui

A terminal-based interactive blog viewer built in Python, fetching posts and profile data from my live website. Navigate your favorite tech posts and view user profile info in a retro-futuristic terminal interface.

<p align="center">
  <img src="https://github.com/viztini/viz-tui/blob/main/boot.png" alt="example">
</p>

---

<p align="center">
  <img src="https://github.com/viztini/viz-tui/blob/main/example.png" alt="example2">
</p>

---

## Features

* Fetches blog posts from [my website](https://viztini.github.io/) using `requests` and `BeautifulSoup`.
* Displays posts and user profile in a clean, terminal-friendly layout using [Rich](https://github.com/Textualize/rich).
* Supports interactive navigation:

  * `[TAB]` — Toggle between Home and About pages.
  * `[UP/DOWN]` or `j/k` — Scroll through blog posts.
  * `[Q]` — Quit the application.
* Highlights tags, dates, and important text in different colors for readability.
* Includes a “boot sequence” animation and clean shutdown message.

---

## Requirements

* [Python 3.10+](https://www.python.org/downloads/release/python-3100/)
* [requests](https://pypi.org/project/requests/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
* [rich](https://pypi.org/project/rich/)
* [readchar](https://pypi.org/project/readchar/)

Install dependencies via pip:

```bash
pip install requests beautifulsoup4 rich readchar
```

---

## Installation & Usage

1. Clone or download this repository:

```bash
git clone https://github.com/viztini/viz-tui.git
cd viz-tui
```

2. Run the application:

```bash
python main.py
```

3. Use the interactive controls to navigate posts and view the About page.

---

## Navigation Controls

| Key       | Action                      |
| --------- | --------------------------- |
| `TAB`     | Toggle between Home / About |
| `UP/DOWN` | Navigate posts              |
| `j/k`     | Navigate posts (vim-style)  |
| `Q`       | Quit the application        |

---

## Project Structure

```
blog.py          # Main application script
```

* `fetch_data()` — Retrieves posts and about info from the website.
* `boot_sequence()` — Displays boot animation.
* `make_layout()` — Sets up the Rich terminal layout.
* `main()` — Handles interactive loop, rendering, and navigation.

---

## Notes

* Works best on terminals with 80+ columns for proper layout display.
* If the website is unreachable, the application shows an offline message in place of posts and profile.

---

## License

This project is licensed with the MIT License

---
