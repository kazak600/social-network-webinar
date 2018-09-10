class User:

    collection = None

    def __init__(self):
        pass

    @classmethod
    async def get_user(cls, uid):
        return cls.collection.find_one(uid)
