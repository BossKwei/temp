from sanic import exceptions
from sanic import Sanic
from sanic import response

app = Sanic(__name__)


@app.route('/')
async def get(request):
    return response.json({"GET": request.path})


@app.route('/get/uid=<uid:int>&key=<key:int>')
async def get(request, uid: int, key: int):
    return response.json({"GET": [uid, key]})


@app.route('/login', methods=['POST',])
async def post(request):
    return response.json({"POST": request.body})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, access_log=False)
