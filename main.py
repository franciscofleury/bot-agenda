import discord
import asyncio
from discord.ext import commands
import pandas as pd
import datetime

intents = discord.Intents.all()
client = commands.Bot(command_prefix='?', intents=intents)

deveres = {}
def read_token():
    with open("token.txt",'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

@client.command(name ='prazo')
async def prazo(context):
    dever  = context.message.content[7:]
    restante = (deveres[dever] - datetime.datetime.today()).days +1
    await context.message.channel.send(restante)

@client.command(name ='add')
async def add(context):
    dever_last = context.message.content.find(' * ')
    dever = context.message.content[5:dever_last]
    
    if dever_last != -1:
        prazo = context.message.content[dever_last+3:]
        dia = int(prazo[0:2])
        
        mes = int(prazo[3:5])
        
        ano = int(prazo[6:10])
        
        deveres[dever] = datetime.datetime(ano,mes,dia)
        await context.message.channel.send('ITEM ADICIONADO COM SUCESSO!\nLISTA ATUAL:\n'+str(deveres))
    else:
        await context.message.channel.send('POR FAVOR INSIRA UMA DATA')


@client.command(name ='del')
async def delete(context):
    elemento = context.message.content[5:]
    try:
        deveres.pop(elemento)
        if len(deveres) < 1 :
            await context.message.channel.send("ITEM REMOVIDO COM SUCESSO!")
            await context.message.channel.send("Você não tem deveres para essa semana!")
        else:
            await context.message.channel.send("ITEM REMOVIDO COM SUCESSO! \n LISTA ATUAL:\n "+str(deveres))
    except:
        await context.message.channel.send('ESSE ITEM NÃO EXISTE, POR FAVOR INSIRA UM ITEM VÁLIDO')
    
    
@client.command(name = 'lst')
async def lista(context):
    await context.message.channel.send(str(deveres))


@client.event
async def on_ready():
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Rental Girlfriend!"))


client.run(token)

