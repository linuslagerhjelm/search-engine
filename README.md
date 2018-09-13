# Search engine
This project hosts the source code of an information retreival system (search
engine in layman terms). It implements algorithms for efficient indexing of
large collections of documents as well as high performance for retreival. 

The retreival is done using the tf-idf weighting method. The system has been
demonstrated to index more than 80k documents in less than 5 minutes on a 2011
year MacBook.

The program operates on `.vert` files and performance can be determined using
the [trec_eval tool](https://github.com/usnistgov/trec_eval)

The program was implemented as part of the course *Information retreival* at
Charles University during the winter semester 2017/2018.
