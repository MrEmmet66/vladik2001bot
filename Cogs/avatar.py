import discord
from discord.ext import commands

class AvatarCog(commands.Cog, name="get avatar command"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
        
	@commands.command(name = "avatar", description = "Get user avatar", aliases=["a", "ava"])
	async def avatar(self, ctx, member: discord.Member = None):
            if member is None:
                member = ctx.author
            avatarEmbed = discord.Embed(title=f"Avatar of user {member.name}", timestamp=ctx.message.created_at, color=0x3ee08c)
            avatarEmbed.set_image(url=member.avatar_url)
            await ctx.send(embed = avatarEmbed)

def setup(bot:commands.Bot):
	bot.add_cog(AvatarCog(bot))