import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = 'https://ar.shein.com'
cookies = {
    'armorUuid': '20250725223033096855d31e119f3b7d95baca8e9be9eb00902c87f792044300',
    'sessionID_shein': 's%3ACknB--1T8tOz6jogF9neWe2_Kr11q39f.Ikt6TRQkykLZ4kHliF5Hyz%2BPGOqb3MQNrOC6JgN3DRs',
    'AT': 'MDEwMDE.eyJiIjo3LCJnIjoxNzUzNDUzODMzLCJyIjoiYmdrcHRKIiwidCI6MX0.69663287b99befb2',
    'smidV2': '2025072520003517f49ce34415328894ed822af23ba86700967f3d3e2259100',
    'zpnvSrwrNdywdz': 'center',
    '_pin_unauth': 'dWlkPU4ySTFPVFV4TWpZdE9USXlOeTAwTWpSa0xXSTJZMk10Tm1Oak1UaGpNV1UzTjJabA',
    '_gcl_au': '1.1.1536806071.1753453838',
    '_cbp': 'fb.1.1753453838297.844880012',
    'fita.sid.shein': 'r0hJYNNFAfHeKKgirRPpWLDCePYmflUi',
    '_f_c_llbs_': 'K1905_1753538603_GSQd9dpSpUAkcLiCeG3O7w9HNaYBxddvUfGUM-V7daWPKUU1PjYwBGE1SwVrJxWjK06Jfk8kiZ_afWYH9Q6illTPpkuAnVFDgttpYdJdy2L92qykDNp750dgm3EzQrJnB9CJjxLAXfiLn5nhch3-_xths-9pBKwmihWGA7s8LCuN7qKFmJX1bgsOBjJ4dRyAr79Q86LBtHADchR_Wk-yNtwFXvbTZxRRYJgZ8aj2VVYzNFC9yYBajF_DbjzQ8tVMN9HeIiYyMtiBwZkMtc3L1fARR2Jrghcbnoi6uMcvxai1u2XT5qZ6mWyWOiLP9aAtX5q6g2_vldh5z1R9DzuCxw',
    'fita.short_sid.shein': 'u1zKXMSzvnmy9j3ZjaLPLUdLURO9uWQj',
    '_uetsid': 'eebb33e0696311f0b939d16d38215199',
    '_uetvid': 'eebb7330696311f0a96c0d3b8481af9c',
    'cto_bundle': 'HeRvwV9SUWdCbmNrRGx0dGglMkJFZ2NjVU1uOHZkM1RvbnFvdjYzVlE5bW1aTkRkUWd1VmgzSGdnaVlHVTFrbnhremtNRWV2MkxBT1dLQVM1SDNvWlo0N2xBRjEyME5vSkNlJTJCMm5jc2txcXM0ZWJtRHclMkJCb2tkeFg1T0h5YzFxM1Fxa2glMkJp',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://ar.shein.com/risk/challenge?captcha_type=905&redirection=https%3A%2F%2Far.shein.com%2FKids-c-2031.html&risk-id=E2947629945785303041',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'armorUuid=20250725223033096855d31e119f3b7d95baca8e9be9eb00902c87f792044300; sessionID_shein=s%3ACknB--1T8tOz6jogF9neWe2_Kr11q39f.Ikt6TRQkykLZ4kHliF5Hyz%2BPGOqb3MQNrOC6JgN3DRs; AT=MDEwMDE.eyJiIjo3LCJnIjoxNzUzNDUzODMzLCJyIjoiYmdrcHRKIiwidCI6MX0.69663287b99befb2; smidV2=2025072520003517f49ce34415328894ed822af23ba86700967f3d3e2259100; zpnvSrwrNdywdz=center; _pin_unauth=dWlkPU4ySTFPVFV4TWpZdE9USXlOeTAwTWpSa0xXSTJZMk10Tm1Oak1UaGpNV1UzTjJabA; _gcl_au=1.1.1536806071.1753453838; _cbp=fb.1.1753453838297.844880012; fita.sid.shein=r0hJYNNFAfHeKKgirRPpWLDCePYmflUi; _f_c_llbs_=K1905_1753500449_drCmrtjF3XGjXaDNFkwdrP50Jr_S74idcLQiw_2panT00R3WZeG8UlJdJWwACUntC1iKRzUEVRD0h9xgry0AWB5nvKkZ9jWZCE2SMMfIdQpf2pHmFgkJpEvdV5PJFh_7_Ovcv85XMvoTZ-n0acXos091mgq0bQ3jSFEHujTRSvosKA-U3Nkd9CnHG_FvHEBZo8ysfbf4TmJRjCR4By7AnfcqPxPhZG6sBxRTqHk5_0W82wH2hEQ5e1-P3g47U5shOgdvqOtSb4O7474uwhQ-c8yW9Gm6gwVodDGgP-s2Bv8cGseLQajq1H6-twCsGoaKMciX1_FNywf_qXAqV9C-2w; _uetsid=eebb33e0696311f0b939d16d38215199; _uetvid=eebb7330696311f0a96c0d3b8481af9c; cto_bundle=0e9kVF9SUWdCbmNrRGx0dGglMkJFZ2NjVU1uOGt3U052UFRNRmhGb3VHaHFYVGxveDJZU1pldVZaaW5pYzNSVW5kMkhqMmZLb211Tzh1NUs5Q2QydFd3SE0zMXNUejFmWFI1TEZ6TGI2bzdFMFU5SVkzY1l0R2VuMlZlSWFQMlJLUFFOY1RE',
}

response = requests.get('https://ar.shein.com/Kids-c-2031.html', cookies=cookies, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')
absolute_url = [urljoin(base_url, urls.get('href').split('?')[0]) for urls in soup.select('.product-list-v2__section [role="listitem"] a')]
print(len(absolute_url))
for item in absolute_url:
    print(item)