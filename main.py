import discord
import json
import os
import pyowm
from discord import embeds
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, NotOwner
from pyowm.utils.config import get_default_config
from datetime import date, datetime
from inspect import ArgInfo

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="за вами"))

	bot.remove_command('help')
	@bot.command(pass_context = True)
	async def help(ctx):
		embed=discord.Embed(title="Список команд", color=0x3ee08c)
		embed.add_field(name="{}calculate".format(prefix), value="Простой калькулятор", inline=False)
		embed.add_field(name="{}help".format(prefix), value="Выводит данное сообщение", inline=False)
		embed.add_field(name="{}ping".format(prefix), value="Выводит задержку между ботом и сервером", inline=False)
		embed.add_field(name="{}weather [город]".format(prefix), value="Показывает погоду в указанном вами городе", inline=False)
		embed.add_field(name="{}avatar [@user]".format(prefix), value="Показывает аватар указанного пользователя", inline=False)
		embed.set_author(name="Vladik2001", icon_url=bot.user.avatar_url)
		await ctx.send(embed=embed)

@bot.command(pass_context = True)
async def calculate(ctx, *, nums: str):
	math_expression = nums
	if 'os' not in math_expression:
		try:
    			result = eval(math_expression)
		except ZeroDivisionError:
			await ctx.send("Деление на 0 невозможно!")
		else: 
			await ctx.send("Результат: %s = %s" % (math_expression, result))

@bot.command(pass_context = True)
async def weather(ctx, city: str):
	place = city
	config_dict = get_default_config()
	config_dict['language'] = 'ru'
	owm = pyowm.OWM("f46cd7668657e50c31b41887016f3b65")
	weather_mgr = owm.weather_manager()
	try:
		observation = weather_mgr.weather_at_place(place)
	except: await ctx.send("Город не найден")
	else:
		weather = observation.weather
	weather.status          
	weather.detailed_status
	midtemp =  weather.temperature("celsius")["temp_min"]
	tempFeelsLike = weather.temperature("celsius")["feels_like"]
	speedwind = observation.weather.wind()["speed"]
	degWind = observation.weather.wind()["deg"]
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	embed=discord.Embed(title=f"Погода для города {city}", color=0x2fcdcd)
	embed.add_field(name="Общее состояние:", value=f"{weather.detailed_status}", inline=False)
	embed.add_field(name="Температура:", value=f"{str(midtemp)}°C, ощущается как {tempFeelsLike}°C", inline=False)
	embed.add_field(name="Скорость ветра", value=f"{speedwind} м/с, угол наклона {degWind}°", inline=False)
	embed.set_author(name="Weather", icon_url="https://image.flaticon.com/icons/png/512/252/252035.png")
	embed.set_footer(text=f"Текущее время: {dt_string}")
	await ctx.send(embed=embed)

@weather.error
async def weather_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		errorEmbed = discord.Embed(title="Ошибка", color=0xf70002)
		errorEmbed.add_field(name="Пожалуйста, укажите город", value="Пример использования: {}weather Москва".format(prefix))
		await ctx.send(embed=errorEmbed)


@calculate.error
async def calculate_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		errorEmbed = discord.Embed(title="Ошибка", color=0xf70002)
		errorEmbed.add_field(name="Пожалуйста, укажите аргументы вычисления", value="Пример использования: {}calculate 2 + 2".format(prefix))
		await ctx.send(embed=errorEmbed)

bot.run(token)
	