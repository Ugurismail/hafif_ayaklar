def task(prompt, checkpoints, focus):
    return {
        "prompt": prompt,
        "checkpoints": checkpoints,
        "sample_focus": focus,
    }


LOGIC_CORE_PRODUCTION_TASKS = {
    "ders-1-onerme-nedir": [task(
        "Gündelik hayattan üç önerme ve önerme olmayan üç ifade yaz; her kararını gerekçelendir.",
        ["Doğruluk değeri ölçütünü kullandın mı?", "Soru, emir ve ünlemi ayırdın mı?", "Belirsiz bir ifadeyi daha açık biçimde yeniden yazdın mı?"],
        "Cümle türünden önce ifadenin doğru ya da yanlış olabilmesine bak.",
    )],
    "ders-2-arguman-oncul-ve-sonuc": [task(
        "Kısa bir gazete paragrafını öncüller ve sonuç biçiminde yeniden kur; örtük kalan bir öncülü de belirt.",
        ["Sonucu desteklenen iddia olarak ayırdın mı?", "Her öncülü açık bir cümle halinde yazdın mı?", "Örtük öncülün gerçekten gerekli olduğunu açıkladın mı?"],
        "Metni özetlemek yerine gerekçe yapısını görünür hale getir.",
    )],
    "ders-3-gecerlilik-ve-dogruluk": [task(
        "Öncülleri ve sonucu doğru olan geçersiz bir argüman kur; geçersizliği aynı biçimde bir karşı örnekle göster.",
        ["Doğruluk ile geçerliliği ayırdın mı?", "Karşı örnekte öncüller doğru, sonuç yanlış mı?", "İki argümanın aynı biçimi taşıdığını gösterdin mi?"],
        "Geçerlilik, tek tek cümlelerin doğruluğu değil doğruluğu koruyan çıkarım biçimidir.",
    )],
    "ders-4-mantik-baglaclari": [task(
        "En az üç bağlaç içeren bir doğal dil cümlesini sembolleştir ve ana bağlacı gerekçelendir.",
        ["Açık bir sembol anahtarı verdin mi?", "Parantezler kapsamı tek anlamlı kılıyor mu?", "Ana bağlacın bütün formülü nasıl ayırdığını gösterdin mi?"],
        "Atomik cümleleri sabitle, sonra kapsamı dıştan içe kur.",
    )],
    "ders-5-zorunlu-ve-yeterli-kosul": [task(
        "Bir gündelik kuralda zorunlu koşulu, yeterli koşulu ve ikisinin karıştırılmasından doğan hatayı göster.",
        ["'A ancak B ise' ile 'A, B ise' yapılarını ayırdın mı?", "Her yön için karşı örnek düşündün mü?", "Koşullu ifadeyi sembolleştirdin mi?"],
        "Okun yönünü ezberlemek yerine hangi durumun hangisini garanti ettiğini sor.",
    )],
    "ders-6-gecerli-kaliplar-ve-yon-hatalari": [task(
        "Aynı konu hakkında bir modus ponens, bir modus tollens ve bir sonucu doğrulama hatası kur.",
        ["p ve q her örnekte aynı anlamda mı?", "Geçerli kalıpların sonuçları kurallara uygun mu?", "Hatalı kalıp için karşı örnek verdin mi?"],
        "İçerik değişse bile çıkarım iskeletinin aynı kaldığını görünür kıl.",
    )],
    "ders-7-metin-icinde-arguman-ayiklama": [task(
        "En az beş cümlelik bir tartışma metnini standart biçime getir ve gerekçe zincirini göster.",
        ["Arka plan bilgisi ile öncülleri ayırdın mı?", "Ara sonucu nihai sonuçtan ayırdın mı?", "Eksik bağlantıya en tutumlu örtük öncülü ekledin mi?"],
        "Her cümlenin argümandaki işlevini belirt; metindeki sırayı korumak zorunda değilsin.",
    )],
    "ders-9-karsi-ornek-sema-ve-curutme-teknikleri": [task(
        "Geçersiz bir çıkarım şeması seç ve aynı şemaya sahip iki farklı karşı örnek üret.",
        ["Öncüller iki örnekte de doğru mu?", "Sonuçlar iki örnekte de yanlış mı?", "Sembolik şema ile örneklerin eşleşmesini gösterdin mi?"],
        "Karşı örnek, çıkarım biçiminin doğruluğu korumadığını gösterir.",
    )],
    "ders-10-tanim-ve-kavramsal-cerceve": [task(
        "Tartışmalı bir kavram için ölçüt veren tanım yaz; tanımı fazla geniş ve fazla dar örneklerle sınayıp düzelt.",
        ["Tanım döngüsel mi?", "Sınır örnekleri kapsamı gerçekten test ediyor mu?", "Düzeltmede hangi ölçütün değiştiğini açıkladın mı?"],
        "İyi tanım, dahil etme ve dışlama kararlarında kullanılabilir olmalıdır.",
    )],
    "ders-12-ad-hominem-ve-otoriteye-basvuru": [task(
        "Bir uzman görüşünün ne zaman makul kanıt, ne zaman safsata olduğunu iki sürümle göster.",
        ["Uzman ilgili alanda yetkin mi?", "Görüş birliği ve dayanak değerlendirildi mi?", "Kişisel bilginin iddiayla ilgisini kurdun mu?"],
        "Her kişisel bilgi ad hominem değildir; ilgisiz saldırı kanıtın yerini aldığında hata oluşur.",
    )],
    "ders-13-yanlis-ikilem-ve-kaygan-zemin": [task(
        "Bir yanlış ikilem ile bir kaygan zemin argümanı yaz; sonra ikisini de makul hale gelecek biçimde onar.",
        ["Göz ardı edilen seçenekleri gösterdin mi?", "Kaygan zemindeki her geçişi ayrı sınadın mı?", "Onarım kanıtlanabilir kısmı koruyor mu?"],
        "Safsatayı yalnız etiketleme; bozuk geçişi ve onarımını göster.",
    )],
    "ders-14-dongusel-gerekce-ve-saman-adam": [task(
        "Bir görüşü önce saman adam, sonra en güçlü haliyle kur; döngüsel bir gerekçeyi bağımsız kanıtla onar.",
        ["Güçlü sürüm görüş sahibince kabul edilebilir mi?", "Sonuç öncülde yalnız başka sözlerle mi tekrarlanıyor?", "Yeni kanıt sonuçtan bağımsız mı?"],
        "Eleştiriden önce hedef görüşü doğru temsil et.",
    )],
    "ders-15-neden-sonuc-karisikliklari": [task(
        "Bir korelasyon için ters nedensellik, ortak neden ve seçim etkisi açıklamaları üret.",
        ["Gözlem ile nedensel sonucu ayırdın mı?", "Her açıklamanın gerektirdiği yeni veriyi yazdın mı?", "İddiayı sınayacak bir karşılaştırma tasarladın mı?"],
        "Hangi ek kanıtın rakip nedensel açıklamaları ayıracağını sor.",
    )],
    "ders-16-safsata-atolyesi-ve-yogun-vaka-analizi": [task(
        "Gerçek bir tartışma vakasını yeniden kur, olası safsatayı teşhis et ve daha güçlü bir sürümünü yaz.",
        ["Etiketten önce bozuk çıkarım adımını gösterdin mi?", "En yardımsever makul yorumu korudun mu?", "Onarımın gerektirdiği yeni kanıtı belirttin mi?"],
        "Amaç hata avcılığı değil, argümanın hangi koşullarda savunulabilir olduğunu bulmaktır.",
    )],
    "ders-17-sembollestirmeye-giris": [task(
        "Dört atomik önermeli kısa bir paragraf için sembol anahtarı kur ve paragrafı formüllere çevir.",
        ["Her sembol tek anlam taşıyor mu?", "Bağlaç kapsamını parantezlerle korudun mu?", "Geri çeviride anlam kayması oluyor mu?"],
        "Sembolleştirme sözcükleri değil, doğruluk koşullarını koruyan yapıyı çevirir.",
    )],
    "ders-18-degil-ve-ve-baglaclari": [task(
        "İç içe olumsuzlama ve birleşim içeren üç cümleyi sembolleştir; doğruluk koşullarını yaz.",
        ["'İkisi de değil' ile 'ikisi birden değil'i ayırdın mı?", "Olumsuzlamanın kapsamı açık mı?", "Birleşimin iki bileşenini de sınadın mı?"],
        "Olumsuzlamanın nereye uygulandığı formülün tamamını değiştirir.",
    )],
    "ders-19-veya-ve-ise": [task(
        "Aynı atomik önermelerle kapsayıcı veya, dışlayıcı veya, koşul ve çift yönlü koşul kurup sembolleştir.",
        ["Dışlayıcı veya için ek koşul var mı?", "Koşulun yönünü ters çevirdin mi?", "Çift yönlü koşulu iki yönlü gereklilik olarak açıkladın mı?"],
        "Benzer görünen bağlaçları doğruluk koşullarıyla karşılaştır.",
    )],
    "ders-20-dogruluk-tablolari-i": [task(
        "¬(p∧q) formülü için tam doğruluk tablosu kur ve ana sütundaki her değeri gerekçelendir.",
        ["Dört atamanın tamamı var mı?", "Önce p∧q sütununu hesapladın mı?", "Ana bağlacı ve nihai sütunu işaretledin mi?"],
        "Alt formüllerden ana bağlaca doğru ilerle.",
    )],
    "ders-21-dogruluk-tablolari-ii-ve-gecerlilik": [task(
        "p→q, q→r, p ∴ r argümanını doğruluk tablosuyla sınayıp geçerlilik kararını yaz.",
        ["Sekiz satırın tamamı var mı?", "Bütün öncüllerin doğru olduğu satırları işaretledin mi?", "Bu satırlarda sonucun değerine bakarak karar verdin mi?"],
        "Geçerlilik kararını öncüllerin birlikte doğru olduğu kritik satırlardan ver.",
    )],
    "ders-22-esdegerlik-kurallari-i": [task(
        "¬(p∧(q∨r)) formülünü De Morgan ve çift olumsuzlama kurallarıyla adım adım dönüştür.",
        ["Her satırda tek lisanslı dönüşüm var mı?", "Değişen alt formülü işaretledin mi?", "Son biçimi kısa tabloyla kontrol ettin mi?"],
        "Eşdeğerlik oku çıkarım değil, iki yönlü aynı doğruluk davranışıdır.",
    )],
    "ders-23-esdegerlik-kurallari-ii": [task(
        "p↔q formülünü yalnız ¬, ∧ ve ∨ kullanarak iki farklı eşdeğer biçimde yaz.",
        ["Koşul eşdeğerliklerini doğru kullandın mı?", "İki son biçim farklı yapı gösteriyor mu?", "Dönüşümlerde eşdeğerlik işareti kullandın mı?"],
        "Eşdeğer biçimler farklı kanıt ve hesaplama amaçlarına hizmet eder.",
    )],
    "ders-24-cikarim-kurallari-i": [task(
        "p→q, p∨r, ¬r öncüllerinden q sonucuna giden numaralı bir türetim yaz.",
        ["Her satırın dayanağı belirtilmiş mi?", "Ayrık tasım ve modus ponens adımları ayrı mı?", "Sonuç gizlice öncül olarak eklenmiş mi?"],
        "Önce ara hedef p'yi elde et, sonra koşullu öncülü kullan.",
    )],
    "ders-25-cikarim-kurallari-ii-ve-kisa-ispatlar": [task(
        "(p∧q)→r, p, q öncüllerinden r sonucuna giden en kısa gerekçeli türetimi yaz.",
        ["Birleşim kurma adımı açık mı?", "Her kural uygulaması biçimine uygun mu?", "Kısalık uğruna gerekçe atlandı mı?"],
        "Kanıt ekonomisi, lisanslı adımları koruyarak gereksiz satırları azaltmaktır.",
    )],
    "ders-26-niceleyicilere-giris": [task(
        "Aynı yüklemlerle 'her', 'bazı' ve 'hiçbir' içeren dört cümleyi açık bir söylem alanıyla sembolleştir.",
        ["Söylem alanını belirttin mi?", "Evrensel koşul ile varoluşsal birleşimi ayırdın mı?", "Formülleri geri çevirerek kontrol ettin mi?"],
        "Niceleyici, değişkeni bağlayan yüklem yapısı ve alanla birlikte anlam verir.",
    )],
    "ders-27-niceleyici-olumsuzlamalari": [task(
        "Üç niceleyicili cümlenin olumsuzunu sembolik ve doğal dilde yaz.",
        ["∀ ve ∃ değişimini yaptın mı?", "İç yüklemi olumsuzladın mı?", "'Her değil' ile 'hiçbiri değil'i ayırdın mı?"],
        "¬∀xFx, ∃x¬Fx demektir; ∀x¬Fx demek değildir.",
    )],
    "ders-28-coklu-niceleyici-ve-kapsam": [task(
        "∀x∃yRxy ile ∃y∀xRxy formüllerini ayıran küçük bir model kur.",
        ["Bireyleri ve R ilişkisini tanımladın mı?", "İlk formül modelde doğru mu?", "Tek bir ortak y bulunmadığını gösterdin mi?"],
        "Niceleyici sırası, seçimin kişiye göre değişip değişemeyeceğini belirler.",
    )],
    "ders-29-kimlik-yuklemler-ve-alan": [task(
        "Üç bireyli bir model kur; kimlik, tekli yüklem ve ikili ilişki içeren beş formülü değerlendir.",
        ["Alan ve sembol yorumları açık mı?", "Kimlik sıradan yüklem gibi ele alındı mı?", "R(a,b) ile R(b,a) yönü korundu mu?"],
        "Model, alan ile sembollerin yorumundan oluşur.",
    )],
    "ders-30-dogal-dilden-sembole-i": [task(
        "A/E/I/O biçimindeki dört kategorik cümleyi aynı yüklem anahtarıyla niceleyicili mantığa çevir.",
        ["Evrenselde koşul, varoluşsalda birleşim kullandın mı?", "'Hiçbir' için eşdeğer iki çeviri yazdın mı?", "Geri çeviri anlamı koruyor mu?"],
        "Sözcük sırasını değil bireyler üzerindeki doğruluk koşulunu koru.",
    )],
    "ders-31-dogal-dilden-sembole-ii": [task(
        "'Herkes birini eleştiriyor' cümlesinin iki kapsam okumasını sembolleştir ve ayırıcı bir model ver.",
        ["Niceleyici sıraları farklı mı?", "Bir okumada kişi seçimi bireye göre değişiyor mu?", "Model birini doğru, diğerini yanlış yapıyor mu?"],
        "Doğal dil belirsizliğini iki ayrı mantıksal okuma olarak görünür kıl.",
    )],
    "ders-32-bicimsel-sozdizim": [task(
        "İkisi iyi kurulmuş, ikisi bozuk dört formül üret; oluşum ağacını ya da ilk bozukluk noktasını göster.",
        ["Bağlaçların doğru sayıda bileşeni var mı?", "Bağlı ve serbest değişkenler işaretli mi?", "Parantez ve niceleyici kapsamı kurallı mı?"],
        "İyi kurulmuşluk anlamdan önce gelen özyinelemeli bir sözdizim koşuludur.",
    )],
    "ders-33-semantik-ve-modeller": [task(
        "Bir formül kümesi için küçük bir model, ardından sonucu yanlış yapan bir karşı model kur.",
        ["Alan ve sembol yorumları ayrı mı?", "Her öncül modelde doğru mu?", "Karşı model sonucu gerçekten yanlış yapıyor mu?"],
        "Semantik karar, sembollerin yorumlandığı yapı üzerinde tek tek doğrulanır.",
    )],
}
