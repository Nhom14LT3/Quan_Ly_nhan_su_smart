from app.models.user import User
from app.utils.score_utils import calculate_score

def ranking_demo():
    users = User.query.all()
    ranked = sorted(users, key=lambda u: calculate_score(u), reverse=True)
    return [
        {
            "id": u.id,
            "name": u.username,
            "score": calculate_score(u)
        }
        for u in ranked
    ]
