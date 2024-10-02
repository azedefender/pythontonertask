import subprocess
from PIL import Image


def calculate_toner_usage(image_path):
    # Преобразуем изображение в формат CIE LAB для определения цветовой составляющей
    # Используем ImageMagick для конвертации
    output_path = "white-cat.jpg"
    subprocess.run(["convert", image_path, "-colorspace", "RGB", output_path])

    # Загружаем изображение с помощью Pillow
    img = Image.open(output_path)
    width, height = img.size
    total_pixels = width * height

    # Считаем количество пикселей для каждого цвета
    c_count = m_count = y_count = k_count = 0

    for pixel in img.getdata():
        r, g, b = pixel

        # Преобразуем RGB в CMYK
        c = 1 - (r / 255.0)
        m = 1 - (g / 255.0)
        y = 1 - (b / 255.0)
        k = min(c, m, y)

        if k < 1:  # игнорируем полностью черные пиксели
            c = (c - k) / (1 - k)
            m = (m - k) / (1 - k)
            y = (y - k) / (1 - k)

        c_count += round(c * 100)
        m_count += round(m * 100)
        y_count += round(y * 100)
        k_count += round(k * 100)

    # Рассчитываем процентные соотношения
    c_usage = c_count / total_pixels
    m_usage = m_count / total_pixels
    y_usage = y_count / total_pixels
    k_usage = k_count / total_pixels

    return c_usage, m_usage, y_usage, k_usage


def calculate_print_cost(tone_usage, toner_costs):
    c_usage, m_usage, y_usage, k_usage = tone_usage
    c_cost, m_cost, y_cost, k_cost = toner_costs

    total_cost = (c_usage * c_cost) + (m_usage * m_cost) + (y_usage * y_cost) + (k_usage * k_cost)
    return total_cost


if __name__ == "__main__":
    image_path = input("Введите путь к изображению: ")
    c_cost = float(input("Введите стоимость картриджа Cyan: "))
    m_cost = float(input("Введите стоимость картриджа Magenta: "))
    y_cost = float(input("Введите стоимость картриджа Yellow: "))
    k_cost = float(input("Введите стоимость картриджа Black: "))

    toner_costs = (c_cost, m_cost, y_cost, k_cost)

    toner_usage = calculate_toner_usage(image_path)
    print(
        f"Расход тонера: C: {toner_usage[0] * 100:.2f}%, M: {toner_usage[1] * 100:.2f}%, Y: {toner_usage[2] * 100:.2f}%, K: {toner_usage[3] * 100:.2f}%")

    total_cost = calculate_print_cost(toner_usage, toner_costs)
    print(f"Стоимость печати: {total_cost:.2f} руб.")
