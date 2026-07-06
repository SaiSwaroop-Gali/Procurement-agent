USER_STATES = {}


# =====================================
# MODIFY STATE
# =====================================

def set_pending_modification(
    chat_id,
    request_id
):

    USER_STATES[chat_id] = {

        "type": "MODIFICATION",

        "request_id": request_id
    }


def get_pending_modification(
    chat_id
):

    state = USER_STATES.get(chat_id)

    if state and state["type"] == "MODIFICATION":

        return state["request_id"]

    return None


# =====================================
# CONFIRMATION STATE
# =====================================

def set_pending_confirmation(
    chat_id,
    request_id,
    instructions
):

    USER_STATES[chat_id] = {

        "type": "CONFIRMATION",

        "request_id": request_id,

        "instructions": instructions
    }


def get_pending_confirmation(
    chat_id
):

    state = USER_STATES.get(chat_id)

    if state and state["type"] == "CONFIRMATION":

        return state

    return None


# =====================================
# CLEAR STATE
# =====================================

def clear_pending_modification(
    chat_id
):

    USER_STATES.pop(chat_id, None)