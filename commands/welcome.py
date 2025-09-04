import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='환영')
    async def welcome_prefix(self, ctx, *members: discord.Member):
        """
        특정 멤버에게 환영 메시지를 보냅니다.
        최대 5명까지 멘션 가능합니다.
        """
        # 멘션된 멤버가 없는 경우
        if not members:
            await ctx.send("❗환영 메시지를 보낼 멤버를 멘션해주세요.")
            return

        # 멘션된 멤버가 5명을 초과하는 경우
        if len(members) > 5:
            await ctx.send("❗멘션은 최대 5명까지 가능합니다.")
            return

        # 각 멤버 멘션에 '님'을 붙여서 문자열 생성
        member_mentions = ' '.join([f'{member.mention}님' for member in members])

        welcome_message = (
            f'{member_mentions} 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍에 오신 것을 환영합니다!\n\n'
            f'<a:s10:1381626541150175332> <#1381621263730086060>에서 규칙을 꼭 확인해주세요!\n'
            f'<:19_:1381626681357238452> 규칙을 읽지 않아 생기는 불이익은 책임지지 않아요!\n\n'
            f'<a:s10:1381626541150175332> 적응이 어렵다면 <@&1381621262291570842> 를 맨션해주세요!\n\n'
            f'<:1911:1381626675489669220> 앞으로 잘 부탁드려요!\n'
            f'<@&1381621262291570844>'
        )
        await ctx.send(welcome_message)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
