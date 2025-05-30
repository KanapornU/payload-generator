'''
ไฟล์นี้ใช้สำหรับเข้ารหัส (encode) payload ที่เป็น XSS หรือ SQLi
เพื่อใช้ในการทดสอบความปลอดภัยของเว็บ เช่น bypass WAF หรือหลบการ filter
'''

import base64
import urllib.parse

def encode_payload(payload, method):
    # ถ้าเลือก method = base64 → เข้ารหัสแบบ Base64
    if method == "base64":
        # แปลงข้อความเป็น bytes → เข้ารหัส base64 → แปลงกลับเป็น string
        return base64.b64encode(payload.encode()).decode()
    
    # ถ้าเลือก method = url → เข้ารหัส URL (เช่น %3Cscript%3E)
    elif method == "url":
        return urllib.parse.quote(payload)
    
    # ถ้าเลือก method = hex → เข้ารหัสเป็น ASCII \x...
    elif method == "hex":
        # วนลูปทีละตัวอักษร → แปลงเป็น ASCII → แปลงเป็นเลขฐาน 16 (hex) → รวมเป็น string
        return ''.join(['\\x'+format(ord(c), 'x') for c in payload])
    
    # ถ้าไม่เลือก หรือเลือก method ผิด → คืนค่า payload ดิบ (ไม่เข้ารหัส)
    else:
        return payload
