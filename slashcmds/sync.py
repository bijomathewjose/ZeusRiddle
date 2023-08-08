import discord
from discord import app_commands

async def setup(bot):
    @app_commands.command(name="sync_database")
    async def sync_from_db(interaction: discord.Interaction):
        
        await interaction.response.send_message("Syncing Database")
        
    @app_commands.command(name="sync_discord")
    async def sync_from_discord(interaction: discord.Interaction):
        await interaction.response.send_message("Syncing Discord",ephemeral=True)
        
    bot.tree.add_command(sync_from_db)
    bot.tree.add_command(sync_from_discord)