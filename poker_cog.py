from typing import Dict, TYPE_CHECKING

from discord.ext.commands import Cog, command

from game import Game
import poker_func as pf


if TYPE_CHECKING:
    from discord import TextChannel
    from discord.ext.commands import Context


class Poker(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.games: Dict['TextChannel', Game] = {}

    async def cog_before_invoke(self, ctx: 'Context'):
        """Is invoked before every command in this cog.

        Ensures that there is an instance of the Game in the games dictionary.
        At the same time, plays around with the Context instance,
            adding some useful attributes and methods.
        """
        ctx.game = self.games.setdefault(ctx.channel, Game())
        ctx.messages = []

    async def cog_after_invoke(self, ctx):
        """Automatically sends out the messages, if there are any."""
        if ctx.messages:
            await ctx.send('\n'.join(ctx.messages))

    @command(name="newgame")
    async def new_game(self, ctx):
        """Starts a new game, allowing players to join."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.new_game(game, message, ctx)

    @command()
    async def join(self, ctx):
        """Lets you join a game that is about to begin."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.join_game(game, message, ctx)

    @command()
    async def start(self, ctx):
        """Begins a game after all players have joined.

        So long as one hasn't already started, and there are enough players joined to play.
        """
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.start_game(game, message, ctx)

    @command()
    async def deal(self, ctx):
        """Deals the hole cards to all the players."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.deal_hand(game, message, ctx)

        if ctx.messages[0] == 'The hands have been dealt!':
            await game.tell_hands()

    @command()
    async def call(self, ctx):
        """Matches the current bet."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.call_bet(game, message, ctx)

    @command()
    async def strip(self, ctx):
        """Increases your balance .. by stripping!"""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.strip_bet(game, message, ctx)

    @command()
    async def bind(self, ctx):
        """Increases your balance .. with bondage!"""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.bind_bet(game, message, ctx)

    @command(name="raise")
    async def _raise(self, ctx):
        """Increase the size of current bet."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.raise_bet(game, message, ctx)

    @command()
    async def check(self, ctx):
        """Bet no money."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.check(game, message, ctx)

    @command()
    async def fold(self, ctx):
        """Discard your hand and forfeit the pot."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.call_bet(game, message, ctx)

    @command()
    async def options(self, ctx):
        """Show the list of options and their current values."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.show_options(game, message)

    @command()
    async def set(self, ctx):
        """Set the value of an option."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.set_option(game, message, ctx)

    @command()
    async def count(self, ctx):
        """Shows how many chips each player has left."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.chip_count(game)

    @command(name="all-in")
    async def all_in(self, ctx):
        """Bets the entirety of your remaining chips."""
        game = ctx.game
        message = ctx.message
        ctx.messages = pf.all_in(game, message, ctx)
