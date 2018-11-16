import argparse
import time
import pyndri
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def main(args=None):

    parser = argparse.ArgumentParser(
            description='Create term timeseries index')
    parser.add_argument('--start-time', dest='start_time', type=int)
    parser.add_argument('--end-time', dest='end_time', type=int)
    parser.add_argument('--interval', dest='interval', type=int)
    parser.add_argument('--index', dest='index')

    args = parser.parse_args()

    index = pyndri.Index(args.index)
    # start = args.start_time
    # end = args.end_time
    # interval = args.interval
    # bins = (end-start)/interval

    print('Get dictionary')
    token2id, id2token, id2df = index.get_dictionary()

    doc_ids = range(index.document_base(), index.maximum_document())

    print('Building index')
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
    print('Creating dataframe')
    df = pd.DataFrame.from_dict(ts, orient='index', dtype=int)
    t1 = time.time()
    print(t1 - t0)

    t0 = time.time()
    print('Serializing dataframe')
    # df.to_pickle("ap-tsindex.pkl", compression="gzip", protocol=2)
    df.to_csv("ap-tsindex.csv", compression="gzip")
    # df.to_parquet('ap-tsindex.parquet.gzip', compression='gzip')
    # df.to_json('ap-tsindex.json.gzip', orient='index', compression='gzip')
    t1 = time.time()
    print(t1 - t0)


if __name__ == "__main__":
    main()
