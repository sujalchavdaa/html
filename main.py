import telebot
import os
import re
import random
import time
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

OWNER = 8118667253 
API_ID = os.getenv("API_ID", "25933223")
API_HASH = os.getenv("API_HASH", "6ef5a426d85b7f01562a41e6416791d3")
TOKEN = os.getenv("BOT_TOKEN", "8003010506:AAE6Pbjg4eZhmSflIHKtVxmeQU8L7KbCQi0")

bot = telebot.TeleBot(TOKEN)

user_state = {}



# Function to extract URLs from text
def txt_to_html(txt_path, html_path):
    import os, html, re
    file_name = os.path.basename(txt_path).replace('.txt', '')

    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    sections = {
        'video': {"title": "video", "items": []},
        'pdf': {"title": "pdf", "items": []},
        'other': {"title": "other", "items": []}
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^(.*?)(https?://\S+)$', line)
        if match:
            name, url = match.groups()
            name, url = name.strip(), url.strip()
            category = categorize_link(name, url)
            sections[category]["items"].append((name, url))

    html_blocks = ""
    for key in ['video', 'pdf', 'other']:
        section = sections[key]
        links = "\n".join([
            f"""<a href="{url}" target="_blank">
  <div class='video'>{html.escape(name)}</div>
</a>"""
            for name, url in section["items"]
        ])
        html_blocks += f"""
<div id="{key}" class="tab-content" style="display:none;">
  <div class="video-list">
    {links}
  </div>
</div>
"""

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{html.escape(file_name)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
  <style>
    body {{
      background: #0a0a0a;
      color: #fff;
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 20px;
      overflow-x: hidden;
    }}
    h1 {{
      background: #111;
      color: #00ffe0;
      font-size: 24px;
      padding: 20px;
      border-radius: 12px;
      text-align: center;
      margin-bottom: 30px;
      box-shadow: 0 0 15px #00ffe0;
      word-wrap: break-word;
      overflow-wrap: break-word;
      box-sizing: border-box;
      max-width: 100%;
    }}
    .tabs {{
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 20px;
      box-sizing: border-box;
      max-width: 100%;
    }}
    .tab-button {{
      padding: 12px 20px;
      font-size: 16px;
      background: rgba(255,255,255,0.05);
      color: #fff;
      border: 1px solid #444;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;
      transition: all 0.3s;
    }}
    .tab-button:hover {{
      background: #00ffe0;
      color: #000;
    }}
    .tab-button.active {{
      background: linear-gradient(135deg, #00ffe0, #00ffa2);
      color: #000;
      box-shadow: 0 0 12px #00ffe0;
    }}
    .video-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 0 5%;
    }}
    .video {{
      background: #1c1c1c;
      padding: 14px 18px;
      border-radius: 10px;
      font-size: 15px;
      font-weight: 500;
      transition: 0.3s ease;
      border-left: 4px solid #00ffe0;
    }}
    .video:hover {{
      transform: translateX(6px);
      background: #2a2a2a;
      box-shadow: 0 0 10px #00ffe0;
    }}
    a {{
      color: inherit;
      text-decoration: none;
    }}
    .footer {{
      text-align: center;
      margin-top: 30px;
      font-size: 13px;
      color: #888;
    }}
    .footer a {{
      color: #00ffe0;
    }}
  </style>
</head>
<body>
  <h1 class="heading">{html.escape(file_name)}</h1>
  <div class="tabs">
    <button class="tab-button" onclick="showTab('video')">📺 video</button>
    <button class="tab-button" onclick="showTab('pdf')">📄 pdf</button>
    <button class="tab-button" onclick="showTab('other')">🧩 other</button>
  </div>
  {html_blocks}
  <div class="footer">
    ᗪEᐯEᒪOᑭEᗪ ᗷY <a href="https://t.me/Lallantoop">𓍯𝙎𝙪𝙟𝙖𝙡⚝</a>
  </div>
  <script>
    function showTab(tabId) {{
      var tabs = document.querySelectorAll('.tab-content');
      tabs.forEach(tab => tab.style.display = 'none');
      document.getElementById(tabId).style.display = 'block';

      var buttons = document.querySelectorAll('.tab-button');
      buttons.forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
    }}
    function scrollToTop() {{
      window.scrollTo({{top: 0, behavior: 'smooth'}});
    }}
    document.addEventListener("DOMContentLoaded", () => {{
      document.querySelector(".tab-button").click();
    }});
  </script>
</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def categorize_link(name, url):
    import re
    if re.search(r'\.(mp4|mkv|avi|mov|flv|wmv|m3u8)$', url, re.IGNORECASE):
        return 'video'
    elif re.search(r'\.pdf$', url, re.IGNORECASE):
        return 'pdf'
    else:
        return 'other'




# Function to create inline keyboard
def start_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("ＣＨＡＮＮＥＬ", url="https://t.me/studywithsv"),
        InlineKeyboardButton("ＯＷＮＥＲ", url="https://t.me/Lallantoop")
    )
    return keyboard

@bot.message_handler(commands=["info"])
def info(message: Message):
    text = (
        f"╭────────────────╮\n"
        f"│✨ __Your Telegram Info__ ✨\n"
        f"├────────────────\n"
        f"├🔹 Name : `{message.from_user.first_name} {message.from_user.last_name or ''}`\n"
        f"├🔹 User ID : @{message.from_user.username or 'N/A'}\n"
        f"├🔹 TG ID : `{message.from_user.id}`\n"
        f"╰────────────────╯"
    )

    bot.send_message(
        message.chat.id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=start_keyboard()
    )


# Start Command
@bot.message_handler(commands=["start"])
def start_command(message):
    user_state.pop(message.chat.id, None)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    mention = f"[{first_name}](tg://user?id={user_id})"

    random_image_url = random.choice([
        "https://envs.sh/Qt9.jpg/IMG20250621443.jpg",
        "https://envs.sh/Fio.jpg/IMG2025070370.jpg",
        "https://envs.sh/Fir.jpg/IMG20250703829.jpg",
    ])

    caption = (
        f"**ʜᴇʟʟᴏ {mention}**\n\n"
        f"✿ I am a **Txt To HTML Converter Bot**\n"
        "✿ Use **/html** to convert a .txt file to .html\n\n"
         "𝐂𝐑𝐄𝐀𝐓𝐎𝐑:- [𓍯𝙎𝙪𝙟𝙖𝙡⚝](http://t.me/Lallantoop)"
    )

    bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=start_keyboard()
    )

# /html Command
@bot.message_handler(commands=["html"])
def ask_for_file(message):
    user_state[message.chat.id] = "awaiting_txt"
    bot.send_message(
        message.chat.id,
        "❁ <b>Hii, I am TXT TO Html bot ❁ </b> \n\n"
        "<blockquote>"
        "Send me your .txt file to convert it to HTML\n"
        "</blockquote>",
        parse_mode="HTML"
    )



# TXT File Handling
@bot.message_handler(content_types=['document'])
def handle_txt_file(message: Message):
    # Check if user is in /html flow
    if user_state.get(message.chat.id) != "awaiting_txt":
        return
    
    # Clear state after accepting file
    user_state.pop(message.chat.id, None)
    
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        
        original_file_name = message.document.file_name
        if not original_file_name.endswith('.txt'):
            bot.send_message(message.chat.id, "⚠️ Please send a valid .txt file.")
            return

        file_name_without_ext = os.path.splitext(original_file_name)[0].replace(" ", "_")
        txt_path = f"{file_name_without_ext}.txt"
        html_path = f"{file_name_without_ext}.html"

        downloaded_file = bot.download_file(file_info.file_path)
        with open(txt_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        txt_to_html(txt_path, html_path)

        with open(html_path, 'rb') as html_file:
            # ✅ Send to user
            bot.send_document(
                message.chat.id, html_file, 
                caption=f"✅ 𝚈𝚘𝚞𝚛 𝙷𝚃𝙼𝙻 𝙵𝚒𝚕𝚎 𝚒𝚜 𝚁𝚎𝚊𝚍𝚢❗",
                parse_mode="Markdown"
            )

            # ✅ Reset file pointer & send to log group
            html_file.seek(0)
            bot.send_document(
                chat_id= -1002799217873,  # ⬅️ Replace with your log group ID
                document=html_file,
                caption=(
                    f"📥 New TXT ➜ HTML Received\n"
                    f"👤 From: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                    f"📝 File: `{original_file_name}`"
                ),
                parse_mode="Markdown"
            )

        # ✅ Optional promotion
        bot.send_message(
            message.chat.id,
            "𝔍𝔬𝔦𝔫 𝔒𝔲𝔯 ℭ𝔥𝔞𝔫𝔫𝔢𝔩𝔰 𝔣𝔬𝔯 𝔘𝔭𝔡𝔞𝔱𝔢𝔰",
            reply_markup=start_keyboard()
        )

        # ✅ Cleanup
        os.remove(txt_path)
        os.remove(html_path)

    except Exception as e:
        bot.send_message(message.chat.id, "❌ An error occurred while processing your file.")
        print(f"Error: {e}")

# ✅ Run bot only once (no duplicates)
if __name__ == "__main__":
    print("🤖 Bot is running... Waiting for messages.")
    bot.infinity_polling()

         
 