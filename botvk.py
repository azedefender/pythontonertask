from PIL import Image


def calculate_toner_usage(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    width, height = image.size
    total_pixels = width * height

    color_usage = {'black': 0, 'cyan': 0, 'magenta': 0, 'yellow': 0}

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]

            # Расчет количества каждого цвета на изображении
            if r + g + b < 182:  # черный
                color_usage['black'] += 1
            elif r > 200 and g < 50 and b < 50:  # маджента
                color_usage['magenta'] += 1
            elif r < 50 and g > 200 and b < 50:  # циан
                color_usage['cyan'] += 1
            elif r < 50 and g < 50 and b > 200:  # желтый
                color_usage['yellow'] += 1

    # Расчет процента использования тонера
    for color in color_usage:
        color_usage[color] = round((color_usage[color] / total_pixels) * 100, 2)

    return color_usage


def calculate_cost(cartridge_costs, toner_usage):
    total_cost = 0
    for color in toner_usage:
        total_cost += (toner_usage[color] / 100) * cartridge_costs[color]
    return total_cost


# Пример использования
cartridge_costs = {'black': 50, 'cyan': 45, 'magenta': 45, 'yellow': 45}
image_path = 'white-cat.jpg'

toner_usage = calculate_toner_usage(image_path)
total_cost = calculate_cost(cartridge_costs, toner_usage)

print(f'Использование тонера: {toner_usage}')
print(f'Общая стоимость печати: {total_cost}')
