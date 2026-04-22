SESSION_STORE = {}
def save_context(session_id, data):
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = {}

    SESSION_STORE[session_id].update(data)
def get_context(session_id):
    return SESSION_STORE.get(session_id, {})

def clear_context(session_id):
    if session_id in SESSION_STORE:
        del SESSION_STORE[session_id]