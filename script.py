import re
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json


# https://api.scryfall.com/cards/cmm/742

cards = [
    {
        "template": "green",
        "mana1_path": "mtg/1.png",
        "mana2_path": "mtg/G.png",
        "mana_cost" : "{1}{G}{G}",
        "card_name": "Nyxborn Behemoth",
        "type_line": "Enchantment Creature — Beast",
        "text": "This spell costs {X} less to cast, where X is the total mana value of noncreature enchantments you control.\nTrample\n{1}{G}, Sacrifice another enchantment: Nyxborn Behemoth gains indestructible until end of turn.",
        "output_path": "output_card1.png",
        "power": "10",
        "toughness": "10"
    },
]
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
    draw = ImageDraw.Draw(template)
    
    font_path = "assets/fonts/Cheboyga.ttf"
    font_text = create_font(font_path, 22)
    font_name = create_font(font_path, 33)
    font_pt = create_font(font_path, 44)
    
    render_text(draw, card["card_name"], (60, 50), font_name)
    render_text(draw, card["type_line"], (77, 585), font_text)
    
    mana_cost_end_x = parse_mana_cost(draw, card["mana_cost"], template, template.width - 181, 50, font_text)
    
    pt_text = f"{card['power']}/{card['toughness']}"
    pt_position = (template.width - draw.textbbox((0, 0), pt_text, font=font_pt)[2] - 66, template.height - 73)
    render_text(draw, pt_text, pt_position, font_pt, fill=(255, 255, 255))
    
    replace_symbols_with_images(template, draw, card["text"], 111, 650, font_text, 656)
    
    template.save(card["output_path"], format='PNG')

for card_obj in cards:
    create_card(card_obj)
