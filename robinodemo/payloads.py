class PayloadGenerator:

    @staticmethod
    def profile_payload(user_id, _id):
        payload = {
            "user_id": str(user_id),
            "_id": str(_id),
        }
        return payload

    @staticmethod
    def home_payload(user_id):
        payload = {
            "user_id": str(user_id),
        }
        return payload

    @staticmethod
    def add_post_payload(content, user):
        payload = {
            "content": str(content),
            "user": str(user),
        }
        return payload

    @staticmethod
    def add_comment_payload(content, writer, post_id):
        payload = {
            "content": str(content),
            "writer": str(writer),
            "post_id": str(post_id),
            "replies": 0
        }
        return payload

    @staticmethod
    def reply_comment_payload(content, writer, post_id, source_id):
        payload = {
            "content": str(content),
            "writer": str(writer),
            "post_id": post_id,
            "source_id": source_id
        }
        return payload

    @staticmethod
    def like_post_payload(liker, post_id):
        payload = {
            "liker": str(liker),
            "post_id": post_id
        }
        return payload

    @staticmethod
    def post_liker_list_payload(post_id, _id):
        payload = {
            "post_id": post_id,
            "_id": str(_id)
        }
        return payload

    @staticmethod
    def show_comment_payload(_id, post_id):
        payload = {
            "_id": str(_id),
            "post_id": post_id,
        }
        return payload

    @staticmethod
    def show_reply_payload(_id, comment_id):
        payload = {
            "_id": str(_id),
            "comment_id": comment_id,
        }
        return payload

    @staticmethod
    def follow_unfollow_payload(_id, profile_id):
        payload = {
            "user_id": str(_id),
            "profile_id": profile_id
        }
        return payload

    @staticmethod
    def show_follower_payload(_id):
        payload = {
            "user_id": str(_id),
        }
        return payload

    @staticmethod
    def show_following_payload(user_id, _id):
        payload = {
            "user_id": str(user_id),
            "_id": _id
        }
        return payload

    @staticmethod
    def delete_post_payload(user_id, post_id):
        payload = {
            "user_id": str(user_id),
            "post_id": post_id
        }
        return payload

    @staticmethod
    def delete_comment_payload(user_id, comment_id):
        payload = {
            "user_id": str(user_id),
            "comment_id": comment_id
        }
        return payload
