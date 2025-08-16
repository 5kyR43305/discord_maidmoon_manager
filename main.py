# main.py

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv  # dotenv 라이브러리 임포트

# 24/7 구동을 위한 keep_alive.py 파일
from keep_alive import keep_alive

# 명령어 모듈 임포트
from commands.welcome import Welcome
from commands.roles import Roles
from commands.name import Name
from commands.logger import Logger

# .env 파일에서 환경 변수를 불러옵니다. 이 코드가 반드시 있어야 합니다.
load_dotenv()

# intents 설정
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# 봇 생성
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('-----------------------------------------')
    if bot.user:
        print(f'봇이 로그인했습니다: {bot.user.name} (ID: {bot.user.id})')
    else:
        print('봇이 로그인했지만 사용자 정보를 가져올 수 없습니다. 인텐트 설정을 확인해주세요.')
    print('-----------------------------------------')
    print('슬래시 커맨드 동기화 중...')
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)}개의 슬래시 커맨드가 동기화되었습니다.')
    except Exception as e:
        print(f'슬래시 커맨드 동기화 오류: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❗명령어를 다시 입력해주세요.", delete_after=5)
        if ctx.guild:
            print(f"[{ctx.guild.name}] {ctx.author} 존재하지 않는 명령어 시도: {ctx.message.content}")
        return

    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command:
            if ctx.command.name == '역할지급':
                await ctx.send("❗순서는 성별 >> 나이 순으로 작성해주세요. 나이는 '미자/성인' 중 하나여야 합니다.", delete_after=5)
            elif ctx.command.name == '이름':
                await ctx.send("❗변경할 닉네임을 입력해주세요.", delete_after=5)
            elif ctx.command.name == '환영':
                await ctx.send("❗환영 메시지를 보낼 유저를 멘션해주세요.", delete_after=5)
        return

    if isinstance(error, commands.MemberNotFound):
        await ctx.send("❗올바른 유저를 멘션했는지 확인해주세요.", delete_after=5)
        return

    if isinstance(error, discord.Forbidden):
        await ctx.send("❗봇에게 필요한 권한이 없습니다.", delete_after=5)
        return

    await ctx.send("❗명령어 실행 중 알 수 없는 오류가 발생했습니다.", delete_after=5)
    print(f"오류: {error}")

async def main():
    # Cogs를 로드합니다.
    await bot.add_cog(Welcome(bot))
    await bot.add_cog(Roles(bot))
    await bot.add_cog(Name(bot))
    await bot.add_cog(Logger(bot))

    # 24/7 구동을 위한 keep_alive 서버 실행
    keep_alive()

    # 봇 실행
    token = os.getenv('TOKEN')
    if token:
        await bot.start(token)
    else:
        print("❌ TOKEN 환경 변수가 설정되지 않았습니다.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

