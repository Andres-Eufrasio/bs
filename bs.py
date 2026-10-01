import argparse
import webbrowser
from urllib.parse import quote



parser = argparse.ArgumentParser(
    description="Easy search from your terminal"
)

parser.add_argument(
    "-l", "--local",
    help="Search localhost on the specified port",
)

parser.add_argument(
    "-e", "--engine",
    default="google",
    help="Select a search engine",
)

parser.add_argument(
    "-b", "--browser",
    help="Select the browser to use - must be PATH to executable",
)

parser.add_argument(
    "-u", "--url",
    action="store_true",
    help="Treat the search argument as a URL",
)

parser.add_argument(
    "search",
    help="Search query or URL",
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


            if not self.search_string.startswith((
				"http://",
				"https://",
				"ftp://",
				"ftps://",
				"ws://",
				"wss://",
                )):
                self.search_string = "https://" + self.search_string

            return

        # Localhost search
        if self.args.local:
            self.search_string = (
                f"https://localhost:{self.args.local}/"
                f"{quote(self.args.search)}"
            )
            return

        # Search engine
        engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "brave": "https://search.brave.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
			"yandex": "https://yandex.com/search/?text=",
			"duckduckgo": "https://duckduckgo.com/?q=",
			"baidu": "https://www.baidu.com/s?wd=",
			"brave": "https://search.brave.com/search?q=",
			"ecosia": "https://www.ecosia.org/search?q=",
			"naver": "https://search.naver.com/search.naver?query=",
			"seznam": "https://search.seznam.cz/?q=",
			"qwant": "https://www.qwant.com/?q=",
			"startpage": "https://www.startpage.com/sp/search?query=",
			"swisscows": "https://swisscows.com/en/web?query=",
			"aol": "https://search.aol.com/aol/search?q=",
			"ask": "https://www.ask.com/web?q=",
			"coccoc": "https://coccoc.com/search?query=",
			"daum": "https://search.daum.net/search?q=",
			"petal": "https://petalsearch.com/search?query=",
			"mojeek": "https://www.mojeek.com/search?q=",
			"you": "https://you.com/search?q=",
        }

        engine_url = engines[self.args.engine]

        self.search_string = (
            engine_url + quote(self.args.search)
        )

    def search(self):
        if self.args.browser:
            browser = webbrowser.get(self.args.browser)
            browser.open(self.search_string)
        else:
            webbrowser.open(self.search_string)


if __name__ == "__main__":
    start = Search(args)
    start.search()

