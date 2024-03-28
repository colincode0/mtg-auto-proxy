from PIL import Image, ImageDraw, ImageFont
import textwrap

# https://api.scryfall.com/cards/cmm/742

cards = [
    {
        "template": "green",
        "mana1_path": "mtg/1_colorless.png",
        "mana2_path": "mtg/forest.png",
        "card_name": "Demo Test",
        "text": "This is the card text.",
        "output_path": "output_card1.png"
    },
    # ... other cards
]

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
    mana1 = Image.open("assets/mana/1_colorless.png")
    mana2 = Image.open("assets/mana/forest.png")

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

    # Add card text
    draw = ImageDraw.Draw(template)
    font_text = ImageFont.truetype("assets/fonts/Cheboyga.ttf", 17)  # Adjust font and size for the card text
    text_x = 111  # Adjust the x-coordinate for text placement
    text_y = 650  # Adjust the y-coordinate for text placement

    # Text wrapping (if necessary)
    wrapped_text = textwrap.fill(card["text"], width=40)  # Adjust 'width' as needed for your card
    draw.text((text_x, text_y), wrapped_text, (0, 0, 0), font=font_text)

    # Save the result
    template.save(card["output_path"], format='PNG')

# Use the function
for card_obj in cards:
    create_card(card_obj)