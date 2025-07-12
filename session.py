import json
import os

import jmcomic
from jmcomic import PartialDownloadFailedException

from util import images_to_pdf

options = jmcomic.create_option_by_file("./option.yml")


def is_valid(code: str) -> bool:
    return code.isdigit()


def push_request(code: str) -> dict:
    if not is_valid(code):
        return {
            "success": False,
            "msg": f"收到了格式不合法的门牌号：{code}"
        }

    try:
        detailIns, downloader = jmcomic.download_album(code, options)
    except PartialDownloadFailedException as e:
        return {
            "success": False,
            "msg": f"下载时发生错误：{e.msg}"
        }

    detail = detailIns.__dict__

    os.mkdir(f"./pdfs/{code}")

    episodes = []

    for episode in detail["episode_list"]:
        imageFolder = f"./downloads/{code}/{episode[1]}"
        outputPdf = f"./pdfs/{code}/{episode[1]}.pdf"
        images_to_pdf(
            imageFolder,
            outputPdf
        )
        episodes.append(outputPdf)

    return {
        "success": True,
        "detail": detail,
        "pdf": episodes
    }
