import itertools
import ujson


def saveToJSON(d, fileName):
    jsonData = ujson.dumps(d)
    with open(fileName, 'w+') as f:
        f.write(jsonData)


def fromJSON(fileName):
    with open(fileName, 'r') as f:
        jsonIndex = ujson.load(f)

    return {'numDoc': jsonIndex['numDoc'], 'index': jsonIndex['index']}


def constructIndex(documents):
    index = {}
    chain = itertools.chain.from_iterable([d.getPostingsList() for d in documents])
    postings = []
    for e in chain:
        postings.append(e)
    postings.sort()

    idx = {}
    for term, docid in postings:
        if term in idx:
            if docid in idx[term]:
                idx[term][docid] += 1
            else:
                idx[term][docid] = 1
        else:
            idx[term] = {docid: 1}

    index['index'] = idx
    index['numDoc'] = len(documents)

    return index
