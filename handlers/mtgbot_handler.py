import ast
from utils.slack_client import app
import scry


@app.view("")
def post_random_card(ack, body, say, context):
    ack()
    user_token = context.get('authorize_result').get('user_token')
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
        token=user_token,
        response_type="in_channel",
        as_user=True,
        blocks=[card_section]
    )


@app.action("Random")
def get_random_card_modal(ack, body, context):
    ack()
    user_token = context.get('authorize_result').get('user_token')
    # print(body)
    card = scry.random_card()
    metadata_dict = ast.literal_eval(body['view']['private_metadata'])
    channel = metadata_dict['channel']
    res = app.client.views_update(
        view_id=body["container"]["view_id"],
        token=user_token,
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
                    "image_url": card['image_uris']['normal'],
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
def mtg_search(ack, body, say, context, respond):
    user_token = context.get('authorize_result').get('user_token')
    # Acknowledge command request
    ack()
    text = body.get('text')
    if text and user_token:
        info = scry.search_card(search_term=text)
        card_block_type = info[0]['type']
        if card_block_type == "image":
            say(
                token=user_token,
                response_type="in_channel",
                blocks=info
            )
        else:
            respond(
                response_type="ephemeral",
                blocks=info
            )
    elif user_token:
        print(body)
        card = scry.random_card()
        # print(f"random: {card}")
        res = app.client.views_open(
            trigger_id=body["trigger_id"],
            token=user_token,
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
                        "image_url": card['image_uris']['normal'],
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
    else:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "You'll need to authorize MtGSearch before you can use this bot!"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Authorize!",
                            "emoji": True
                        },
                        "value": "authorizebutton",
                        "action_id": "auth_button",
                        "url": user_auth_url
                    }
                ]
            }
        ]
        # print(blocks)
        respond(
            response_type="ephemeral",
            blocks=blocks
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


@app.action("auth_button")
def button_auth(ack, respond):
    ack()
    respond(
        response_type="ephemeral",
        text='',
        replace_original=True,
        delete_original=True
    )