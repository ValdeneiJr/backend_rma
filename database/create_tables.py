from tortoise import Tortoise, run_async
from db_config import db_config

# Esse arquivo deve ser executado uma unica vez, e responsavel por criar as tabelas no banco

async def main():
    await db_config()
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(main())