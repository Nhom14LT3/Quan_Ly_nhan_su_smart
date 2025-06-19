from flask import Blueprint
from flask_login import current_user, login_required
from app.models.user import User
from app.models.gameboard import ranking_demo
from app.utils.score_utils import calculate_score
from app.decorators.role_required import role_required
from app.utils.render_with_role_layout import render_with_role


gameboard_bp = Blueprint('gameboard', __name__)

@gameboard_bp.route('/gameboard/<int:user_id>')
@login_required
@role_required('admin', 'employee', 'manager')
def gameboard(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    score = calculate_score(user)
    ranking = ranking_demo()

    for r in ranking:
        if r.get("id") == user.id:
            r["me"] = True

    return render_with_role(
        'gamebroad/gamebroad.html',
        user=user,
        score=score,
        ranking=ranking
    )
