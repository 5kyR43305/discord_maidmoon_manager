# commands/logger.py

import discord
from discord.ext import commands
from datetime import datetime

# 음성 채널에 접속했던 유저 이름을 기록할 리스트
logged_users = set()

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        사용자가 음성 채널에 입장하면 이름을 기록합니다.
        """
        # 사용자가 채널에 입장했을 때
        if before.channel is None and after.channel is not None:
            # 유저 이름을 logged_users 세트에 추가
            logged_users.add(member.display_name)
            print(f'[{member.guild.name}] {member.display_name} 이(가) 음성 채널 "{after.channel.name}"에 입장했습니다.')
        
        # 사용자가 채널에서 퇴장했을 때는 별도의 동작을 하지 않습니다.
        elif before.channel is not None and after.channel is None:
            pass

    @commands.command(name='로그')
    async def voice_log(self, ctx):
        """
        음성 채팅에 접속한 적이 있는 모든 유저 목록을 보여줍니다.
        """
        # logged_users 세트가 비어있으면 메시지 전송
        if not logged_users:
            await ctx.send("❗현재까지 음성 채널에 접속한 유저가 없습니다.", delete_after=5)
            return

        # 유저 목록을 한 줄에 하나씩 정렬하여 표시
        user_list = "\n".join(sorted(list(logged_users)))
        
        # 로그 메시지 생성
        log_message = (
            f"**🔊 음성 채널 접속 기록**\n\n"
            f"**접속했던 유저 목록:**\n"
            f"```{user_list}```"
        )

        try:
            # 명령어가 사용된 채널에 로그 전송
            await ctx.send(log_message)
        except Exception as e:
            await ctx.send("❗로그 기록 중 오류가 발생했습니다.", delete_after=5)
            print(f"로그 기록 오류: {e}")

async def setup(bot):
    await bot.add_cog(Logger(bot))
