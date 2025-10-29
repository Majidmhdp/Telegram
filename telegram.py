from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio

# === Replace with your credentials ===
api_id = 1234567  # your API ID
api_hash = 'your_api_hash_here'
phone = '+1234567890'  # your phone number
password = 'your_2fa_password_here'  # optional if 2FA is enabled
# =====================================

client = TelegramClient('telegram_session', api_id, api_hash)


async def login():
    """Connects and logs into Telegram (supports 2FA)"""
    print("🔌 Connecting to Telegram...")
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input('📨 Enter the code you received: ')
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            print("🔐 Two-step verification required.")
            await client.sign_in(password=password)

    print("✅ Logged in successfully!\n")


async def list_entities():
    """Lists all channels, groups, and contacts"""
    dialogs = await client.get_dialogs()

    channels, groups, contacts = [], [], []

    for dialog in dialogs:
        entity = dialog.entity
        if getattr(entity, 'megagroup', False):
            groups.append((entity.id, entity.title))
        elif getattr(entity, 'broadcast', False):
            channels.append((entity.id, entity.title))
        elif getattr(entity, 'first_name', None):
            contacts.append((entity.id, f"{entity.first_name} {entity.last_name or ''}".strip()))

    print("📡 Channels:")
    for i, (cid, title) in enumerate(channels, 1):
        print(f"{i}. {title} (ID: {cid})")

    print("\n👥 Groups:")
    for i, (gid, title) in enumerate(groups, 1):
        print(f"{i + len(channels)}. {title} (ID: {gid})")

    print("\n📞 Contacts:")
    for i, (uid, name) in enumerate(contacts, 1):
        print(f"{i + len(channels) + len(groups)}. {name} (ID: {uid})")

    return channels, groups, contacts


async def fetch_messages(entity_name):
    """Fetches all messages from the selected entity"""
    print(f"📥 Fetching messages from {entity_name}...")
    messages = []

    async for message in client.iter_messages(entity_name):
        messages.append({
            "id": message.id,
            "date": message.date,
            "text": message.text
        })

    print(f"✅ Total messages fetched: {len(messages)}")

    # Save messages to file
    safe_name = entity_name.replace('/', '_').replace(' ', '_')
    filename = f"{safe_name}_messages.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        for m in reversed(messages):
            text = m['text'] or ''
            f.write(f"[{m['date']}] {text}\n")

    print(f"💾 Messages saved to '{filename}'")


async def main():
    await login()
    channels, groups, contacts = await list_entities()

    all_entities = channels + groups + contacts
    if not all_entities:
        print("⚠️ No channels, groups, or contacts found.")
        return

    # Ask user to pick an entity
    choice = input("\nEnter the number of the chat to fetch messages from: ")

    try:
        choice = int(choice) - 1
        entity_id, entity_name = all_entities[choice]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return

    await fetch_messages(entity_name)


with client:
    client.loop.run_until_complete(main())
