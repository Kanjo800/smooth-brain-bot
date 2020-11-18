# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )



@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


 
@bot.command(name='give_elf_tea', help='gives the best beverage to the elf')
async def give_elf_tea(ctx):
    give_elf_tea = [
        '*sips*',
        '*pats*',
    ]

    response = random.choice(give_elf_tea)
    await ctx.send(response)

@bot.command(name='give_elf_coffee', help='gives the worst beverage to the elf')
async def give_elf_coffee(ctx):
    give_elf_coffee = [
        '*elf grrrrr*',
        '**spank**',
    ]

    response = random.choice(give_elf_coffee)
    await ctx.send(response)



bot.run(TOKEN)