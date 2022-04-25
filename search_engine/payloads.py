class PayloadGenerator:

    @staticmethod
    def search_account_payload(query, _id):
        payload = {
            "query": str(query),
            "_id": str(_id)
        }
        return payload

    @staticmethod
    def search_post_payload(query):
        payload = {
            "query": str(query)
        }
        return payload
