import discord
import asyncio
import random
import os

intents = discord.Intents.default()
client = discord.Client()


@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("조달")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.content.startswith("에렌빌 안녕"):
        await message.channel.send("안녕. 잘 지내?")

    if message.content.startswith("에렌빌 뭐해"):
        await message.channel.send("조달한다. 당신은 단골 거래 수주권 태우기 백화작 자화작 음식 및 장비 제작 크리스탈 및 재료 채집 다 했지?")

    if message.content.startswith("에렌빌 공지"):
        await message.channel.send("https://discord.com/channels/991610817856425997/991615156335427624/991720865769201785")

    if message.content.startswith("에렌빌 도움말"):
        await message.channel.send("**수상한 조달꾼** 명령어 모음: https://posty.pe/sfi4mx")

    if message.content.startswith("에렌빌 바보"):
        await message.channel.send("그 말 할 시간에 생산적인 일을 하나 더 하겠어.")

    if message.content.startswith("에렌빌 초대링크"):
        await message.channel.send("https://discord.gg/GR3EpVGGMR")

    if message.content.startswith("에렌빌 에렌빌"):
        await message.channel.send("왜 불러.")

    if message.content.startswith("에렌빌 심심해"):
        await message.channel.send("가서 할 일 해.")

    if message.content.startswith(";주사위"):
        roll = message.content.split(" ")
        rolld = roll[1].split ("d")
        dice = 0
        for i in range(1, int(rolld[0])+1):
            dice = dice + random.randint(1, int(rolld[1]))
        await message.channel.send(str(dice))

    if message.content.startswith(";골라줘"):
        choice = message.content.split(" ")
        choicenumber = random.randint(1, len(choice) - 1)
        choiceresult = choice[choicenumber]
        await message.channel.send(choiceresult)

    if message.content.startswith("HQ"):
        pic = message.content.split(" ")[1]
        await message.channel.send(file=discord.File(pic))

    if message.content.startswith("에렌빌 전해줘"):
        channel = message.content[8:26]
        msg = message.content[27:]
        await client.get_channel(int(channel)).send(msg)


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
