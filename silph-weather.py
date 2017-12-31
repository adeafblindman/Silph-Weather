import discord
from discord.ext import commands
import pyowm
from geopy.geocoders import Nominatim

bot = commands.Bot(command_prefix='!')
owm = pyowm.OWM('OPENWEATHERMAP API')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----RUNNING-----')

#-------------
#utility functions
#-------------
def degToCompass(num):
    val = int((num/22.5)+.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


#-------------
#bot commands
#-------------


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("i'm alive!")


@bot.command(pass_context=True)
async def w(ctx, *args):

    ## Join all the strings given.
    string = ' '.join(args)

    geolocator = Nominatim()
    location = geolocator.geocode(string)

    try:
        ## Get the weather
        observation = owm.weather_at_coords(location.latitude, location.longitude)
        w = observation.get_weather()

        sky_status = w.get_detailed_status()
        temp_f     = w.get_temperature(unit = 'fahrenheit')
        wind       = w.get_wind()
        wind_mph   = round(wind["speed"] * 2.23694, 2)
        cloud_cov  = w.get_clouds()
        humidity   = w.get_humidity()
        wx_code    = w.get_weather_code()

        ## Print the weather.
        msg = discord.Embed(title= "Weather for " + str(location), description = str(sky_status), color=0xDF4D11)
        msg.add_field(name = "Temperature", value = str(temp_f["temp"]) + " F", inline = False)
        msg.add_field(name = "Wind", value =  degToCompass(wind["deg"]) + ' ' + str(wind_mph) + " MPH", inline = False)
        msg.add_field(name = "Cloud Coverage", value =  str(cloud_cov) + " %", inline = False)
        msg.add_field(name = "Humidity", value =  str(humidity) + " %", inline = False)
        ## msg.add_field(name = "Code", value =  str(wx_code), inline = False)

        ## Clear conditions
        if(wx_code == 800):
            msg.add_field(name = "Boosted Types", value = "<:Grass:393253049545654272> <:Fire:389113469665804318> <:Ground:389121614048133130>", inline = False)
        ## Partly Cloudy
        elif(wx_code == 801 or wx_code == 802 or wx_code == 701):
            msg.add_field(name = "Boosted Types", value = "<:Normal:389121615490842634> <:Rock:389121614098464788>", inline = False)
        ## Cloudy
        elif(wx_code == 803 or wx_code == 804 or wx_code == 721):
            msg.add_field(name = "Boosted Types", value = "<:Fairy:389121572616667145> <:Fighting:389121572620992534> <:Poison:389121615545368577>", inline = False)
        ## Fog
        elif(wx_code == 741):
            msg.add_field(name = "Boosted Types", value = "<:Dark:389121572813799424> <:Ghost::389121615318745090>", inline = False)
        ## Rain
        elif(wx_code >= 200 and wx_code < 600):
            msg.add_field(name = "Boosted Types", value = "<:Water:389121613804601345> <:Electric:389121572612341760> <:Bug:389121572431986688>", inline = False)
        ## Wind
        elif(wx_code >= 952 and wx_code < 958):
            msg.add_field(name = "Boosted Types", value = "<:Flying:389121613905526786> <:Dragon:389121572859936769> <:Psychic:389121615402762261>", inline = False)
        ## Snow
        elif(wx_code >= 600 and wx_code < 700):
            msg.add_field(name = "Boosted Types", value = "<:Ice:389121615453093888> <:Steel:389121615541043200>", inline = False)

        await bot.send_message(ctx.message.channel, embed = msg)

    ## If the location is not found alert the user.
    except pyowm.exceptions.not_found_error.NotFoundError:
        await bot.say("Location not found!")
#---------
#bot TOKEN
#---------

bot.run('DISCORD TOKEN')
