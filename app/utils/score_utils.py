def calculate_score(user):
    score = 0

    # Ví dụ: tính 10 điểm cho mỗi ngày có chấm công
    if hasattr(user, 'attendance_records'):
        score += len(user.attendance_records) * 10

    # KPI giả định nếu có: user.kpi_score
    if hasattr(user, 'kpi_score'):
        score += user.kpi_score or 0

    # Deadline giả định nếu có: user.deadline_score
    if hasattr(user, 'deadline_score'):
        score += user.deadline_score or 0

    return score
