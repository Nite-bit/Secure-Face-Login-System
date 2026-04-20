from flask import Flask, jsonify

from app import app

@app.route("/user/dashboard", methods=["GET"])
def user_dashboard():
    return jsonify({
        "message": "Welcome User"
    })

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "message": "Logged out successfully"
    })