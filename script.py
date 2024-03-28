from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_card(template_path, mana1_path, mana2_path, card_name, card_text, output_path):
    # Load the main card template
    template = Image.open("mtg/main_temp.png")

    template_white = Image.open("mtg/main_temp.png")
    template_green = Image.open("mtg/green_temp.png")
    template_blue = Image.open("mtg/blue_temp.png")
    template_red = Image.open("mtg/red_temp.png")
    template_black = Image.open("mtg/black_temp.png")
    
    # Load mana images
    mana1 = Image.open("mtg/1_colorless.png")
    mana2 = Image.open("mtg/forest.png")

    # Calculate position for mana images (top-right corner)
    mana1_x = template.width - mana1.width - 70  # 10 pixels from the right edge
    mana1_y = 63  # 63 pixels from the top

    mana2_x = mana1_x - mana2.width - 5  # 5 pixels left to the first mana
    mana2_y = 63

    # Paste mana images on the template
    template.paste(mana1, (mana1_x, mana1_y), mana1)
    template.paste(mana2, (mana2_x, mana2_y), mana2)

    # Add card name
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("mtg/Cheboyga.ttf", 33)  # You might need to adjust the font and size
    text_x = 60  # 60 pixels from the left
    text_y = 60  # 60 pixels from the top
    draw.text((text_x, text_y), card_name, (0, 0, 0), font=font)  # Black text


    # Add card text
    draw = ImageDraw.Draw(template)
    font_text = ImageFont.truetype("mtg/Cheboyga.ttf", 17)  # Adjust font and size for the card text
    text_x = 111  # Adjust the x-coordinate for text placement
    text_y = 660  # Adjust the y-coordinate for text placement

    # Text wrapping (if necessary)
    wrapped_text = textwrap.fill(card_text, width=40)  # Adjust 'width' as needed for your card
    draw.text((text_x, text_y), wrapped_text, (0, 0, 0), font=font_text)

    # Save the result
    template.save(output_path, format='PNG')

# Use the function
create_card('main_temp.png', '1_colorless.png', 'forrest.png', 'Demo Test', 'This is the card text.', 'output_card.jpg')
