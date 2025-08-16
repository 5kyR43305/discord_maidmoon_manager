# commands/roles.py

import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='역할지급')
    async def assign_role(self, ctx, gender: str, age: str):
        """
        성별과 나이에 따라 역할을 지급합니다.
        !역할지급 [남/여] [성인/미자]
        """
        # 봇에게 역할 관리 권한이 있는지 확인
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send("❗봇에게 '역할 관리' 권한이 없습니다.")
            return

        gender = gender.lower()
        age = age.lower()

        # 성별 역할 결정
        gender_role_name = None
        if gender == '남':
            gender_role_name = '남자'
        elif gender == '여':
            gender_role_name = '여자'
        else:
            await ctx.send("❗성별은 '남' 또는 '여'로 입력해주세요.")
            return

        # 나이 역할 결정
        age_role_name = None
        if age == '성인':
            age_role_name = '성인'
        elif age == '미자':
            age_role_name = '미성년자'
        else:
            await ctx.send("❗나이는 '성인' 또는 '미자'로 입력해주세요.")
            return

        # 역할 찾기
        gender_role = discord.utils.get(ctx.guild.roles, name=gender_role_name)
        age_role = discord.utils.get(ctx.guild.roles, name=age_role_name)

        if not gender_role or not age_role:
            await ctx.send("❗필요한 역할이 서버에 존재하지 않습니다.")
            return

        # 역할 지급
        try:
            await ctx.author.add_roles(gender_role, age_role)
            await ctx.send(f"✅ {ctx.author.mention} 님에게 '{gender_role_name}'과 '{age_role_name}' 역할이 지급되었습니다.", delete_after=5)
            
            # '새로운 인원' 역할 제거
            new_member_role = discord.utils.get(ctx.guild.roles, name="새로운 인원")
            if new_member_role and new_member_role in ctx.author.roles:
                await ctx.author.remove_roles(new_member_role)

        except discord.Forbidden:
            await ctx.send("❗봇의 역할 권한이 부족하여 역할을 지급할 수 없습니다. 봇 역할이 지급하려는 역할들보다 위에 있는지 확인해주세요.")
