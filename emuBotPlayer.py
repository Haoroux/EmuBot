import discord
import json
import os
import sys

from pyKey import pressKey, releaseKey, press, sendSequence, showKeys
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
    print(dataSave)


@bot.event
async def on_ready():
    print('System operating!')
    synced = await bot.tree.sync()
    print("Slash CMDs Synced " + str(len(synced)))


verifLetters = ['a','b','x','y']
verifArrows = ['haut','bas','gauche','droite']
answers = []
data = dataSave
# modRole = 'PokeManager'
modRole = data['lastModRole']
hello = 'hello world!'
channelId = data['lastChannelId']
totalAnswers = data['lastTotalAnswers']
requiredAmountAnswers = data['lastRequiredAmountAnswers']

@bot.tree.command(description="montre le guide d'utilisation")
async def help(interaction: discord.Interaction):
    embed=discord.Embed()
    embed.add_field(name="Help:", value="voici ce que vous devez écrire pour jouer : \na = confirmer\nb = retour\ny = raccourcis\nx = ouvrir le menu\nles autres options disponibles sont haut,bas,gauche,droite\n\nslash commandes disponibles : \n-help : montre les touches à écrire afin de jouer\n-amountofanswers : défini le nombre de réponses nécessaires avant de jouer\n-info : montre les infos actuelles du bot\n-managerole : sert à définir le rôle nécessaire afin de changer les options du bot(redémarrage nécessaire)\n-managechannel : sert à changer le channel où le bot lit les actions(pour le changer il vous faut l'id du channel)\n-restart : redémarre le bot", inline=False)
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


@bot.tree.command(description='redémarre le bot')
@app_commands.checks.has_role(modRole)
async def restart(interaction: discord.Interaction):
    # print(data)
    await interaction.response.send_message("Bot en redémarrage . . .", ephemeral=True)
    with open("save.json", "w") as outfile:
        newSave = json.dumps({"lastModRole" : modRole,
                            "lastChannelId": channelId,
                            "lastTotalAnswers" : totalAnswers,
                            "lastRequiredAmountAnswers": requiredAmountAnswers})
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
    if msg.channel.id == int(channelId):
        await bot.process_commands(msg)
        answers.append(msg.content.lower())
        print(answers)
    # print(totalAnswers)
    if len(answers) >= requiredAmountAnswers:
        play()

def play():
    global totalAnswers
    action = Counter(answers).most_common(1)[0][0]

    # print('action ' + action)
    answers.clear()
    if action in verifLetters:
        print('victory')
        press(action,0.1)
        totalAnswers = totalAnswers + 1
        return totalAnswers
    elif action in verifArrows:
        if action == 'haut':
            press('0', 0.2)
        elif action == 'bas':
            press('1', 0.2)
        elif action == 'gauche':
            press('2', 0.2)
        elif action == 'droite':
            press('3', 0.2)
    
        totalAnswers = totalAnswers + 1
        return totalAnswers




bot.run(TOKEN2)