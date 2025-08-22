import discord
from discord.ext import commands
from datetime import datetime
import pytz

# 음성 채널 입장 시간을 기록할 딕셔너리
# 봇이 재시작되면 기록이 초기화됩니다.
voice_start_times = {}

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        사용자가 음성 채널에 입장하거나 퇴장할 때 시간을 기록합니다.
        """
        # 봇 자신은 무시합니다.
        if member.id == self.bot.user.id:
            return

        # 사용자가 채널에 입장했을 때
        if before.channel is None and after.channel is not None:
            # 해당 사용자의 입장 시간을 기록합니다.
            voice_start_times[member.id] = datetime.now()
            print(f'[입장 감지] {member.display_name}이(가) "{after.channel.name}"에 입장했습니다.')
        
        # 사용자가 채널에서 퇴장했을 때 (혹은 다른 채널로 이동했을 때)
        elif before.channel is not None and after.channel is None:
            # 사용자가 나간 경우에만 딕셔너리에서 시간을 삭제합니다.
            if member.id in voice_start_times:
                del voice_start_times[member.id]
                print(f'[퇴장 감지] {member.display_name}이(가) "{before.channel.name}"에서 퇴장했습니다.')

    @commands.command(name='로그')
    async def voice_log(self, ctx):
        """
        음성 채널에 접속한 모든 유저의 접속 시간을 임베드 형식으로 보여줍니다.
        """
        member = ctx.author

        # 명령어 사용자가 음성 채널에 있는지 확인합니다.
        if not member.voice or not member.voice.channel:
            await ctx.send("❗음성 채널에 접속 중이어야만 이 명령어를 사용할 수 있습니다.", delete_after=5)
            return

        voice_channel = member.voice.channel
        
        # 현재 KST(한국 표준시) 날짜 및 시간 계산
        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst)
        date_string = now_kst.strftime("%Y년 %m월 %d일 (%a) %H:%M:%S")

        # 임베드 메시지 생성
        embed = discord.Embed(
            title=f"🔊 {voice_channel.name} 음성 채널 접속 기록",
            description=f"현재 **{len(voice_channel.members)}명**이 접속 중입니다.\n**({date_string} 기준)**",
            color=0x42f5a7 # 밝은 초록색
        )

        # 명령어 사용자 접속 시간 계산 및 임베드 필드 추가
        if member.id in voice_start_times:
            start_time = voice_start_times[member.id]
            duration = datetime.now() - start_time
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            embed.add_field(
                name="👤 명령어 사용자", 
                value=f"{member.mention} : {hours}시간 {minutes}분 {seconds}초",
                inline=False
            )
        else:
            embed.add_field(
                name="👤 명령어 사용자",
                value=f"{member.mention} : 접속 기록을 찾을 수 없습니다.",
                inline=False
            )

        # "방문객" 리스트 (명령어 사용자를 제외한 모든 멤버)
        guest_list = [
            f"- {current_member.display_name}"
            for current_member in voice_channel.members
            if current_member.id != member.id
        ]

        # 방문객 목록이 있을 경우 임베드 필드 추가
        if guest_list:
            embed.add_field(
                name="👥 방문객",
                value="\n".join(guest_list),
                inline=False
            )
        
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("❗로그 기록 중 오류가 발생했습니다.", delete_after=5)
            print(f"로그 기록 오류: {e}")

async def setup(bot):
    await bot.add_cog(Logger(bot))

