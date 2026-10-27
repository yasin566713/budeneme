import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
IMAGE_PATHS = ["image.png", "image.jpg", "image.jpeg"]  # Görseli bu isimlerden biriyle botun yanına koy
IMAGE_URL = os.getenv("IMAGE_URL", "image.jpg")  # image.png yoksa bu link kullanılır

MESSAGE_TEXT = """https://www.tiktok.com/@comolokko.46
https://www.instagram.com/hturk46
https://kick.com/comolokko-46

https://www.tiktok.com/@raiwennxd
https://www.instagram.com/yasinnx_06
https://kick.com/raiwenn06"""


def build_message():
    """Embed'i ve (varsa) görsel dosyasını hazırlar."""
    embed = discord.Embed(description=MESSAGE_TEXT, color=0x0A0A0C)
    file = None

    found = next((p for p in IMAGE_PATHS if os.path.exists(p)), None)
    if found:
        file = discord.File(found, filename=found)
        embed.set_image(url=f"attachment://{found}")
    elif IMAGE_URL:
        embed.set_image(url=IMAGE_URL)

    return embed, file


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


bot = Bot()


@bot.tree.command(name="sosyal", description="Sosyal medya linklerini gönderir")
async def sosyal(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    embed, file = build_message()
    if file:
        await interaction.channel.send(embed=embed, file=file)
    else:
        await interaction.channel.send(embed=embed)
    await interaction.delete_original_response()


@bot.event
async def on_ready():
    print(f"Giriş yapıldı: {bot.user}")


bot.run(TOKEN)