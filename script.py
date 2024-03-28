import re
from PIL import Image, ImageDraw, ImageFont
import textwrap

# https://api.scryfall.com/cards/cmm/742

cards = [
    {
        "template": "green",
        "mana1_path": "mtg/1.png",
        "mana2_path": "mtg/G.png",
        "card_name": "Demo Test",
        "text": "This spell costs {X} less to cast, where X is the total mana value of noncreature enchantments you control.\nTrample\n{1}{G}, Sacrifice another enchantment: Nyxborn Behemoth gains indestructible until end of turn.",
        "output_path": "output_card1.png"
    },
    # ... other cards
]

def replace_symbols_with_images(template, draw, text, start_x, start_y, font):
    pattern = re.compile(r'\{[0-9XGURWB]+\}')
    current_position = start_x, start_y

    for line in text.split('\n'):
        offset = 0
        for match in pattern.finditer(line):
            part = line[offset:match.start()]
            # Draw the text part
            draw.text(current_position, part, font=font, fill=(0, 0, 0))
            bbox = font.getbbox(part)  # Using getbbox instead of getsize
            current_position = (current_position[0] + bbox[2], current_position[1])

            # Draw the symbol image
            symbol = match.group()
            symbol_image = Image.open(f'assets/mana/{symbol[1:-1]}.png')
            template.paste(symbol_image, (current_position[0], current_position[1] - symbol_image.height // 2 + bbox[3] // 2), symbol_image)
            current_position = (current_position[0] + symbol_image.width, current_position[1])

            offset = match.end()

        remaining_text = line[offset:]
        draw.text(current_position, remaining_text, font=font, fill=(0, 0, 0))
        bbox = font.getbbox(remaining_text)
        current_position = (start_x, current_position[1] + bbox[3])


def create_card(card):
    # Load the main card template
    template_files = {
        "white": "assets/templates/white_temp.png",
        "green": "assets/templates/green_temp.png",
        "blue": "assets/templates/blue_temp.png",
        "red": "assets/templates/red_temp.png",
        "black": "assets/templates/black_temp.png"
    }
    template = Image.open(template_files[card["template"]])
    
    # Load mana images
    mana1 = Image.open("assets/mana/1.png")
    mana2 = Image.open("assets/mana/G.png")

    # Calculate position for mana images (top-right corner)
    mana1_x = template.width - mana1.width - 70  # 10 pixels from the right edge
    mana1_y = 55  # 63 pixels from the top

    mana2_x = mana1_x - mana2.width - 5  # 5 pixels left to the first mana
    mana2_y = 55

    # Paste mana images on the template
    template.paste(mana1, (mana1_x, mana1_y), mana1)
    template.paste(mana2, (mana2_x, mana2_y), mana2)

  # Add card name
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("assets/fonts/Cheboyga.ttf", 33)  # Adjust font and size
    text_x = 60  # 60 pixels from the left
    text_y = 50  # 60 pixels from the top
    draw.text((text_x, text_y), card["card_name"], (0, 0, 0), font=font)  # Black text

 # Add card text with symbols
    draw = ImageDraw.Draw(template)
    font_text = ImageFont.truetype("assets/fonts/Cheboyga.ttf", 17)
    text_x = 111
    text_y = 650
    wrapped_text = textwrap.fill(card["text"], width=40)
    replace_symbols_with_images(template, draw, wrapped_text, text_x, text_y, font_text)

    # # Text wrapping (if necessary)
    # wrapped_text = textwrap.fill(card["text"], width=40)  # Adjust 'width' as needed for your card
    # draw.text((text_x, text_y), wrapped_text, (0, 0, 0), font=font_text)

    # Save the result
    template.save(card["output_path"], format='PNG')

# Use the function
for card_obj in cards:
    create_card(card_obj)