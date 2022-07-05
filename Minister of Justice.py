from database import *
from interactions.ext.get import get
import interactions


Channel_logs = 0 #There will be logs of everything that happens
test_guild_id = 0 #Development Guild

bot = interactions.Client(token="😏")

@bot.command(
    name="choice_employee",
    description="Choice of a ministry employee",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="role",
            description="The role of the ministry employee",
            type=interactions.OptionType.ROLE,
            required=True,
        ),
    ],
)
async def choice_employee(ctx: interactions.CommandContext, role: str):
    db = AdminStaff.get_or_skip(member = (ctx.author).id)
    if ctx.author.permissions & interactions.Permissions.ADMINISTRATOR or db != None:
        db = Guilds.get_or_create(guild = ctx.guild_id)
        db.role = role.id
        db.save()
        await ctx.send(f"Employee role was added successfully", ephemeral=True)
        channel = await get(bot, interactions.Channel, channel_id=Channel_logs)
        embed = interactions.Embed(description=f'' 
                                    f'**id Guilds:** {ctx.guild_id} \n \n'
                                    f'**id new role:** {role.id} \n\n'
                                    f'**Who changed:** {ctx.author} ({(ctx.author).id})', color=0x008000)
        await channel.send('Changing the role of a ministry employee', embeds=embed)
    else:
        await ctx.send(f"You are not an admin on this discord so you can't do this.", ephemeral=True)
        channel = await get(bot, interactions.Channel, channel_id=Channel_logs)
        embed = interactions.Embed(description=f'' 
                                    f'**id Guilds:** {ctx.guild_id} \n \n'
                                    f'**id the role they tried to put:** {role.id} \n\n'
                                    f'**who tried to change:** {ctx.author} ({(ctx.author).id})', color=0x008000)
        await channel.send('Unsuccessful attempt to change the role of a ministry employee (no rights)', embeds=embed)

@bot.command(
    name="registration-of-cities",
    description="Registering a city in a bot",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="name",
            description="City name",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def registration_of_cities(ctx: interactions.CommandContext, name: str):
    db = AdminStaff.get_or_skip(member = (ctx.author).id)
    if db != None:
        db = Guilds.get_or_create(guild = ctx.guild_id)
        if db.verified == True:
            await ctx.send(f"The city is already in the system", ephemeral=True)
            return
        db.verified = True
        db.city = name
        db.number = int(str(db.guild)[15: ])
        db.save()
        await ctx.send(f"The city has been successfully added and verified", ephemeral=True)
        channel = await get(bot, interactions.Channel, channel_id=Channel_logs)
        embed = interactions.Embed(description=f'' 
                                    f'**id Guilds:** {ctx.guild_id} \n \n'
                                    f'**City name:** {db.city} \n \n'
                                    f'**id ministry roles:** {db.role} \n\n'
                                    f'**Who registered:** {ctx.author} ({(ctx.author).id})', color=0x008000)
        await channel.send('Added city to the system', embeds=embed)
    else:
        await ctx.send(f"You are not a bot admin so you can't do this", ephemeral=True)
        channel = await get(bot, interactions.Channel, channel_id=Channel_logs)
        embed = interactions.Embed(description=f'' 
                                    f'**id Guilds:** {ctx.guild_id} \n \n'
                                    f'**The name of the city they tried to verify:** {name} \n\n'
                                    f'**Who tried to register:** {ctx.author} ({(ctx.author).id})', color=0x008000)
        await channel.send('Unsuccessful attempt to verify the city (no rights)', embeds=embed)

@bot.command(
    name="registration-streets",
    description="Street registration",
    scope=test_guild_id,
    options = [
        interactions.Option(
            name="name",
            description="Street name",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def registration_streets(ctx: interactions.CommandContext, name: str):
    db2 = AdminStaff.get_or_skip(member = (ctx.author).id)
    db = Guilds.get_or_create(guild = ctx.guild_id)
    if db.verified == False:
        await ctx.send(f"City {db.city} not verified", ephemeral=True)
        return
    if db.role in ctx.author.roles or db2 != None:
        db2 = Streets.get_or_skip(name = name)
        if db2 != None:
            await ctx.send(f"street '{name}' has already.", ephemeral=True)
            return
        db3 = Streets()
        db3.name = name
        db3.number = Streets.get_number(db)
        db3.city = db
        db3.save()
        await ctx.send(f"Street '{name}' was successfully created", ephemeral=True)
        channel = await get(bot, interactions.Channel, channel_id=Channel_logs)
        embed = interactions.Embed(description=f'' 
                                    f'**id Guilds:** {ctx.guild_id} \n \n'
                                    f'**City name:** {db.city} \n \n'
                                    f'**new street:** {name} \n\n'
                                    f'**City number:** {db3.city.number} \n\n'
                                    f'**Who created:** {ctx.author} ({(ctx.author).id})', color=0x008000)
        await channel.send('Created a new street', embeds=embed)
    else:
        await ctx.send(f"You don't have rights to this", ephemeral=True)

bot.start()