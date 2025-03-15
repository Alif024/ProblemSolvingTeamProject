from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import textwrap
import os

# โหลดฟอนต์ภาษาไทย (ใช้ฟอนต์ Sarabun)
FONT_PATH = "fonts/Sarabun-Regular.ttf"  # เปลี่ยนเป็น path ของคุณ
FONT_NAME = "Sarabun"

if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
else:
    print(f"Warning: ฟอนต์ {FONT_PATH} ไม่พบ! ใช้ฟอนต์เริ่มต้นแทน")

# ขนาด A4
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = MARGIN_Y = 36  # **ปรับขอบเป็น 1 นิ้ว (72 points)**
LINE_HEIGHT = 14  # ระยะห่างระหว่างบรรทัด
MAX_WIDTH = PAGE_WIDTH - 2 * MARGIN_X  # ความกว้างที่พิมพ์ได้

def wrap_text(line, max_width, font_size):
    """ตัดข้อความที่ยาวเกิน และแสดงให้รู้ว่าเป็นบรรทัดเดียวกัน"""
    wrap_width = int(max_width // (font_size * 0.6))  # แปลงเป็น int
    wrapped_lines = textwrap.wrap(line, width=wrap_width)

    if len(wrapped_lines) > 1:
        for i in range(1, len(wrapped_lines)):
            wrapped_lines[i] = "···" + wrapped_lines[i]  

    return wrapped_lines

def python_to_pdf(input_file, output_pdf):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.setFont(FONT_NAME, 12)

    y_position = PAGE_HEIGHT - MARGIN_Y  # เริ่มต้นที่ขอบบน 1 นิ้ว

    for line in lines:
        wrapped_lines = wrap_text(line.rstrip(), MAX_WIDTH, 12)

        for wrapped_line in wrapped_lines:
            if y_position < MARGIN_Y:  # **ถ้าถึงขอบล่าง 1 นิ้ว → ขึ้นหน้าใหม่**
                c.showPage()
                c.setFont(FONT_NAME, 12)
                y_position = PAGE_HEIGHT - MARGIN_Y  # เริ่มบรรทัดใหม่ที่ขอบบน 1 นิ้ว

            c.drawString(MARGIN_X, y_position, wrapped_line)
            y_position -= LINE_HEIGHT  # เลื่อนลงบรรทัดถัดไป

    c.save()
    print(f"บันทึกไฟล์ PDF สำเร็จ: {output_pdf}")

# ใช้งานฟังก์ชัน
python_to_pdf("test.py", "output.pdf")
