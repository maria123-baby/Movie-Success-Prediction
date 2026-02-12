from flask import Flask, jsonify, render_template, request, redirect, url_for
import import_ipynb
import Index

app = Flask(__name__)

@app.route('/')
def fetch_data():
    return render_template("index.html")

@app.route('/index', methods=['POST'])
def send_data():
    print("Request Content-Type:", request.content_type)
    print("Raw Request Data:", request.data.decode('utf-8'))  # Print raw request body

    if request.is_json:
        data = request.get_json()
        print("Parsed JSON Data:", data)  # Print parsed JSON for debugging
    else:
        return jsonify({"error": "Invalid input format. Expected JSON."}), 400

    genre = data.get('genre')
    cast = data.get('cast')
    plot = data.get('plot')  
    director = data.get('director')

    if not all([genre, cast, plot, director]):
        return jsonify({"error": "Missing required fields"}), 400

    # Predict movie success
    predicted_rating, predicted_audience = Index.predict_movie_success(genre, cast, director, plot)

    # Determine movie status based on rating
    if predicted_rating >= 9:
        movie_status = "SUPER HIT"
    elif 7 <= predicted_rating < 9:
        movie_status = "HIT"
    elif 5 <= predicted_rating < 7:
        movie_status = "AVERAGE"
    else:
        movie_status = "FLOP"

    response_data = {
        "movie_status": movie_status,
        "predicted_rating": round(float(predicted_rating), 2),
        "predicted_audience": predicted_audience
    }

    print("Response Data:", response_data)  # Debugging print

    return response_data

@app.route('/result')
def result_page():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(port=5500, debug=True)
