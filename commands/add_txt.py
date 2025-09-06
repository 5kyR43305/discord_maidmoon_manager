import discord
from discord.ext import commands

class TextSender(commands.Cog):
    """
    '!txtlog' 명령어 뒤에 오는 텍스트를 송출하는 Cog입니다.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='txtlog')
    async def txtlog_command(self, ctx, *, message_content: str):
        """
        '!txtlog' 명령어 뒤에 오는 모든 텍스트와 이모지를 그대로 채널에 송출합니다.
        
        파라미터:
        - ctx: 명령어 호출의 컨텍스트를 담고 있는 객체
        - message_content: 명령어 뒤에 입력된 모든 텍스트
        """
        try:
            # 명령어 뒤에 있는 내용을 그대로 송출합니다.
            await ctx.send(message_content)

        except Exception as e:
            # 예외 발생 시, 사용자에게 오류 메시지를 보냅니다.
            await ctx.send(f"❌ 오류가 발생했습니다: {e}")

    @txtlog_command.error
    async def txtlog_error(self, ctx, error):
        """
        'txtlog' 명령어 사용 시 발생하는 에러를 처리합니다.
        """
        if isinstance(error, commands.MissingRequiredArgument):
            # '!txtlog' 뒤에 아무 내용도 없을 경우, 안내 메시지를 보냅니다.
            await ctx.send("❗ 명령어 뒤에 송출하고 싶은 텍스트나 이모지를 입력해주세요.")
            
async def setup(bot):
    """
    봇에 이 Cog(확장 기능)를 추가하는 함수입니다.
    `main.py`가 이 함수를 호출하여 명령어를 로드합니다.
    """
    await bot.add_cog(TextSender(bot))
