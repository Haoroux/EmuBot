import discord
import json
import os
import sys

from pyKey import press
from discord.ext.commands import has_permissions, MissingPermissions 
from discord import app_commands
from discord.ext import commands
from collections import Counter
from config import TOKEN2

#Démmarage et intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
guild_ids = [1035614329678082098]


#Ouverture des fichiers de sauvegardesde
with open('save.json', 'r') as openfile:
    global dataSave
    dataSave = json.load(openfile)
    # print(dataSave)


@bot.event
async def on_ready():
    print('System operating!')
    synced = await bot.tree.sync()
    print("Slash CMDs Synced " + str(len(synced)))


data = dataSave
verifLetters = ['a','b','x','y']
up = data["up"]
down = data["down"]
left = data["left"]
right = data["right"]
confirm = data["confirm"]
back = data["back"]
shortcuts = data["shortcuts"]
backpack = data["backpack"]
gameCommands = up + down + left + right + confirm + back + shortcuts + backpack
# gameCommand = [up,down,left,right,confirm,back,shortcuts,backpack]
answers = []
# modRole = 'PokeManager'
modRole = data['lastModRole']
hello = 'hello world!'
channelId = data['lastChannelId']
totalAnswers = data['lastTotalAnswers']
requiredAmountAnswers = data['lastRequiredAmountAnswers']
usersStat = data['usersStat']


@bot.tree.command(description="montre le guide d'utilisation")
async def help(interaction: discord.Interaction):
    embed=discord.Embed()
    embed.add_field(name="Help:", value="voici ce que vous devez écrire pour jouer : \nconfirmer = "+str(confirm)+"\nretour = "+str(back)+"\nraccourcis = "+str(shortcuts)+"\nouvrir le menu = "+str(confirm)+"\nhaut = "+str(up)+"\nbas = "+str(down)+"\ngauche = "+str(left)+"\ndroite = "+str(right)+"\n\nslash commandes disponibles : \n-help : montre les touches à écrire afin de jouer\n-amountofanswers : défini le nombre de réponses nécessaires avant de jouer\n-info : montre les infos actuelles du bot\n-managerole : sert à définir le rôle nécessaire afin de changer les options du bot(redémarrage nécessaire)\n-managechannel : sert à changer le channel où le bot lit les actions(pour le changer il vous faut l'id du channel)\n-managecontrols : sert à changer ce qu'il est nécessaire d'écrire afin de faire une action\n-usertotalactions : montre le nombre d'action effectué par soi ou une autre personne\n-usertop10 : montre le top 10 des joueurs les plus actifs\n-restart : redémarre et sauve les données du bot", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description='montres les informations utiles du bot')
async def infos(interaction: discord.Interaction):
    embed=discord.Embed()
    embed.add_field(name="Informations:", value="nombres d'action : "+str(totalAnswers)+"\nrôle de paramètrages : "+modRole+"\nchannel d'actions : "+str(bot.get_channel(int(channelId)))+"\nnbr de réponse nécessaire : "+str(requiredAmountAnswers), inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(description='change le rôle nécessaire pour modifier les paramètres du bot')
@app_commands.checks.has_permissions(manage_roles = True)
async def managerole(interaction: discord.Interaction, role_name: str):
    global modRole
    modRole = role_name
    await interaction.response.send_message("le role de paramètrages a bien été remplacé par " + modRole, ephemeral=True)
@managerole.error
async def managerole(interaction:discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Il semble que tu n'ais pas la permission requise pour utilisez cette commande ", ephemeral=True)


@bot.tree.command(description="change le channel où l'ont doit écrire les actions")
@app_commands.checks.has_role(modRole)
async def managechannel(interaction: discord.Interaction, channel_id: str):
    global channelId
    channelId = channel_id
    await interaction.response.send_message("le channel d'actions a bien été remplacé par " + str(bot.get_channel(int(channelId))), ephemeral=True)
@managechannel.error
async def managechannel(interaction:discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("Il semble que tu n'ais pas le rôle requis pour openSave()")


@app_commands.choices(what_action = [
    app_commands.Choice(name="up", value="up"),
    app_commands.Choice(name="down", value="down"),
    app_commands.Choice(name="left", value="left"),
    app_commands.Choice(name="right", value="right"),
    app_commands.Choice(name="confirm", value="confirm"),
    app_commands.Choice(name="back", value="back"),
    app_commands.Choice(name="shortcuts", value="shortcuts"),
    app_commands.Choice(name="backpack", value="backpack")
])

@app_commands.choices(manage_control = [
    app_commands.Choice(name="add",value='append'),
    app_commands.Choice(name="delete", value='remove')
])

@bot.tree.command(description="change les touches a écrire")
@app_commands.checks.has_role(modRole)
async def mannagecontrols(interaction:discord.Interaction, what_action: str,manage_control:str,object:str):
    await interaction.response.send_message("les changements ont bel et bien été appliqués", ephemeral=True)
    changeControls(what_action, manage_control, object)
@mannagecontrols.error
async def mannagecontrols(interaction:discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("Il semble que tu n'ais pas le rôle requis pour utilisez cette commande ", ephemeral=True)

def changeControls(what,action,value):
    if what == 'up':
        getattr(up, action)(value.lower())
        print(up)
    elif what == 'down':
        getattr(down, action)(value.lower())
        print(down)
    elif what == 'left':
        getattr(left, action)(value.lower())
        print(left)
    elif what == 'right':
        getattr(right, action)(value.lower())
        print(right)
    elif what == 'confirm':
        getattr(confirm, action)(value.lower())
        print(confirm)
    elif what == 'back':
        getattr(back, action)(value.lower())
        print(back)
    elif what == 'shortcuts':
        getattr(shortcuts, action)(value.lower())
        print(shortcuts)
    elif what == 'backpack':
        getattr(backpack, action)(value.lower())
        print(backpack)


@bot.tree.command(description="change le nombre de réponse nécessaire")
@app_commands.checks.has_role(modRole)
async def amountofanswers(interaction: discord.Interaction, num: int):
    global requiredAmountAnswers
    requiredAmountAnswers = num
    await interaction.response.send_message("le nombre de réponse nécessaire a bien été remplacé par " + str(requiredAmountAnswers), ephemeral=True)
@amountofanswers.error
async def amountofanswers(interaction:discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("Il semble que tu n'ais pas le rôle requis pour utilisez cette commande ", ephemeral=True)


@bot.tree.command(description="affiche votre nombre d'actions total ou d'un autre joueur via son id")
async def usertotalactions(interaction: discord.Interaction, searched_id : str=None):
    # userId = interaction.message.id
    if searched_id == None:
        userId = str(interaction.user.id)
        member = interaction.guild.get_member(int(userId))
        username = member.display_name 
        if userId in usersStat:
            await interaction.response.send_message("Jusqu'à maintenant tu as effectué "+ str(usersStat[userId])+ " action.s " + username)
        else:
            usersStat[userId] = 0
            await interaction.response.send_message("Jusqu'à maintenant tu as effectué "+ str(usersStat[userId])+ " action.s " + username)
            print(usersStat)
    else :
        userId = str(searched_id)
        member = interaction.guild.get_member(int(userId))
        username = member.display_name        
        if userId in usersStat:
            print(hello)
            await interaction.response.send_message("Voici le nombre d'actions qu'a effectuées "+ username +" : " + str(usersStat[userId]))
        else:
            usersStat[userId] = 0
            await interaction.response.send_message("Voici le nombre d'actions qu'a effectuées "+ username +" : " + str(usersStat[userId]))
            print(usersStat)


@bot.tree.command(description="montre les 10 joueurs les plus actifs")
async def usertop10(interaction: discord.Interaction):
    sorted_users = sorted(usersStat.items(), key=lambda x: x[1], reverse=True)
    topTen = sorted_users[:10]
    one = topTen[0]
    two = topTen[1]
    three = topTen[2]
    four = topTen[3]
    five = topTen[4]
    six = topTen[5]
    seven = topTen[6]
    eight = topTen[7]
    nine = topTen[8]
    ten = topTen[9]
    first = "\n🥇1:"+  interaction.guild.get_member(int(one[0])).display_name +" avec " +str(one[1])+ " réponses\n\n"
    second = "🥈2:"+  interaction.guild.get_member(int(two[0])).display_name +" avec " +str(two[1])+ " réponses\n\n"
    third = "🥉3:"+  interaction.guild.get_member(int(three[0])).display_name +" avec " +str(three[1])+ " réponses\n\n"
    fourth = "4:"+  interaction.guild.get_member(int(four[0])).display_name +" avec " +str(four[1])+ " réponses\n\n"
    fifth = "5:"+  interaction.guild.get_member(int(five[0])).display_name +" avec " +str(five[1])+ " réponses\n\n"
    sixth  = "6:"+  interaction.guild.get_member(int(six[0])).display_name +" avec " +str(six[1])+ " réponses\n\n"
    seventh = "7:"+  interaction.guild.get_member(int(seven[0])).display_name +" avec " +str(seven[1])+ " réponses\n\n"
    eighth = "8:"+  interaction.guild.get_member(int(eight[0])).display_name +" avec " +str(eight[1])+ " réponses\n\n"
    ninth  = "9:"+  interaction.guild.get_member(int(nine[0])).display_name +" avec " +str(nine[1])+ " réponses\n\n"
    tenth = "10:"+  interaction.guild.get_member(int(ten[0])).display_name +" avec " +str(ten[1])+ " réponses"
    embed=discord.Embed()
    embed.add_field(name="🏆Top 10🏆 des joueurs les plus actifs :", value=first+second+third+fourth+fifth+sixth+seventh+eighth+ninth+tenth,inline=False)
    await interaction.response.send_message(embed=embed)
@usertop10.error
async def usertop10(interaction:discord.Interaction, error: app_commands.AppCommandError):
    await interaction.response.send_message("il semblerait qu'il n'y ai pas encore participants", ephemeral=True)


@bot.tree.command(description='redémarre le bot')
@app_commands.checks.has_role(modRole)
async def restart(interaction: discord.Interaction):
    # print(data)
    await interaction.response.send_message("Bot en redémarrage . . .", ephemeral=True)
    with open("save.json", "w") as outfile:
        newSave = json.dumps({"lastModRole" : modRole,
                            "lastChannelId": channelId,
                            "lastTotalAnswers" : totalAnswers,
                            "lastRequiredAmountAnswers": requiredAmountAnswers,
                            "up" : up,
                            "down" : down,
                            "left" : left,
                            "right" : right,
                            "confirm" : confirm,
                            "back" : back,
                            "shortcuts" : shortcuts,
                            "backpack" : backpack,
                            "usersStat" : usersStat})
        outfile.write(newSave)
    await restart_bot()
@restart.error
async def restart(interaction:discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("Il semble que tu n'ais pas le rôle requis pour utilisez cette commande ", ephemeral=True)

def restart_bot():
    python = sys.executable
    os.execl(python, python, * sys.argv)   


@bot.event
async def on_message(msg):
    global usersStat
    if msg.channel.id == int(channelId):
        if msg.content.lower() in gameCommands:
            userId = str(msg.author.id)
            print("ok?")
            if userId in usersStat:
                userStat  = usersStat.get(userId)
                usersStat[userId] += 1
                print(usersStat[userId])
            else:
                usersStat[userId] = 1
                # print(usersStat)
        await bot.process_commands(msg)
        answers.append(msg.content.lower())
        print(answers)
    # print(totalAnswers)
    if len(answers) >= requiredAmountAnswers:
        play()

def play():
    global totalAnswers
    action = Counter(answers).most_common(1)[0][0]

    answers.clear()

    if action in confirm:
        press('A', 0.1)
    elif action in back:
        press('B', 0.1)
    elif action in shortcuts:
        press('Y', 0.1)
    elif action in backpack:
        press('X', 0.1)
    elif action in up:
        press('0', 0.2)
    elif action in down:
            press('1', 0.2)
    elif action in left:
            press('2', 0.2)
    elif action in right:
            press('3', 0.2)
    
    totalAnswers = totalAnswers + 1
    return totalAnswers


bot.run(TOKEN2)