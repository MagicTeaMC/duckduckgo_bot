from .ddginternal import Result, get_djs, get_result_binding
from .primp import Client, Response


def raise_for_status(res: Response):
    assert res.status_code == 200, res.text


def organic_search(q: str) -> str:
    client = Client(impersonate="chrome_127", verify=False)

    # Get the start page (simpler search, possibly fewer ads)
    res = client.get("https://start.duckduckgo.com", params={"q": q})
    raise_for_status(res)

    # The /d.js file stores all information about the search results
    djs_url = get_djs(res.text)

    djs_res = client.get("https://links.duckduckgo.com" + djs_url)
    raise_for_status(djs_res)

    return djs_res.text


def get_results(djs: str) -> Result:
    return get_result_binding(djs)


def search(q: str) -> Result:
    return get_results(organic_search(q))
