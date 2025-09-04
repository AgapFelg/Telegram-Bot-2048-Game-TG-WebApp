# импорт необходимых модулей из библиотеки PIL (Python Imaging Library)
from PIL import Image, ImageDraw, ImageFont

# функция для генерации изображения игрового поля в черно-белой теме
def generate_image(board, size, filename):
    # базовый размер одной ячейки в пикселях
    cell_size = 100
    # отступ между ячейками
    padding = 15
    # отступ всего игрового поля от краев изображения
    board_padding = 15

    # расчет общей ширины и высоты изображения
    width = height = size * cell_size + (size - 1) * padding + 2 * board_padding

    # создание нового изображения с серым фоном
    img = Image.new('RGB', (width, height), color='#ccc')
    # создание объекта для рисования на изображении
    draw = ImageDraw.Draw(img)

    # попытка загрузить шрифт arial размером 36 пунктов
    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        # если шрифт не найден, использование шрифта по умолчанию
        font = ImageFont.load_default()

    # рисование прямоугольника-фона всего изображения
    draw.rectangle([0, 0, width, height], fill='#ccc', outline='#ccc')

    # отрисовка пустых ячеек сетки
    for i in range(size):
        for j in range(size):
            # расчет координат ячейки
            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # рисование прямоугольника ячейки
            draw.rectangle([x1, y1, x2, y2], fill='#d8d8d8', outline='#ccc')

    # отрисовка заполненных ячеек с числами
    for i in range(size):
        for j in range(size):
            value = board[i][j]

            # пропуск пустых ячеек
            if value == 0:
                continue

            # словарь цветов фона для разных значений плиток
            bg_colors = {
                2: '#eee', 4: '#ddd', 8: '#ccc',
                16: '#bbb', 32: '#aaa', 64: '#999',
                128: '#888', 256: '#777', 512: '#666',
                1024: '#555', 2048: '#333'
            }

            # словарь цветов текста для разных значений плиток
            text_colors = {
                2: '#000', 4: '#000', 8: '#000',
                16: '#fff', 32: '#fff', 64: '#fff',
                128: '#fff', 256: '#fff', 512: '#fff',
                1024: '#fff', 2048: '#fff'
            }

            # получение цвета фона и текста для текущего значения
            bg_color = bg_colors.get(value, '#eee')
            text_color = text_colors.get(value, '#000')

            # расчет координат ячейки
            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # рисование прямоугольника ячейки с цветом фона
            draw.rectangle([x1, y1, x2, y2], fill=bg_color, outline='#ccc')

            # скругление углов ячейки (рисуем круги в углах)
            radius = 3
            draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=bg_color)

            # отрисовка числа в ячейке
            if value != 0:
                text = str(value)
                # получение размеров текста
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # расчет координат для центрирования текста
                text_x = x1 + (cell_size - text_width) // 2
                text_y = y1 + (cell_size - text_height) // 2

                # для больших чисел используем меньший шрифт
                if value >= 1024:
                    try:
                        small_font = ImageFont.truetype('arial.ttf', 27)
                    except:
                        small_font = font
                    draw.text((text_x, text_y), text, fill=text_color, font=small_font)
                else:
                    draw.text((text_x, text_y), text, fill=text_color, font=font)

    # сохранение изображения в файл
    img.save(filename, 'PNG')
    return img

# функция для генерации изображения игрового поля в классической теме
def generate_image_classic(board, size, filename):
    # базовый размер одной ячейки в пикселях
    cell_size = 100
    # отступ между ячейками
    padding = 15
    # отступ всего игрового поля от краев изображения
    board_padding = 15

    # расчет общей ширины и высоты изображения
    width = height = size * cell_size + (size - 1) * padding + 2 * board_padding

    # создание нового изображения с цветным фоном (классическая тема)
    img = Image.new('RGB', (width, height), color='#bbada0')
    # создание объекта для рисования на изображении
    draw = ImageDraw.Draw(img)

    # попытка загрузить шрифт arial размером 36 пунктов
    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        # если шрифт не найден, использование шрифта по умолчанию
        font = ImageFont.load_default()

    # рисование прямоугольника-фона всего изображения
    draw.rectangle([0, 0, width, height], fill='#bbada0', outline='#bbada0')

    # отрисовка пустых ячеек сетки
    for i in range(size):
        for j in range(size):
            # расчет координат ячейки
            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # рисование прямоугольника ячейки (классический цвет)
            draw.rectangle([x1, y1, x2, y2], fill='#eee4da', outline='#bbada0')

    # отрисовка заполненных ячеек с числами
    for i in range(size):
        for j in range(size):
            value = board[i][j]

            # пропуск пустых ячеек
            if value == 0:
                continue

            # словарь цветов фона для разных значений плиток (классическая тема)
            bg_colors = {
                2: '#eee4da', 4: '#ede0c8', 8: '#f2b179',
                16: '#f59563', 32: '#f67c5f', 64: '#f65e3b',
                128: '#edcf72', 256: '#edcc61', 512: '#edc850',
                1024: '#edc53f', 2048: '#edc22e'
            }

            # словарь цветов текста для разных значений плиток (классическая тема)
            text_colors = {
                2: '#776e65', 4: '#776e65',
                8: '#f9f6f2', 16: '#f9f6f2', 32: '#f9f6f2',
                64: '#f9f6f2', 128: '#f9f6f2', 256: '#f9f6f2',
                512: '#f9f6f2', 1024: '#f9f6f2', 2048: '#f9f6f2'
            }

            # получение цвета фона и текста для текущего значения
            bg_color = bg_colors.get(value, '#eee4da')
            text_color = text_colors.get(value, '#776e65')

            # расчет координат ячейки
            x1 = j * (cell_size + padding) + board_padding
            y1 = i * (cell_size + padding) + board_padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # рисование прямоугольника ячейки с цветом фона
            draw.rectangle([x1, y1, x2, y2], fill=bg_color, outline='#bbada0')

            # скругление углов ячейки (рисуем круги в углах)
            radius = 3
            draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=bg_color)
            draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=bg_color)
            draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=bg_color)

            # отрисовка числа в ячейке
            if value != 0:
                text = str(value)
                # получение размеров текста
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # расчет координат для центрирования текста
                text_x = x1 + (cell_size - text_width) // 2
                text_y = y1 + (cell_size - text_height) // 2

                # для больших чисел используем меньший шрифт
                if value >= 1024:
                    try:
                        small_font = ImageFont.truetype('arial.ttf', 27)
                    except:
                        small_font = font
                    draw.text((text_x, text_y), text, fill=text_color, font=small_font)
                else:
                    draw.text((text_x, text_y), text, fill=text_color, font=font)

    # сохранение изображения в файл
    img.save(filename, 'PNG')
    return img