class MockIndex:

    def get_dictionary(self):
        token2id = {
                'airbus': 6146,
                'subsidies': 3313
        }
        id2token = {
                6146: 'airbus',
                3313: 'subsidies'
        }
        id2df = {
                6146: 508,
                3313: 1479
        }

        return (token2id, id2token, id2df)

    def get_term_frequencies(self):
        id2tf = {
                6146: 1086,
                3313: 2608
        }
        return id2tf

    def query(self, query, results_requested):
        return ((76674, -5.605415176179421), (26759, -5.830037530724974))

    def document(self, docid):
        return('AP880318-0287', ([6146]*16 + [3313]*8))

    # def ext_document_id(self, docid):
    #    if docid == 76674:
    #        return 'AP880318-0287'
    #    return None

    # def maximum_document(self):
    #    return 164598

    # def document_count(self):
    #    return 164597

    def total_terms(self):
        return 76148180

    # def unique_terms(self):
    #    return 413810

    def document_length(self, docid):
        if docid == 76674:
            return 596
        return 0

    def close(self):
        pass


class MockQueryEnv:

    def query(self, query,  results_requested):
        index = MockIndex()
        return index.query(query, results_requested)
