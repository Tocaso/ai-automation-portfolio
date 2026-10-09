from app.schemas import LeadClassification, Route


def next_action(result: LeadClassification) -> str:
    if result.route is Route.SALES:
        return "notify_sales"
    if result.route is Route.NURTURE:
        return "enroll_sequence"
    return "archive"