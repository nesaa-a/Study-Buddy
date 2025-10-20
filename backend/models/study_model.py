from datetime import datetime, timedelta
from backend.config.db_config import get_db_connection

# Cap any single heartbeat gap to 180 seconds to avoid huge jumps when tab sleeps
MAX_GAP_SECONDS = 180


def _now() -> datetime:
    return datetime.utcnow()


def upsert_active_session(user_id: int, now: datetime | None = None) -> None:
    now = now or _now()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # If there is an active session, do nothing
        cur.execute(
            "SELECT id FROM study_sessions WHERE user_id = %s AND active = 1 LIMIT 1",
            (user_id,),
        )
        row = cur.fetchone()
        if row:
            return
        # Otherwise create a new active session
        cur.execute(
            """
            INSERT INTO study_sessions (user_id, start_time, last_seen, total_seconds, active)
            VALUES (%s, %s, %s, %s, 1)
            """,
            (user_id, now, now, 0),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def touch_heartbeat(user_id: int, now: datetime | None = None) -> None:
    now = now or _now()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Ensure active session exists
        cur.execute(
            "SELECT id, last_seen FROM study_sessions WHERE user_id = %s AND active = 1 ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            # Start a new session
            cur.execute(
                "INSERT INTO study_sessions (user_id, start_time, last_seen, total_seconds, active) VALUES (%s, %s, %s, %s, 1)",
                (user_id, now, now, 0),
            )
            conn.commit()
            return

        session_id, last_seen = row
        if hasattr(last_seen, 'timestamp'):
            # last_seen is datetime; compute delta
            delta = int((now - last_seen).total_seconds())
        else:
            delta = 0
        if delta < 0:
            delta = 0
        if delta > MAX_GAP_SECONDS:
            delta = MAX_GAP_SECONDS

        cur.execute(
            """
            UPDATE study_sessions
            SET last_seen = %s,
                total_seconds = total_seconds + %s
            WHERE id = %s
            """,
            (now, delta, session_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def get_stats(user_id: int, now: datetime | None = None) -> dict:
    now = now or _now()
    start_of_day = datetime(now.year, now.month, now.day)
    start_of_week = start_of_day - timedelta(days=start_of_day.weekday())

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Sum totals; include active session delta from last_seen to now in the SELECT for better accuracy
        # Today
        cur.execute(
            """
            SELECT COALESCE(SUM(total_seconds), 0)
            FROM study_sessions
            WHERE user_id = %s AND last_seen >= %s
            """,
            (user_id, start_of_day),
        )
        today = cur.fetchone()[0] or 0

        # This week
        cur.execute(
            """
            SELECT COALESCE(SUM(total_seconds), 0)
            FROM study_sessions
            WHERE user_id = %s AND last_seen >= %s
            """,
            (user_id, start_of_week),
        )
        week = cur.fetchone()[0] or 0

        # All time
        cur.execute(
            "SELECT COALESCE(SUM(total_seconds), 0) FROM study_sessions WHERE user_id = %s",
            (user_id,),
        )
        all_time = cur.fetchone()[0] or 0

        # Add current active delta (if any) to all three
        cur.execute(
            "SELECT last_seen FROM study_sessions WHERE user_id = %s AND active = 1 ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        row = cur.fetchone()
        if row:
            last_seen = row[0]
            extra = int((now - last_seen).total_seconds())
            if extra < 0:
                extra = 0
            if extra > MAX_GAP_SECONDS:
                extra = MAX_GAP_SECONDS
            today += extra
            week += extra
            all_time += extra

        return {
            "today_seconds": int(today),
            "week_seconds": int(week),
            "all_time_seconds": int(all_time),
        }
    finally:
        cur.close()
        conn.close()
