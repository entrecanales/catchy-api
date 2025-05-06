from sqlalchemy import text

def new_user(db, user):
    sql = text("SELECT * FROM users WHERE id = :user_id")
    return db.execute(sql, {"user_id": user.id}).fetchall()