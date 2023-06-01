from flask import *
import jsonify
import webview
from web import fetchQuery, getMovie, fetchReviewsAPI, fetch_query, get_movie

app = Flask(__name__)
# window = webview.create_window("Spoiler Detector", app)


@app.route('/', methods=["GET"])
def home():
    return render_template('main.html', data={'reviews': None,'status':False})

# @app.route('/predict', methods=["POST", "GET"])
# def predict():
#     # contains all the data in JSON/Python __dict__
#     dataGet = request.get_json(force=True)

#     # Processing goes here

#     # Preparing response data in Python __dict__
#     responseData = {}
#     return jsonify(responseData)

@app.route("/query", methods=["GET"])
def getMovieNames():
    query = request.args.get('query')
    result = fetchQuery(query)
    result['reviews'] = None
    print(query,result)
    return render_template('main.html', data=result)


# JSON API for movie title search
@app.route("/<movie>", methods=["GET"])
def searchMovie(movie):

    print("\nI am from searchMovie\n")
    result = fetchQuery(movie)
    # print(result)
    page = render_template('search_results.html', data=result)
    result = {"status": result['status'], "page": page}
    # print(json.dumps(result))
    return json.dumps(result)

@app.route("/movie/<id>",methods=["GET"])
def fetchMovie(id):
    movie_details = getMovie(id)
    print(movie_details)
    reviews = fetchReviewsAPI(id)

    movie_details['reviews'] = reviews
    page = render_template("movie_reviews.html", data=movie_details)

    # return render_template("main.html", data=movie_details)
    return json.dumps(page)

# SpoilerDetection - v1.5
# building API's

@app.route('/api/query', methods=["GET"])
def get_search_result():
    title = request.args.get('title')
    internal_response = fetch_query(title)

    result = json.dumps(
        internal_response
    )

    return result


@app.route('/api/movie', methods=["GET"])
def get_movie_result(): 
    id = request.args.get('id')
    internal_response = get_movie(id)

    result = json.dumps(
        internal_response
    )

    return result


if __name__ == '__main__':
    app.run(debug=True)
    # webview.start()

