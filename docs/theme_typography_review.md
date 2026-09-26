# Tema ve Tipografi Incelemesi

2026-09-20. Kapsam: user_settings.html icindeki 28 hazir tema, font secimi ve
profil kayit akisi. Bu turda tema paletleri degistirilmedi; kullanici genel
yorum ve daha fazla font istedi. Old Money ve The Philosopher korunacak.

## Genel Yargi

- Old Money, The Philosopher ve Astra sitenin uzun metin okuma kimligine
  uygun uc farkli yon sunuyor: sicak klasik, dusunce/kitap ve temiz cagdas.
- The Sapiens, The Man ve gpt5.6 da temel renk ciftlerinde guclu alternatifler.
  The Last koyu temalar icin iyi bir baslangic; tum bilesenlerde test edilmeli.
- Ocean, Sunset, Sakura ve Lavanta'da renk karakteri var, fakat pastel/parlak
  yuzey ustunde acik yazi veya link tercihleri okunurlugu zayiflatiyor.
- Nordic ve The Porcelain'in sade yaklasimi korunabilir; dugmelerde daha koyu
  vurgu gerekiyor. Tema sayisini azaltmak yerine mevcut isimleri koruyup
  okunurluk revizyonu yapmak daha az surpriz yaratir.
- Cyberpunk ve The Artist secenek olarak kalabilir; bunlari uzun okumaya
  yonelik varsayilanlar gibi sunmam. Neon vurgu, monospace govde veya display
  yazi tipini tum arayuze uygulamak yorucu/yer israfli olabilir. Bu bir tasarim
  yargisidir; herkesin zevkini tek bir palete indirmek hedef degildir.

## Olcum

Asagidaki oranlar dogrudan hazir tema renklerinden hesaplanan normal durum
metin/zemin kontrastidir; ekran goruntusunden tahmin degildir. Sira:
govde metni, link, birincil dugme yazisi. Normal boyutta metin icin 4.5:1
hedefi kullanildi. Buyuk metin istisnasi, odak, hover, devre disi durum,
saydamlik ve tum gercek bilesenler bu tablonun disindadir; tam WCAG uyum
sertifikasi olarak yorumlanmamali.

| Tema | Govde | Link | Dugme | Oncelikli yorum |
| --- | ---: | ---: | ---: | --- |
| Astra | 14.09 | 6.16 | 6.68 | Temel renkler dengeli |
| Old Money | 15.20 | 5.54 | 2.89 | Altin dugme ustundeki acik yazi guclendirilmeli |
| gpt5.6 | 13.74 | 5.39 | 4.54 | Korunabilir; dugme esige yakin |
| Gece | 5.59 | 8.34 | 11.33 | Govde daha soluk; eksik alan/kisa hex sorunu |
| Ocean | 10.19 | 2.41 | 2.70 | Link ve dugmeler oncelikli |
| Sunset | 14.20 | 2.15 | 2.78 | Navbar da 2.78; belirgin kontrast sorunu |
| Forest | 11.64 | 2.32 | 3.83 | Yesil tonlar birbirine fazla yakin |
| Monochrome | 17.40 | 12.63 | 13.97 | Ikincil dugme 3.95; govde guclu |
| Lavanta | 14.37 | 3.89 | 2.92 | Ikincil dugme 1.91; navbar 3.27 |
| Coffee | 12.73 | 4.26 | 6.55 | Link ve ikincil dugme koyulastirilmali |
| Cyberpunk | 14.40 | 14.99 | 3.62 | Neon yerine metin okunurlugu once gelmeli |
| Sakura | 12.84 | 2.19 | 1.89 | En oncelikli dugme revizyonlarindan |
| Nordic | 10.44 | 3.52 | 3.50 | Sade kimlik iyi, vurgu fazla soluk |
| Klasik Garamond | 19.26 | 3.23 | 3.52 | Yazi guclu, link/dugme soluk |
| The Porcelain | 14.32 | 5.26 | 3.49 | Birincil dugme duzeltilmeli |
| The Man | 17.37 | 7.92 | 4.94 | Temel renkler dengeli |
| The Woman | 15.50 | 8.10 | 2.89 | Birincil dugme yazi kontrasti |
| The 2SLGBTQ+ | 18.32 | 9.24 | 7.14 | Temel ciftler guclu |
| The Philosopher | 16.74 | 4.81 | 4.81 | Korunacak; Cardo ile kitap karakteri |
| The Artist | 16.71 | 4.42 | 4.87 | Link/ikincil dugme; Playfair govde icin tartismali |
| The Sapiens | 13.26 | 6.05 | 8.85 | Uzun okuma icin guclu aday |
| The Animal | 13.96 | 2.70 | 3.00 | Link/dugme revizyonu |
| The Plant | 14.25 | 5.94 | 3.79 | Birincil dugme revizyonu |
| The Pastel | 13.27 | 4.48 | 7.23 | Link esigin hemen altinda |
| The Darkness | 14.23 | 7.56 | 5.45 | Space Grotesk artik secicide de var |
| The Last | 14.78 | 8.86 | 6.20 | Koyu okuma temasi olarak korunabilir |
| The Warrior | 14.94 | 5.69 | 4.55 | Dugme esige yakin, kuvvetli vurgu |
| The Cleric | 16.04 | 2.90 | 5.54 | Altin link acik zeminde zayif |

## Yapisal Bulgular ve Sonraki Isler

1. On eski preset `yanit_card` degerini tanimlamiyor. Tema seciminde
   sadece belirtilen alanlar atandigi icin bu renk onceki temadan kalabilir.
   Her preset butun gorunum alanlarini acikca tanimlamali; siradan bagimsiz
   A -> B ve C -> B gecis testleri eklenmeli.
2. Gece temasinda `secondary_button_text_color` kisa `#fff` olarak yazilmis.
   CSS bunu kabul etse de mevcut color input davranisiyle ayni bicimde
   saklanmayabilir. Tum renkler alti haneli hex olarak normalize edilmeli ve
   secim -> onizleme -> POST -> tekrar acma gercek tarayicida kontrol edilmeli.
3. Hazir tema kaydedilen bir kimlik degil, renk/font alanlarini dolduran
   istemci tarafi preset. Kullanici ozel renkleri korunarak secili presetin
   taninmasi ve degistirildiginde 'Ozel' durumuna gecmesi planlanmali.
4. Okuma fontu ile arayuz fontunu ayirmak en degerli sonraki gelistirme.
   Display/el yazisi secenekleri uzun govde metninde ve kucuk kontrol
   etiketlerinde ayni sonucu vermez. Mevcut profil tercihlerini sessizce
   degistirmeden bagimsiz iki secim ve gecis plani gerekir.
5. Ilk hedef yeni tema sayisi degil: mevcut temalarin acik/koyu durumlari,
   buton, modal, hata, tablo, habit tracker ve diyagram gorunum testleri.

## Eklenen Fontlar

40 yeni aile; eski 55 secenek korunarak toplam 95. Bes mevcut kategoriye
eklendi. Temalarin font secimleri degistirilmedi. Her bir yeni ailenin Google
Fonts CSS API cevabi ve donen font dosyasinin cmap tablosu kontrol edildi:
`ABCabc Cc Gg Ii Oo Ss Uu` ASCII harflerine ek olarak Turkce C-cedilla,
G-breve, noktali buyuk I/noktasiz i, O-diaeresis, S-cedilla, U-diaeresis
harflerinin buyuk/kucuk bicimleri ve rakamlar dogrulandi.

- Serif: Literata, Alegreya, Andada Pro, Bitter, Gentium Book Plus, Brygada
  1918, Domine, Faustina, Hepta Slab, IBM Plex Serif, Newsreader, Petrona,
  Roboto Serif, STIX Two Text.
- Sans: Atkinson Hyperlegible Next, Barlow, Cabin, Figtree, Geologica,
  IBM Plex Sans, Manrope, Mulish, Outfit, Public Sans, Sora, Space Grotesk,
  Ubuntu, Urbanist.
- Monospace: IBM Plex Mono, Inconsolata, Recursive, Roboto Mono, Space Mono.
- Display: Bodoni Moda, Cinzel, Fraunces, Unbounded.
- El yazisi: Bad Script, Marck Script, Pangolin.

Assistant ve eski Atkinson Hyperlegible servis dosyalarinda test edilen
Turkce harflerin tamami bulunmadigi icin eklenmedi. Atkinson Hyperlegible Next
testi gecti. Bu kontrol tek basina tipografik kalite veya erisilebilirlik
garantisi degildir; ozellikle display/el yazisi fontlari amacina gore secilmeli.

Katalog genislemesi tum fontlari indirmez. Sayfada kayitli font, secim
degistiginde yeni secilen font yuklenir; mevcut display=swap korunur.
Ayarlar acilirken ayni font icin yapilan fazladan dinamik istek kaldirildi;
base.html zaten kayitli fontu yukler. Yeni harici servis veya paket eklenmedi;
Google Fonts mevcut altyapidir, cevrimdisi/self-hosted font dagitimi degildir.

## Kaynaklar

- [W3C: minimum kontrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [Google Fonts CSS2 API](https://developers.google.com/fonts/docs/css2)
- [Literata projesi](https://github.com/googlefonts/literata)
