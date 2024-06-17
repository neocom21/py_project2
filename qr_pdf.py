import qrcode
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

my_path = os.path.dirname(__file__)+"/"

# Генерация QR-кода
qr_data = ['ЕЛЕКТРОННИЙ ДОКУМЕНТ АІС "МІСЦЕВИЙ БЮДЖЕТ" \n',
'Електронний підпис №1 \n', 
'Підписувач:Вербицька Тамара Василівна \n', 
'Організація:Фінансове управління Ізмаїльської міської ради \n', 
'Сертифікат:3FAA9288358EC003040000005A21160091A4B500 дійсний з 29.03.2023 по 29.03.2025 \n', 
'Час підпису:08.06.2024 11:06']

# Путь к изображению QR-кода
qr_code_image_path = my_path + "qr_code.png"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(qr_data)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
img.save(qr_code_image_path)

# Открытие исходного PDF

reader = PdfReader(my_path + '1.pdf')
writer = PdfWriter()



# Определите страницу и координаты для QR-кода
page_number = 0  # Номер страницы (0 - первая страница)
x = 10  # Позиция по оси X
y = 10  # Позиция по оси Y

# Чтение содержимого страницы
page = reader.pages[page_number]

# Создание временного PDF с QR-кодом
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawImage(qr_code_image_path, x, y, width=100, height=100)  # Задайте размеры QR-кода
can.save()

# Перемотка буфера к началу
packet.seek(0)
qr_pdf = PdfReader(packet)
qr_page = qr_pdf.pages[0]

# Слияние QR-кода с оригинальной страницей
page.merge_page(qr_page)

# Добавление измененной страницы в новый PDF
writer.add_page(page)

# Добавление остальных страниц
for i in range(1, len(reader.pages)):
    writer.add_page(reader.pages[i])

# Сохранение нового PDF
with open(my_path + "output.pdf", "wb") as output_pdf:
    writer.write(output_pdf)

# удалить qr-код
os.remove(qr_code_image_path)
