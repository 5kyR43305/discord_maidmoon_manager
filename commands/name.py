# commands/name.py

import discord
from discord.ext import commands

class Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='이름')
    async def change_nickname_prefix(self, ctx, member: discord.Member, *, new_nickname: str):
        """
        특정 멤버의 닉네임을 변경합니다.
        """
        if len(new_nickname) > 32:
            return await ctx.send("❗닉네임은 32자 이내로 입력해주세요.", delete_after=5)
        try:
            new_nick_formatted = f'『🤍』︰{new_nickname} ꒷꒦₊'
            await member.edit(nick=new_nick_formatted)
            await ctx.send(f'✨ {member.mention} 님의 닉네임이 `{new_nick_formatted}` 으로 변경되었습니다!')
        except discord.Forbidden:
            await ctx.send("❗봇에게 닉네임 변경 권한이 없습니다.", delete_after=5)
        except Exception as e:
            await ctx.send("❗닉네임 변경 중 오류가 발생했습니다.", delete_after=5)
            print(f"닉네임 변경 오류: {e}")

async def setup(bot):
    await bot.add_cog(Name(bot))
