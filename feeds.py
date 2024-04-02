import feedparser


def create_favorites():
    urls = []
    favorites = []
    with open("/home/jimmy/.newsboat/urls", "r") as f:
        urls = f.readlines()

    for url in urls[:2]:
        feed = feedparser.parse(url)
        try:
            feed_title = feed.feed.title

            for entry in feed.entries:
                print("Do you like? {} - {}".format(feed_title, entry.title))

                user_in = "hop"
                while user_in != "n" and user_in != "y" and user_in != "":
                    user_in = input("[y/N] ").lower()

                if user_in == "y":
                    favorites.append("{}-{}".format(feed_title, entry.title))
        except Exception as e:
            print(e)

    return favorites


def get_new_entries():
    entries = []
    with open("urls", "r") as f:
        for url in f.readlines():
            feed = feedparser.parse(url)
            feed_title = feed.feed.title
            for entry in feed.entries:
                entries.append("{}-{}".format(feed_title, entry.title))

    return entries


def get_entry_url(entry: str):
    feed_title = entry.split("-")[0]
    entry_title = entry.split("-")[1]

    with open("/home/jimmy/.newsboat/urls", "r") as f:
        urls = f.readlines()

    for url in urls:
        feed = feedparser.parse(url)

        if feed_title == feed.feed.title:
            return list(
                filter(
                    lambda x: entry_title == x.title,
                    feed.entries
                )
            )[0].link

    raise Exception