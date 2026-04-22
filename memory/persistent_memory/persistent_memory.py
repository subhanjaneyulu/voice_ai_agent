PERSISTENT_STORE = {}

def save_user_data(user_id, data):
    if user_id not in PERSISTENT_STORE:
        PERSISTENT_STORE[user_id] = {}

    PERSISTENT_STORE[user_id].update(data)
def get_user_data(user_id):
    return PERSISTENT_STORE.get(user_id, {})