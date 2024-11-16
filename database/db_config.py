from tortoise import Tortoise

async def db_config():
    await Tortoise.init(
        db_url=r'sqlite://C:\Users\tahad\projeto\data\data.db',
        modules={'models': ['models']}
    )

async def close():
    await Tortoise.close_connections()