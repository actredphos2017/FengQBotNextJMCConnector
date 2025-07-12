import json
import os
from json import JSONDecodeError

import jmcomic
from jmcomic import PartialDownloadFailedException

from util import images_to_pdf, force_rmdir

options = jmcomic.create_option_by_file("./option.yml")


def is_valid(code: str) -> bool:
    return code.isdigit()


def check_exist(code: str) -> None | tuple[list[str], dict]:

    if not os.path.isdir(f"./pdfs/{code}"):
        return None

    if not os.path.isfile(f"./pdfs/{code}/detail.json"):
        force_rmdir(f"./pdfs/{code}")
        return None

    detailJson: str
    with open(f"./pdfs/{code}/detail.json") as f:
        detailJson = f.read()

    existedDetail: dict
    try:
        existedDetail = json.loads(detailJson)

    except JSONDecodeError:
        force_rmdir(f"./pdfs/{code}")
        return None

    episodes = []

    for episode in existedDetail["episode_list"]:
        if os.path.isfile(f"./pdfs/{code}/{episode[1]}.pdf"):
            episodes.append(os.path.abspath(f"./pdfs/{code}/{episode[1]}.pdf"))
        else:
            force_rmdir(f"./pdfs/{code}")
            return None

    return episodes, existedDetail




def push_request(code: str) -> dict:
    if not is_valid(code):
        return {
            "success": False,
            "msg": f"收到了格式不合法的门牌号：{code}"
        }

    exist = check_exist(code)

    if exist is not None:
        episodes, existedDetail = exist
        return {
            "success": True,
            "detail": existedDetail,
            "pdf": episodes
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

    with open(f"./pdfs/{code}/detail.json", "w") as f:
        f.write(json.dumps(detail))

    episodes = []

    for episode in detail["episode_list"]:
        imageFolder = f"./downloads/{code}/{episode[1]}"
        outputPdf = f"./pdfs/{code}/{episode[1]}.pdf"
        images_to_pdf(
            imageFolder,
            outputPdf
        )
        episodes.append(os.path.abspath(outputPdf))

    return {
        "success": True,
        "detail": detail,
        "pdf": episodes
    }
