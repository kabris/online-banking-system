from backend import mysql

class LoginHistory:
    __tablename__ = "login_history"  # ✅ Ensure this matches the DB table name
    @staticmethod
    def record_login(user_id, ip_address, status):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO login_history (user_id, ip_address, status)
            VALUES (%s, %s, %s)
        """, (user_id, ip_address, status))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_login_attempts(user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login_history WHERE user_id = %s ORDER BY login_time DESC", (user_id,))
        logins = cur.fetchall()
        cur.close()
        return logins
