from retrievable.core.config import Config


def test_config():
    cfg = Config()
    cfg.read_config('retrievable/tests/test_config.yaml')
    cols = cfg.get_collections()
    assert len(cols) == 1
    assert cols[0] == {
       'name': 'test_collection',
       'index': 'test_index',
       'queries': {'title': 'test_topics'},
       'qrels': 'test_qrels'
    }

    scorers = cfg.get_scorers()
    assert len(scorers) == 1

    assert cfg.get_output_dir() == 'test_output'
    assert cfg.get_run_prefix() == 'test_prefix'
    assert cfg.get_index_root() == '/data/indexes'

    params_list, params_str_list = cfg.get_param_combinations('test')
    assert len(params_list) == 9
