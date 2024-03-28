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
    lines = text.split('\n')
    current_y = start_y

    for line in lines:
        words = re.split(r'(\{[0-9XGURWB]+\})', line)  # Split by symbols only
        current_x = start_x
        for word in words:
            if word == "":
                continue

            # If the word is a symbol, paste the symbol image
            if pattern.fullmatch(word):
                symbol = word.strip('{}')
                symbol_image = Image.open(f'assets/manaSmall/{symbol}.png')
                if symbol_image.mode != 'RGBA':
                    symbol_image = symbol_image.convert('RGBA')
                template.paste(symbol_image, (current_x, current_y), symbol_image)
                current_x += symbol_image.size[0]
            else:  # If the word is a text
                # Add spaces back except for the first word in a line
                if current_x > start_x:
                    word = " " + word
                word_width, word_height = draw.textsize(word, font=font)
                if current_x + word_width > template.size[0]:  # New line if text overflows
                    current_y += word_height + 5  # Adjust line spacing if needed
                    current_x = start_x
                draw.text((current_x, current_y), word, font=font, fill=(0, 0, 0))
                current_x += word_width

        # Increment y-coordinate for the next line
        current_y += font.getsize('Ay')[1] + 5  # Adjust line spacing if needed


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
    font_text = ImageFont.truetype("assets/fonts/Cheboyga.ttf", 22)
    text_x = 111
    text_y = 650
   
    replace_symbols_with_images(template, draw, card["text"], text_x, text_y, font_text)

    # # Text wrapping (if necessary)
    # wrapped_text = textwrap.fill(card["text"], width=40)  # Adjust 'width' as needed for your card
    # draw.text((text_x, text_y), wrapped_text, (0, 0, 0), font=font_text)

    # Save the result
    template.save(card["output_path"], format='PNG')

# Use the function
for card_obj in cards:
    create_card(card_obj)