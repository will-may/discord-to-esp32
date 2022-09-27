import numpy as np
from struct import *
import discord 
import wikiGrab

import bmp2hex
import dither
import bmp2bit

import paho.mqtt.client as mqtt
from PIL import Image
import urllib
import cv2
from discord.ext import commands

wG = wikiGrab.wikiGrabber()

server_message = "no connection"
broker = '45.79.2.107'

# Initialize the bot instance: 
bot = commands.Bot(command_prefix=";", activity=discord.Activity(name='the cars go by', type=discord.ActivityType.watching), intents=discord.Intents.all())

### MQTT setup and call back functions
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global server_message
    print("Connected with result code "+str(rc))
    server_message = "Connected to {} with code {}".format(broker, str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("image")
    client.subscribe("vga/image")
    client.subscribe("discord")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    return

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883)

#Gets a random image from Wikimedia, sometimes it's a pdf so that could be fixed.
@bot.command(brief = 'Receive one of Josies\'s pictures',description='Josie has a lot of pcitures and she\'ll give you one if you ask!' )
async def pic(ctx):
    images = wG.search_wiki()
    if (images == ''):
      await ctx.send("Sorry boss, I couldn't find nothing!")
    else:
      for i in images:
       print(i) 
       await ctx.send(i)
       break

@bot.command()
async def push(ctx, vga:str = None):
  img = Image.open('image.jpg')
  img = img.convert("RGB")
  if (vga == "vga"):
    img = img.resize((300, 300))
    await ctx.send('You got it! VGA weee')
  else:
    await ctx.send('You got it! Writing the pixels now!')
    img = img.resize((160, 80))
  img.save('resized.png')

  #dithers or doesn't
  if (vga == "vga"):
    dither.start_dithering('resized.png')
    img1 = Image.open('dithered-2.png').convert()
  else:
    img1 = Image.open('resized.png').convert()
  img1 = np.array(img1)
  img1 = cv2.normalize(img1, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
  img1 = Image.fromarray(img1)
  
  img1.save('image.bmp')

  if (vga == "vga"):
    bmp2bit.bmptobytes()
  else:
    bmp2hex.bmptohex()

  #reads the hex or bytes into message
  text_file = open("image2.h", "r")
  message = text_file.read()
  message = message[:-1]
  text_file.close()

  #sends the message to mqtt
  if (vga == "vga"):
    topic = "vga/image"
  else:
    topic = "image"
  #sends
  try:
      client.publish(topic, payload=message, qos=2, retain=False)
  except Exception as e :
      await ctx.send('something when wrong!')
      print(e)
      return

@bot.command()
async def publish(ctx, topic:str, message: str):
    """sends a message to the server"""
    try:
        #send the message on the MQTT server
      result = client.publish(topic, payload=message, qos=0, retain=False)
    except Exception as e :
        await ctx.send('something when wrong!')
        print(e)
        return

    await ctx.send("The publish attempt was {}".format(result.is_published()))

#if the command is ;tv, it sends it to the TV
@bot.event
async def on_message(message):
  stringforya = message.content
  try:
    if ((stringforya[0:4] == ";tv ")):
      print(message.content[4:])
      try:
        #send the message on the MQTT server
        fullmessage = message.author.display_name+ ":" +message.content[4:]
        client.publish("discord", payload=fullmessage, qos=0, retain=False)
      except Exception as e :
          print(e)
          return
  except:
      pass
  await bot.process_commands(message)

#Saves the reacted image into image.jpg
@bot.event
async def on_raw_reaction_add(payload):
  try:
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
  except:
    message = await bot.get_user(payload.user_id).fetch_message(payload.message_id)
  reaction = payload.emoji.name
  if reaction == '📸':
    try:
      await message.attachments[0].save("image.jpg")
      print("captured!")
    except:
      try:
        urllib.request.urlretrieve(message.content, "image.jpg")
        print("link captured!")
      except:
        pass

#start non blocking MQTT
client.loop_start()

Secret = open("secret.txt", 'r')
Secret = Secret.read()
bot.run(Secret)

client.loop_stop(force=True)