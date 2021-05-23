import discord
from discord.ext import commands
from discord.ext.commands import Bot
from json import load
from datetime import datetime
import enum


client = commands.Bot("-")
client.remove_command("help")
utils = discord.utils
utc = datetime.utcnow()

#client = discord.Client()

text = """
    **• -help** --> Shows this msg

    **--- Clear commands ---**
    **• -delete** --> _Delete msgs from CCleaner_
    **• -clear <symbol>** --> _Delete msgs that starts with_ <symbol>
    **• -Botclean** --> _Delete msgs from Bots_

    **--- Roles commands ---**
    **• -addrole <RoleName> <R> <G> <B>** --> _Create a role with RGB colour tuple and_ @everyone _permissions_
        [Default <RoleName> set to "role" and <R><G><B> colour set to 0 0 0, IMPORTANT the spaces between R G B values]
    **• -joinrole <RoleName> <@Someone>** --> _If there is No one, the evoker of the command joins the role_ <RoleName>_, If not_ <@Someone> _joins the role_ <RoleName>
        [Default <RoleName> set to "@everyone", so it would be an error if don't <RoleName> added. Default <@Someone> set to **None**, it needs to be mention]
    **• -removerole <RoleName> <@Someone>** --> _Removes the_ <RoleName> _of_ <@Someone>
        [<@Someone> needs to be mention]    
    **• -showroles** --> _Show the list of all roles on the server_
    **• -deleterole <RoleName>** --> _Delete the role <RoleName> from the server_
        [Default <RoleName> set to "role", if it doesn't exist an error will occurred]

    **--- Morse Translator ---**
    **• -morse <msg>** --> _Translate from ASCII to Morse code_ [<msg> MUST BE DECLARED]
    **• -es <msg>** --> _Translate from Morse code to ASCII_ [<msg> MUST BE DECLARED, this command is still in progress]

    ***- If you have any question or problem about the bot, contact with the Bot-Owner -***

"""
role_text = "***This are the roles of the server:*** \n\n"

with open("token.json", encoding="utf-8") as tokens:
    token = load(tokens)["token"]
emoji_str="emoji"
emoji_id="id"

emoji_list = {
    "id0": '🔴',
    "id1": '🔵',
    "id2": '🟢',
    "id3": '🟠',
    "id4": '🟡',
    "id5": '🟣',
    "id6": '🟥',
    "id7": '🟦',
    "id8": '🟩',
    "id9": '🟧',
    "id10": '🟨',
    "id11": '🟪',
    "id12": '❤️',
    "id13": '💙',
    "id14": '💚',
    "id15": '💛',
    "id16": '💜',
    "id17": '🔺',
    "id18": '🔹',
    "id19": '🔸'

}


#log = open("file.log", "a", encoding="utf-8")

@client.event
async def on_ready():
    print("Bot connected!")
    game = discord.Game('Clean | -help')
    await client.change_presence(activity=game)
    log = open("file.log", "a", encoding="utf-8")
    log.write("Connected date: {}\n".format(utc))
    log.close()



@client.command(pass_context = True)
async def help(m):
    log = open("file.log", "a", encoding="utf-8")
    log.write("Help command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc,m.message.channel, m.message.author))
    await m.message.delete()
    embed = discord.Embed(title="Help:", description = text, colour = discord.Color.green())
    await m.message.channel.send(embed=embed)
    log.close()

@client.command(pass_context = True)
async def delete(m):
    log = open("file.log", "a", encoding="utf-8")
    log.write("Deleted command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc, m.message.channel, m.message.author))
    await m.message.delete()
    await m.message.channel.purge(limit=100, check=lambda m: m.author == client.user)
    log.close()

@client.command(pass_context = True)
async def clear(context, part = None):
    log = open("file.log", "a", encoding="utf-8")
    log.write("Clear command summon: {}\nWith <symbol>: {}\nIn Channel: {}\nBy: {}\n".format(utc, part, context.message.channel, context.message.author))
    await context.message.delete()
    def someone(m):             #Visto bueno de @Gulis
        if m.content.startswith(part):
            print(m.content)
            log.write("{}:: {}\n".format(m.content, m.author))
            return True
    deleted = await context.message.channel.purge(limit=10, check=someone)
    print("Deleted {} message(s)".format(len(deleted)))
    log.close()

# @client.command(pass_context = True)      #Metodo @Gulis
# async def clear(context, part = None):
#     part = context.message.content[7:]
#     await context.message.delete()
#     await context.message.channel.purge(limit=10, check=lambda m: m.content.startswith(part))

### @client.event
### async def on_reaction_add(reaction, user):
###     if reaction.emoji == "":
###         # do stuff


@client.command(pass_context = True)
async def Botclean(m):
    log = open("file.log", "a", encoding="utf-8")
    log.write("Botclean command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc, m.message.channel, m.message.author))
    await m.message.delete()
    await m.message.channel.purge(limit = 20, check=lambda m: m.author.bot)
    log.close()


@client.command(pass_context = True)
async def addrole(context, part = "role", r = 0, g = 0, b = 0):
    log = open("file.log", "a", encoding="utf-8")
    log.write("AddRole command summon: {}\nWith <name>: {}\nWith <r><g><b>: {}, {}, {}\nIn Channel: {}\nBy: {}\n".format(utc, part, r, g, b, context.message.channel, context.message.author))
    await context.message.delete()
    if r>255 or g>255 or b>255:
        await context.message.channel.send("RGB values cannot be greater than 255")
        log.write("RGBcolourError\n")
    else:
        exists = False
        rols = utils.find(lambda r:r.name == part, context.guild.roles)
        if rols:
            await context.message.channel.send('_The role_ "{}" _already exists_'.format(rols.mention))
            exists = True
        if not exists:
            permission = 0
            for role in context.guild.roles:
                if role.name == "@everyone":
                    permission = role.permissions
            await context.guild.create_role(name=part, colour=discord.Colour.from_rgb(r,g,b), mentionable=True)
            print('Successfully role "{}" created'.format(part))
            for role in context.guild.roles:
                if role.name == part:
                    await role.edit(reason=None, permissions=permission)
            print('Successfully permissions given to role "{}"'.format(part))
            log.write('Successfully role "{}" created\n'.format(part))
        else:
            log.write("ExistingRoleError\n")
            print('The role "@{}" already exists'.format(part))
    log.close()
            
# @client.command(pass_context = True)
# async def getroleinfo(context, part = ""):
#     for role in context.guild.roles:
#         if role.name == part:
#             print(str(role.permissions))

@client.command(pass_context = True)
async def joinrole(context, part = "@everyone", user:discord.Member = None):
    log = open("file.log", "a", encoding="utf-8")
    log.write("JoinRole command summon: {}\nWith <RoleName>: {}\nIn Channel: {}\nBy: {}\n".format(utc, part, context.message.channel, context.message.author))
    await context.message.delete()
    exits = True
    try:
        rols = utils.find(lambda r:r.name == part, context.guild.roles)
        if user == None:
            member = context.message.author
            if rols not in member.roles and exits:
                rol = utils.get(context.guild.roles, name=part)
                await member.add_roles(rol)
                print('"{}" successfully added to role "{}"'.format(member.display_name, rols.mention))
                await context.message.channel.send('"{}" _successfully added to role_ "{}"'.format(member.display_name, rols.mention))
                exits=False
                log.write('"{}" successfully added to role "@{}"\n'.format(member.display_name, part))
            else:
                await context.message.channel.send('_You are already in role_ "{}"'.format(rols.mention))
                log.write('"{}" is already in the role "@{}"\n'.format(member.display_name, part))
        else:
            if rols not in user.roles and exits:
                rol = utils.get(context.guild.roles, name=part)
                await user.add_roles(rol)
                print('"{}" successfully added to role "{}"'.format(user.display_name, rols.mention))
                await context.message.channel.send('"{}" _successfully added to role_ "{}"'.format(user.display_name, rols.mention))
                exits=False
                log.write('"{}" successfully added to role "@{}"\n'.format(user.display_name, part))
            else:
                await context.message.channel.send('_You are already in role_ "{}"'.format(rols.mention))
                log.write('"{}" is already in the role "@{}"\n'.format(user.display_name, part))
    except:
        print(Exception)
        log.write("An Exception has occurred\n")
        await context.message.channel.send("_An exception has occurred_")
    log.close()

@client.command(pass_context = True)
async def removerole(context, role = "",  user : discord.Member = None):
    Role = utils.get(user.roles, name = role)
    log = open("file.log", "a", encoding="utf-8")
    if user == None:
        member = context.message.author
        log.write("RemoveRole command summon: {}\nTo: {}\nWith <RoleName>: {}\nIn Channel: {}\nBy: {}\n".format(utc, member, role, context.message.channel, context.message.author))
        member.remove_roles(Role)
        await context.message.channel.send('_The user_ "{}" _has been removed from role_ "{}"'.format(user, Role.mention))
        log.write('The user "{}" has been removed from role "{}"'.format(user, Role.mention))
    else:
        log.write("RemoveRole command summon: {}\nTo: {}\nWith <RoleName>: {}\nIn Channel: {}\nBy: {}\n".format(utc, user, role, context.message.channel, context.message.author))
        await user.remove_roles(Role)
        await context.message.channel.send('_The user_ "{}" _has been removed from role_ "{}"'.format(user, Role.mention))
        log.write('The user "{}" has been removed from role "{}"'.format(user, Role.mention))
    log.close()


@client.command(pass_context = True)
async def showroles(m):
    log = open("file.log", "a", encoding="utf-8")
    log.write("ShowRoles command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc, m.message.channel, m.message.author))
    await m.message.delete()
    roles = ""
    cont = 0
    for role in m.guild.roles:
        with open("emoji.json", encoding="utf-8") as emoji_name:
            emoji = load(emoji_name)["emojis"][emoji_str+str(cont)]
        if role.name != "@everyone":
            roles = roles + ":{}:: {} \n".format(emoji, role.mention)
            cont+=1
            if cont==20: cont=0     #emoji-list resets at 20
    embed = discord.Embed(title="Roles:", description = role_text+roles, colour = discord.Color.purple())
    msg = await m.message.channel.send(embed=embed)
    for x, v in enumerate(emoji_list.values()):
        if x==cont: break
        await msg.add_reaction(v)
    log.close()


@client.command(pass_context = True)
async def deleterole(context, part = "role"):
    log = open("file.log", "a", encoding="utf-8")
    log.write("DeleteRole command summon: {}\nWith <RoleName>: {}\nIn Channel: {}\nBy: {}\n".format(utc, part, context.message.channel, context.message.author))
    msg=True
    for role in context.guild.roles:
        if role.name == part:
            await role.delete()
            msg=False
    if msg:
        await context.message.channel.send('_A problem has occurred deleting the role_ "{}"_, check if if you typed it right if not, contact the Bot Mod_'.format(part))
        log.write("DeletingRoleError")
    else:
        await context.message.channel.send('_The role_ "{}" _was deleted_'.format(part))
        log.write('The role "{}" was deleted'.format(part))
    log.close()

@client.command(pass_context = True)
async def ban(context, part = ""):
    banned = False
    log = open("file.log", "a", encoding="utf-8")
    log.write("Ban command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc, context.message.channel, context.message.author))
    with open("banlist.txt", "r") as read_file:
        for line in read_file:
            if part in line:
                banned = True
    if banned:
        await context.message.channel.send('"{}" is already on the blacklist'.format(part))
        log.write('User "{}" already banned'.format(part))
    else:
        banlist=open("banlist.txt", "a", encoding="utf-8")
        banlist.write("{} \n".format(part))
        await context.message.channel.send('"{}" susccessfully added on the blacklist'.format(part))
        log.write('User "{}" banned'.format(part))
        banlist.close()
    log.close()


@client.command(pass_context = True)
async def morse(context):
    log = open("file.log", "a", encoding="utf-8")
    log.write("Morse Translator command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc, context.message.channel, context.message.author))
    await context.message.delete()
    # await context.message.channel.send("{}".format(context.message.content))
    await context.message.channel.send("{}: {}".format(context.message.author, translate(context.message.content[7:])))
    log.close()


def translate(sentence):
    msg = ""
    for c in sentence:
        if c == 'a' or c == 'A':
            msg+=".- "
        elif c == 'b' or c == 'B':
            msg+="-... "
        elif c == 'c' or c == 'C':
            msg+="-.-. "
        elif c == 'd' or c == 'D':
            msg+="-.. "
        elif c == 'e' or c == 'E':
            msg+=". "
        elif c == 'f' or c == 'F':
            msg+="..-. "
        elif c == 'g' or c == 'G':
            msg+="--. "
        elif c == 'h' or c == 'H':
            msg+="---- "
        elif c == 'i' or c == 'I':
            msg+=".. "
        elif c == 'j' or c == 'J':
            msg+=".--- "
        elif c == 'k' or c == 'K':
            msg+="-.- "
        elif c == 'l' or c == 'L':
            msg+=".-.. "
        elif c == 'm' or c == 'M':
            msg+="-- "
        elif c == 'n' or c == 'N':
            msg+="-. "
        elif c == 'o' or c == 'O':
            msg+="--- "
        elif c == 'p' or c == 'P':
            msg+=".--. "
        elif c == 'q' or c == 'Q':
            msg+="--.- "
        elif c == 'r' or c == 'R':
            msg+=".-. "
        elif c == 's' or c == 'S':
            msg+="... "
        elif c == 't' or c == 'T':
            msg+="- "
        elif c == 'u' or c == 'U':
            msg+="..- "
        elif c == 'v' or c == 'V':
            msg+="...- "
        elif c == 'w' or c == 'W':
            msg+=".-- "
        elif c == 'x' or c == 'X':
            msg+="-..- "
        elif c == 'y' or c == 'Y':
            msg+="-.-- "
        elif c == 'z' or c == 'Z':
            msg+="--.. "
        elif c == ' ':
            msg+="/ "
        else:
            msg+=c
    return msg

@client.command(pass_content = True)
async def es(context):
    log = open("file.log", "a", encoding="utf-8")
    log.write("Morse Inverse Translator command summon: {}\nIn Channel: {}\nBy: {}\n".format(utc, context.message.channel, context.message.author))
    sentence = context.message.content[4:]
    msg = ""
    final = ""
    for c in sentence:
        if(c != ' '):
            msg += c
        else:
            final += inverse_tranlate(msg)
            msg=""
    final = final[:-1]
    print(final)
    final += inverse_tranlate(msg)
    print(msg)        
    await context.message.channel.send("{}: {}".format(context.message.author, final))
    log.close()


def inverse_tranlate(sentence):
    final = ""
    i = len(sentence)
    while(i > 0):
        if(sentence == ".-"):
            final += "a"
            sentence = sentence[2:]
            i-=2
        elif(sentence == "-..."):
            final += "b"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "-.-."):
            final += "c"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "-.."):
            final += "d"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "."):
            final += "e"
            sentence = sentence[1:]
            i-=1
        elif(sentence == "..-."):
            final += "f"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "--."):
            final += "g"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "----"):
            final += "h"
            sentence = sentence[4:]
            i-=4
        elif(sentence == ".."):
            final += "i"
            sentence = sentence[2:]
            i-=2
        elif(sentence == ".---"):
            final += "j"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "-.-"):
            final += "k"
            sentence = sentence[3:]
            i-=3
        elif(sentence == ".-.."):
            final += "l"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "--"):
            final += "m"
            sentence = sentence[2:]
            i-=2
        elif(sentence == "-."):
            final += "n"
            sentence = sentence[2:]
            i-=2
        elif(sentence == "---"):
            final += "o"
            sentence = sentence[3:]
            i-=3
        elif(sentence == ".--."):
            final += "p"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "--.-"):
            final += "q"
            sentence = sentence[4:]
            i-=4
        elif(sentence == ".-."):
            final += "r"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "..."):
            final += "s"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "-"):
            final += "t"
            sentence = sentence[1:]
            i-=1
        elif(sentence == "..-"):
            final += "u"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "...-"):
            final += "v"
            sentence = sentence[4:]
            i-=4
        elif(sentence == ".--"):
            final += "w"
            sentence = sentence[3:]
            i-=3
        elif(sentence == "-..-"):
            final += "x"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "-.--"):
            final += "y"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "--.."):
            final += "z"
            sentence = sentence[4:]
            i-=4
        elif(sentence == "/"):
            final += " "
            sentence = sentence[1:]
            i-=1
        else:
            final+=sentence
            i = 0

    return final


# async def checkrole(context, member: discord.Member = None, *, reason=None):
#     rol = utils.find(lambda r:r.name == part, context.guild.roles)
#     if rol not in member.roles:
#         print("You do not have this role")
#     else:
#         print("You are already in this role")

#TODO list
# def addreactions():
# async def ban():
# --

#run without being a bot (token of any non-bot user)
#client.run(token, bot = False)

#run being a bot (token of bot)
client.run(token)
