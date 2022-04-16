from mongoengine import Document, fields


class User(Document):
    _id = fields.IntField(null=False)
    username = fields.StringField(null=False)
    password = fields.StringField(null=False)
    followers = fields.ListField()
    following = fields.ListField()


class Post(Document):
    _id = fields.IntField(null=False)
    content = fields.StringField(null=False)
    user = fields.ObjectIdField(null=False)


class Comment(Document):
    _id = fields.IntField(null=False)
    content = fields.StringField(null=False)
    post_id = fields.IntField(null=False)
    writer = fields.ObjectIdField(null=False)


class Like(Document):
    _id = fields.IntField(null=False)
    post_id = fields.IntField(null=False)
    liker = fields.ObjectIdField(null=False)


class TokenBlackList(Document):
    _id = fields.IntField(null=False)
    token = fields.StringField(null=False)

