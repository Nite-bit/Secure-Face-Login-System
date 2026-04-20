from flask import Flask, jsonify, request
import pandas as pd
from app import app

LOG_FILE = "logs/login_log.csv"

# 📊 Get all logs
@app.route("/admin/logs", methods=["GET"])
def get_logs():
    df = pd.read_csv(LOG_FILE)
    return jsonify(df.to_dict(orient="records"))

# 📊 Status statistics
@app.route("/admin/status-stats", methods=["GET"])
def status_stats():
    df = pd.read_csv(LOG_FILE)
    stats = df["Status"].value_counts().to_dict()
    return jsonify(stats)

# 📊 Role distribution
@app.route("/admin/role-stats", methods=["GET"])
def role_stats():
    df = pd.read_csv(LOG_FILE)
    stats = df["Role"].value_counts().to_dict()
    return jsonify(stats)

# 📅 Filter by date
@app.route("/admin/filter-date", methods=["GET"])
def filter_by_date():
    date = request.args.get("date")
    df = pd.read_csv(LOG_FILE)
    filtered = df[df["Date"] == date]
    return jsonify(filtered.to_dict(orient="records"))

# 🔍 Search by name
@app.route("/admin/search", methods=["GET"])
def search_user():
    name = request.args.get("name")
    df = pd.read_csv(LOG_FILE)
    filtered = df[df["Name"].str.contains(name, case=False)]
    return jsonify(filtered.to_dict(orient="records"))

# 🚪 Logout
@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"})