from typing import List

def get_djs(html: str) -> str:
    """Gets `d.js` from the initial HTML.

    Args:
        html (str): The HTML.
    """

def get_result_binding(content: str):
    """Gets the result binding from `d.js`.

    Args:
        content (str): The `d.js` content.
    """

class Result:
    web: List["Web"]
    images: List["Image"]
    news: List["NewsArticle"]

class Web:
    raw_description: str
    description: str
    domain: str
    shortened_url: str
    url: str
    title: str

class Image:
    url: str
    title: str
    description: str
    thumbnail: str
    width: int
    height: int

class NewsArticle:
    date: int
    excerpt: str
    title: str
    url: str
    source: str
    relative_time: str
    image: str
