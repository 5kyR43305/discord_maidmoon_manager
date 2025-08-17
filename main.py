# commands/roles.py

import discord
from discord.ext import commands
from datetime import datetime
from settings import ROLE_IDS, LOG_CHANNEL_ID

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='역할지급')
    async def add_roles_prefix(self, ctx, member: discord.Member, gender_str: str, age_str: str):
        """
        특정 멤버에게 성별, 연령대 및 기본 역할을 지급합니다.
        !역할지급 @멤버이름 남/여 성인/미자
        """
        guild = ctx.guild
        roles_to_add = []
        roles_to_remove = []

        # 봇에게 역할 관리 권한이 있는지 확인
        if not guild.me.guild_permissions.manage_roles:
            return await ctx.send("❗봇에게 '역할 관리' 권한이 없습니다.", delete_after=5)

        gender_map = {
            '남자': '남자', '남성': '남자', '남': '남자', 'ㄴ': '남자',
            '여자': '여자', '여성': '여자', '여': '여자', 'ㅇ': '여자'
        }
        age_group_map = {
            '10': '미자', '10대': '미자', '1': '미자', '미자': '미자', '미성년자': '미자', '미': '미자',
            '20': '성인', '20대': '성인', '2': '성인', '성인': '성인', '성': '성인'
        }

        normalized_gender = gender_map.get(gender_str.lower())
        if not normalized_gender:
            return await ctx.send("❗성별은 '남자/여자' 중 하나여야 합니다.", delete_after=5)

        role_id = ROLE_IDS.get(normalized_gender)
        if role_id:
            role = guild.get_role(role_id)
            if role:
                roles_to_add.append(role)

        normalized_age = age_group_map.get(age_str.lower())
        if not normalized_age:
            return await ctx.send("❗나이는 '미자/성인' 중 하나여야 합니다.", delete_after=5)

        role_id = ROLE_IDS.get(normalized_age)
        if role_id:
            role = guild.get_role(role_id)
            if role:
                roles_to_add.append(role)
        
        # '주인님' 역할 추가 (기존 로직)
        for role_key in ['주인님']:
            role_id = ROLE_IDS.get(role_key)
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    roles_to_add.append(role)
        
        # '첫방문' 역할 추가 (새로운 로직)
        first_visit_role_id = ROLE_IDS.get('첫방문')
        if first_visit_role_id:
            first_visit_role = guild.get_role(first_visit_role_id)
            if first_visit_role:
                roles_to_add.append(first_visit_role)
                
        # '미확인' 역할을 제거합니다.
        unverified_role_id = ROLE_IDS.get('미확인')
        if unverified_role_id:
            role_to_remove = guild.get_role(unverified_role_id)
            if role_to_remove and role_to_remove in member.roles:
                roles_to_remove.append(role_to_remove)

        if not roles_to_add:
            return await ctx.send("❗해당하는 역할을 찾을 수 없습니다.", delete_after=5)

        try:
            # 이미 가지고 있는 역할 제외
            existing_roles = member.roles
            new_roles = [r for r in roles_to_add if r not in existing_roles]
            if not new_roles and not roles_to_remove:
                return await ctx.send("❗이미 모든 역할이 지급되어 있습니다.", delete_after=5)

            # 역할 지급 및 제거
            if new_roles:
                await member.add_roles(*new_roles)
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)

            added_names = ", ".join([r.name for r in new_roles])
            removed_names = ", ".join([r.name for r in roles_to_remove])
            
            response = f"✅ {member.mention}님에게 역할이 지급되었습니다!"
            if added_names:
                response += f" 지급된 역할: `{added_names}`"
            if removed_names:
                response += f" 제거된 역할: `{removed_names}`"
            
            await ctx.send(response)

            # 로그 채널에 임베드 메시지 전송
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel and isinstance(log_channel, discord.TextChannel):
                embed = discord.Embed(
                    title="<a:cxr_1110:1406184343168094269> 역할 지급/제거 완료",
                    description=f"{member.display_name} 님에게 역할이 지급/제거되었습니다.",
                    color=discord.Color.from_rgb(255, 182, 193),
                    timestamp=datetime.now()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.add_field(name="관리자", value=ctx.author.mention, inline=False)
                embed.add_field(name="대상", value=member.mention, inline=False)
                if added_names:
                    embed.add_field(name="지급된 역할", value=added_names, inline=False)
                if removed_names:
                    embed.add_field(name="제거된 역할", value=removed_names, inline=False)
                embed.set_footer(text=f"ID: {member.id}")
                await log_channel.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("❗봇에게 역할 부여/제거 권한이 없습니다. 봇 역할이 지급하려는 역할들보다 위에 있는지 확인해주세요.", delete_after=5)
        except Exception as e:
            await ctx.send("❗역할 지급 중 알 수 없는 오류가 발생했습니다.", delete_after=5)
            print(f"역할 지급 오류: {e}")

# Cog를 봇에 추가하기 위한 setup 함수
async def setup(bot):
      await bot.add_cog(Roles(bot))
