import discord
import asyncio
from discord.ext import commands
from settings import DICOAL_WRITER_ID, DICOAL_MENTION_ROLE_ID, DICOAL_MENTION_CHANNEL_ID

class DicoalMention(commands.Cog):
    """
    특정 메시지 감지 후 1시간 뒤에 Dicoal 멘션 메시지를 보냅니다.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        메시지가 보내질 때마다 실행되는 이벤트 리스너입니다.
        """
        # 봇 자신의 메시지는 무시합니다.
        if message.author == self.bot.user:
            return

        # Dicoal 사이트에서 자동으로 보내지는 메시지 내용을 정의합니다.
        required_content = """🔗 [서버 추천/부스트 하기](https://kr.dicoall.com/server/1381621261976731744/bump)

후원 시스템에 **월 7달러**로 이용 가능한 '활동 시 자동 UP' 기능이 추가되었습니다.
선택된 서버의 인원이 활동하면 자동으로 서버가 UP! 되는 편리한 기능입니다.
(dicoall 사이트 계정 설정에서 확인 가능합니다)"""

        # 메시지 내용, 채널, 그리고 작성자 ID를 확인합니다.
        if (str(message.author.id) == DICOAL_WRITER_ID and
                message.channel.id == DICOAL_MENTION_CHANNEL_ID and
                message.content == required_content):
            
            print("Dicoal 자동 UP 메시지를 감지했습니다. 1시간 뒤 멘션 메시지를 보낼 예정입니다.")
            
            # asyncio.sleep(3600)을 사용하여 1시간(3600초)을 기다립니다.
            await asyncio.sleep(3600)

            # 메시지를 보낼 채널과 역할을 다시 가져옵니다.
            channel = self.bot.get_channel(DICOAL_MENTION_CHANNEL_ID)
            guild = self.bot.get_guild(channel.guild.id)
            role = guild.get_role(DICOAL_MENTION_ROLE_ID)
            
            if channel and role:
                mention_content = f"{role.mention}\n서버 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍 주인님들! 서버 추천하기, 혹은 UP! 한번씩만 부탁드릴게요~"
                try:
                    # 멘션 메시지를 보냅니다.
                    await channel.send(mention_content)
                    print("1시간 지연 후 Dicoal 멘션 메시지를 성공적으로 보냈습니다.")
                except discord.Forbidden:
                    print("Dicoal 멘션 권한이 부족하여 메시지를 보낼 수 없습니다.")
                except Exception as e:
                    print(f"Dicoal 멘션 중 오류 발생: {e}")

async def setup(bot):
    """
    봇에 이 Cog(확장 기능)를 추가하는 함수입니다.
    `main.py`가 이 함수를 호출하여 명령어를 로드합니다.
    """
    await bot.add_cog(DicoalMention(bot))
