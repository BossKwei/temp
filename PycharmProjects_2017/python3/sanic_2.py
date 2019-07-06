import sanic, sanic.response, sanic.exceptions

app = sanic.Sanic(__name__)


@app.route('/')
async def get(request):
    return sanic.response.json({"GET": request.path})


@app.route('/login', methods=['POST'])
async def post(request):
    return sanic.response.json({"POST": request.body})


@app.exception(sanic.exceptions.NotFound)
async def handle_404(request, exception):
    return sanic.response.text('404 Not Found', status=404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
