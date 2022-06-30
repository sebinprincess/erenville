import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

bot = commands.Bot(command_prefix=';')

user = []
musictitle = []
song_queue = []
musicnow = []


def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"E:\크롬드라이버\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options=options)
    driver.get("https://www.youtube.com/results?search_query=" + msg + "+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()

    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com' + test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()

    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)


@bot.command()
async def 입장(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send("음성 채널에 들어갈게.")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 없으면서 부르는 거야? 음성 채널 확인해.")


@bot.command()
async def 퇴장(ctx):
    try:
        await vc.disconnect()
        await ctx.send("음성 채널에서 나갔어.")
    except:
        await ctx.send("난 이미 채널에 없어.")


@bot.command()
async def 링크재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "🎵🎶🎧", description = "현재 " + url + " 을(를) 재생하고 있어.", color = 0x00ff00))
    else:
        await ctx.send("노래는 이미 틀어져 있는데?")


@bot.command()
async def 일시정지(ctx,):
    if vc.is_playing():
        vc.pause()
        await ctx.send("재생하던 노래를 일시정지 했어.")
    else:
        await ctx.send("지금 노래가 재생되지 않고 있어.")


@bot.command()
async def 다시재생(ctx,):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않고 있어.")
    else:
         await ctx.send("재생하던 노래를 다시 틀게.")


@bot.command()
async def 중단(ctx,):
    if vc.is_playing():
        vc.stop()
        await ctx.send("노래 재생을 종료했다.")
    else:
        await ctx.send("지금 노래가 재생되지 않고 있어.")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않고 있어.")
    else:
        await ctx.send(embed = discord.Embed(title = "재생 중...", description = "현재 " + musicnow[0] + "을(를) 재생하고 있어.", color = 0x00ff00))


@bot.command()
async def 재생(ctx, *, msg):
    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        chromedriver_dir = r"E:\크롬드라이버\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=" + msg)
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com' + musicurl

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(
            embed=discord.Embed(title="🎵🎶🎧", description="현재 " + musicnow[0] + "을(를) 재생하고 있어.", color=0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이야. 새로운 노래를 재생할 수 없어.")


@bot.command()
async def 추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어.")


@bot.command()
async def 삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number) - 1]
        del musicnow[int(number) - 1 + ex]

        await ctx.send("대기열이 정상적으로 삭제되었다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없는데? 삭제할 수 없어.")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났다. 다시 확인해봐.")
            else:
                await ctx.send("숫자를 입력해줘.")


@bot.command()
async def 재생목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])

        await ctx.send(embed=discord.Embed(title="노래목록", description=Text.strip(), color=0x00ff00))


@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(
            embed=discord.Embed(title="목록초기화", description="""목록이 정상적으로 초기화되었어. 이제 노래를 다시 등록할 수 있다.""", color=0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어.")


@bot.command()
async def 목록재생(ctx):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있는데?")

@bot.command()
async def 스킵(ctx):
    if len(user) > 1:
        if vc.is_playing():
            vc.stop()
            global number
            number = 0
            await ctx.send(embed = discord.Embed(title = "스킵", description = musicnow[1] + "을(를) 다음에 재생할게.", color = 0x00ff00))
        else:
            await ctx.send("노래가 이미 재생되고 있어.")
    else:
        await ctx.send("목록에 노래가 2개 이상 없다. 중단 명령어를 사용해줘.")

bot.run('OTkxNjIzMzQ5OTMzNDQ1MTQw.G83VK8.6UWlcjS8F5dXqJQNPgBs3NAisl4c922ohnw8gA')

