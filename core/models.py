from mongoengine import fields, Document, EmbeddedDocument, EmbeddedDocumentField


# connect('core')


class user_profile(Document):
    _id = fields.IntField(null=False)
    email = fields.EmailField(null=False)
    password = fields.StringField(null=False)
    username = fields.StringField(null=False)
    # new_posts = fields.ListField(EmbeddedDocumentField('post'), null=True)


class post(EmbeddedDocument):
    _id = fields.IntField(null=False)
    content = fields.StringField(null=False)
    user = fields.ReferenceField(user_profile)


class comment(Document):
    _id = fields.IntField(null=False)
    content = fields.StringField(null=False)
    writer = fields.ReferenceField(user_profile)
    post_id = fields.StringField(null=False)
    source_id = fields.StringField(null=True)


class like(Document):
    _id = fields.IntField(null=False)
    liker = fields.ReferenceField(user_profile)
    post_id = fields.StringField(null=False)


class TokenBlackList(Document):
    _id = fields.IntField(null=False)
    token = fields.StringField(null=False)


class followings(Document):
    _id = fields.IntField(null=False)
    user_id = fields.StringField(null=False)
    following = fields.StringField(null=False)


class followers(Document):
    _id = fields.IntField(null=False)
    user_id = fields.StringField(null=False)
    follower = fields.StringField(null=False)
