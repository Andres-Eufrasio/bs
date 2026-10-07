import argparse
import json
import os
import sys
import webbrowser
from urllib.parse import quote

import tomli_w as tomw
import tomllib as tom


""" TODO
Make it so engine can be both positional and flag based
Have auto browser searching for non listed browsers, and auto add them to the list if found
"""

if os.name == "nt": 
    appdata_path = os.environ['APPDATA']
    folder_path = appdata_path + r"/bs"
if os.name == "posix":
    config_path = r"~/.config/nvim"
    folder_path = appdata_path + r"/bs"
else:
    print(f"operating system {os.name} not supported")
    sys.exit(1)

parser = argparse.ArgumentParser(description="Easy search from your terminal")
subparser = parser.add_subparsers(dest = "cmd", help="Subcommad help")


try:
    with open(folder_path+"/bsconfig.toml", "rb") as f:
        default_args = tom.load(f)
except FileNotFoundError:
    print("Error: bsconfig.toml not found. Create it first.")
    sys.exit(1)



parser.add_argument(
    "search",
    # nargs is needed here otherwise it breaks the subparser?
    nargs='?',
    help="Search query or URL",
)

parser.add_argument(
    "engine",
    nargs='?',
    help="Select a search engine",
    default=default_args.get("engine", "google"),
    type=str.lower,
)

parser.add_argument(
    "-l",
    "--local",
    default=default_args.get("local", None),
    help="Search localhost on the specified port\n use / for empty search",
)

# parser.add_argument(
#     "-e",
#     "--engine",
#     default=default_args.get("engine", "google"),
#     help="Select a search engine",
#     type=str.lower,
# )

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

parser_config = subparser.add_parser("set_config")

parser_config.add_argument(
    "flag",
    help = "select the flag default you'd wish to change"
)

parser_config.add_argument(
    "value",
    help = "select the value you want to change it to"

)


args = parser.parse_args()


class Search:
    def __init__(self, args):
        self.args = args
        print(args.cmd)

        if args.cmd == "set_config":
            self.change_config()

        else:
            self.search_string = ""
            self.build_search()

    def change_config(self):
        if args.flag in ("-e"  "engine"  "--engine"):
           print("huzzah")




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
        try:
            engine_url = engines[self.args.engine]
        except KeyError:

            print("Error engine not in engine.json\nthis is not an included engine, please add your own using bsconfig.toml")
            sys.exit()

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
