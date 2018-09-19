import hashlib
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class User:

    @staticmethod
    async def get_user_by_email(db: AsyncIOMotorDatabase, email: str):
        user = await db.users.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
            user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return dict(error='User with email {} not found'.format(email))

    @staticmethod
    async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return None

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

    @staticmethod
    async def save_avatar_url(db: AsyncIOMotorDatabase, user_id: str, url: str):
        if url and user_id:
            db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'avatar_url': url}})

    @staticmethod
    async def get_user_friends_suggestions(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        query = {'_id': {'$ne': ObjectId(user_id)}}
        users = await db.users.find(query).to_list(limit)
        return users

    @staticmethod
    async def add_friend(db: AsyncIOMotorDatabase, user_id: str, friend_id: str):
        await db.users.update_one({'_id': ObjectId(user_id)}, {'$addToSet': {'friends': ObjectId(friend_id)}})

    @staticmethod
    async def get_user_friends(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        user_friends = await db.users.find({'_id': {'$in': user['friends']}}).to_list(limit)
        return user_friends
