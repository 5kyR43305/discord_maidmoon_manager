import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
from settings import DICOAL_MENTION_ROLE_ID, DICOAL_MENTION_CHANNEL_ID

class DicoalMention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dicoal_mention_task.start()

    def cog_unload(self):
        self.dicoal_mention_task.cancel()

    @tasks.loop(hours=1)
    async def dicoal_mention_task(self):
        """
        KST 기준 1시간마다 Dicoal 추천 채널에 멘션을 보냅니다.
        """
        # 봇이 준비될 때까지 기다립니다.
        await self.bot.wait_until_ready()

        # Dicoal 추천 채널과 역할을 가져옵니다.
        channel = self.bot.get_channel(DICOAL_MENTION_CHANNEL_ID)
        role = self.bot.get_guild(channel.guild.id).get_role(DICOAL_MENTION_ROLE_ID)
        
        if channel and role:
            message_content = f"{role.mention}\n서버 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍 주인님들! 서버 추천하기, 혹은 UP! 한번씩만 부탁드릴게요~"
            try:
                # 멘션 메시지를 보냅니다.
                await channel.send(message_content)
                kst = pytz.timezone('Asia/Seoul')
                now_kst = datetime.now(kst).strftime("%Y년 %m월 %d일 %H시 %M분")
                print(f"[{now_kst}] Dicoal 멘션 메시지를 성공적으로 보냈습니다.")
            except discord.Forbidden:
                print("Dicoal 멘션 권한이 부족하여 메시지를 보낼 수 없습니다.")
            except Exception as e:
                print(f"Dicoal 멘션 중 오류 발생: {e}")

    @dicoal_mention_task.before_loop
    async def before_dicoal_mention_task(self):
        # 봇이 완전히 준비된 후에 루프를 시작합니다.
        await self.bot.wait_until_ready()

    @commands.command(name='dicoal_controls')
    @commands.is_owner() # 봇 소유자만 사용 가능
    async def dicoal_controls_command(self, ctx):
        """
        Dicoal 멘션 기능의 상태를 보여줍니다.
        """
        status = "실행 중" if self.dicoal_mention_task.is_running() else "중지됨"
        await ctx.send(f"Dicoal 멘션 기능이 현재 **{status}**입니다.")
        
async def setup(bot):
    await bot.add_cog(DicoalMention(bot))
