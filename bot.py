import os
import traceback

from typing import TYPE_CHECKING

import discord

from discord.ext.commands import Bot, CommandNotFound
from dotenv import load_dotenv

if TYPE_CHECKING:
    from discord import Message


load_dotenv()
POKER_BOT_TOKEN = os.getenv('DISCORD_TOKEN')


class WolfoBot(Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

    async def on_ready(self):
        print("Poker bot ready!")

    async def on_message(self, message: 'Message'):
        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return
        # Ignore empty messages
        if len(message.content.split()) == 0:
            return

        # Ignore private messages
        is_private = message.channel.type == discord.ChannelType.private
        if is_private:
            return

        # If on CC, ignore other channels
        if message.guild.id == 695460634405371955:
            # horni-jail ID: 695823498009903124
            # kanjos-kasino ID: 760063437291782195
            if message.channel.id not in [695823498009903124, 760063437291782195]:
                return

        # here's the actual 'meat' of the processing
        # do not touch unless you've read the documentation
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_command_error(self, ctx, exception: 'Exception'):
        """This method handles command errors.

        Every error other than CommandNotFound is just logged into the console.
        """

        if isinstance(exception, CommandNotFound):
            await ctx.send(
                f"{ctx.message.content} is not a valid command. "
                f"Message {ctx.prefix}help to see the list of commands."
            )
            return

        # spews the exception into the console
        # invest into logging later? or maybe send a DM to the bot owner?
        traceback.print_exception(
            etype=type(exception), value=exception, tb=exception.__traceback__)


def main():
    from poker_cog import Poker
    bot = WolfoBot()
    bot.add_cog(Poker(bot))
    bot.run(POKER_BOT_TOKEN)


if __name__ == '__main__':
    main()
