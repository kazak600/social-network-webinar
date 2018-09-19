from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


class Message:

    @staticmethod
    async def create_message(db: AsyncIOMotorDatabase, from_user: str, to_user: str, message: str):
        data = {
            'from_user': ObjectId(from_user),
            'to_user': ObjectId(to_user),
            'message': message,
            'date_created': datetime.utcnow()
        }
        await db.messages.insert_one(data)

    @staticmethod
    async def get_inbox_messages_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        messages = await db.messages.find({'to_user': ObjectId(user_id)}).to_list(limit)
        return messages

    @staticmethod
    async def get_send_messages_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        messages = await db.messages.find({'from_user': ObjectId(user_id)}).to_list(limit)
        return messages
