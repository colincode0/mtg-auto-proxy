import re
from PIL import Image, ImageDraw, ImageFont
import textwrap

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
    # ... other cards
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
                symbol_image = Image.open(f'assets/manaSmall/{symbol}.png').convert('RGBA')
                if current_x + symbol_image.width > max_width:  # Check if symbol overflows max width
                    current_y += draw.textbbox((0, 0), 'Ay', font=font)[3] + 10  # Add line height
                    current_x = start_x  # Reset to start_x
                template.paste(symbol_image, (current_x, current_y), symbol_image)
                current_x += symbol_image.width
            else:  # Regular text
                # Add space if it's not the first word/symbol on the line
                if current_x > start_x:
                    word = ' ' + word
                # Check if word overflows max width
                if current_x + draw.textbbox((0, 0), word, font=font)[2] > max_width:
                    current_y += draw.textbbox((0, 0), 'Ay', font=font)[3] + 10  # Add line height
                    current_x = start_x  # Reset to start_x
                draw.text((current_x, current_y), word, font=font, fill=(0, 0, 0))
                current_x += draw.textbbox((0, 0), word, font=font)[2]
        current_y += draw.textbbox((0, 0), 'Ay', font=font)[3] + 10  # Move to next line after each line

def parse_mana_cost(mana_cost, template, start_x, start_y):
    # Use regex to find all instances of mana symbols
    mana_symbols = re.findall(r'\{[0-9XGURWB]+\}', mana_cost)
    current_x = start_x
    for symbol in mana_symbols:
        # Strip the curly braces and construct the image path
        symbol = symbol.strip('{}')
        symbol_image = Image.open(f'assets/mana/{symbol}.png').convert('RGBA')
        # Paste the symbol image onto the template
        template.paste(symbol_image, (current_x, start_y), symbol_image)
        # Update x position for next symbol
        current_x += symbol_image.size[0] + 5  # Add a small margin
    return current_x


def create_card(card):
    # Load the main card template
    template_files = {
        # ... other template files
        "green": "assets/templates/green_temp.png",
        # ... other template files
    }
    template = Image.open(template_files[card["template"]])

    # Create a drawing context for the template
    draw = ImageDraw.Draw(template)

    # Define the font for the card text
    font_path = "assets/fonts/Cheboyga.ttf"
    font_size_text = 22
    font_text = ImageFont.truetype(font_path, font_size_text)

    # Render the mana cost at the top-right corner
    mana_cost_start_x = template.width - 181  # Adjust based on your template
    mana_cost_start_y = 50  # Adjust based on your template
    current_x = parse_mana_cost(card["mana_cost"], template, mana_cost_start_x, mana_cost_start_y)

    # Render the type line
    type_line_x = 77  # Adjust based on your template
    type_line_y = 585  # Adjust based on your template
    draw.text((type_line_x, type_line_y), card["type_line"], (0, 0, 0), font=font_text)

    # Define font for power/toughness
    font_pt = ImageFont.truetype(font_path, font_size_text)  # Assuming same size as card text for now

    # Calculate position for power/toughness text
    pt_text = f"{card['power']}/{card['toughness']}"
    pt_width, pt_height = draw.textsize(pt_text, font=font_pt)
    pt_x = template.width - pt_width - 30  # 30 pixels padding from the right edge
    pt_y = template.height - pt_height - 30  # 30 pixels padding from the bottom edge

    # Render power/toughness text
    draw.text((pt_x, pt_y), pt_text, (255, 255, 255), font=font_pt)  # White text for visibility


    # Add card name
    font_size_name = 33
    font_name = ImageFont.truetype(font_path, font_size_name)
    text_x = 60  # Adjust as needed
    text_y = 50  # Adjust as needed
    draw.text((text_x, text_y), card["card_name"], (0, 0, 0), font=font_name)

    # Add card text with symbols
    text_x = 111
    text_y = 650
    max_text_width = 656  # Adjust this value based on your card's actual template size
    replace_symbols_with_images(template, draw, card["text"], text_x, text_y, font_text, max_text_width)

    # Save the result
    template.save(card["output_path"], format='PNG')

# Use the function
for card_obj in cards:
    create_card(card_obj)
