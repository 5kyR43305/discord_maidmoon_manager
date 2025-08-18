# commands/vacation.py

import discord
import os
from discord.ext import commands
from datetime import datetime

class Vacation(commands.Cog):
    """
    휴가 관리를 위한 명령어들을 모아놓은 Cog입니다.
    !휴가생성, !휴가반납, !휴가연장 기능을 제공합니다.
    """
    def __init__(self, bot):
        self.bot = bot
        # 환경 변수에서 5kyr4 유저 ID와 휴가 채널 ID를 가져옵니다.
        # ID가 숫자인지 확인하고 int형으로 변환합니다.
        try:
            self._5kyr4_user_id = int(os.getenv('SKILA_USER_ID'))
            self.vacation_channel_id = int(os.getenv('VACATION_CHANNEL_ID'))
        except (ValueError, TypeError):
            print("❗[환경 변수 오류] SKILA_USER_ID 또는 VACATION_CHANNEL_ID가 없거나 올바르지 않습니다.")
            self._5kyr4_user_id = None
            self.vacation_channel_id = None

    async def cog_check(self, ctx):
        # 5kyr4님(본인) 또는 '관리국' 역할을 가진 사용자만 사용 가능
        required_role_name = '관리국'
        has_required_role = any(role.name == required_role_name for role in ctx.author.roles)
        is_5kyr4 = ctx.author.id == self._5kyr4_user_id
        
        if not is_5kyr4 and not has_required_role:
            await ctx.send(f"❗{ctx.author.mention}님, 이 명령어는 5kyr4님 또는 '{required_role_name}' 역할을 가진 사용자만 사용할 수 있습니다.", delete_after=10)
            return False
        return True

    async def _send_log_and_dm(self, ctx, action, title, description, color, duration=None, reason=None):
        """
        휴가 로그를 채널에 전송하고 5kyr4님에게 DM을 보냅니다.
        """
        if self._5kyr4_user_id is None or self.vacation_channel_id is None:
            await ctx.send("❗봇의 환경 설정이 올바르지 않아 명령어를 실행할 수 없습니다.", delete_after=10)
            return

        # 5kyr4 유저와 휴가 채널을 찾습니다.
        _5kyr4_user = self.bot.get_user(self._5kyr4_user_id)
        vacation_channel = self.bot.get_channel(self.vacation_channel_id)
        
        # 로그 채널에 보낼 임베드 생성
        log_embed = discord.Embed(
            title=title,
            description=f"**대상:** {ctx.author.mention}",
            color=color,
            timestamp=datetime.now()
        )
        if duration:
            log_embed.add_field(name="기간", value=duration, inline=True)
        if reason:
            log_embed.add_field(name="사유", value=reason, inline=True)

        log_embed.set_footer(text=f"요청자 ID: {ctx.author.id}")
        
        if vacation_channel:
            await vacation_channel.send(embed=log_embed)
        else:
            print("❌ 휴가 로그 채널을 찾을 수 없습니다.")

        # 5kyr4님에게 보낼 DM 메시지
        dm_message = f"**{ctx.author.name}**님이 **{action}**을 요청했습니다.\n"
        if duration:
            dm_message += f"**기간:** {duration}\n"
        if reason:
            dm_message += f"**사유:** {reason}\n"
        dm_message += "확인하고 필요한 조치를 취해주세요."

        if _5kyr4_user:
            try:
                await _5kyr4_user.send(dm_message)
                await ctx.send(f"✅ 휴가 요청이 5kyr4님에게 전달되었습니다.", delete_after=10)
            except discord.Forbidden:
                await ctx.send("❗5kyr4님의 DM이 막혀있어 메시지를 보낼 수 없습니다.", delete_after=10)
        else:
            await ctx.send("❗5kyr4님을 찾을 수 없습니다. 사용자 ID가 올바른지 확인해주세요.", delete_after=10)

    @commands.command(name='휴가생성')
    async def create_vacation(self, ctx, duration: str, *, reason: str):
        """
        휴가를 신청합니다.
        !휴가생성 (기간) (사유)
        예시: !휴가생성 3일 개인 사정
        """
        title = "📋 휴가 생성 요청"
        color = discord.Color.from_rgb(144, 238, 144) # 연한 초록색
        await self._send_log_and_dm(ctx, "휴가 생성", title, None, color, duration, reason)
        
    @commands.command(name='휴가반납')
    async def return_vacation(self, ctx):
        """
        휴가를 반납합니다.
        !휴가반납
        """
        title = "🔄 휴가 반납 요청"
        color = discord.Color.from_rgb(255, 105, 97) # 연한 빨강색
        await self._send_log_and_dm(ctx, "휴가 반납", title, "본인 의사에 의한 휴가 반납", color)

    @commands.command(name='휴가연장')
    async def extend_vacation(self, ctx, duration: str, *, reason: str):
        """
        휴가를 연장합니다.
        !휴가연장 (기간) (사유)
        예시: !휴가연장 1주 추가 작업
        """
        title = "📅 휴가 연장 요청"
        color = discord.Color.from_rgb(173, 216, 230) # 연한 파랑색
        await self._send_log_and_dm(ctx, "휴가 연장", title, None, color, duration, reason)

# Cog를 봇에 추가하기 위한 setup 함수
async def setup(bot):
    await bot.add_cog(Vacation(bot))
