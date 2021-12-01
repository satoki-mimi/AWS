import requests

url = "https://discord.com/api/v8/applications/{application.id}/guilds/{guild.id}/commands"

json = {
    "name": "minecraft-server",
    "type": 1,
    "description": "Post to Amazon API Gateway",
    "options": [
        {
            "name": "control",
            "description": "Select a command",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "start",
                    "value": "control_start"
                },
                {
                    "name": "stop",
                    "value": "control_stop"
                }
            ]
        }
    ]
}

headers = {
    "Authorization": "Bot {bot.token}"
}

r = requests.post(url, headers=headers, json=json)
