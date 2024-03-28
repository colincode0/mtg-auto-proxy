import re
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
import requests

# https://api.scryfall.com/cards/cmm/742
# url = 'https://api.scryfall.com/cards/cmm/742'

def fetch_card_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch card data: {response.status_code}")
        return None

# Function to fetch card data from the API
def fetch_card_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch card data: {response.status_code}")
        return None

def create_card_data_from_api(api_data):
    card_data = {
        "template": api_data["colors"][0].lower() if api_data["colors"] else "colorless",  # Handle cards without colors
        "mana_cost": api_data["mana_cost"],
        "card_name": api_data["name"],
        "type_line": api_data["type_line"],
        "text": api_data["oracle_text"],
        "output_path": "output_card.png"  # Define your desired output file name
    }

    # Add power and toughness only if they are present
    if 'power' in api_data and 'toughness' in api_data:
        card_data["power"] = api_data["power"]
        card_data["toughness"] = api_data["toughness"]

    return card_data

def replace_symbols_with_images(template, draw, text, start_x, start_y, font, max_width):
    pattern = re.compile(r'\{[0-9XGURWB]+\}')
    lines = text.split('\n')
    current_y = start_y
    for line in lines:
        current_x = start_x
        line_words = re.split(r'(\s+|\{[0-9XGURWB]+\})', line)  # Split by whitespace and symbols
        for word in line_words:
            if word.isspace() or word == "":
                continue
            if pattern.fullmatch(word):  # Symbol
                symbol = word.strip('{}')
                symbol_image_path = f'assets/manaSmall/{symbol}.png'
                with Image.open(symbol_image_path) as symbol_image:
                    template.paste(symbol_image.convert('RGBA'), (current_x, current_y), symbol_image)
                    current_x += symbol_image.width
            else:  # Regular text
                # Add space if it's not the first word/symbol on the line
                if current_x > start_x:
                    word = ' ' + word
                word_bbox = draw.textbbox((0, 0), word, font=font)
                word_width = word_bbox[2] - word_bbox[0]
                # Check if word overflows max width
                if current_x + word_width > max_width:
                    current_y += word_bbox[3] + 10  # Adjust line spacing
                    current_x = start_x  # Reset to start_x
                draw.text((current_x, current_y), word, (0, 0, 0), font=font)
                current_x += word_width
        current_y += draw.textbbox((0, 0), 'Ay', font=font)[3] + 10  # Move to next line after each line


def render_text_with_stroke(draw, text, position, font, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2):
    x, y = position
    # Draw stroke
    for adj in range(-stroke_width, stroke_width+1):
        for adjy in range(-stroke_width, stroke_width+1):
            draw.text((x + adj, y + adjy), text, font=font, fill=stroke_fill)
    # Draw main text
    draw.text((x, y), text, font=font, fill=fill)


def create_font(font_path, size):
    return ImageFont.truetype(font_path, size)

def render_text(draw, text, position, font, fill=(0, 0, 0)):
    draw.text(position, text, fill, font=font)



def parse_mana_cost(draw, mana_cost, template, start_x, start_y, font):
    mana_symbols = re.findall(r'\{[0-9XGURWB]+\}', mana_cost)
    current_x = start_x
    for symbol in mana_symbols:
        symbol = symbol.strip('{}')
        symbol_image_path = f'assets/mana/{symbol}.png'
        with Image.open(symbol_image_path) as symbol_image:
            template.paste(symbol_image.convert('RGBA'), (current_x, start_y), symbol_image)
            current_x += symbol_image.size[0] + 5
    return current_x

def create_card(card):
    template = Image.open(f"assets/templates/{card['template']}_temp.png")
    # template = Image.open(f"assets/templates/white_temp.png")
    draw = ImageDraw.Draw(template)
    
    font_path = "assets/fonts/Cheboyga.ttf"
    font_text = create_font(font_path, 22)
    font_name = create_font(font_path, 33)
    font_pt = create_font(font_path, 44)
    
    render_text_with_stroke(draw, card["card_name"], (60, 50), font_name)
    render_text_with_stroke(draw, card["type_line"], (77, 585), font_text)
    
    mana_cost_end_x = parse_mana_cost(draw, card["mana_cost"], template, template.width - 181, 50, font_text)
    
 # Render power/toughness if present
    if 'power' in card and 'toughness' in card:
        font_pt = create_font(font_path, 44)
        pt_text = f"{card['power']}/{card['toughness']}"
        pt_position = (template.width - draw.textbbox((0, 0), pt_text, font=font_pt)[2] - 72, template.height - 107)
        render_text_with_stroke(draw, pt_text, pt_position, font_pt, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2)


    replace_symbols_with_images(template, draw, card["text"], 99, 646, font_text, 656)
    
    template.save(card["output_path"], format='PNG')

if __name__ == "__main__":
    card_api_url = "https://api.scryfall.com/cards/cmm/828"
    card_api_data = fetch_card_data(card_api_url)

    if card_api_data:
        card_details = create_card_data_from_api(card_api_data)
        create_card(card_details)
