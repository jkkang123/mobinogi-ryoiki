import discord
from discord.ext import commands, tasks
import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']
CHANNEL_ID = 1362718703610757250
# THREAD_ID = 1372181523901579337  # <- 스레드 ID로 바꾸세요
THREAD_ID = 1372181402627346552  # <- 스레드 ID로 바꾸세요

USER_IDS = [
    255382502120620051, 370916619397890059, 355341303388831745,
    276241842708807680, 310386677048934421
]

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

KST = ZoneInfo("Asia/Seoul")

# 서버가 켜진 시간 저장 (KST 기준)
boot_time = datetime.now(KST)


# def get_now():
#     return datetime.now(KST)
#
#
# def make_mention_text():
#     mentions = ' '.join(f"<@{uid}>" for uid in USER_IDS)
#     return f"{mentions} ⏰ 곧 결계입니다! (1분 전 알림)"
#
#
# def get_next_target_time():
#     """
#     KST 기준으로, 3시부터 시작해 매 3시간마다 1분 전 알림을 계산.
#     서버 시작 시간 이후의 알림만 반환.
#     """
#     now = get_now()
#     base_times = [3, 6, 9, 12, 15, 18, 21, 0]  # 기준 시간들 (24시간제)
#
#     today = now.date()
#     schedule = []
#
#     for hour in base_times:
#         # 0시는 다음날 처리
#         if hour == 0:
#             dt = datetime.combine(today + timedelta(days=1),
#                                   datetime.min.time(),
#                                   tzinfo=KST)
#         else:
#             dt = datetime.combine(today, datetime.min.time(),
#                                   tzinfo=KST) + timedelta(hours=hour)
#
#         schedule.append(dt - timedelta(minutes=1))  # 1분 전으로
#
#     # 다음 알림 시간 찾기 (부팅 이후, 현재 이후)
#     for t in schedule:
#         if t > now and t > boot_time:
#             return t
#
#     # 못 찾으면 다음날 첫 알림 반환
#     next_day = datetime.combine(today + timedelta(days=1),
#                                 datetime.min.time(),
#                                 tzinfo=KST)
#     return next_day + timedelta(hours=3) - timedelta(minutes=1)
#
#
#
# async def reminder_loop():
#     await bot.wait_until_ready()
#
#     try:
#         thread = await bot.fetch_channel(THREAD_ID)
#     except Exception as e:
#         print(f"❌ 스레드를 찾을 수 없습니다: {e}")
#         return
#
#     while not bot.is_closed():
#         target_time = get_next_target_time()
#         wait_time = (target_time - get_now()).total_seconds()
#         print(
#             f"📢 다음 멘션 시간: {target_time.strftime('%Y-%m-%d %H:%M:%S')} (대기: {int(wait_time)}초)"
#         )
#
#         await asyncio.sleep(wait_time)
#         await thread.send(make_mention_text())
#         await asyncio.sleep(1)
#
# @bot.event
# async def on_ready():
#     print(f"{bot.user} is now online!")
#     bot.loop.create_task(reminder_loop())


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    test_mention.start()

@tasks.loop(seconds=5)
async def test_mention():
    try:
        thread = await bot.fetch_channel(THREAD_ID)
        if thread:
            await thread.send(f"<@{USER_IDS[0]}> 테스트 메시지입니다! (5초마다)")
        else:
            print("❌ 스레드를 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

keep_alive()
bot.run(TOKEN)
