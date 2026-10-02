import argparse
import json
import webbrowser
from urllib.parse import quote

import tomllib as tom

parser = argparse.ArgumentParser(description="Easy search from your terminal")


with open("./bsconfig.toml", "rb") as f:
    default_args = tom.load(f)

parser.add_argument(
    "search",
    help="Search query or URL",
)

parser.add_argument(
    "-l",
    "--local",
    default=default_args.get("local", None),
    help="Search localhost on the specified port\n use / for empty search",
)

parser.add_argument(
    "-e",
    "--engine",
    default=default_args.get("engine", "google"),
    help="Select a search engine",
    type=str.lower,
)

parser.add_argument(
    "-b",
    "--browser",
    default=default_args.get("browser"),
    help="Select the browser to use - must be PATH to executable",
)

parser.add_argument(
    "-s",
    "--secure_off",
    help="use http",
    default=default_args.get("secure_off", False),
    action="store_true",
)

parser.add_argument(
    "-u",
    "--url",
    action="store_true",
    help="Treat the search argument as a URL",
)


args = parser.parse_args()


class Search:
    def __init__(self, args):
        self.args = args
        self.search_string = ""
        self.build_search()

    def build_search(self):
        if self.args.url:
            self.search_string = self.args.search

            if not self.search_string.startswith(
                (
                    "http://",
                    "https://",
                    "ftp://",
                    "ftps://",
                    "ws://",
                    "wss://",
                )
            ):
                self.search_string = f"{self.check_secure()}://{self.search_string}"

            return

        # Localhost search
        if self.args.local:
            if self.args.search == "/":
                self.search_string = (
                    f"{self.check_secure()}://localhost:{quote(self.args.local)}"
                )
            else:
                self.search_string = (
                    f"{self.check_secure()}://localhost:{self.args.local}/"
                    f"{quote(self.args.search)}"
                )
            return

        # Search engine
        with open("./resources/engines.json", "r") as engines_json:
            engines = json.load(engines_json)

        engine_url = engines[self.args.engine]

        self.search_string = engine_url + quote(self.args.search)

    def search(self):
        if self.args.browser:
            browser = webbrowser.get(self.args.browser)
            browser.open(self.search_string)
        else:
            webbrowser.open(self.search_string)

    # rename this to something better when I think of it
    def check_secure(self) -> str:
        return "http" if self.args.secure_off else "https"







if __name__ == "__main__":
    start = Search(args)
    start.search()
