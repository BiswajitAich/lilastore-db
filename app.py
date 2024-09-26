from flask import Flask, request, jsonify
from recommendation.getRecommendation import getRecommendation
from recommendation.setRecommendation import setRecommendation

app = Flask(__name__)

@app.route('/get-recommendation', methods=['GET'])
def get_recommendation():
    try:
        id = request.args.get('id')
        if not id:
            return jsonify({"error": "path_id is required"}), 400
        recommendations = getRecommendation(id)
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/set-recommendation', methods=['GET'])
def set_recommendation():
    try:
        isSuccessfull = setRecommendation()
        return jsonify({"message": isSuccessfull})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return jsonify({"message": "Backend API for private use"})

@app.route('/routes', methods=['GET'])
def list_routes():
    return jsonify({"routes": ["/get-recommendation", "/"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)