import discord
import re
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
        서버 이모지(정적 및 움직이는 이모지)를 자동으로 변환합니다.
        
        파라미터:
        - ctx: 명령어 호출의 컨텍스트를 담고 있는 객체
        - message_content: 명령어 뒤에 입력된 모든 텍스트
        """
        try:
            # 이모지 이름 또는 ID 패턴을 찾는 정규 표현식
            # <:이름:ID>, <a:이름:ID>, :이름: 형식을 모두 처리합니다.
            emoji_pattern = re.compile(r'<a?:(\w+):(\d+)>|:(\w+):')
            
            processed_message = message_content
            
            # 메시지에서 모든 이모지 패턴을 찾습니다.
            matches = emoji_pattern.finditer(message_content)
            
            # 찾은 패턴을 순회하며 실제 이모지 객체로 변환합니다.
            for match in matches:
                # <:이름:ID> 또는 <a:이름:ID> 형식일 경우
                if match.group(1) and match.group(2):
                    emoji_name = match.group(1)
                    emoji_id = int(match.group(2))
                    found_emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name, id=emoji_id)
                    
                # :이름: 형식일 경우
                else:
                    emoji_name = match.group(3)
                    found_emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)

                if found_emoji:
                    # 이모지를 찾았다면, 텍스트 형태의 이모지를 실제 이모지 객체로 변환합니다.
                    processed_message = processed_message.replace(match.group(0), str(found_emoji), 1)

            # 메시지 내용을 2000자씩 분할하여 전송합니다.
            # 텍스트를 코드 블록에 담기 위해 ```로 시작하고 ```로 끝내도록 처리합니다.
            chunks = [processed_message[i:i + 1994] for i in range(0, len(processed_message), 1994)]
            
            for chunk in chunks:
                await ctx.send(f"```\n{chunk}\n```")

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
