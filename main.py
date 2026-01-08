import os
import discord
from discord.ext import commands

# ====== INTENTS ======
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== READY ======
@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

# ====== COMMAND ĐẾM ẢNH TRONG FORUM ======
@bot.command(name="demanh")
async def demanh(ctx, forum_id: int):
    forum = ctx.guild.get_channel(forum_id)

    if not forum:
        await ctx.send("❌ Không tìm thấy forum")
        return

    if forum.type != discord.ChannelType.forum:
        await ctx.send("❌ Channel này không phải Forum")
        return

    await ctx.send("🔍 Đang truy cập từng mục để đếm ảnh (chuẩn 100%)...")

    ket_qua = []

    # 🔹 THREAD ĐANG MỞ
    tat_ca_threads = list(forum.threads)

    # 🔹 THREAD ĐÃ ARCHIVE
    async for t in forum.archived_threads(limit=None):
        tat_ca_threads.append(t)

    # ====== DUYỆT TỪNG MỤC ======
    for thread in tat_ca_threads:
        so_anh = 0

        async for msg in thread.history(limit=None):
            if not msg.attachments:
                continue

            for att in msg.attachments:
                # ❗ CHỈ TÍNH ẢNH
                if att.content_type and att.content_type.startswith("image/"):
                    so_anh += 1

        ket_qua.append(f"🧵 **{thread.name}**: {so_anh} ảnh")

    if not ket_qua:
        await ctx.send("Không có bài đăng nào.")
    else:
        # Discord giới hạn 2000 ký tự
        await ctx.send("\n".join(ket_qua)[:1900])

# ====== RUN BOT (RAILWAY ENV) ======
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ Chưa set DISCORD_TOKEN trong Railway")

bot.run(TOKEN)
