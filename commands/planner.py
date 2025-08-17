# commands/planner.py

import discord
from discord.ext import commands
from datetime import datetime
import sqlite3

class Planner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_name = 'plans.db'
        self.conn = None
        self.cursor = None
        self.connect_db()

    def connect_db(self):
        """데이터베이스에 연결하고 테이블을 생성합니다."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # plans 테이블이 없으면 생성합니다.
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS plans (
                    date TEXT NOT NULL,
                    name TEXT NOT NULL,
                    PRIMARY KEY (date, name)
                )
            ''')
            self.conn.commit()
            print("✅ 데이터베이스 연결 및 테이블 생성 완료")
        except sqlite3.Error as e:
            print(f"❌ 데이터베이스 오류: {e}")

    @commands.command(name='일정추가')
    async def add_plan(self, ctx, date_str: str, *, name: str):
        """
        일정을 추가합니다.
        !일정추가 YYYY-MM-DD 일정내용
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return await ctx.send("❗날짜 형식이 올바르지 않습니다. `YYYY-MM-DD` 형식으로 입력해주세요. 예: `!일정추가 2025-12-25 크리스마스 파티`", delete_after=10)

        try:
            self.cursor.execute("INSERT INTO plans (date, name) VALUES (?, ?)", (date_str, name))
            self.conn.commit()
            
            embed = discord.Embed(
                title="✅ 일정 추가 완료",
                description=f"`{date_str}`에 `{name}` 일정이 추가되었습니다.",
                color=discord.Color.from_rgb(144, 238, 144) # 연두색
            )
            await ctx.send(embed=embed)

        except sqlite3.IntegrityError:
            await ctx.send(f"❗{date_str}에 이미 `{name}` 일정이 존재합니다.", delete_after=5)
        except sqlite3.Error as e:
            await ctx.send("❗일정 추가 중 오류가 발생했습니다.", delete_after=5)
            print(f"데이터베이스 오류: {e}")

    @commands.command(name='일정제거')
    async def remove_plan(self, ctx, date_str: str, *, name: str):
        """
        일정을 제거합니다.
        !일정제거 YYYY-MM-DD 일정내용
        """
        try:
            self.cursor.execute("DELETE FROM plans WHERE date = ? AND name = ?", (date_str, name))
            self.conn.commit()

            if self.cursor.rowcount == 0:
                await ctx.send(f"❗`{date_str}`에 `{name}` 일정이 존재하지 않습니다.", delete_after=5)
            else:
                embed = discord.Embed(
                    title="✅ 일정 제거 완료",
                    description=f"`{date_str}`의 `{name}` 일정이 삭제되었습니다.",
                    color=discord.Color.from_rgb(255, 105, 97) # 붉은색
                )
                await ctx.send(embed=embed)
        except sqlite3.Error as e:
            await ctx.send("❗일정 제거 중 오류가 발생했습니다.", delete_after=5)
            print(f"데이터베이스 오류: {e}")

    @commands.command(name='일정보기')
    async def view_plans(self, ctx):
        """
        등록된 모든 일정을 보여줍니다.
        """
        self.cursor.execute("SELECT date, name FROM plans ORDER BY date ASC, name ASC")
        rows = self.cursor.fetchall()

        if not rows:
            return await ctx.send("❗현재 등록된 일정이 없습니다.", delete_after=5)

        embed = discord.Embed(
            title="📋 기획팀 일정",
            description="현재 등록된 모든 일정입니다.",
            color=discord.Color.from_rgb(173, 216, 230) # 하늘색
        )
        
        # 날짜별로 일정을 그룹화합니다.
        grouped_plans = {}
        for date, name in rows:
            if date not in grouped_plans:
                grouped_plans[date] = []
            grouped_plans[date].append(name)

        # 그룹화된 일정을 임베드 필드로 추가합니다.
        for date, events in grouped_plans.items():
            event_list = "\n".join([f"• {event}" for event in events])
            embed.add_field(name=f"📅 {date}", value=event_list, inline=False)
        
        await ctx.send(embed=embed)

    def cog_unload(self):
        """코그가 언로드될 때 데이터베이스 연결을 닫습니다."""
        if self.conn:
            self.conn.close()

# 봇에 코그(Cog)를 추가하는 함수
async def setup(bot):
    await bot.add_cog(Planner(bot))
