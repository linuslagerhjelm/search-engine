import os
import sys
import time
import math
import operator
import itertools
from difflib import SequenceMatcher
from sortedcontainers import SortedList
from src.Topic import createTopic
from src.Index import constructIndex
from src.Document import createDocument, l2norm


def getDocuments(args):
    bufsize = 65536
    documents = []
    with open(os.path.join(args['-dir'], args['-d']), 'r') as docs:
        while True:
            lines = docs.readlines(bufsize)
            if not lines:
                break
            for line in lines:
                doc = os.path.join(args['-dir'], line).strip()
                documents.append(createDocument(doc))

    return documents


def getTopics(args):
    topics = []
    terms = set()
    with open(os.path.join(args['-dir'], args['-q']), 'r') as docs:
        for document in docs:
            doc = os.path.join(args['-dir'], document).strip()
            topic = createTopic(doc)
            topics.append(topic)
            terms.update(topic.title)

    return topics, terms


def normalizeDocuments(documents, invertedIndex):
    dNorms = {}
    idx = invertedIndex['index']
    for d in documents:
        content = set(d.getContent())
        vec = []
        for term in content:
            vec.append(idx[term][d.docid])
        dNorms[d.docid] = l2norm(vec)
    return dNorms


def expandQuery(orig, library):
    query = []
    for t1 in orig:
        for t2 in library:
            r = SequenceMatcher(None, t1, t2).ratio()
            if r >= 1:
                query.append(t1)

    return query


def runQuery(queryTerms, index, dNorms):
    idx = index['index']
    scores = {}
    for term in queryTerms:
        if term not in idx: continue
        df = len(idx[term])
        tf = queryTerms.count(term)
        wtq = (1 + math.log(tf)) * math.log(index['numDoc'] / df)
        for document in idx[term]:
            tf = idx[term][document]
            wtd = (1 + math.log(tf)) * math.log(index['numDoc'] / df)
            if document not in scores:
                scores[document] = wtd * wtq
            else:
                scores[document] += wtd * wtq

    # noinspection PyArgumentList
    res = SortedList(key=operator.itemgetter(0))
    for document, score in scores.items():
        r = score / dNorms[document]
        res.add((r, document))

    return itertools.islice(reversed(res), 1000)


def main():
    argsList = sys.argv[1:]
    args = {}
    for flag, value in zip(argsList[0::2], argsList[1::2]):
        args[flag] = value

    documents = getDocuments(args)
    invertedIndex = constructIndex(documents)

    dNorms = normalizeDocuments(documents, invertedIndex)
    topics, queryTermsLib = getTopics(args)

    with open(os.path.join(args['-dir'], args['-o']), 'w') as f:
        for query in topics:
            print(query.id)
            queryTerms = expandQuery(query.title, queryTermsLib)
            qRes = runQuery(queryTerms, invertedIndex, dNorms)
            i = 0
            for score, id in qRes:
                f.write("{0} {1} {2} {3} {4} {5}\n".format(
                    query.id, 0, id, i, score, args['-r']
                ))
                i += 1


if __name__ == "__main__":
    start = time.time()
    main()
    print("--- %s minutes ---" % (round((time.time() - start) / 60, 3)))
