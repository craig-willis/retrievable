import argparse
import time
import pyndri
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def main(args=None):

    parser = argparse.ArgumentParser(
            description='Create term timeseries index')
    parser.add_argument('--index', dest='index')
    parser.add_argument('--output', dest='output')

    args = parser.parse_args()

    index = pyndri.Index(args.index)

    print('Reading dictionary...')
    token2id, id2token, id2df = index.get_dictionary()

    doc_ids = range(index.document_base(), index.maximum_document())

    print('Building timeseries...')
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

    t0 = time.time()
    print('Creating dataframe...')
    df = pd.DataFrame.from_dict(ts, orient='index', dtype=int)
    t1 = time.time()
    print(t1 - t0)

    t0 = time.time()
    print('Serializing dataframe...')
    df.to_csv(args.output, compression="gzip")
    t1 = time.time()
    print(t1 - t0)


if __name__ == "__main__":
    main()
