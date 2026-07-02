USER_STATES = {}


def set_pending_modification(chat_id, request_id):

    USER_STATES[chat_id] = request_id


def get_pending_modification(chat_id):

    return USER_STATES.get(chat_id)


def clear_pending_modification(chat_id):

    USER_STATES.pop(chat_id, None)