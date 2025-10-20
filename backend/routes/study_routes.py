from flask import Blueprint, jsonify, request
from backend.utils.jwt_utils import verify_token
from backend.models.study_model import upsert_active_session, touch_heartbeat, get_stats
from datetime import datetime

study_bp = Blueprint("study", __name__)

@study_bp.route("/heartbeat", methods=["POST"])
@verify_token()
def heartbeat():
    now = datetime.utcnow()
    upsert_active_session(request.user_id, now)
    touch_heartbeat(request.user_id, now)
    stats = get_stats(request.user_id, now)
    return jsonify({"ok": True, "stats": stats})

@study_bp.route("/stats", methods=["GET"])
@verify_token()
def stats():
    now = datetime.utcnow()
    data = get_stats(request.user_id, now)
    return jsonify(data)
