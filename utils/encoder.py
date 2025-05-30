# import ไลบรารีมาตรฐานสำหรับการเข้ารหัสข้อมูล
import base64            # สำหรับแปลงข้อมูลเป็น base64 เช่น <script> → PHNjcmlwdD4=
import urllib.parse      # สำหรับ URL encoding เช่น space → %20

# ฟังก์ชันเข้ารหัส payload ตามประเภทที่ผู้ใช้เลือก
def encode_payload(payload: str, encode_type: str) -> str:
    # base64 encoding
    if encode_type == "base64":
        # แปลง string → byte → base64 แล้ว decode กลับเป็น string
        return base64.b64encode(payload.encode()).decode()

    # URL encoding (ใช้ใน query string, URL path)
    elif encode_type == "url":
        # แปลงตัวอักษรพิเศษให้ปลอดภัย เช่น < → %3C, space → %20
        return urllib.parse.quote(payload)

    # Hex encoding (นิยมใช้ในบาง context เช่น JavaScript หรือ shellcode)
    elif encode_type == "hex":
        # แปลงแต่ละ character เป็น \\xHH เช่น <script> → \\x3c\\x73\\x63...
        return ''.join(f'\\x{ord(c):02x}' for c in payload)

    # หากไม่เลือกหรือพิมพ์ encode_type ผิด จะคืน payload เดิมกลับไป
    else:
        return payload  # fallback if none or unknown