import requests


def search_card(search_term):
    url = "https://api.scryfall.com/cards/named?fuzzy="
    response = requests.get(f"{url}{search_term}")
    card = response.json()
    if response.status_code == 200:
        card_section = {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": card['name'],
                    "emoji": True
                },
                "image_url": card['image_uris']['normal'],
                "alt_text": card['name']
            }
        blockInfo = [
            card_section,
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Post",
                            "emoji": True
                        },
                        "value": f"{card_section}",
                        "style": "primary",
                        "action_id": "post"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "delete",
                        "style": "danger",
                        "action_id": "delete"
                    }
                ]
            }
        ]
        return [card_section]
    elif response.status_code == 404:
        blockInfo = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": card['details']
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "delete",
                        "style": "danger",
                        "action_id": "delete"
                    }
                ]
            }
        ]
    return blockInfo


def random_card():
    url = "https://api.scryfall.com/cards/random"
    response = requests.get(url)
    card = response.json()
    # print(card)
    return card

def card_by_id(id):
    url = "https://api.scryfall.com/cards/"
    response = requests.get(f"{url}{id}")
    card = response.json()
    # print(card)
    return card

