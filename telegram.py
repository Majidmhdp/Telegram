from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio
from models import User
from models import Channel
from models import Chat

# === Replace with your credentials ===
api_id = 123456  # your API ID
api_hash = ''
phone = '+1234567890'  # your phone number
password = 'password'  # optional if 2FA is enabled
# =====================================

client = TelegramClient('telegram_session', api_id, api_hash)
channels, groups, contacts = [], [], []


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

def auto_assign(obj, target_class):
    target = target_class()
    for key, value in vars(obj).items():
        if hasattr(target, key):
            setattr(target, key, value)
    return target

async def find_user_by_id(user_id):
    return next((u for u in contacts if u.id == int(user_id)), None)

async def list_entities():
    """Lists all channels, groups, and contacts"""
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        entity = dialog.entity

        if (type(entity).__name__ == 'User'):
            result = auto_assign(entity, User)
            contacts.append(result)
        elif (type(entity).__name__ == 'Channel'):
            result = auto_assign(entity, Channel)
            channels.append(result)
        elif (type(entity).__name__ == 'Chat'):
            result = auto_assign(entity, Chat)
            groups.append(result)
    print(contacts)

async def fetch_messages(entity):
    if not entity:
        raise ValueError("Entity not found")
    
    print(f"📥 Fetching messages from {entity.id}...")
    messages = []

    async for message in client.iter_messages(entity.id):
        messages.append({
            "id": message.id,
            "date": message.date,
            "text": message.text
        })

    print(f"✅ Total messages fetched: {len(messages)}")

    # Save messages to file
    filename = f"{entity.id}_messages.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        for m in reversed(messages):
            text = m['text'] or ''
            f.write(f"[{m['date']}] {text}\n")

    print(f"💾 Messages saved to '{filename}'")

async def main():
    await login()
    await list_entities()

    while True:
        print("\n📋 Menu:")
        print("1️⃣  Fetch messages from a chat")
        print("2️⃣  Send message to a contact")
        print("3️⃣  Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            # Ask user to pick an entity
            choice = input("\nEnter the number of the chat to fetch messages from: ")

            try:
                entity = await find_user_by_id(choice)
                await fetch_messages(entity)
            except (ValueError, IndexError):
                print("❌ Invalid selection.")
                return

        elif choice == '2':
            choice = input("\nEnter the number of the contact id to message: ")
            try:
                entity = await find_user_by_id(choice)
                message = input("💬 Enter your message: ")
                await client.send_message(entity.id, message)
                print(f"✅ Message sent to {entity.id}!")

            except (ValueError, IndexError):
                print("❌ Invalid choice.")
                return

        elif choice == '3':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option.")

    

with client:
    client.loop.run_until_complete(main())
