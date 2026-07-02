from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "ak_m1qpurdj7v2ie5u9s53acybo"
YOUR_EMAIL = "your_login_email@example.com"  # <-- put your real login email here

@app.after_request
def add_cors_headers(response):
    # This lets the grader's browser page talk to your server
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.route("/analytics", methods=["POST", "OPTIONS"])
def analytics():
    # Browsers send an OPTIONS "preflight" request before POST — just say OK
    if request.method == "OPTIONS":
        return "", 200

    # Step A: Check the API key
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Step B: Read the events from the request body
    data = request.get_json(force=True, silent=True) or {}
    events = data.get("events", [])

    # Step C: Do the math
    total_events = len(events)

    unique_users = set()
    revenue = 0.0
    user_totals = {}  # tracks each user's positive-amount total

    for event in events:
        user = event.get("user")
        amount = event.get("amount", 0)

        unique_users.add(user)

        if amount > 0:
            revenue += amount
            user_totals[user] = user_totals.get(user, 0) + amount

    # Find the user with the highest positive total
    top_user = None
    if user_totals:
        top_user = max(user_totals, key=user_totals.get)

    # Step D: Send back the answer
    return jsonify({
        "email": YOUR_EMAIL,
        "total_events": total_events,
        "unique_users": len(unique_users),
        "revenue": round(revenue, 2),
        "top_user": top_user
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)