# commands/welcome.py

import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='환영')
    async def welcome(self, ctx, member: discord.Member):
        """
        특정 유저를 멘션하여 환영 메시지를 보냅니다.
        !환영 @유저이름
        """
        # 봇에게 관리자 권한이 있는지 확인
        if not ctx.guild.me.guild_permissions.manage_guild:
            await ctx.send("❗봇에게 '서버 관리' 권한이 없습니다.")
            return

        # '새로운 인원' 역할 찾기
        role = discord.utils.get(ctx.guild.roles, name="새로운 인원")
        if not role:
            await ctx.send("❗'새로운 인원' 역할이 존재하지 않습니다.")
            return

        # 역할이 이미 있는지 확인
        if role in member.roles:
            await ctx.send(f"✅ {member.display_name} 님은 이미 '새로운 인원' 역할을 가지고 있습니다.", delete_after=5)
            return

        # 역할 지급
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ {member.mention} 님, 우리 서버에 오신 것을 환영합니다! 🎉")
        except discord.Forbidden:
            await ctx.send("❗봇의 역할 권한이 부족하여 역할을 지급할 수 없습니다. 봇 역할이 '새로운 인원' 역할보다 위에 있는지 확인해주세요.")
