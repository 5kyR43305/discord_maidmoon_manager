# main.py

import os
import discord
from discord.ext import commands
import asyncio

# intents 설정
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# 봇 생성
bot = commands.Bot(command_prefix='!', intents=intents)

# 코그(Cog)를 로드하는 함수
async def load_cogs():
    """
    commands 폴더의 모든 코그 파일들을 자동으로 로드합니다.
    """
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                # 파일명을 확장자 제외하고 가져와서 모듈 경로로 사용
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f"✅ 코그 로드 성공: {filename}")
            except Exception as e:
                print(f"❌ 코그 로드 실패: {filename} - {e}")

@bot.event
async def on_ready():
    """
    봇이 준비되면 실행되는 이벤트 핸들러
    """
    print('-----------------------------------------')
    if bot.user:
        print(f'봇이 로그인했습니다: {bot.user.name} (ID: {bot.user.id})')
    else:
        print('봇이 로그인했지만 사용자 정보를 가져올 수 없습니다.')
    print('-----------------------------------------')
    
    # 봇이 준비되면 코그를 로드합니다.
    # on_ready 이벤트가 발생할 때마다 로드되지 않도록 한 번만 실행되게 합니다.
    if not bot.extensions:
        print('모든 코그 로드 중...')
        await load_cogs()
        print('모든 코그가 로드되었습니다.')

    await bot.change_presence(activity=discord.Game(name="명령어는 !도움"))

@bot.event
async def on_command_error(ctx, error):
    """
    명령어 실행 중 오류가 발생했을 때 처리하는 이벤트 핸들러
    """
    # 오타로 인해 명령어를 찾을 수 없을 때
    if isinstance(error, commands.CommandNotFound):
        # 메시지 내용이 '!출첵'으로 시작하면 아무 메시지도 보내지 않고 종료합니다.
        if ctx.message.content.startswith('!출첵'):
            print(f"[{ctx.guild.name}] {ctx.author}의 '!출첵' 명령어는 무시되었습니다.")
            return

        # 다른 오타일 경우에만 메시지를 보냅니다.
        await ctx.send("❗명령어를 다시 입력해주세요.", delete_after=5)
        if ctx.guild:
            print(f"[{ctx.guild.name}] {ctx.author} 존재하지 않는 명령어 시도: {ctx.message.content}")
        return

    # 나머지 오류는 로그만 출력하고 메시지를 보내지 않습니다.
    print(f"명령어 실행 중 오류 발생: {error}")

# 봇 실행
if __name__ == "__main__":
    token = os.environ.get('TOKEN')
    if token:
        try:
            bot.run(token)
        except discord.errors.LoginFailure:
            print("❌ 토큰이 유효하지 않습니다. 환경 변수를 확인해주세요.")
    else:
        print("❌ TOKEN 환경 변수가 설정되지 않았습니다.")
