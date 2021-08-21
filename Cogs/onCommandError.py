import discord
import time
import json
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, NotOwner

with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

class OnCommandErrorCog(commands.Cog, name="on command error"):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
        
	@commands.Cog.listener()
	async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
		if isinstance(error, commands.CommandOnCooldown):
			day = round(error.retry_after/86400)
			hour = round(error.retry_after/3600)
			minute = round(error.retry_after/60)
			if day > 0:
				await ctx.send('This command has a cooldown, for '+str(day)+ "day(s)")
			elif hour > 0:
				await ctx.send('This command has a cooldown, for '+str(hour)+ " hour(s)")
			elif minute > 0:
				await ctx.send('This command has a cooldown, for '+ str(minute)+" minute(s)")
			else:
				await ctx.send(f'This command has a cooldown, for {error.retry_after:.2f} second(s)')
		elif isinstance(error, CommandNotFound):
			errorEmbed = discord.Embed(title="Ошибка", description="Команда не найдена, убедитесь, что вы ввели всё правильно.\nДля вывода списка команд введите {}help".format(prefix),  color=0xf70002)
			await ctx.send(embed=errorEmbed)
		elif isinstance(error, MissingPermissions):
 			await ctx.send(error)
		elif isinstance(error, CheckFailure):
			await ctx.send(error)
		elif isinstance(error, NotOwner):
			await ctx.send(error)
		else:
			print(error) 

def setup(bot):
	bot.add_cog(OnCommandErrorCog(bot))
