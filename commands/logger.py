# commands/logger.py

import discord
from discord.ext import commands
from datetime import datetime, timedelta

# 음성 채널 입장 시간을 기록할 딕셔너리
voice_start_times = {}

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        사용자가 음성 채널에 입장하거나 퇴장할 때 시간을 기록합니다.
        """
        # 사용자가 채널에 입장했을 때
        if before.channel is None and after.channel is not None:
            voice_start_times[member.id] = datetime.now()
            print(f'[{member.guild.name}] {member.display_name} 이(가) 음성 채널 "{after.channel.name}"에 입장했습니다.')
        
        # 사용자가 채널에서 퇴장했을 때
        elif before.channel is not None and after.channel is None:
            if member.id in voice_start_times:
                # !로그 명령어로 접속 시간을 확인하도록 처리합니다.
                pass

    @commands.command(name='로그')
    async def voice_log(self, ctx):
        """
        음성 채널에 접속한 시간을 기록하고 현재 채널에 보냅니다.
        """
        member = ctx.author

        if member.voice is None or member.id not in voice_start_times:
            await ctx.send("❗음성 채널에 접속 중이거나 접속 기록이 없습니다.", delete_after=5)
            return

        # 접속 시간 계산
        start_time = voice_start_times.get(member.id)
        if start_time is None:
            await ctx.send("❗접속 시작 시간을 찾을 수 없습니다. 다시 시도해 주세요.", delete_after=5)
            return

        duration = datetime.now() - start_time
        minutes, seconds = divmod(duration.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        # 로그 메시지 생성
        log_message = (
            f"**🔊 음성 채널 접속 기록**\n\n"
            f"- **유저:** {member.mention}\n"
            f"- **접속 시간:** {hours}시간 {minutes}분 {seconds}초\n"
            f"- **채널:** {member.voice.channel.mention}"
        )

        try:
            # 명령어가 사용된 채널에 로그 전송
            await ctx.channel.send(log_message)
            await ctx.send("✅ 음성 채널 접속 기록이 현재 채널에 기록되었습니다.", delete_after=5)
        except Exception as e:
            await ctx.send("❗로그 기록 중 오류가 발생했습니다.", delete_after=5)
            print(f"로그 기록 오류: {e}")

async def setup(bot):
    await bot.add_cog(Logger(bot))
