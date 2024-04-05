import re
import requests
from bs4 import BeautifulSoup
from .get_group import Group


class SpamComment(Group):
    def __init__(self, cookie: str) -> None:
        super().__init__(cookie=cookie)

    def PostComment(self, url: str, comment: str, file: str) -> bool:
        attachments = self.GetAttachments(url=url)
        soup_attachments = BeautifulSoup(attachments, "html.parser")
        form_attachments = soup_attachments.find(
            "form", attrs={"enctype": "multipart/form-data"}
        )
        data_attachments = {
            x.get("name"): x.get("value")
            for x in form_attachments.findAll(
                "input", attrs={"name": True, "value": True, "type": "hidden"}
            )
        }
        data_attachments["comment_text"] = comment
        files = {"photo": open(file, "rb")}
        post_comment = requests.post(
            form_attachments["action"],
            data=data_attachments,
            files=files,
            cookies=self.cookies,
        )

        if str(post_comment.status_code) != "200":
            return False

        return True

    def GetAttachments(self, url: str) -> str:
        session = requests.Session()
        session.headers.update({"Host": "mbasic.facebook.com"})
        soup = BeautifulSoup(session.get(url, cookies=self.cookies).text, "html.parser")
        form = soup.find("form", attrs={"method": "post"})
        data = {
            x.get("name"): x.get("value")
            for x in form.findAll("input", attrs={"name": ["jazoest", "fb_dstg"]})
        }
        data["view_photo"] = "Lampirkan Foto"

        attachments = session.post(
            f"https://{self.host}{form['action']}", cookies=self.cookies, data=data
        )
        target_id = re.findall("ft_ent_identifier=(.*)&", str(form["action"]))[0]
        attachments = session.get(
            f"https://mbasic.facebook.com/mbasic/comment/advanced/?target_id={target_id}&pap=1&at=compose&photo_comment=1",
            cookies=self.cookies,
        )

        return attachments.text
