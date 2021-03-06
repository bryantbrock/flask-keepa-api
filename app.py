from flask import Flask, json, request
from flask_cors import CORS
import keepa
import uuid
from datetime import date
import os

app = Flask(__name__)
CORS(app)

# POST /current-used-price 
# POST public
@app.route('/current-used-price', methods=['POST'])
def current_used_price():
  try:
    accesskey = os.environ['KEEPA_KEY']
    api = keepa.Keepa(accesskey)
    products = api.query(request.get_json()['isbn'], product_code_is_asin=False)
  except (ConnectionError, OSError, Exception) as msg:
    packet = {
      "id": uuid.uuid4(),
      "isbn": request.get_json()['isbn'],
      "price": "none",
      "title": "none",
      "date": "none",
      "msg": str(msg),
      "status": "500"
    }
    return json.dumps(packet)
    
  if products == []:
    packet = {
      "id": uuid.uuid4(),
      "price": "none",
      "title": "none",
      "date": "none",
      "isbn": request.get_json()['isbn'],
      "msg": str("Found no price for sku #" + str(request.get_json()['isbn'])),
      "status": "401"
    }
  else:
    packet = {
      "id": uuid.uuid4(),
      "price": str(products[0]['data']['USED'][-1]),
      "title": str(products[0]['title']),
      "date": date.today().strftime("%m/%d/%y"),
      "isbn": request.get_json()['isbn'],
      "msg": "none",
      "status": "200"
    }
  return json.dumps(packet)

if __name__ == "__main__":
  app.run()
