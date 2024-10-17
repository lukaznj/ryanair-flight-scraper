import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

for path in sys.path:
    print(path)

from backend.custom_types import User
from backend.mongo_service import serialize_user

print(serialize_user(User(email="dawwaddaw", tracked_flight_route_ids=[])))
