import argparse
import logging
import pyndri
import pandas as pd
import time

from datetime import datetime
from tqdm import tqdm


def main(args=None):

    parser = argparse.ArgumentParser(
            description='Create term timeseries index')
    parser.add_argument('-i', '--index', dest='index', help='Input index path')
    parser.add_argument('-o', '--output', dest='output', help='Output path')
    parser.add_argument("-v", "--verbose", help='Verbose logging',
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    index = pyndri.Index(args.index)

    logging.info('Get dictionary')
    token2id, id2token, id2df = index.get_dictionary()

    doc_ids = range(index.document_base(), index.maximum_document())

    logging.info('Building index')
    ts = {}
    for doc_id in tqdm(doc_ids):

        epoch = int(index.field(doc_id, 'epoch'))
        date = datetime.fromtimestamp(epoch).date()

        docno, token_ids = index.document(doc_id)

        for token_id in token_ids:
            if token_id > 0 and id2df[token_id] > 1000:
                if date not in ts:
                    ts[date] = {}

                if token_id not in ts[date]:
                    ts[date][token_id] = 0

                ts[date][token_id] += 1

    logging.info('Creating dataframe')
    t0 = time.time()
    df = pd.DataFrame.from_dict(ts, orient='index', dtype=int)
    t1 = time.time()
    logging.debug("time: %s" % (t1 - t0))

    logging.info('Serializing dataframe')
    t0 = time.time()
    df.to_csv(args.output, compression="gzip")
    t1 = time.time()
    logging.debug("time: %s" % (t1 - t0))


if __name__ == "__main__":
    main()
