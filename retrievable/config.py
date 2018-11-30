import itertools
import yaml


class Config:

    cfg = None

    def read_config(self, path):
        with open(path, 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)

    def get_run_prefix(self):
        return self.cfg['run_prefix']

    def get_output_dir(self):
        return self.cfg['output_dir']

    def get_eval_dir(self):
        return self.cfg['eval_dir']

    def get_index_root(self):
        return self.cfg['index_root']

    def get_collections(self):
        return self.cfg['collections']

    def get_scorers(self):
        return self.cfg['scorers']

    def get_param_combinations(self, scorer):

        params_list = []
        params_str_list = []
        for scorer in self.get_scorers():

            param_names = []
            param_values = []
            for name, values in scorer['params'].items():
                param_names.append(name)
                param_values.append(values)

            # Each parameter combination
            for values in itertools.product(*param_values):

                # Construct string
                params = {}
                param_str = ""
                for idx, val in enumerate(values):
                    name = param_names[idx]
                    if (idx > 0):
                        param_str += ":"
                    param_str += "{}={}".format(name, val)
                    params[name] = val

                params_list.append(params)
                params_str_list.append(param_str)

        return (params_list, params_str_list)
