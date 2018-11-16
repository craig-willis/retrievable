import subprocess


def trec_eval(metric, qrels_path, results_path, output_path):
    output = open(output_path, 'w')
    proc = subprocess.Popen(['/home/jovyan/bin/trec_eval', '-c', '-q', '-m',
                            metric, qrels_path, results_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    for line in proc.stdout:
        output.write(line.decode('utf-8'))
    proc.wait()
