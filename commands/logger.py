# commands/logger.py

import discord
from discord.ext import commands
from datetime import datetime, timedelta

# 음성 채널 입장 시간을 기록할 딕셔너리
voice_start_times = {}

# 음성 채널별 접속 기록을 저장할 딕셔너리
# Key: 채널 ID, Value: Set of member IDs
channel_members_history = {}

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        사용자가 음성 채널에 입장하거나 퇴장할 때 관련 기록을 업데이트합니다.
        """
        # 봇의 음성 상태는 무시합니다.
        if member.id == self.bot.user.id:
            return

        # 음성 채널에 입장했을 때
        if before.channel is None and after.channel is not None:
            voice_start_times[member.id] = datetime.now()
            print(f'[{member.guild.name}] {member.display_name} 이(가) 음성 채널 "{after.channel.name}"에 입장했습니다.')
            
            # 현재 채널에 접속한 멤버들을 기록합니다.
            if after.channel.id not in channel_members_history:
                channel_members_history[after.channel.id] = set()
            
            for m in after.channel.members:
                channel_members_history[after.channel.id].add(m.id)

        # 음성 채널에서 퇴장했을 때
        elif before.channel is not None and after.channel is None:
            if member.id in voice_start_times:
                del voice_start_times[member.id]
            print(f'[{member.guild.name}] {member.display_name} 이(가) 음성 채널 "{before.channel.name}"에서 퇴장했습니다.')

        # 채널을 이동했을 때
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:
            if member.id in voice_start_times:
                voice_start_times[member.id] = datetime.now()
            print(f'[{member.guild.name}] {member.display_name} 이(가) 음성 채널 "{before.channel.name}" 에서 "{after.channel.name}"(으)로 이동했습니다.')
            
            # 이동한 채널의 멤버들을 기록합니다.
            if after.channel.id not in channel_members_history:
                channel_members_history[after.channel.id] = set()
            
            for m in after.channel.members:
                channel_members_history[after.channel.id].add(m.id)

    @commands.command(name='로그')
    async def voice_log(self, ctx):
        """
        음성 채널에 접속한 시간을 기록하고, 한 번이라도 같이 있던 사람들을 출력합니다.
        """
        member = ctx.author

        if member.voice is None or member.voice.channel is None:
            await ctx.send("❗음성 채널에 접속 중이 아닙니다.", delete_after=5)
            return
            
        current_channel_id = member.voice.channel.id
        
        # 현재 채널의 접속 기록을 가져옵니다.
        channel_history = channel_members_history.get(current_channel_id)

        if not channel_history or len(channel_history) == 1 and list(channel_history)[0] == self.bot.user.id:
            await ctx.send("❗현재 음성 채널의 접속 기록이 없습니다.", delete_after=5)
            return

        # 봇 자신을 제외한 멤버 목록을 만듭니다.
        member_list = [
            f'<@{m_id}>'
            for m_id in channel_history
            if m_id != self.bot.user.id
        ]
        
        # 접속 시간 계산
        start_time = voice_start_times.get(member.id)
        duration = timedelta(0)
        if start_time:
            duration = datetime.now() - start_time
        
        minutes, seconds = divmod(int(duration.total_seconds()), 60)
        hours, minutes = divmod(minutes, 60)
        
        # 임베드 메시지 생성
        embed = discord.Embed(
            title=f"🔊 {member.voice.channel.name} 음성 채널 로그",
            description=f"{member.voice.channel.mention} 채널의 기록입니다.",
            color=discord.Color.from_rgb(173, 216, 230),
            timestamp=datetime.now()
        )
        
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.add_field(name="총 접속 시간", value=f"{hours}시간 {minutes}분 {seconds}초", inline=False)
        
        if member_list:
            embed.add_field(name="한 번이라도 함께 있던 사람들", value="\n".join(member_list), inline=False)
        else:
            embed.add_field(name="한 번이라도 함께 있던 사람들", value="기록된 사람이 없습니다.", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logger(bot))
