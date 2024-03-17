import io
import asyncio

from aiogram import Bot, Dispatcher, F
from minio import Minio

bot = Bot(token="bot_token")
dp = Dispatcher()

client = Minio("localhost:9000",
    access_key="admin",
    secret_key="secret_key",
    secure=False
)

@dp.message(F.photo)
async def download_photo(message):
    file_in_io = io.BytesIO()
    photo = message.photo[-1]
    await bot.download(
        photo, destination=file_in_io)
    
    bucket_name = "test"
    destination_file = f"{photo.file_id}.jpg"

    client.put_object(
        bucket_name, destination_file, file_in_io, photo.file_size
    )
    
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

