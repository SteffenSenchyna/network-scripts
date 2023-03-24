import os
import subprocess
import threading
from dotenv import load_dotenv
from flask import Response
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed


def getScan():
    load_dotenv()
    discordURL = "https://discord.com/api/webhooks/1088239694464168088/wNsQL0Pem8UAUrqpNKqfXSJwho4jExIPNGpXQGVn7txCUNpUm0e2uv879L3S3U84Iz8U"
    url = "http://0.0.0.0:8000/api/dcim/devices/"
    threads = []
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': os.environ["NETBOXTOKEN"]
    }

    response = requests.get(url, headers=headers).json()
    response = response["results"]
    # with open("devices.json", "w") as outfile:
    #     json.dump(response, outfile)
    downHosts = []

    def ping(ip, host, downHosts):
        result = subprocess.run(
            ['ping', '-c', '1', ip], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            host["ping_status"] = "up"
        else:
            host["ping_status"] = "down"
            downHosts.append(host["name"])

    try:
        for i in response:
            t = threading.Thread(target=ping, args=(
                i["primary_ip4"]["address"], i, downHosts))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        if len(downHosts) > 0:
            webhook = DiscordWebhook(
                url=discordURL)
            embed = DiscordEmbed(
                title='Network Event', description='The following network devices management IPs cannot be pinged', color='03b2f8')
            embed.set_author(name='NetBot',
                             icon_url='https://avatars0.githubusercontent.com/u/14542790')
            embed.set_footer(text='Down Network Devices')
            embed.set_timestamp()
            embed.add_embed_field(name='Devices', value=str(downHosts)[1:-1])
            # add embed object to webhook
            webhook.add_embed(embed)
            response = webhook.execute()
    except Exception as e:
        print(e)
        return Response(e, status=400)


getScan()
