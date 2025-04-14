from app.dao.dao_athletes import AthleteDAO

class AthleteHandler:
    def __init__(self):
        self.dao = AthleteDAO()

    def get_all_athletes(self):
        athletes = self.dao.get_all_athletes()
        result = []
        for row in athletes:
            result.append({
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "height": float(row[4]),
                "weight": float(row[5])
            })
        return result

    def get_athlete_by_id(self, athlete_id):
        athlete = self.dao.get_athlete_by_id(athlete_id)
        if not athlete:
            return {"error": "Athlete not found"}, 404
        return {
            "id": athlete[0],
            "name": athlete[1],
            "age": athlete[2],
            "gender": athlete[3],
            "height": float(athlete[4]),
            "weight": float(athlete[5])
        }

    def insert_athlete(self, item):
        required_fields = ["name", "age", "gender", "height", "weight"]
        if not all(field in item for field in required_fields):
            return {"error": "Missing required fields"}, 400

        
        name = item["name"]
        age = item["age"]
        gender = item["gender"]
        height = item["height"]
        weight = item["weight"]

        athlete_id = self.dao.create_athlete(name, age, gender, height, weight)
        
        return {
            "id": athlete_id,
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight
        }, 201

    def update_athlete(self, athlete_id, item):
        existing = self.dao.get_athlete_by_id(athlete_id)
        if not existing:
            return {"error": "Athlete not found"}, 404

        required_fields = ["name", "age", "gender", "height", "weight"]
        if not all(field in item for field in required_fields):
            return {"error": "Missing required fields"}, 400

        name = item["name"]
        age = item["age"]
        gender = item["gender"]
        height = item["height"]
        weight = item["weight"]

        self.dao.update_athlete(athlete_id, name, age, gender, height, weight)
        return {
            "id": athlete_id,
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight
        }, 200

    def delete_athlete(self, athlete_id):
        existing = self.dao.get_athlete_by_id(athlete_id)
        if not existing:
            return {"error": "Athlete not found"}, 404
        self.dao.delete_athlete(athlete_id)
        return {}, 204
