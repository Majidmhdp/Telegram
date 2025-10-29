# models/chat.py

# Chat(id=4960471805, title='Is-fund Dashboard', photo=ChatPhoto(photo_id=5857281067923392403, dc_id=4, has_video=False, 
#         stripped_thumb=b'\x01\x08\x08\xac\xac\x9eP\xe7\xe6\xcd\x14Q[\xa63'), participants_count=6, 
#         date=datetime.datetime(2025, 5, 18, 5, 40, 25, tzinfo=datetime.timezone.utc), version=5, creator=False, 
#         left=False, deactivated=False, call_active=False, call_not_empty=False, noforwards=False, migrated_to=None,
#           admin_rights=None, default_banned_rights=ChatBannedRights(until_date=datetime.datetime(2038, 1, 19, 3, 14, 7, tzinfo=datetime.timezone.utc),
#             view_messages=False, send_messages=False, send_media=False, send_stickers=False, send_gifs=False, send_games=False, send_inline=False,
#               embed_links=False, send_polls=False, change_info=False, invite_users=False, pin_messages=False, manage_topics=False, send_photos=False,
#                 send_videos=False, send_roundvideos=False, send_audios=False, send_voices=False, send_docs=False, send_plain=False))


class Chat:
    def __init__(self, id=None, title=None, participants_count=None, date=None, version=None):
        self.id = id
        self.title = title
        self.participants_count = participants_count
        self.date = date
        self.version = version

    def __repr__(self):
        return f"<Chat id={self.id}, name={self.title}>"