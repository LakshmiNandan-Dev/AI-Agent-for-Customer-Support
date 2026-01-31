import requests
import json

def handoff_to_human(query,  response=None):
    webhook_url = "https://discord.com/api/webhooks/1465450296770695351/NyViBXjmSWuuac2NkEFXhs0iUqMUqUqwD4TkhL9rCgueVyoeST7IwH9olHPZjxRSAOmR"

    payload = {
        "text" : f"Escalates query : {query}\nResponse: {response if response else 'N/A'}"
    }
    requests.post(webhook_url, data=json.dumps(payload))
    return "Query escalated to human support"
