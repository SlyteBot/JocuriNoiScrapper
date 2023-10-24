from threading import Thread
from select_pages import Page


class ThreadLink(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)

    def run(self):
        if self._target != None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


class Links:
    def __init__(self, links: [str]) -> None:
        self.links = links
        self.generate_links()

    def generate_links(self, number_of_pages: int = 5):
        self.scraping_links = []
        numbers = [str(x) for x in range(1, number_of_pages+1)]
        for link in self.links:
            index_link = link.index("&page=")
            for number in numbers:
                self.scraping_links.append(
                    link.replace("&page=", "&page="+number))

    def threading_games(self):
        self.threads = []
        games = []
        for link in self.scraping_links:
            instance = Page(link)
            thread = ThreadLink(target=instance.get_all_games, args=[])
            thread.start()
            self.threads.append(thread)
        for thread in self.threads:
            games += thread.join()
        return games


if __name__ == "__main__":
    links = ["https://www.jocurinoi.ro/ps5&page=",
             "https://www.jocurinoi.ro/ps4&page=",
             "https://www.jocurinoi.ro/xbox-series&page=",
             "https://www.jocurinoi.ro/nintendo-switch&page=",
             "https://www.jocurinoi.ro/pc&page=&filter_id=527"]
    instance = Links(links)
    instance.generate_links(number_of_pages=1)
    instance.threading_games()
