import discord
import asyncio
from discord.ext import commands
import pandas as pd
import datetime

#intents = discord.Intents.all()
client = commands.Bot(command_prefix='#')

deveres = {}
calendario_escola = {'SEGUNDA':['Física 2','Física 2','Biologia 1','Biologia 1','Matemática 1','Matemática 1'],'TERÇA':['Literatura','Matemática 2','Matemática 2','Redação','Biologia 2','Biologia 2'],'QUARTA':['Química 2','Química 2','Literatura','Português','Espanhol','Sociologia'],'QUINTA':['Geografia','Geografia','História 2','Biologia 2','História 2','Português','Geografia','Química 1','Redação','Física 1'],'SEXTA':['SOE','Matemática 2','Matemática 2','Física 1','Física 1','Filosofia'],'SÁBADO':['Química 1','Química 1','Inglês','História 1','História 1','História 2']}
def read_token():
    with open("token.txt",'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

@client.command(name = 'clear')
async def limpar(context):
    deveres.clear()
    await  context.message.channel.send("A agenda foi limpa!")


@client.command(name ='prazo')
async def prazo(context):
    dever  = context.message.content[7:]
    restante = (deveres[dever] - datetime.date.today()).days
    await context.message.channel.send('RESTAM '+str(restante)+' DIAS PARA O PRAZO FINAL.')

@client.command(name ='add')
async def add(context):
    dever_last = context.message.content.find(' * ')
    dever = context.message.content[5:dever_last]
    
    if dever_last != -1:
        prazo = context.message.content[dever_last+3:]
        dia = int(prazo[0:2])
        
        mes = int(prazo[3:5])
        
        ano = int(prazo[6:10])
        
        deveres[dever] = datetime.date(ano,mes,dia)
        await context.message.channel.send('ITEM ADICIONADO COM SUCESSO!')
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
    
    
@client.command(name = 'agenda')
async def lista(context):
    await context.message.channel.send('AGENDA:\n')
    agenda_string = ''
    for key, value in deveres.items():
        agenda_string += key + '  ---->'+f'{value.day}/{value.month}/{value.year}\n'
    await context.message.channel.send(agenda_string)
@client.command(name = 'calendario')
async def calendario(context):
    if len(context.message.content) > 11:
        dia = context.message.content[12:].upper()
        await context.message.channel.send('**'+dia+'**'+'\n\n')
        to_print = ''
        for tempo in calendario_escola[dia]:
            to_print += tempo+'\n'
        print(to_print)
        await context.message.channel.send(to_print)
    else:
        for key, value in calendario_escola.items():
            await context.message.channel.send('**'+key+'**')
            to_print = ''
            for tempo in value:
                to_print += tempo+'\n'
            await context.message.channel.send(to_print)

@client.event
async def on_ready():
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("a puta do sampaio"))


client.run(token)

