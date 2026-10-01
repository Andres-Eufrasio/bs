# BS

Quick, easy browser searches from your terminal.

BS lets you search the web, open URLs, or access a local development server without leaving your terminal.

## Usage

```bash
python bs.py [options] search
```

### Search the web

```bash
python bs.py "python argparse tutorial"
```

By default, BS uses Google.

### Choose a search engine

```bash
python bs.py -e duckduckgo "how to tie a tie"
python bs.py -e bing "linux commands"
python bs.py -e brave "c, c# and c sharper"
```

Supported engines:

* `google`
* `bing`
* `brave`
* `duckduckgo`

### Open a URL

Use `-u` to treat the argument as a URL:

```bash
python bs.py -u example.com
```

BS automatically adds `https://` when needed.

### Search localhost

Use `-l` to search a local development server:

```bash
python bs.py -l 3000 "about"
```

This opens:

```text
https://localhost:3000/about
```

### Choose a browser

Pass the path to a browser executable with `-b`:

```bash
python bs.py -b "/path/to/browser" "github"
```

## Options

| Option            | Description                            |
| ----------------- | -------------------------------------- |
| `-e`, `--engine`  | Search engine to use                   |
| `-l`, `--local`   | Search localhost on the specified port |
| `-u`, `--url`     | Treat the search argument as a URL     |
| `-b`, `--browser` | Path to the browser executable         |
| `search`          | Search query or URL                    |

## Requirements

* Python 3
* A web browser

### future funcitonality
At present this is very simple but I will add additonal functionality to easily save settings, config files, add searching from specific sites such as amazon or youtube.