import discord
import json
import pyowm
from pyowm.utils import config
from pyowm.utils.config import get_default_config
from datetime import date, datetime
from discord.ext import commands
from pyowm.weatherapi25 import observation
from inspect import ArgInfo

with open("configuration.json", "r") as config: 
	data = json.load(config)
	prefix = data["prefix"]

class WeatherCog(commands.Cog, name="weather"):
	def __init__(self, bot:commands.bot):
		self.bot = bot

	@commands.command(name= "weather", description= "Getting weather info", aliases=["w"])
	async def weather(self, ctx, city:str):
			config_dict = get_default_config()
			config_dict['language'] = 'ru'
			owm = pyowm.OWM("f46cd7668657e50c31b41887016f3b65")
			weather_mgr = owm.weather_manager()
			try:
				observation = weather_mgr.weather_at_place(city)
			except: await ctx.send("Город на найден")
			else:
				weather = observation.weather
				midtemp = weather.temperature("celsius")["temp_min"]
				tempFeelsLike = weather.temperature("celsius")["feels_like"]
				speedwind = observation.weather.wind()["speed"]
				degWind = observation.weather.wind()["deg"]
				embed=discord.Embed(title=f"Погода для города {city}", color=0x2fcdcd, timestamp=ctx.message.created_at)
				embed.add_field(name="Общее состояние:", value=f"{weather.detailed_status}", inline=False)
				embed.add_field(name="Температура:", value=f"{str(midtemp)}°C, ощущается как {tempFeelsLike}°C", inline=False)
				embed.add_field(name="Скорость ветра", value=f"{speedwind} м/с, угол наклона {degWind}°", inline=False)
				embed.set_author(name="Weather", icon_url="https://image.flaticon.com/icons/png/512/252/252035.png")
				await ctx.send(embed=embed)

	@weather.error
	async def weather_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			errorEmbed = discord.Embed(title="Ошибка", color=0xf70002)
			errorEmbed.add_field(name="Пожалуйста, укажите город", value="Пример использования: weather Москва")
			await ctx.send(embed=errorEmbed)

def setup(bot:commands.Bot):
	bot.add_cog(WeatherCog(bot))