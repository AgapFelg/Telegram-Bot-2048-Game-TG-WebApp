from PIL import Image, ImageDraw, ImageFont

def generate_image(board, size, filename):

    cell_size = 50
    padding = 5

    width = height = size * cell_size + (size + 1) * padding

    img = Image.new('RGB', (width, height), color='#fff')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('arial.ttf', 15)
    except:
        font = ImageFont.load_default()
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            bg_color = '#fff'
            text_color = '#000'

            # координаты ячейки
            x1 = j * cell_size + (j + 1) * padding
            y1 = i * cell_size + (i + 1) * padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            draw.rectangle([x1, y1, x2, y2], fill=bg_color, outline='#000', width=2)

            if value != 0:
                text = str(value)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                text_x = x1 + (cell_size - text_width) // 2
                text_y = y1 + (cell_size - text_height) //2

                draw.text((text_x, text_y), text, fill=text_color, font=font)

            img.save(filename, 'PNG')
    return img