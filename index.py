import json
import tornado.web
import tornado.ioloop
from connector import insert_adverts
from collect_data import get_advert, get_adverts, create_sorted_adverts, collect_current_currencies
from check_change import check_adverts_changes

url = 'https://partners-api.999.md/adverts'

# for this step I write adverts in the page
class step1(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        adverts = get_adverts(url)
        adverts_sorted = create_sorted_adverts(adverts, url)
        
        print('Write data in the page...')
        self.write(json.dumps(adverts_sorted, ensure_ascii=False).encode('utf-8'))

# for this step I write adverts in MongoDB
class step2(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        adverts = get_adverts(url)
        adverts_sorted = create_sorted_adverts(adverts, url)

        print('Insert to MongoDB...')
        insert_adverts(adverts_sorted)
        
        self.write({'result':'Adverts saved to MongoDB'})
        
# for this step I write only currencies
class step3(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        currencies = collect_current_currencies()
        
        print('Write data in the page...')
        self.write({'Currencies':currencies})

# this step returns OK if all the changes have been made successfully
class step4(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        try:
            check_adverts_changes(url)
            self.write({'result':'OK'})
        except:
            self.write({'result':'KO'})

# in this step all the steps are executed        
class getAdverts(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        adverts = check_adverts_changes(url)
        
        print('Write data in the page...')
        self.write(json.dumps(adverts, ensure_ascii=False).encode('utf-8'))

# this stept returns only the advert wich we need
class getAdvert(tornado.web.RequestHandler):
    def get(self):
        id_advert = self.get_argument('id', None)

        advert = get_advert(url, id_advert)
        json_data = json.dumps(advert, ensure_ascii=False).encode('utf-8')

        print('Write data in the page...')
        self.write(json_data)

if __name__=='__main__':
    app = tornado.web.Application(
        [
            (r"/adverts", getAdverts),
            (r"/advert", getAdvert),
            (r"/step1", step1),
            (r"/step2", step2),
            (r"/step3", step3),
            (r"/step4", step4),
        ]
    )

    app.listen(8080)
    print("start listening")
    tornado.ioloop.IOLoop.current().start()