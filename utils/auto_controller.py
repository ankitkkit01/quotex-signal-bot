# utils/auto_controller.py

active_auto_users = set()

def enable_auto_mode(user_id):
    active_auto_users.add(user_id)

def disable_auto_mode(user_id):
    active_auto_users.discard(user_id)

def is_auto_enabled(user_id):
    return user_id in active_auto_users
