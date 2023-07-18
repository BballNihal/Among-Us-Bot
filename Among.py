import discord
import os
from discord.ext import commands
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
app = Flask('')

bot_enabled = True


@bot.event
async def on_ready():
  print(f'Bot is ready. Logged in as {bot.user.name}')


@bot.event
async def on_voice_state_update(member, before, after):
  if bot_enabled:
    guild = member.guild
    voice_channel1_id = 901910274217488435
    voice_channel2_id = 906667744366317609
    voice_channel3_id = 934664474055548928
    yo_chat_channel_id = 714669144825528331
    yo_chat_channel = bot.get_channel(yo_chat_channel_id)

    if ((before.channel
         and before.channel.id in [voice_channel1_id, voice_channel2_id])
        or (after.channel
            and after.channel.id in [voice_channel1_id, voice_channel2_id])):
      channel1 = guild.get_channel(voice_channel1_id)
      channel2 = guild.get_channel(voice_channel2_id)
      channel3 = guild.get_channel(voice_channel3_id)

      total_members = sum(1 for member in channel1.members + channel2.members +
                          channel3.members if not member.bot)
      if total_members >= 9:
        await yo_chat_channel.send('It\'s AMONG US TIME!')
        destination_channel = channel3
        for voice_channel in [channel1, channel2]:
          for member in voice_channel.members:
            if not member.bot:
              await member.move_to(destination_channel)
              await destination_channel.send(
                f'@{member.mention} All members have been moved to this channel.'
              )


@bot.command()
async def toggle(ctx):
  global bot_enabled
  bot_enabled = not bot_enabled
  if bot_enabled:
    await ctx.send("Not Among us :(")
  else:
    await ctx.send("Among us!")


@app.route('/')
def home():
  return "Bot running"


def run_bot():
  bot.run(os.environ['bot_token'])


def run_flask():
  app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
  bot_thread = Thread(target=run_bot)
  bot_thread.start()

  flask_thread = Thread(target=run_flask)
  flask_thread.start()
