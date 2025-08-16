# commands/name.py

import discord
from discord.ext import commands

class Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='이름')
    async def change_name(self, ctx, *, new_name: str):
        """
        자신의 닉네임을 변경합니다.
        !이름 [새로운 닉네임]
        """
        # 봇에게 닉네임 관리 권한이 있는지 확인
        if not ctx.guild.me.guild_permissions.change_nickname:
            await ctx.send("❗봇에게 '닉네임 변경' 권한이 없습니다.")
            return
            
        try:
            # 닉네임 변경
            await ctx.author.edit(nick=new_name)
            await ctx.send(f"✅ {ctx.author.mention} 님의 닉네임이 '{new_name}'(으)로 변경되었습니다.", delete_after=5)
        except discord.Forbidden:
            await ctx.send("❗봇의 권한이 부족하여 닉네임을 변경할 수 없습니다.")
