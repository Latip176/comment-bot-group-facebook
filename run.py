from os import system

from app import Group
from app import SpamComment
from app import check_cookie
from app import session


import platform
from time import sleep
from datetime import datetime


posts = []


def main():
    system("cls" if platform.system() == "Windows" else "clear")

    cookies = input(" >> cookie: ")
    if check_cookie(cookie=cookies) == False:
        exit("Cookie Invalid")

    system("cls" if platform.system() == "Windows" else "clear")
    print(
        """
    Spam Comment Post Group
  Author: Latip176 | Version: v1.2
"""
    )

    len_target = input(" >> JUMLAH target: ")

    for _ in range(int(len_target)):
        target = input(f" {_+1} >> URL group: ")
        count_post = int(input(" >> JUMLAH post: "))
        print(" @ path file foto (wajib)")
        foto = input(" >> File Foto: ")
        print(" @ multi komen pisah pake '|' (komen1 | komen2)")
        comments = input(" >> COMMENTS: ").split("|")
        posts.append(
            {
                "target": target,
                "count_post": count_post,
                "comments": comments,
                "file": foto,
            }
        )

    print("\n @ Dalam Detik")
    delay = int(input(" >> Delay Komen: "))

    print(" #~ Program Berjalan (CTRL + Z to STOP) ~#")

    for post in posts:
        target = post["target"]
        count_post = post["count_post"]
        comments = post["comments"]
        file = post["file"]

        Start = SpamComment(session=session, cookie=cookies)
        InfoGroup = Start.GetInfoGroup(url=target, count=count_post)
        if InfoGroup == False:
            print(" Group Tidak Ditemukan ")
            break
        urls = InfoGroup["urls"]
        print(f"\n # Name Group: {InfoGroup['name']}")
        print(f" # Post di dapatkan: {len(urls)}")

        for i in range(len(comments)):
            for j in range(len(urls)):
                url = urls[j]
                comment = comments[i].strip()
                time = datetime.now()
                if Start.PostComment(url=url, comment=comment, file=file):
                    print(
                        f" #~ Komentar Berhasil Terkirim - {time.hour}:{time.minute}:{time.strftime('%S')}"
                    )
                else:
                    print(
                        f" #~ Komentar Gagal Terkirim - {time.hour}:{time.minute}:{time.strftime('%S')}"
                    )
                sleep(delay)


if __name__ == "__main__":
    main()
