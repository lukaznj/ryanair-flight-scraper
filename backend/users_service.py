from backend import mongo_service


def user_exists(email: str) -> bool:
    if mongo_service.find_user_by_email(email) is None:
        return False
    return True
