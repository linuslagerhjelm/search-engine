from math import sqrt
from lxml import etree as ET
from src.czech_stemmer import cz_stem
from src.cz_stopwords import stopwords
import gzip


class Document:
    def __init__(self, docid, title=[], heading=[], text=[]):
        self.docid = docid
        self.title = title
        self.heading = heading
        self.text = text

    def getPostingsList(self):
        content = self.getContent()
        return [(t, self.docid) for t in content]

    def getContent(self):
        return self.title + self.heading + self.text


def createDocument(filename):
    f = gzip.open(filename, 'r')
    xml = f.read()
    parser = ET.XMLParser(encoding="utf-8", recover=True)
    root = ET.fromstring(xml, parser=parser)

    title = []
    heading = []
    text = []

    docid = root.find('DOCNO')
    titleElem = root.find('TITLE')
    headingElem = root.find('HEADING')
    textElem = root.find('TEXT')

    if titleElem is not None:
        title = parse_vert(titleElem.text)
    if headingElem is not None:
        heading = parse_vert(headingElem.text)
    if textElem is not None:
        text = parse_vert(textElem.text)
    f.close()

    return Document(docid.text, title, heading, text)


def parse_vert(text):
    lines = filter(lambda l: l, text.split('\n'))
    words = [cz_stem(line.split('\t')[1].lower()) for line in lines]
    return [w for w in words if w not in stopwords]


def l2norm(vector):
    vector = [x ** 2 for x in vector]
    a = .5
    return a * sqrt(sum(vector)) + (1 - a) * 50
