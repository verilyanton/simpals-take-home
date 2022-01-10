class AdRepository:

    def __init__(self, db):
        self.db = db

    async def get_all(self):
        ads = []
        cursor = self.db.ads.find()

        for document in await cursor.to_list(length=1000):
            ads.append(document)

        return ads

    async def insert(self, ads: list):
        result = await self.db.ads.insert_many(ads)
        return repr(result.inserted_ids)
