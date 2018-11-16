import math


class ScorerDirichlet:

    def score(self, query_vector, document_vector, doc_length, term_count,
              col_prob, params):
        ll = 0.0
        for feature in query_vector:
            df = document_vector[feature]
            cp = col_prob[feature]
            pr = (df + params['mu']*cp) / (doc_length + params['mu'])
            qw = query_vector[feature]/sum(query_vector)

            ll += qw * math.log(pr)

        return ll
