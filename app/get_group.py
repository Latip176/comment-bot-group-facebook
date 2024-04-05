import re
import requests
from bs4 import BeautifulSoup
from typing import Union


class Group:
    def __init__(self, cookie: str, session: requests.Session()) -> None:
        self.host = "mbasic.facebook.com"
        self.session = session
        self.session.headers.update(
            {
                "Host": self.host,
                "Connection": "keep-alive",
                "Cookie": cookie,
                "User-Agent": "Chrome",
            }
        )

        self.cookies = {"cookie": cookie}
        self.comment_urls = []

    def response(self, url: str) -> BeautifulSoup:
        response = self.session.get(
            url, headers={"Host": self.host}, cookies=self.cookies
        )
        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    def CollectPost(self, soup: BeautifulSoup, count: int) -> list:
        m_group_stories_container = soup.find(
            "div", attrs={"id": "m_group_stories_container"}
        )
        for comment in re.findall(
            r'href="(https:\/\/mbasic\.facebook\.com\/groups\/\d+\/permalink\/\d+\/.*?)">.*?(?:Komentar|Komentari)</a>',
            str(m_group_stories_container),
        ):
            if comment in self.comment_urls:
                continue
            self.comment_urls.append(comment)
            if len(self.comment_urls) >= count:
                return self.comment_urls

        action = soup.find("a", string="Lihat Postingan Lainnya")
        if action:
            self.CollectPost(
                soup=self.response(f"https://{self.host}{action['href']}"), count=count
            )

        return self.comment_urls

    def GetInfoGroup(self, url: str, count: int) -> Union[dict, bool]:
        soup = self.response(url)
        comment_urls = self.CollectPost(soup=soup, count=count)

        if "Konten Tidak Ditemukan" in soup.title:
            return False

        return {
            "name": soup.title.string,
            "urls": comment_urls,
            "count": len(self.comment_urls),
        }
