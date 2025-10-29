# models/user.py

# User(id=5576705954, is_self=False, contact=True, mutual_contact=True, deleted=False, bot=False, 
#      bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, 
#      min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=True,
#        fake=False, bot_attach_menu=False, premium=False, attach_menu_enabled=False, bot_can_edit=False, 
#        close_friend=False, stories_hidden=False, stories_unavailable=True, contact_require_premium=False, 
#        bot_business=False, bot_has_main_app=False, access_hash=6840830239824727804, first_name='Maman', last_name=None,
#          username=None, phone='989131031370', photo=None, status=None, bot_info_version=None, restriction_reason=[],
#            bot_inline_placeholder=None, lang_code=None, emoji_status=None, usernames=[], stories_max_id=None, color=None,
#              profile_color=None, bot_active_users=None, bot_verification_icon=None, send_paid_messages_stars=None)

class User:
    def __init__(self, id=None, first_name=None, last_name=None, username=None, phone=None, is_self=False):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.is_self = is_self

    def __repr__(self):
        return f"<User id={self.id}, name={(self.first_name or '') + '' + (self.last_name or '')}>"