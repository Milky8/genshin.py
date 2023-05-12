import genshin
import os
import asyncio
import typing
from genshin import types, utility
from genshin.client import cache as client_cache
from genshin.client import routes
from genshin.client.components import base
from genshin.client.manager import managers
from genshin.models import hoyolab as models
from discord_webhook import DiscordWebhook, DiscordEmbed

global trewards

def recognize_starrail_server(uid: int) -> str:
    """Recognize which server a Star Rail UID is from."""
    server = {
        "1": "prod_gf_cn",
        "2": "prod_gf_cn",
        # "5": unknown if this exists at the moment. pattern would imply "prod_qd_cn"
        "6": "prod_official_usa",
        "7": "prod_official_eur",
        "8": "prod_official_asia",
        "9": "prod_official_cht",
    }.get(str(uid)[0])

    if server:
        return server

    raise ValueError(f"UID {uid} isn't associated with any server")


async def login():
    client = genshin.Client(game=genshin.Game.STARRAIL)
    client.set_cookies(ltuid=43680158, ltoken='u3zMuT1RN0eou5oCMkvNom7ryYla0HyLEpdZodtU')
    global trewards
    signed_in, claimed_rewards = await client.get_reward_info()
    try:
        reward = await client.claim_daily_reward()
    except genshin.AlreadyClaimed:
        trewards = claimed_rewards
        print(f"Daily reward already claimed ")
    except:
        trewards = claimed_rewards
        print(f"Claimed {reward.amount} x {reward.name}")
    else:
        print(f'Error claiming reward')

async def main():
    client = genshin.Client(game=genshin.Game.STARRAIL)
    client.set_cookies(ltuid=43680158, ltoken='u3zMuT1RN0eou5oCMkvNom7ryYla0HyLEpdZodtU')
    signed_in, claimed_rewards = await client.get_reward_info()
    trewards = claimed_rewards
    accounts = await client.get_game_accounts()
    for account in accounts:
        if account.uid == 600192311 and account.level >=17: 
            uid = account.uid
            level = account.level
    nickname = 'Milky'
    region_name = recognize_starrail_server(uid)
    if region_name == "prod_official_usa":
        region_name = "NA"
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1101980521254359171/X8c8oPDWsCyazJHU5dVHfcNPZ7fTEjdbH8QE3AtBCYlexevZaBG2bKLLRFcUUQLsDa7A')
    embed = DiscordEmbed(title='Honkai: Star Rail Auto Login', description=' ', color='ffccff')
    embed.set_footer(text=f'Honkai: Star Rail Auto Login Executed', icon_url='https://img-os-static.hoyolab.com/favicon.ico')
    embed.set_timestamp()
    embed.add_embed_field(name="Nickname", value=nickname)
    embed.add_embed_field(name="UID", value=uid)
    embed.add_embed_field(name="Level", value=level)
    embed.add_embed_field(name="Server", value=f'{region_name}')
    async for reward in client.claimed_rewards(limit=1):
        embed.add_embed_field(name="Today's rewards", value=f'{reward.amount} x {reward.name}')  
    embed.add_embed_field(name="Monthly Check-ins", value= f'{trewards} days')   
    webhook.add_embed(embed)
    response = webhook.execute()
    exit(0)

asyncio.run(login())
asyncio.run(main())
