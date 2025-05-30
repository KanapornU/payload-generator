"""
python payload_gen.py --type sqli --encode none
python payload_gen.py --type sqli --encode url
python payload_gen.py --type sqli --encode base64
python payload_gen.py --type sqli --encode hex 
python payload_gen.py --type xss --encode none
encode มีหลายแบบ เลือกเอา
"""

import argparse      # ใช้จัดการ argument จาก command line เช่น --type, --encode
import json          # ใช้อ่านไฟล์ .json ที่เก็บ payload
import random        # ใช้สำหรับสุ่ม payload จาก list
import os            # ใช้ตรวจสอบ path และไฟล์
from utils.encoder import encode_payload  # เรียกฟังก์ชันเข้ารหัสจากไฟล์ encoder.py

def load_payloads(payload_type):
    filename = f"payloads/{payload_type}.json"  # สร้าง path ไฟล์ตามประเภท xss หรือ sqli
    if not os.path.exists(filename):
        raise FileNotFoundError(f"[!] ไม่พบไฟล์: {filename}")  # แจ้ง error ถ้าไฟล์หาย
    with open(filename, "r", encoding="utf-8") as f:
        payloads = json.load(f)  # โหลดข้อมูลจาก .json → เป็น list ใน Python
    return payloads

def display_payload(payload, output_file=None):
    print(f"\n[🎯 Payload ที่สร้างขึ้น]\n{payload}\n")  # แสดงผลลัพธ์ใน terminal
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(payload)  # บันทึก payload ลงในไฟล์ .txt
        print(f"[💾 บันทึกลงไฟล์]: {output_file}")

def main():
    # สร้าง parser เพื่อรับ argument จากผู้ใช้
    parser = argparse.ArgumentParser(description="🔥 Payload Generator สำหรับ XSS / SQLi")

    # รับ argument --type (บังคับต้องกรอก)
    parser.add_argument("--type", choices=["xss", "sqli"], required=True,
                        help="ประเภท payload ที่ต้องการสร้าง (xss หรือ sqli)")

    # รับ argument --encode (มีค่า default เป็น none)
    parser.add_argument("--encode", choices=["base64", "url", "hex", "none"], default="none",
                        help="วิธีการเข้ารหัส payload")

    # รับ argument --output (ไม่บังคับ)
    parser.add_argument("--output",
                        help="หากต้องการบันทึก payload ลงไฟล์ .txt")

    # แปลง argument ที่รับเข้ามาเก็บไว้ในตัวแปร args
    args = parser.parse_args()

    try:
        payloads = load_payloads(args.type)  # โหลด payload จากไฟล์ตามประเภท
    except FileNotFoundError as e:
        print(e)
        return  # หยุดทำงานถ้าไฟล์หาย

    selected = random.choice(payloads)  # สุ่ม 1 payload จาก list

    if args.encode != "none":
        final_payload = encode_payload(selected, args.encode)  # แปลง encode ถ้าต้องการ
    else:
        final_payload = selected  # ไม่แปลงถ้าเลือก "none"

    display_payload(final_payload, args.output)  # แสดงผล หรือบันทึกไฟล์

if __name__ == "__main__":
    main()
