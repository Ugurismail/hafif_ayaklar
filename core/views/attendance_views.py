"""DJ-only printable personnel attendance sheet tool."""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


ATTENDANCE_SHEETS = [
    {
        "page": 1,
        "sections": [
            {"code": "120", "people": [
                "Hacı NALBANT",
                "Emrah YEŞİLBAŞ",
                "İsmail AYGÜN",
                "Mert Furkan TÖTÜNCÜ",
                "Said Mehdi DEMİR",
            ]},
            {"code": "130", "people": [
                "Ayşe ÖZCAN BATAN",
                "Makbule Aslı TANAGAR",
            ]},
            {"code": "140", "people": [
                "Mehmet BİRCAN",
                "Altuğ DEVECİOĞLU",
            ]},
            {"code": "145", "people": [
                "Elif ARI",
                "Çağla DOĞAN",
                "Akın KAYA",
            ]},
            {"code": "150", "people": [
                "Seval KILIÇ",
                "Hatice ASLAN",
            ]},
        ],
    },
    {
        "page": 2,
        "sections": [
            {"code": "160", "people": [
                "Dilek ÖZBAY",
                "Şevket Cansın BEYSANOĞLU",
            ]},
            {"code": "170", "people": [
                "Ezgi DİLMEN",
                "Dilek KOÇ",
                "Cahide Elif DİKAN",
            ]},
            {"code": "180", "people": [
                "D. Melih TÜRKOĞLU",
                "Sevgi TOPRAK AYDOĞDU",
            ]},
            {"code": "190", "people": [
                "Nazan AKYOL",
                "Meltem SÖZERİ",
            ]},
            {"code": "200", "people": [
                "Abdurrahman YILDIRIM",
                "Damla DEĞİRMENCİ",
                "Hülya OFLAZ",
            ]},
        ],
    },
]


@login_required
def attendance_sheet_tool(request):
    profile = getattr(request.user, "userprofile", None)
    if not (request.user.is_staff or getattr(profile, "is_dj", False)):
        raise PermissionDenied

    return render(request, "core/attendance_sheet_tool.html", {"sheets": ATTENDANCE_SHEETS})
