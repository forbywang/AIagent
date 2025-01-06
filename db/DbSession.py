from tortoise import Tortoise, run_async

async def init(db_url):
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

def start_mysql_db(db_url):
    run_async(init(db_url))