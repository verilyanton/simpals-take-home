import motor
import tornado.web
import tornado.ioloop
import nest_asyncio

from app.repository.ad import AdRepository
from app.api.simpals_account import SimpalsAccountApi


nest_asyncio.apply()


class MainHandler(tornado.web.RequestHandler):

    async def get(self):
        ads_repo = AdRepository(self.settings['db'])
        ads = tornado.ioloop.IOLoop.current().run_sync(ads_repo.get_all)

        if not ads:
            self.write("Syncing the database... Please, reload the page")

            account_api = SimpalsAccountApi()
            result = await account_api.fetch_all_ads()

            if 'ads' in result:
                await ads_repo.insert(result['ads'])
            else:
                self.write(result['error'])

        else:
            self.write("<h2>Ads</h1>")
            for ad in ads:
                if 'price' in ad:
                    price = f"{ad['price']['value']} {ad['price']['unit']}"
                else:
                    price = '---'

                self.write(f"id: {ad['id']}, price: {price}, title: {ad['title']}<br>")


def make_app():
    db = motor.motor_tornado.MotorClient('simpals_mongodb', 27017).test_database

    return tornado.web.Application([
        (r"/", MainHandler),
    ], db=db)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
