import bcrypt
from app.model.dao.dao_user import UserDAO

class UserHandler:
    def __init__(self):
        self.dao = UserDAO()

    def signup(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "Missing username, email, or password"}, 400

        if not email.endswith("@upr.edu"):
            return {"error": "Only @upr.edu email addresses are allowed."}, 400

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        result = self.dao.create_user(username, hashed_pw, email)

        if "error" in result:
            return result, 400

        return {"message": "Account created successfully", "user_id": result["id"]}, 201

    def login(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Missing username or password"}, 400

        user_id, memory = self.dao.user_exists(username, password)
        if user_id:
            return {"message": "Login successful", "user_id": user_id, "memory": memory}, 200
        else:
            return {"error": "Invalid username or password"}, 401

    def user_exists(self, username, password):
        user_id, memory = self.dao.user_exists(username, password)
        if user_id:
            return user_id, memory or "[]"
        else:
            return False, None

    def insert_memory(self, userid, memory):
        return self.dao.insert_memory(userid, memory)