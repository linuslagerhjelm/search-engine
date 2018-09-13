from lxml import etree as ET
from src.Document import parse_vert


class Topic:
    def __init__(self, id, title=[], desc=[], narr=[]):
        self.id = id
        self.title = title
        self.desc = desc
        self.narr = narr


def createTopic(file):
    parser = ET.XMLParser(encoding="utf-8", recover=True)
    root = ET.parse(file, parser=parser)

    title = []

    id = root.find('num')
    titleElem = root.find('title')

    if titleElem is not None:
        title = parse_vert(titleElem.text)

    return Topic(id.text.strip(), title)
