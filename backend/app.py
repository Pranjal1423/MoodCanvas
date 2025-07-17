# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from art_generator import generate_art
# from sentiment import analyze_sentiment
# import traceback

# app = Flask(__name__)
# CORS(app)

# # Fix the route - your frontend is calling root "/" not "/generate"
# @app.route("/", methods=["POST"])  # Changed from "/generate" to "/"
# def generate():
#     try:
#         data = request.json
#         prompt = data.get("prompt", "")
#         if not prompt:
#             return jsonify({"error": "Prompt is required"}), 400

#         # Analyze sentiment
#         sentiment, scores = analyze_sentiment(prompt)

#         # Generate art
#         base64_image = generate_art(prompt)

#         if base64_image:
#             return jsonify({
#                 "image": base64_image,
#                 "sentiment": sentiment,
#                 "scores": scores
#             })
#         else:
#             return jsonify({"error": "Failed to generate image"}), 500
#     except Exception as e:
#         print("❌ Flask error:", e)
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     # Run the app
#     app.run(host='0.0.0.0', port=5000, debug=True)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from art_generator import generate_art
# from sentiment import analyze_sentiment
# import traceback

# app = Flask(__name__)
# CORS(app)

# @app.route("/", methods=["POST"])
# def generate():
#     try:
#         data = request.json
#         prompt = data.get("prompt", "")
        
#         if not prompt:
#             return jsonify({"error": "Prompt is required"}), 400

#         print(f"📝 Received prompt: {prompt}")

#         # Analyze sentiment first
#         sentiment, scores = analyze_sentiment(prompt)
#         print(f"😊 Sentiment detected: {sentiment}")

#         # Generate art using Pollinations.ai
#         base64_image = generate_art(prompt)

#         if base64_image:
#             return jsonify({
#                 "image": base64_image,
#                 "sentiment": sentiment,
#                 "scores": scores,
#                 "status": "success"
#             })
#         else:
#             return jsonify({
#                 "error": "Failed to generate image", 
#                 "sentiment": sentiment,
#                 "scores": scores
#             }), 500
            
#     except Exception as e:
#         print("❌ Flask error:", e)
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500

# # Add a test route
# @app.route("/test", methods=["GET"])
# def test():
#     return jsonify({"message": "MoodCanvas API is running!", "status": "ok"})

# if __name__ == "__main__":
#     print("🚀 Starting MoodCanvas server...")
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from art_generator import generate_art, get_available_styles
from sentiment import analyze_sentiment
import traceback

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        style = data.get("style", "realistic")  # New: Get style from request
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        print(f"📝 Received prompt: {prompt}")
        print(f"🎨 Selected style: {style}")

        # Analyze sentiment first
        sentiment, scores = analyze_sentiment(prompt)
        print(f"😊 Sentiment detected: {sentiment}")

        # Generate art with selected style
        base64_image = generate_art(prompt, style)

        if base64_image:
            return jsonify({
                "image": base64_image,
                "sentiment": sentiment,
                "scores": scores,
                "style": style,
                "status": "success"
            })
        else:
            return jsonify({
                "error": "Failed to generate image", 
                "sentiment": sentiment,
                "scores": scores,
                "style": style
            }), 500
            
    except Exception as e:
        print("❌ Flask error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# New route: Get available art styles
@app.route("/styles", methods=["GET"])
def get_styles():
    """Return available art styles for the frontend"""
    try:
        styles = get_available_styles()
        return jsonify({
            "styles": styles,
            "status": "success"
        })
    except Exception as e:
        print("❌ Error getting styles:", e)
        return jsonify({"error": str(e)}), 500

# Test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "message": "MoodCanvas API is running!", 
        "status": "ok",
        "version": "2.0 - Enhanced with Styles"
    })

if __name__ == "__main__":
    print("🚀 Starting Enhanced MoodCanvas server...")
    print("🎨 Features: Multiple Art Styles, Enhanced Emotion Detection")
    app.run(host='0.0.0.0', port=5000, debug=True)