import discord, config, json
from discord.ext import commands

bot = commands.Bot(command_prefix = "!")

@bot.command()
async def addRole(ctx, role: discord.Role):
	role_id = role.id
	guild_id = ctx.guild.id
	file = open("roles.json", "r")
	roles = json.loads(file.read())
	try:
		in_roles = roles[str(guild_id)]
		if str(role_id) in in_roles:
			await ctx.send(f"Role {role.mention} already in moderation roles!")
		else:
			in_roles.append(str(role_id))
			roles[str(guild_id)] = in_roles
			with open("roles.json", "w") as file:
				json.dump(roles, file)
			await ctx.send(f"Role {role.mention} successfuly added!")
	except:
		roles[str(guild_id)] = [str(role_id)]
		with open("roles.json", "w") as file:
			json.dump(roles, file)
		await ctx.send(f"Role {role.mention} successfuly added!")

@bot.command()
async def mute(ctx, user: discord.Member):
	file = open("roles.json", "r")
	roless = json.loads(file.read())
	try:
		roles = roless[str(ctx.guild.id)]
		roles_id = []
		for i in ctx.author.roles:
			roles_id.append(str(i.id))
		if any(i in roles_id for i in roles):
			await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(permissions=1024))
			mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
			await user.add_roles(mute_role)
			await ctx.send(f"{user.mention} muted!")
		else:
			await ctx.send("You are not a moderator!")
	except:
		await ctx.send("You have not moderation roles")

bot.run(config.token)