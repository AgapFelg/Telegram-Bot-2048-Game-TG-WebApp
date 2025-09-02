from PIL import Image, ImageDraw, ImageFont


def generate_image(board, size, filename):
    cell_size = 100  # базовый размер ячейки
    padding = 15  # отступ между ячейками
    board_padding = 15  # отступ поля от краев

    width = height = size * cell_size + (size - 1) * padding + 2 * board_padding

    img = Image.new('RGB', (width, height), color='#ccc')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        font = ImageFont.load_default()

    draw.rectangle([0, 0, width, height], fill='#ccc', outline='#ccc')

    for i in range(size):
        for j in range(size):
            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            draw.rectangle([x1, y1, x2, y2], fill='#d8d8d8', outline='#ccc')

    for i in range(size):
        for j in range(size):
            value = board[i][j]

            if value == 0:
                continue

            bg_colors = {
                2: '#eee', 4: '#ddd', 8: '#ccc',
                16: '#bbb', 32: '#aaa', 64: '#999',
                128: '#888', 256: '#777', 512: '#666',
                1024: '#555', 2048: '#333'
            }

            text_colors = {
                2: '#000', 4: '#000', 8: '#000',
                16: '#fff', 32: '#fff', 64: '#fff',
                128: '#fff', 256: '#fff', 512: '#fff',
                1024: '#fff', 2048: '#fff'
            }

            bg_color = bg_colors.get(value, '#eee')
            text_color = text_colors.get(value, '#000')

            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            draw.rectangle([x1, y1, x2, y2], fill=bg_color, outline='#ccc')

            radius = 3
            draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=bg_color)

            if value != 0:
                text = str(value)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                text_x = x1 + (cell_size - text_width) // 2
                text_y = y1 + (cell_size - text_height) // 2

                if value >= 1024:
                    try:
                        small_font = ImageFont.truetype('arial.ttf', 27)
                    except:
                        small_font = font
                    draw.text((text_x, text_y), text, fill=text_color, font=small_font)
                else:
                    draw.text((text_x, text_y), text, fill=text_color, font=font)

    img.save(filename, 'PNG')
    return img


def generate_image_classic(board, size, filename):
    cell_size = 100  # базовый размер ячейки
    padding = 15  # отступ между ячейками
    board_padding = 15  # отступ поля от краев

    width = height = size * cell_size + (size - 1) * padding + 2 * board_padding

    img = Image.new('RGB', (width, height), color='#bbada0')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        font = ImageFont.load_default()

    draw.rectangle([0, 0, width, height], fill='#bbada0', outline='#bbada0')

    for i in range(size):
        for j in range(size):
            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            draw.rectangle([x1, y1, x2, y2], fill='#eee4da', outline='#bbada0')

    for i in range(size):
        for j in range(size):
            value = board[i][j]

            if value == 0:
                continue

            bg_colors = {
                2: '#eee4da', 4: '#ede0c8', 8: '#f2b179',
                16: '#f59563', 32: '#f67c5f', 64: '#f65e3b',
                128: '#edcf72', 256: '#edcc61', 512: '#edc850',
                1024: '#edc53f', 2048: '#edc22e'
            }

            text_colors = {
                2: '#776e65', 4: '#776e65',
                8: '#f9f6f2', 16: '#f9f6f2', 32: '#f9f6f2',
                64: '#f9f6f2', 128: '#f9f6f2', 256: '#f9f6f2',
                512: '#f9f6f2', 1024: '#f9f6f2', 2048: '#f9f6f2'
            }

            bg_color = bg_colors.get(value, '#eee4da')
            text_color = text_colors.get(value, '#776e65')

            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            draw.rectangle([x1, y1, x2, y2], fill=bg_color, outline='#bbada0')

            radius = 3
            draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=bg_color)

            if value != 0:
                text = str(value)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                text_x = x1 + (cell_size - text_width) // 2
                text_y = y1 + (cell_size - text_height) // 2

                if value >= 1024:
                    try:
                        small_font = ImageFont.truetype('arial.ttf', 27)
                    except:
                        small_font = font
                    draw.text((text_x, text_y), text, fill=text_color, font=small_font)
                else:
                    draw.text((text_x, text_y), text, fill=text_color, font=font)

    img.save(filename, 'PNG')
    return img