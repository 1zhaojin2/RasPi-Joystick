import discord
from discord.ext import commands
import time
import lirc
import RPi_I2C_driver
import RPi.GPIO as GPIO
import Adafruit_DHT
import openai
import ADC0834
import global_variables

button_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sockid = lirc.init("main")
mylcd = RPi_I2C_driver.lcd()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents)
bot.remove_command("help")

async def setup_hook():
    await bot.load_extension("cogs.cog_function")

bot.setup_hook = setup_hook

user_api_keys = {}

@bot.command()
async def help(ctx):

    await ctx.message.delete()

    # the commands are:
    # -help
    # -display
    # -storekey
    # -usegpt
    # -joystick
    # also add a short description of each command

    embed = discord.Embed(
        title="Help", description="List of commands for the bot", color=0xEEE657
    )
    embed.add_field(
        name="-help", value="Displays this message", inline=False
    )
    embed.add_field(
        name="-display", value="Displays a message on the LCD screen", inline=False
    )
    embed.add_field(
        name="-storekey", value="Stores a user's API key for GPT-3", inline=False
    )
    embed.add_field(
        name="-usegpt", value="Uses GPT-3 to generate text", inline=False
    )
    embed.add_field(
        name="-joystick", value="Displays the values of the joystick", inline=False
    )
    embed.add_field(
        name="-monith", value="Displays the temperature and humidity continuously", inline=False
    )

    await ctx.send(embed=embed)


@bot.command()
async def storekey(ctx, *, key):

    user_api_keys[ctx.message.author.id] = key
    await ctx.message.delete()


    embed = discord.Embed(
        title="API Key Stored",
        description="Your API key has been stored",
        color=0xEEE657,
    )

    
    embed.add_field(name="Key", value=key, inline=False)


@bot.command()
async def usegpt(ctx, *, key):

    if ctx.message.author.id not in user_api_keys:
        embed = discord.Embed(
            title="Error",
            description="You have not stored your API key",
            color=0xEEE657,
        )

        await ctx.send(embed=embed)
        return
    
    await ctx.message.delete()
    await ctx.send("Using GPT-3 to generate text")

    embed = discord.Embed(
        title="GPT-3 Response", description="Your response from GPT-3", color=0xEEE657
    )
    embed.add_field(name="Key", value=key, inline=False)

    openai.api_key = user_api_keys[ctx.message.author.id]

    response = openai.Completion.create(
        engine="davinci",
        prompt=key,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"],
    )

    embed.add_field(name="Response", value=response.choices[0].text, inline=False)

    await ctx.channel.history(limit=1).flatten()[0].delete()
    await ctx.send(embed=embed)


@bot.command()
async def display(ctx, *, text):

    mylcd.lcd_clear()

    embed = discord.Embed(
        title="Displaying Text",
        description="The following text has been displayed as scrolling text. Use green button to scroll through them.",
        color=0xEEE657,
    )

    embed.add_field(name="Text", value=text, inline=False)
    await ctx.send(embed=embed)

    if len(text) > 16:
        text_list = text.split()
        chunk_list = []
        curr_chunk = ""

        for word in text_list:
            if len(curr_chunk) + len(word) + 1 <= 16:
                curr_chunk += word + " "
            else:
                chunk_list.append(curr_chunk)
                curr_chunk = word + " "
        
        chunk_list.append(curr_chunk)
    else:
        chunk_list = [text]

    if chunk_list[0] == "":
        chunk_list.pop(0)

    if len(chunk_list[0]) > 16:
        tempChunk = chunk_list[1]
        chunk_list.pop(1)

        while len(tempChunk) > 16:
            chunk_list.append(tempChunk[:16])
            tempChunk = tempChunk[16:]

        chunk_list.append(tempChunk)
    
    print(chunk_list)

    if len(chunk_list) > 1:
        for i in range(len(chunk_list)):
            mylcd.lcd_display_string(chunk_list[i], 1)

            if i != len(chunk_list) - 1:
                mylcd.lcd_display_string(chunk_list[i + 1], 2)
            
            if len(chunk_list) == 2:
                break

            while True:
                input_state = GPIO.input(23)

                if input_state == True:
                    while GPIO.input(23) == True:
                        pass

                    mylcd.lcd_clear()
                    print("Button Pressed")

                    break
    else:
        mylcd.lcd_display_string(text, 1)
        time.sleep(0.5)


@bot.command()
async def joystick(ctx):

    mylcd.lcd_clear()

    print("printing embed")
    embed = discord.Embed(
        title="Displaying Joystick Values",
        description="Please press the button to stop monitoring",
        color=0xEEE657,
    )
    await ctx.send(embed=embed)

    global_variables.setup()
    prev_x_val = 0
    prev_y_val = 0

    while True:
        x_val = ADC0834.getResult(0)
        y_val = ADC0834.getResult(1)
        button_val = GPIO.input(23)

        lcd_text = "X: " + str(x_val)
        lcd_text2 = "Y: " + str(y_val)

        global_variables.set_angle_x(x_val)
        global_variables.set_angle_y(y_val)


        if len(str(x_val)) < len(str(prev_x_val)):
            mylcd.lcd_clear()
        if len(str(y_val)) < len(str(prev_y_val)):
            mylcd.lcd_clear()


        
        mylcd.lcd_display_string(lcd_text, 1)
        mylcd.lcd_display_string(lcd_text2, 2)


        prev_x_val = x_val
        prev_y_val = y_val

        # print("x_val: " + str(global_variables.curr_x_val) + ", y_val: " + str(global_variables.curr_y_val))

        if button_val == False:
            mylcd.lcd_clear()
            global_variables.destroy()

            print("Button Pressed")

            return

@bot.command()
async def monith(ctx):
    # monitors temperature and humidity indefinitly until the user presses the button

    mylcd.lcd_clear()

    print("printing embed")

    embed = discord.Embed(
        title="Displaying Temperature and Humidity",
        description="Please press the button to stop monitoring",
        color=0xEEE657,
    )

    await ctx.send(embed=embed)

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        lcd_text = "Temp: " + str(temperature) + "C"
        lcd_text2 = "Humidity: " + str(humidity) + "%"

        mylcd.lcd_display_string(lcd_text, 1)
        mylcd.lcd_display_string(lcd_text2, 2)

        button_val = GPIO.input(23)

        if button_val == False:
            mylcd.lcd_clear()

            print("Button Pressed")

            return

        

@bot.event
async def on_ready():

    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):

    print("message-->", message)

    if message.author == bot.user:
        return

    if message.channel.id == 1158793702387499079:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        if message.content == "clear":
            embed = discord.Embed(
                title="Clearing LCD",
                description="The LCD has been cleared",
                color=0xEEE657,
            )

            await message.reply(embed=embed)

            mylcd.lcd_clear()

            return

        if "temperature" and "humidity" in message.content:
            mylcd.lcd_clear()

            embed = discord.Embed(
                title="Temperature and Humidity",
                description="The temperature and humidity has been displayed on the LCD",
                color=0xEEE657,
            )
            await message.reply(embed=embed)

            lcd_text = "Temp: " + str(temperature) + "C"
            lcd_text2 = "Humidity: " + str(humidity) + "%"

            mylcd.lcd_display_string(lcd_text, 1)
            mylcd.lcd_display_string(lcd_text2, 2)

            return

        if "temperature" in message.content:
            mylcd.lcd_clear()

            embed = discord.Embed(
                title="Temperature",
                description="The temperature has been displayed on the LCD",
                color=0xEEE657,
            )
            await message.reply(embed=embed)

            lcd_text = "Temp: " + str(temperature) + "C"
            mylcd.lcd_display_string(lcd_text, 1)

            return

        if "humidity" in message.content:
            mylcd.lcd_clear()

            embed = discord.Embed(
                title="Humidity",
                description="The humidity has been displayed on the LCD",
                color=0xEEE657,
            )
            await message.reply(embed=embed)

            lcd_text = "Humidity: " + str(humidity) + "%"
            mylcd.lcd_display_string(lcd_text, 1)
            
            return

    await bot.process_commands(message)


bot.run("[Enter your bot token here]")
