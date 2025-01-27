import discord
from discord.ext import commands
import requests
import os

# Replace these tokens with your own
BOT_TOKEN = os.getenv("BOT_TOKEN")
COC_API_TOKEN = os.getenv("COC_API_TOKEN")
CLAN_TAG = "#2LLJLU2LY"  # Replace with your clan tag

# Intents and bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Clash of Clans API headers
COC_HEADERS = {
    "Authorization": f"Bearer {COC_API_TOKEN}"
}

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

@bot.command()
async def check(ctx, player_tag: str = None):
    if not player_tag:
        embed = discord.Embed(
            title="Invalid Command Usage",
            description="Please use the command in the following format:\n**!check <COC playerTag>**",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    player_tag = player_tag.upper().replace("#", "")  # Format the player tag

    # Fetch player data from the Clash of Clans API
    player_url = f"https://api.clashofclans.com/v1/players/%23{player_tag}"
    print(player_url)
    response = requests.get(player_url, headers=COC_HEADERS)

    if response.status_code == 200:
        player_data = response.json()
        embed = discord.Embed(
            title=f"Player Information: {player_data.get('name', 'Unknown')}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Player Name", value=player_data.get("name", "N/A"), inline=True)
        embed.add_field(name="Town Hall Level", value=player_data.get("townHallLevel", "N/A"), inline=True)
        embed.add_field(name="Level", value=player_data.get("expLevel", "N/A"), inline=True)
        embed.add_field(name="Trophies", value=player_data.get("trophies", "N/A"), inline=True)
        embed.add_field(name="Best Trophies", value=player_data.get("bestTrophies", "N/A"), inline=True)
        embed.add_field(name="War Stars", value=player_data.get("warStars", "N/A"), inline=True)

        if "clan" in player_data:
            embed.add_field(name="Clan Name", value=player_data["clan"].get("name", "N/A"), inline=True)
            embed.add_field(name="Clan Tag", value=player_data["clan"].get("tag", "N/A"), inline=True)

        embed.set_footer(text="Clash of Clans Player Info")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Player Not Found",
            description=f"The player tag `{player_tag}` is invalid or does not exist.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command()
async def verify(ctx, player_tag: str = None):
    if not player_tag:
        embed = discord.Embed(
            title="Invalid Command Usage",
            description="Please use the command in the following format:\n**!verify <COC playerTag>**",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    """
    Command to verify a user using their Clash of Clans player tag.
    """
    player_tag = player_tag.upper().replace("#", "")  # Format the player tag

    # Fetch player data from the Clash of Clans API
    player_url = f"https://api.clashofclans.com/v1/players/%23{player_tag}"
    response = requests.get(player_url, headers=COC_HEADERS)

    if response.status_code == 200:
        player_data = response.json()
        clan = player_data.get("clan", {})
        name = player_data.get("name")
        # Check if the player is in the specified clan
        if clan and clan.get("tag") == CLAN_TAG:
            # Assign the "Verified" role
            role = discord.utils.get(ctx.guild.roles, name="Membro")
            if role:
                await ctx.author.edit(nick=name)
                await ctx.author.add_roles(role)
                role = discord.utils.get(ctx.guild.roles, name="Utente Verificato")
                await ctx.author.add_roles(role)
                embed = discord.Embed(
                    title="Verification Successful",
                    description=f"{ctx.author.mention}, you have been verified and given the Verified role!",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Role Not Found",
                    description="Verified role does not exist. Please contact an admin.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Verification Failed",
                description=f"{ctx.author.mention}, you are not in the specified clan.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Invalid Player Tag",
            description=f"{ctx.author.mention}, player tag not found or invalid.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)



@bot.command()
async def setup(ctx):
    """
    Command to set up the "Verified" role if it does not exist.
    """
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="Verified")

    if role is None:
        await guild.create_role(name="Verified", colour=discord.Colour.green())
        embed = discord.Embed(
            title="Role Created",
            description="Verified role has been created.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Role Already Exists",
            description="Verified role already exists.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

intents = discord.Intents.default()
intents.message_content = True
bot.run(BOT_TOKEN)
