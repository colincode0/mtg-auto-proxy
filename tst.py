import re
from PIL import Image, ImageDraw, ImageFont

# Load your base image (card template)
base_image = Image.open('assets/templates/white_temp.png')
draw = ImageDraw.Draw(base_image)
font = ImageFont.load_default()

# Your text string
text = "This spell costs {X} less to cast, where X is the total mana value of noncreature enchantments you control.\nTrample\n{1}{G}, Sacrifice another enchantment: Nyxborn Behemoth gains indestructible until end of turn."

# Function to replace mana symbols with images
def replace_symbols_with_images(draw, text, start_position):
    pattern = re.compile(r'\{[0-9XGURWB]+\}')
    current_position = 300,300

    for part in pattern.split(text):
        # Draw the text part
        draw.text(current_position, part, font=font, fill=(0, 0, 0))
        current_position = (current_position[0] + font.getsize(part)[0], current_position[1])

        # Find the next symbol and draw its image
        match = pattern.search(text)
        if match:
            symbol = match.group()
            # Load the symbol image (you need to have these images)
            symbol_image = Image.open(f'assets/mana/{symbol[1:-1]}.png')
            base_image.paste(symbol_image, current_position, symbol_image)
            current_position = (current_position[0] + symbol_image.width, current_position[1])
            text = text[match.end():]

replace_symbols_with_images(draw, text, (10, 10))  # Adjust the starting position as needed

# Save the final image
base_image.save('final_card.png')
