import feedparser
import pandas as pd

RSS_FEEDS = {
    "India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "USA": "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
    "Canada": "https://globalnews.ca/feed/",
    "France": "https://www.france24.com/en/rss",
    "Australia": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Brazil": "https://g1.globo.com/rss/g1/",
    "Russia": "https://www.rt.com/rss/news/"
}

def fetch_rss_headlines():
    records = []

    for country, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]: 
            records.append({
                "country": country,
                "headline": entry.title
            })

    return pd.DataFrame(records)
