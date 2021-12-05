import os
from datetime import datetime

from discord.ext import commands

from bot import path
from cogs.events import Events
from cogs.helpers import Helpers
from sheets.sheet_tasks import SheetTasks
from db.db_management import DB

class ManagerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def manager_command_check(ctx):
        return ctx.channel.name == 'manager-commands'

    @commands.command()
    @commands.check(manager_command_check)
    async def reset_member(self, ctx, member_id):
        member = ctx.guild.get_member(int(member_id))
        await Events.on_member_remove(member)

        await Helpers.update_evaluator_availability_message(self.bot)

    @commands.command()
    @commands.check(manager_command_check)
    async def update_database_sheet(self, ctx):
        await SheetTasks.update_database_sheet()

    @commands.command()
    @commands.check(manager_command_check)
    async def update_evaluation_sheet(self, ctx):
        SheetTasks.update_evaluation_sheet()

    @commands.command()
    @commands.is_owner()
    async def view_db(self, ctx):
        members, evaluators = DB.fetch_all()

        print(members, "members")
        print(evaluators, 'evaluators')

    @commands.command()
    @commands.is_owner()
    async def reload_cogs(self, ctx):
        for file in os.listdir(path + "/cogs"):
            if file.endswith(".py"):
                self.bot.reload_extension(f"cogs.{file[:-3]}")

        print(f"Cogs reloaded successfuly on {datetime.now()}")

    @commands.command()
    @commands.is_owner()
    async def clear_evaluations(self, ctx, member_id):
        DB.remove_evaluations(int(member_id))
        
def setup(bot):
    bot.add_cog(ManagerCommands(bot))