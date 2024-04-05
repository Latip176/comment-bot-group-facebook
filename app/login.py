import re
import requests
from bs4 import BeautifulSoup


# session
session = requests.Session()


# auto change language to Indonesian language
def change_language() -> bool:
    response = session.get("https://mbasic.facebook.com/language/?paipv=0")
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find(
        "form",
        attrs={
            "method": "post",
            "action": re.compile("\/intl\/save\_locale\/\?loc\=id_ID&.*?"),
        },
    )
    data = {
        dat["name"]: dat["value"]
        for dat in form.find_all("input", attrs={"name": ["fb_dstg", "jazoest"]})
    }
    if (
        session.post(
            "https://mbasic.facebook.com" + str(form["action"]), data=data
        ).status_code
        != 200
    ):
        return False

    return True


def check_cookie(cookie: str) -> bool:
    request_web = session.get(
        "https://mbasic.facebook.com/", cookies={"cookie": cookie}
    )
    if "mbasic_logout_button" in str(request_web.text):
        if change_language() == False:
            print(" #@ Change Language Failed")
            return False
        return True
    else:
        return False
