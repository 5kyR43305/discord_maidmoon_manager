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

        # 각 멘션 뒤에 '님'을 붙여서 문자열 생성 (예: @5kyR4님 @rAI님 ...)
        member_mentions_with_nim = ' '.join([f'{member.mention}님' for member in members])
        
        # 각 멤버의 표시 이름 뒤에 '님'을 붙여서 문자열 생성 (예: 5kyR4님 rAI님 ...)
        member_names_with_nim = ' '.join([f'{member.display_name}님' for member in members])
        
        # 최종 환영 메시지 구성
        welcome_message = (
            f'{member_mentions_with_nim} 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍에 오신 것을 환영합니다!\n\n'
            f'{member_names_with_nim} 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍에 오신 것을 환영합니다! ⁠𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍⁠︱୨📜୧₊：규칙⸝⸝에서 규칙을 꼭 확인해주세요!\n\n'
            f'<:19:1381626681357238452> 규칙을 읽지 않아 생기는 불이익은 책임지지 않아요! 적응이 어렵다면 @알-수-없는-역할 를 맨션해주세요! 앞으로 잘 부탁드려요!\n'
            f'@알-수-없는-역할'
        )
        await ctx.send(welcome_message)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
