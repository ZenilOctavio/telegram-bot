from dotenv import load_dotenv
load_dotenv()
import telebot
from constants import TELEGRAM_ACCESS_TOKEN, HOST, DB_USER, DB_PASSWORD, DB_NAME
from my_database import MySQL
import uuid
import random

db = MySQL(HOST, DB_USER, DB_PASSWORD, DB_NAME, True)
db.connect()

print(TELEGRAM_ACCESS_TOKEN)
bot = telebot.TeleBot(TELEGRAM_ACCESS_TOKEN)



def is_registered(id_usuario: int) -> bool:
  return len(db.select('Usuario', ['id', 'nombres'], f'id = {id_usuario}')) > 0

@bot.message_handler(['register', 'registrarse'])
def registrar(message):
  id_usuario = message.from_user.id
  
  results = db.select('Usuario',['id', 'nombres'], f'id = {id_usuario}')

  if len(results):
    bot.reply_to(message, 'Ya estas registrado')
    return

  nombre = message.from_user.first_name
  apellido = message.from_user.last_name
  id_chat = message.chat.id
  
  try:
    db.insert('Usuario', ['id', 'nombres', 'apellidos', 'chat_id'], [[str(id_usuario), f"'{nombre}'", f"'{apellido}'", str(id_chat)]])
    bot.reply_to(message, 'Fuiste registrado exitosamente')
  
  except:
    bot.reply_to(message, 'Hubo un error en el registro')
    


@bot.message_handler(['help', 'ayuda'])
def ayuda(message):
  bot.reply_to(message, 
    '''
/registrarse o /register -> Registrate en el sistema de notas
/crear_nota o /create_note -> Crea una nota con el siguiente formato de mensaje:
            '/create_note
            Titulo: <titulo de la nota>
            Descripcion: <descripcion de la nota>'
/ver_notas o /get_notes -> 
    '''             
  )

@bot.message_handler(['create_note', 'crear_nota'])
def crear_nota(message):
  id_usuario = message.from_user.id
  
  if not is_registered(id_usuario):
    bot.reply_to(message, 'Aun no estas registrado')

  # print(message.text)
  title_line: str
  description_line:str
  try:
      lines = message.text.split('\n')
      # print(lines)
      title_line = lines[1].split(':')[1]
      description_line = lines[2].split(':')[1]  
      
  except:
    bot.reply_to(message, 'Formato de mensaje inválido')
    return
  
  # id_nota = uuid.uuid4().int = 5624
  id_nota = random.randint(0, 2500000)
  
  db.insert('Nota',['id', 'id_usuario', 'titulo', 'descripcion'], [[str(id_nota), str(id_usuario), f"'{title_line}'", f"'{description_line}'"]])

  bot.reply_to(message, 'Nota guardada correctamente')


@bot.message_handler(['get_notes', 'ver_notas'])
def ver_notas(message):
  id_usuario = message.from_user.id

  if not is_registered(id_usuario):
    bot.reply_to(message, 'Aun no estas registrado')

  notes = db.select('Nota', ['id', 'titulo', 'descripcion'], f'id_usuario = {id_usuario}')

  msg_list: list[str] = []
  for id_nota, titulo, descripcion in notes:
    msg_list.append(f'Id de la nota: {id_nota}\n\tTitulo: {titulo}\n\tDescripcion: {descripcion}')
  
  msg_notes = "\n\n".join(msg_list)

  msg = f'Notas: \n {msg_notes}'
  
  bot.reply_to(message, msg)


chats = db.select('Usuario', ['chat_id'])

for chat in chats:
  bot.send_message(chat[0], 'The bot is currently working')

bot.infinity_polling()