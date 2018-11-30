import argparse
import logging
import os
import parsl
import pyndri

from retrievable.query import list_from_xml
from retrievable.trec import trec_eval
from retrievable.parsl import run_queries
from retrievable.config import Config


def main(args=None):
    """
    Given a config file defining a set of collections and scoreres,
    generate run a parallel Parl workflow to generate run and
    eval output.
    """

    parser = argparse.ArgumentParser(description='Query runner.')
    parser.add_argument('-c', '--config-file', dest='config_file',
                        default='config/scorers.yaml')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')

    args = parser.parse_args()

    overwrite = False

    if args.verbose: 
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cfg = Config()
    cfg.read_config(args.config_file)

    run_prefix = cfg.get_run_prefix()
    output_dir = cfg.get_output_dir()
    eval_dir = cfg.get_eval_dir()

    for col in cfg.get_collections():
        logging.info("Processing collection %s" % col['name'])

        qrels_path = col['qrels']

        index_path = "%s/%s" % (cfg.get_index_root(), col['index'])
        index = pyndri.Index(index_path)
        token2id, id2token, id2df = index.get_dictionary()
        total_terms = index.total_terms()
        id2tf = index.get_term_frequencies()

        for query_file in col['queries']:
            logging.info("Processing query_file %s" % query_file)

            # read the queries as a list
            # TODO: need queries as feature vector
            queries = list_from_xml(col['queries'][query_file], token2id,
                                    id2tf, total_terms)

            for scorer in cfg.get_scorers():

                params_list, params_str_list = cfg.get_param_combinations(
                                                    scorer['name'])

                for idx, params in enumerate(params_list):

                    param_str = params_str_list[idx]

                    # Create output file
                    results_file = "{}/{}/{}/{}.out".format(
                            output_dir, col['name'], 
                            scorer['name'], param_str)
                    eval_file = "{}/{}/{}/{}.eval".format(
                            output_dir, col['name'],
                            scorer['name'], param_str)

                    # skip if exists
                    if not overwrite and os.path.exists(results_file):
                        logging.info("Found existing output file, skipping")
                        pass

                    results_dir = os.path.dirname(results_file)
                    if not os.path.exists(results_dir):
                        os.makedirs(results_dir)

                    # For each col (index + topics + qrels), scorer, paramset
                    r = []
                    for query in queries:
                        r.append(run_queries(index_path, scorer['module'],
                                             scorer['class'], params, query))

                    outputs = [x.result() for x in r]

                    with open(results_file, 'w') as f:
                        for output in outputs:
                            for idx, res in enumerate(output):
                                row = "{} Q0 {} {} {} {}\n".format(
                                        res[0], res[1], idx+1, res[2],
                                        run_prefix)
                                f.write(row)
                    f.close()

                    trec_eval('all_trec', qrels_path, results_file,
                              eval_file)


if __name__ == "__main__":
    main()
