import os
import requests
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("file2link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# -------- CATBOX --------
def upload_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    with open(file_path, "rb") as f:
        r = requests.post(url, data={"reqtype": "fileupload"}, files={"fileToUpload": f})
    return r.text

# -------- GOFILE --------
def upload_gofile(file_path):
    server = requests.get("https://api.gofile.io/getServer").json()["data"]["server"]
    with open(file_path, "rb") as f:
        r = requests.post(
            f"https://{server}.gofile.io/uploadFile",
            files={"file": f}
        )
    return r.json()["data"]["downloadPage"]

# -------- HANDLER --------
@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def handle(client, message):
    msg = await message.reply("📥 Downloading file...")
    
    file_path = await message.download()
    size = os.path.getsize(file_path) / (1024 * 1024)  # MB
    
    await msg.edit(f"☁️ Uploading... ({round(size,2)} MB)")
    
    try:
        # Auto switch
        if size <= 200:
            link = upload_catbox(file_path)
        else:
            link = upload_gofile(file_path)

        await msg.edit(f"✅ Done!\n\n🔗 {link}")
    
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")
    
    os.remove(file_path)

app.run()
