from typing import Dict, TYPE_CHECKING, List

from discord.ext.commands import Cog, command

from game import Game, GAME_OPTIONS, GameState

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
        if ctx.messages:
            await ctx.send('\n'.join(ctx.messages))

    @command()
    async def newgame(self, ctx):
        """Starts a new game, allowing players to join."""
        game = ctx.game
        message = ctx.message

        if game.state == GameState.NO_GAME:
            game.new_game()
            game.add_player(message.author)
            game.state = GameState.WAITING

            ctx.messages.extend(
                [f"A new game has been started by {message.author.display_name}!",
                    "Message !join to join the game."])
        else:
            ctx.messages.append(
                "There is already a game in progress, you can't start a new game.")
            if game.state == GameState.WAITING:
                ctx.messages.append(
                    "It still hasn't started yet, so you can still message !join to join that game.")

    @command()
    async def join(self, ctx):
        """Lets you join a game that is about to begin."""

    @command()
    async def start(self, ctx):
        """Begins a game after all players have joined."""

    @command()
    async def deal(self, ctx):
        """Deals the hole cards to all the players."""

    @command()
    async def call(self, ctx):
        """Matches the current bet."""

    @command()
    async def strip(self, ctx):
        """Increases your balance .. by stripping!"""

    @command()
    async def bind(self, ctx):
        """Increases your balance .. with bondage!"""

    @command(name="raise")
    async def _raise(self, ctx):
        """Increase the size of current bet."""

    @command()
    async def check(self, ctx):
        """Bet no money."""

    @command()
    async def fold(self, ctx):
        """Discard your hand and forfeit the pot."""

    @command()
    async def options(self, ctx):
        """Show the list of options and their current values."""

    @command()
    async def set(self, ctx):
        """Set the value of an option."""

    @command()
    async def count(self, ctx):
        """Shows how many chips each player has left."""

    @command(name="all-in")
    async def all_in(self, ctx):
        """Bets the entirety of your remaining chips."""
