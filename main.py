

import discord
import asyncio
from discord.ext import commands
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

#intents = discord.Intents.all()
cred = credentials.Certificate('./turma-cred.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

def agendaBackup():
    db.collection('AGENDA').document('Agenda').set(deveres)

client = commands.Bot(command_prefix='?')




calendario_escola = {'SEGUNDA':['Física 2','Física 2','Biologia 1','Biologia 1','Matemática 1','Matemática 1'],'TERÇA':['Literatura','Matemática 2','Matemática 2','Redação','Biologia 2','Biologia 2'],'QUARTA':['Química 2','Química 2','Literatura','Português','Espanhol','Sociologia'],'QUINTA':['Geografia','Geografia','História 2','Biologia 2','História 2','Português','Geografia','Química 1','Redação','Física 1'],'SEXTA':['SOE','Matemática 2','Matemática 2','Física 1','Física 1','Filosofia'],'SABADO':['Química 1','Química 1','Inglês','História 1','História 1','História 2']}
def read_token():
    with open("token.txt",'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
def transDever(lista):
    for key, i in lista.items():
        newNumber = int(i['dataEnd'][0:2]) + (int(i['dataEnd'][3:5]) * 100) + (int(i['dataEnd'][6:10])* 10000)
        print(newNumber)
        lista[key]['dataValue'] = newNumber
    print(lista)
    return lista
@client.command(name = 'clear')
async def limpar(context):
    deveres.clear()
    agendaBackup()
    await  context.message.channel.send("A agenda foi limpa!")

@client.command(name ='add')
async def add(context):
    getAgenda()
    msg = context.message.content
    dever_last = msg.find(' * ')
    dever = msg[5:dever_last]
    new_msg = msg[dever_last+3:]
    plat = new_msg[:new_msg.find(' * ')]
    new_2_msg = new_msg[new_msg.find(' * ')+3:]
    materia = new_2_msg[:new_2_msg.find(' * ')]
    new_3_msg = new_2_msg[new_2_msg.find(' * ')+3:]

    if dever_last != -1 and new_msg.find(' * ') != -1 and new_2_msg.find(' * ') != -1:
        prazo = new_3_msg
        # dia = int(prazo[0:2])
        
        # mes = int(prazo[3:5])
        
        # ano = int(prazo[6:10])
        
        deveres[dever] = {'nome':dever,'materia':materia, 'plataforma':plat,'dataEnd': prazo}
        await context.message.channel.send('ITEM ADICIONADO COM SUCESSO!')
        agendaBackup()
    else:
        await context.message.channel.send('POR FAVOR USE O FORMATO ?ADD DEVER * PLATAFORMA * MATERIA * DATA')


@client.command(name ='del')
async def delete(context):
    getAgenda()
    elemento = context.message.content[5:]
    try:
        deveres.pop(elemento)
        await context.message.channel.send("ITEM REMOVIDO COM SUCESSO!")
        agendaBackup()
    except:
        await context.message.channel.send('ESSE ITEM NÃO EXISTE, POR FAVOR INSIRA UM ITEM VÁLIDO')
    
    
@client.command(name = 'agenda')
async def lista(context):
    getAgenda()
    hasFilter = False
    if len(context.message.content) >8:
        hasFilter = True
        filtro = context.message.content[8:].lower()
    if len(deveres) > 0:
        teste_deveres = transDever(deveres)
        new_deveres = sorted(teste_deveres.items(),key=lambda x: x['dataValue'])
        emb = discord.Embed(title='Agenda')
        for key, value in new_deveres.items():
            if hasFilter:
                
                if value['plataforma'].lower() == filtro:
                    emb.add_field(name=f'**{key}**', value="> plataforma: {}\n> materia: {}\n> data: {}".format(value['plataforma'],value['materia'],value['dataEnd']),inline=False)
            else:
                emb.add_field(name=f'**{key}**', value="> plataforma: {}\n> materia: {}\n> data: {}".format(value['plataforma'],value['materia'],value['dataEnd']),inline=False)
        await context.message.channel.send(embed=emb)
    else:
        await context.message.channel.send("Não há deveres na agenda")
@client.command(name = 'calendario')
async def calendario(context):
    if len(context.message.content) > 11:
        dia = context.message.content[12:].upper()
        if dia == 'HOJE':
            semana_dia = datetime.date.today().weekday()
            if semana_dia == 0:
                dia = 'SEGUNDA'
            elif semana_dia == 1:
                dia = 'TERÇA'
            elif semana_dia == 2:
                dia = 'QUARTA'
            elif semana_dia == 3:
                dia = 'QUINTA'
            elif semana_dia == 4:
                dia = 'SEXTA'
            elif semana_dia == 5:
                dia = 'SABADO'
            else:
                dia = 'HOJE NÃO TEM AULA'
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

def getAgenda():
    doc = db.collection('AGENDA').document('Agenda').get()
    if doc.exists:

        global deveres
        deveres = doc.to_dict()
        
    else:
        print('nao')


@client.event
async def on_ready():
    print('Informações básicas:')
    print('Nome do bot: {0}'.format(client.user.name))
    print('Id: {0}'.format(client.user.id))
    print('Server: {0}'.format(client.guilds))
    print('-------------------------------------------------------------------------------')
    getAgenda()
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Guardando os deveres da 3C"))


client.run(token)

