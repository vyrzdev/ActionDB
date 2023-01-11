from os import environ
import discord
import asyncio


intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)
discord_token = environ.get("DISCORDTOKEN")
discord_guild_id = environ.get("DISCORDGUILDID")
discord_channel_id = environ.get("DISCORDCHANNELID")

try:
    with open('./execution_history.txt', 'r') as execution_history_handle:
        execution_history = [batch.strip("\n") for batch in execution_history_handle.readlines()]
except FileNotFoundError:
    execution_history = list()


async def do():
    print("Waiting for login;")
    guild = None
    while guild is None:
        guild = discord_client.get_guild(int(discord_guild_id))
        await asyncio.sleep(0.5)
    channel = guild.get_channel(int(discord_channel_id))
    print("Bot logged in, channel obj acquired.")

    async for message in channel.history(limit=1):
        if message.content.startswith('batch'):
            if str(message.id) not in execution_history:
                content = message.content.split('```')[1]
                execution_history.append(str(message.id))
                with open('journal.txt', 'a') as journal_handle:
                    if not content.endswith("\n"):
                        content = content + "\n"
                    if content.startswith("\n"):
                        content = content.removeprefix("\n")
                    journal_handle.write(content)
                with open('./execution_history.txt', 'w') as execution_history_handle:
                    execution_history_handle.seek(0)
                    execution_history_handle.writelines([execution + '\n' for execution in execution_history])
        if message.content.startswith('delete'):
            if str(message.id) not in execution_history:
                n = message.content.split(" ")[1]
                execution_history.append(str(message.id))
                with open('journal.txt', 'r+') as journal_handle:
                    journal_lines = journal_handle.readlines()
                    journal_lines = journal_lines[:-int(n)]
                    journal_handle.seek(0)
                    journal_handle.truncate(0)
                    journal_handle.writelines(journal_lines)
                with open('./execution_history.txt', 'w') as execution_history_handle:
                    execution_history_handle.seek(0)
                    execution_history_handle.writelines([execution + '\n' for execution in execution_history])


@discord_client.event
async def on_ready():
    print("Logged into discord")


async def main():
    asyncio.create_task(discord_client.start(discord_token))
    await do()

asyncio.run(main())