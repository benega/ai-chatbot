import json
import logging

from flask import current_app, jsonify
import requests

# from app.services.openai_service import generate_response
import re


from typing import Dict

def log_http_response(response: requests.Response) -> None:
    """Log the HTTP response details."""
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient: str, text: str) -> str:
    """Create a JSON string for a text message input.

    Args:
        recipient: The recipient's phone number.
        text: The message text.

    Returns:
        A JSON string representing the text message input.
    """
    message_input = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }
    return json.dumps(message_input)


def generate_response(response: str) -> str:
    """Return text in uppercase."""
    return response.upper()


def send_message(data: str) -> requests.Response:
    """Send a message to WhatsApp.

    Args:
        data: The JSON string representing the message.

    Returns:
        The response from the WhatsApp API.
    """
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = (
        f"https://graph.facebook.com/{current_app.config['VERSION']}"
        f"/{current_app.config['PHONE_NUMBER_ID']}/messages"
    )

    print(f"send_message URL: {url}, data: {data}")

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text: str) -> str:
    """Process text for WhatsApp formatting.

    Removes brackets and applies WhatsApp-style formatting to the text.

    Args:
        text: The text to process.

    Returns:
        The processed text.
    """
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body: Dict) -> None:
    """Process incoming WhatsApp message.

    Extracts relevant information from the message body and
    sends a response.

    Args:
        body: The JSON body of the webhook event.
    """
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    print(f"wa_id: {wa_id}, name: {name}")

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # TODO: implement custom function here
    response = generate_response(message_body)

    # OpenAI Integration
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)

    # data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    data = get_text_message_input(wa_id, response)
    send_message(data)


def is_valid_whatsapp_message(body: Dict) -> bool:
    """Check if the incoming webhook event is a valid message.

    Args:
        body: The JSON body of the webhook event.

    Returns:
        True if the message is valid, False otherwise.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
