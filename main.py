import os
from slack_bolt import App
from dotenv import load_dotenv
import scry
import ast

load_dotenv()

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_USER_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.view("")
def handle_view_submission_events(ack, body, say):
    ack()
    # print(body['view']['blocks'][1]['elements'][0]['value'])
    # card_id = body['view']['blocks'][1]['elements'][0]['value']
    # print(body)
    metadata_dict = ast.literal_eval(body['view']['private_metadata'])
    card_id = metadata_dict['card']
    channel = metadata_dict['channel']
    card = scry.card_by_id(card_id)
    # print(card)
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
    # print(card_section)
    say(
        channel=channel,
        response_type="in_channel",
        as_user=True,
        blocks=[card_section]
    )


@app.action("Random")
def handle_some_action(ack, body):
    ack()
    # print(body)
    card = scry.random_card()
    metadata_dict = ast.literal_eval(body['view']['private_metadata'])
    channel = metadata_dict['channel']
    res = app.client.views_update(
        view_id=body["container"]["view_id"],
        view={
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "Random Card",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Post",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "private_metadata": str({"channel": channel,
                                     "card": card['id']}),
            "blocks": [
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": card['name'],
                        "emoji": True
                    },
                    "image_url": card['image_uris']['small'],
                    "alt_text": card['name']
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Shuffle",
                                "emoji": True
                            },
                            "value": card['id'],
                            "action_id": "Random"
                        }
                    ]
                }
            ]
        }
    )


@app.command("/mtgsearch")
def mtg_search(ack, command, body, say, respond):
    # Acknowledge command request
    ack()
    text = command.get('text')
    if text:
        card = scry.search_card(search_term=text)
        say(
            response_type="in_channel",
            blocks=card
        )
    else:
        # print(body)
        card = scry.random_card()
        # print(f"random: {card}")
        res = app.client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": "Random Card",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Post",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": True
                },
                "private_metadata": str({"channel": body['channel_id'],
                                     "card": card['id']}),
                "blocks": [
                    {
                        "type": "image",
                        "title": {
                            "type": "plain_text",
                            "text": card['name'],
                            "emoji": True
                        },
                        "image_url": card['image_uris']['small'],
                        "alt_text": card['name']
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Shuffle",
                                    "emoji": True
                                },
                                "value": "default",
                                "action_id": "Random"
                            }
                        ]
                    }
                ]
            }
        )


@app.action("post")
def button_post(ack, body, say, respond):
    ack()
    card_string = body['actions'][0]['value']
    json_card = ast.literal_eval(card_string)
    respond(
        response_type="ephemeral",
        text='',
        replace_original=True,
        delete_original=True
    )
    say(
        response_type="in_channel",
        blocks=[json_card],
        replace_original=True,
        delete_original=True
    )


@app.action("delete")
def button_delete(ack, respond):
    ack()
    respond(
        response_type="ephemeral",
        text='',
        replace_original=True,
        delete_original=True
    )


# Ready? Start your app!
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
