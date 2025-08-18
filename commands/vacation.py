# commands/vacation.py

import discord
from discord.ext import commands
from datetime import datetime
from settings import SKILA_USER_ID, VACATION_CHANNEL_ID, MANAGEMENT_ROLE_ID

class Vacation(commands.Cog):
    """
    휴가 관리를 위한 명령어들을 모아놓은 Cog입니다.
    !휴가요청, !휴가반납, !휴가연장 기능을 제공합니다.
    """
    def __init__(self, bot):
        self.bot = bot
        # settings.py에서 직접 ID 값들을 가져옵니다.
        self._5kyr4_user_id = SKILA_USER_ID
        self.vacation_channel_id = VACATION_CHANNEL_ID
        self.management_role_id = MANAGEMENT_ROLE_ID
        # 처리 대기 중인 요청을 저장하는 딕셔너리입니다.
        # { DM 메시지 ID: {'user_id': 요청자 ID, 'action': 요청 유형, ...} }
        self.pending_requests = {}

    async def cog_check(self, ctx):
        # 5kyr4님(본인) 또는 '관리국' 역할을 가진 사용자만 사용 가능
        management_role = ctx.guild.get_role(self.management_role_id)
        
        if not management_role:
            await ctx.send("❗'관리국' 역할이 서버에 존재하지 않습니다. 관리국 역할을 올바르게 설정해주세요.", delete_after=10)
            return False

        has_required_role = management_role in ctx.author.roles
        is_5kyr4 = ctx.author.id == self._5kyr4_user_id
        
        if not is_5kyr4 and not has_required_role:
            await ctx.send(f"❗{ctx.author.mention}님, 이 명령어는 5kyr4님 또는 '{management_role.name}' 역할을 가진 사용자만 사용할 수 있습니다.", delete_after=10)
            return False
        return True

    async def _send_log_and_dm(self, ctx, action, title, description, color, duration=None, reason=None):
        """
        휴가 요청을 5kyr4님에게 DM으로 보냅니다.
        """
        _5kyr4_user = self.bot.get_user(self._5kyr4_user_id)
        vacation_channel = self.bot.get_channel(self.vacation_channel_id)
        
        # 봇이 5kyr4님을 찾을 수 없거나 로그 채널이 없는 경우 오류 처리
        if not _5kyr4_user or not vacation_channel:
            await ctx.send("❗봇의 환경 설정이 올바르지 않아 명령어를 실행할 수 없습니다. 5kyr4 유저 ID 또는 휴가 채널 ID를 확인해주세요.", delete_after=10)
            return

        # 5kyr4님에게 보낼 DM 메시지 임베드 생성
        dm_embed = discord.Embed(
            title=title,
            description=f"**요청자:** {ctx.author.mention}",
            color=color,
            timestamp=datetime.now()
        )
        if duration:
            dm_embed.add_field(name="기간", value=duration, inline=True)
        if reason:
            dm_embed.add_field(name="사유", value=reason, inline=False)
        dm_embed.set_footer(text=f"요청자 ID: {ctx.author.id}")

        try:
            dm_message = await _5kyr4_user.send(
                f"{_5kyr4_user.mention}님, **{ctx.author.name}**님의 휴가 관련 요청입니다.",
                embed=dm_embed
            )
            # DM 메시지에 ✅와 ❌ 이모지 추가
            await dm_message.add_reaction("✅")
            await dm_message.add_reaction("❌")
            
            # 처리 대기 중인 요청 딕셔너리에 추가
            self.pending_requests[dm_message.id] = {
                'requester_id': ctx.author.id,
                'action': action,
                'title': title,
                'description': description,
                'duration': duration,
                'reason': reason
            }
            await ctx.send(f"✅ 휴가 요청이 5kyr4님에게 전달되었습니다.", delete_after=10)

        except discord.Forbidden:
            await ctx.send("❗5kyr4님의 DM이 막혀있어 메시지를 보낼 수 없습니다.", delete_after=10)
        except Exception as e:
            await ctx.send("❗요청 처리 중 알 수 없는 오류가 발생했습니다.", delete_after=10)
            print(f"휴가 요청 오류: {e}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # 봇이 남긴 반응이 아니고, 5kyr4님이 반응한 경우에만 처리
        if user.bot or user.id != self._5kyr4_user_id:
            return

        # 반응이 DM 채널에서 발생했고, 처리 대기 중인 요청인 경우
        if isinstance(reaction.message.channel, discord.DMChannel) and reaction.message.id in self.pending_requests:
            
            request_data = self.pending_requests[reaction.message.id]
            requester_id = request_data['requester_id']
            action = request_data['action']

            # 요청자 멘션 정보 가져오기
            requester = self.bot.get_user(requester_id)
            requester_mention = requester.mention if requester else f"ID: {requester_id}"
            
            vacation_channel = self.bot.get_channel(self.vacation_channel_id)
            
            # 로그 메시지 임베드 생성
            log_embed = discord.Embed(timestamp=datetime.now())
            log_embed.add_field(name="요청자", value=requester_mention, inline=False)
            log_embed.add_field(name="요청 유형", value=action, inline=False)
            
            if reaction.emoji == "✅":
                log_embed.title = f"✅ {requester.name}님의 {action} 승인"
                log_embed.color = discord.Color.green()
                log_embed.description = "요청이 승인되었습니다."
            elif reaction.emoji == "❌":
                log_embed.title = f"❌ {requester.name}님의 {action} 거절"
                log_embed.color = discord.Color.red()
                log_embed.description = "요청이 거절되었습니다."
            else:
                return # ✅나 ❌ 이모지가 아니면 무시

            # 휴가 채널에 로그 메시지 전송
            if vacation_channel:
                await vacation_channel.send(embed=log_embed)
            
            # 요청 처리 완료 후 딕셔너리에서 삭제
            del self.pending_requests[reaction.message.id]
            
            # DM의 이모지 제거하여 처리 완료를 시각적으로 표시
            try:
                await reaction.message.clear_reactions()
                await reaction.message.edit(content="✅ 이 요청은 처리되었습니다.")
            except discord.Forbidden:
                print("❗DM 메시지 이모지 제거 권한이 없습니다.")

    @commands.command(name='휴가요청')
    async def create_vacation(self, ctx, duration: str, *, reason: str):
        """
        휴가를 신청합니다.
        !휴가요청 (기간) (사유)
        예시: !휴가요청 3일 개인 사정
        """
        title = "📋 휴가 요청"
        color = discord.Color.from_rgb(144, 238, 144)
        await self._send_log_and_dm(ctx, "휴가 요청", title, None, color, duration, reason)
        
    @commands.command(name='휴가반납')
    async def return_vacation(self, ctx):
        """
        휴가를 반납합니다.
        !휴가반납
        """
        title = "🔄 휴가 반납 요청"
        color = discord.Color.from_rgb(255, 105, 97)
        await self._send_log_and_dm(ctx, "휴가 반납", title, "본인 의사에 의한 휴가 반납", color)

    @commands.command(name='휴가연장')
    async def extend_vacation(self, ctx, duration: str, *, reason: str):
        """
        휴가를 연장합니다.
        !휴가연장 (기간) (사유)
        예시: !휴가연장 1주 추가 작업
        """
        title = "📅 휴가 연장 요청"
        color = discord.Color.from_rgb(173, 216, 230)
        await self._send_log_and_dm(ctx, "휴가 연장", title, None, color, duration, reason)

# Cog를 봇에 추가하기 위한 setup 함수
async def setup(bot):
    await bot.add_cog(Vacation(bot))
