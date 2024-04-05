import requests


def check_cookie(cookie: str) -> bool:
    request_web = requests.get(
        "https://mbasic.facebook.com/", cookies={"cookie": cookie}
    )
    if "mbasic_logout_button" in str(request_web.text):
        return True
    else:
        return False
