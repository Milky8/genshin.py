import genshin
import os
import asyncio
from log import logging
from discord_webhook import DiscordWebhook, DiscordEmbed

async def login():
    client = genshin.Client(game=genshin.Game.STARRAIL)
    client.set_cookies(ltuid=os.environ.get('43680158'), ltoken=os.environ.get('u3zMuT1RN0eou5oCMkvNom7ryYla0HyLEpdZodtU'))
    try:
        reward = await client.claim_daily_reward()
        return f'Claimed {reward.amount} x {reward.name}'
    except genshin.AlreadyClaimed:
        return f'Reward already claimed'
    except:
        return f'Error claiming reward'
        
def main(data, context):
    webhook = DiscordWebhook(url=os.environ.get('webhook'))
    response = asyncio.run(login())
    embed.set_footer(text=f'Hoyolab Auto Login ({no+1}/{len(cookies)} Executed)', icon_url='https://img-os-static.hoyolab.com/favicon.ico')
    embed.set_timestamp()
    embed.add_embed_field(name="Nickname", value=nickname)
    embed.add_embed_field(name="UID", value=uid)
    embed.add_embed_field(name="Level", value=level)
    embed.add_embed_field(name="Server", value=f'{region_name}')
    embed.add_embed_field(name="Today's rewards", value=f'{award_name} x {award_cnt}')
    embed.add_embed_field(name="Total Daily Check-In", value=total_sign_day)
    embed.add_embed_field(name="Check-in result:", value=status, inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()
