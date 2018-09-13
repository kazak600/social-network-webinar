import hashlib
from motor.motor_asyncio import AsyncIOMotorDatabase


class User:

    def __init__(self):
        pass

    @staticmethod
    async def get_user(db: AsyncIOMotorDatabase, email: str):
        user = await db.users.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
            return user
        else:
            return dict(error='User with email {} not found'.format(email))

    @staticmethod
    async def create_new_user(db: AsyncIOMotorDatabase, data):
        email = data['email']
        user = await db.users.find_one({'email': email})
        if user:
            return dict(error='user with email {} exist'.format(email))

        if data['first_name'] and data['last_name'] and data['password']:
            data = dict(data)
            data['password'] = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
            result = await db.users.insert_one(data)
            return result
        else:
            return dict(error='Missing user data parameters')
