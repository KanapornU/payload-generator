'''
Payload Generator เป็นเครื่องมือสำหรับสร้างและเข้ารหัส payload
ที่ใช้ทดสอบช่องโหว่ของเว็บ เช่น XSS และ SQL Injection

- สุ่ม payload จากไฟล์ .json ตามประเภทที่เลือก
- เข้ารหัส payload ด้วย base64, URL encoding, หรือ hex
- แสดงผลใน Terminal หรือบันทึกลงไฟล์ output.txt

ตัวอย่างวิธีรัน "python payload_gen.py --type xss --encode base64 --store"
'''
# import ไลบรารีที่ใช้ในโปรแกรม
import argparse          # ใช้สำหรับรับ argument จาก command line เช่น --type, --encode
import json              # ใช้อ่านและแปลงข้อมูลจากไฟล์ .json
import random            # ใช้สุ่ม payload
import os                # ใช้ตรวจสอบไฟล์และ path
from utils.encoder import encode_payload  # เรียกใช้ฟังก์ชันเข้ารหัสจาก encoder.py

# ฟังก์ชันโหลด payloads จากไฟล์ JSON ตามประเภท (xss หรือ sqli)
def load_payloads(payload_type):
    filename = f"payloads/{payload_type}.json"  # สร้าง path เช่น payloads/xss.json
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Payload file not found: {filename}")  # แจ้ง error ถ้าไม่มีไฟล์
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)  # อ่านข้อมูลจากไฟล์
    return data.get("payloads", [])  # คืนค่าเฉพาะ list ที่อยู่ใน key "payloads"

# ฟังก์ชันบันทึก payloads ที่สุ่มและเข้ารหัสแล้วลงในไฟล์ output.txt
def store_payloads(payloads, encode_type, output_path="output.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, raw in enumerate(payloads, start=1):  # วนแต่ละ payload
            f.write(f"[{idx}] Raw: {raw}\n")  # เขียน payload ดิบ
            if encode_type and encode_type != "none":  # ถ้าต้อง encode
                encoded = encode_payload(raw, encode_type)
                f.write(f"Encoded ({encode_type}): {encoded}\n")
            else:
                f.write(f"Encoded: {raw}\n")
            f.write("-" * 40 + "\n")  # คั่นบรรทัดระหว่างแต่ละ payload
    print(f"All payloads saved to: {output_path}")  # แจ้งว่าบันทึกเสร็จ

# แสดง payloads ที่สุ่มขึ้นมาทางหน้าจอ พร้อม encode ถ้ามี
def display_payloads(payloads, encode_type=None):
    print(f"Loaded {len(payloads)} payloads")  # แจ้งจำนวน payload ที่โหลดมาได้
    selected_payloads = random.sample(payloads, min(10, len(payloads)))  # สุ่มสูงสุด 10 รายการ
    for idx, raw in enumerate(selected_payloads, start=1):
        print(f"[{idx}] Selected raw payload: {raw}")  # แสดง payload ดิบ
        if encode_type and encode_type != "none":
            encoded = encode_payload(raw, encode_type)  # แปลง encode
            print(f"Encoding: {encode_type}")
            print(f"Payload: {encoded}")  # แสดงผลหลัง encode
        else:
            print(f"Payload: {raw}")  # ถ้าไม่ encode ก็แสดงของเดิม
        print("-" * 40)  # เส้นแบ่งแต่ละอัน
    return selected_payloads  # ส่งคืน payloads ที่สุ่มได้

# ฟังก์ชันหลักที่ควบคุมการทำงานของโปรแกรม
def main():
    parser = argparse.ArgumentParser(description="Payload Generator for XSS / SQLi")
    
    # รับ argument --type เพื่อเลือกประเภท payload
    parser.add_argument("--type", choices=["xss", "sqli"], required=True,
                        help="Payload type to generate (xss or sqli)")
    
    # รับ argument --encode เพื่อเลือกวิธี encode
    parser.add_argument("--encode", choices=["base64", "url", "hex", "none"], default="none",
                        help="Encoding method for payloads")
    
    # argument --store เป็น option สำหรับบันทึกไฟล์
    parser.add_argument("--store", action="store_true",
                        help="Save the generated payloads to a file")

    args = parser.parse_args()  # รับค่าที่ผู้ใช้ใส่เข้ามาทาง CLI

    try:
        payloads = load_payloads(args.type)  # โหลด payload ตามประเภท
    except FileNotFoundError as e:
        print(e)
        return  # หยุดทำงานถ้าไฟล์ไม่เจอ

    # แสดง payloads และแปลงถ้ามี encode
    selected_payloads = display_payloads(payloads, encode_type=args.encode)

    # ถ้าระบุ --store จะบันทึกลงไฟล์ด้วย
    if args.store:
        store_payloads(selected_payloads, args.encode)

# ทำงานเมื่อรันไฟล์นี้โดยตรง
if __name__ == "__main__":
    main()
