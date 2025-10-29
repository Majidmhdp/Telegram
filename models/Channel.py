# models/channel.py

# Channel(id=1212127339, title='قیمت لحظه\u200cای دلار تهران', photo=ChatPhoto(photo_id=6298501748280200145,
#     dc_id=5, has_video=False, stripped_thumb=b'\x01\x08\x08\x9c\x19\xb6\xe3\xfe[n\xfch\xa2\x8a\xc6:\x99E7}O'), 
#     date=datetime.datetime(2023, 2, 3, 15, 21, 20, tzinfo=datetime.timezone.utc), creator=False, left=False, broadcast=True,
#       verified=False, megagroup=False, restricted=False, signatures=False, min=False, scam=False, has_link=False, has_geo=False,
#         slowmode_enabled=False, call_active=False, call_not_empty=False, fake=False, gigagroup=False, noforwards=False, join_to_send=False, 
#         join_request=False, forum=False, stories_hidden=False, stories_hidden_min=False, stories_unavailable=True, signature_profiles=False,
#           autotranslation=False, broadcast_messages_allowed=False, monoforum=False, forum_tabs=False, access_hash=-4134591988182403540, 
#           username='dollar_tehran3bze', restriction_reason=[], admin_rights=None, banned_rights=None, default_banned_rights=None, 
#           participants_count=654057, usernames=[], stories_max_id=None, color=None, profile_color=None, emoji_status=None, level=None, 
#           subscription_until_date=None, bot_verification_icon=None, send_paid_messages_stars=None, linked_monoforum_id=None)

class Channel:
    def __init__(self, id=None, title=None, username=None, participants_count=None, verified=None):
        self.id = id
        self.title = title
        self.username = username
        self.participants_count = participants_count
        self.verified = verified

    def __repr__(self):
        return f"<Channel id={self.id}, name={self.title}>"