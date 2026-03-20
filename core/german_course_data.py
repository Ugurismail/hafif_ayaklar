from copy import deepcopy
from random import SystemRandom
import re


GERMAN_COURSE_LEVELS = [
    {
        "slug": "a1",
        "title": "A1",
        "subtitle": "Temel başlangıç",
        "lesson_count": 10,
        "theme": "Basit cümleler, artikeller, selamlaşma ve gündelik hayata giriş.",
        "status": "active",
    },
    {
        "slug": "a2",
        "title": "A2",
        "subtitle": "Temel iletişim",
        "lesson_count": 10,
        "theme": "Rutinlerden ihtiyaç anlatımına ve kısa geçmiş anlatılarına geçiş.",
        "status": "planned",
    },
    {
        "slug": "b1",
        "title": "B1",
        "subtitle": "Bağımsız kullanım",
        "lesson_count": 15,
        "theme": "Kendi görüşünü ifade etme, neden-sonuç ve günlük iş yaşamı dili.",
        "status": "planned",
    },
    {
        "slug": "b2",
        "title": "B2",
        "subtitle": "Akıcı ifade",
        "lesson_count": 15,
        "theme": "Soyut konular, karmaşık cümle yapıları ve tartışma dili.",
        "status": "planned",
    },
    {
        "slug": "c1",
        "title": "C1",
        "subtitle": "İleri kullanım",
        "lesson_count": 15,
        "theme": "Nüanslı anlatım, akademik dil ve gelişmiş metin çözümleme.",
        "status": "planned",
    },
    {
        "slug": "c2",
        "title": "C2",
        "subtitle": "Ustalık",
        "lesson_count": 15,
        "theme": "İnce anlam farkları, yüksek doğruluk ve doğal akış.",
        "status": "planned",
    },
]


A1_SCOPE_MATRIX = [
    {"topic": "Selamlaşma ve tanışma", "teacher_flow": "Lektion 1-2", "platform_flow": "Ders 1-2", "status": "covered"},
    {"topic": "Wie geht's? ve hâl-hatır", "teacher_flow": "Lektion 2", "platform_flow": "Ders 2 (takviye)", "status": "covered"},
    {"topic": "Sayılar, yaş, ülke ve şehir", "teacher_flow": "Lektion 2", "platform_flow": "Ders 3", "status": "covered"},
    {"topic": "Düzenli fiiller ve soru düzeni", "teacher_flow": "Erken A1 boyunca dağınık", "platform_flow": "Ders 4", "status": "covered"},
    {"topic": "haben ve iyelik yapıları", "teacher_flow": "Erken A1 boyunca dağınık", "platform_flow": "Ders 5", "status": "covered"},
    {"topic": "Rutinler ve temel zaman ifadeleri", "teacher_flow": "Lektion 5", "platform_flow": "Ders 6", "status": "covered"},
    {"topic": "ein / eine / kein / keine", "teacher_flow": "Lektion 3-4", "platform_flow": "Ders 7", "status": "covered"},
    {"topic": "Ev, oda ve mekân soruları", "teacher_flow": "Lektion 4", "platform_flow": "Ders 7", "status": "covered"},
    {"topic": "Saatler, günler ve von-bis", "teacher_flow": "Lektion 5", "platform_flow": "Ders 8", "status": "covered"},
    {"topic": "Ayrılabilen fiillere giriş", "teacher_flow": "Lektion 5", "platform_flow": "Ders 8", "status": "covered"},
    {"topic": "Nominativ / Akkusativ temeli", "teacher_flow": "Lektion 6", "platform_flow": "Ders 9", "status": "covered"},
]


GRAMMAR_GUIDANCE = {
    "Temel artikel tablosu": {
        "teaching_note": (
            "Bu tabloyu cinsiyet ezberi gibi değil, kelime paketi gibi düşün. "
            "Amaç bu derste neden der, die ve das olduğunu çözmek değil; her yeni ismi artikeliyle birlikte görmeye alışmak."
        ),
        "watch_out": (
            "Türkçede artikel olmadığı için öğrenci ismi yalın bırakma eğilimine girer. "
            "Başlangıçtan itibaren der Tisch, die Lampe, das Buch diye blok tekrar yapmak gerekir."
        ),
    },
    "Selamlaşma kalıpları": {
        "teaching_note": (
            "Selamlaşma ifadeleri tek tek çevrilerek değil, hazır iletişim kalıbı olarak öğrenilir. "
            "Önce hangi saatte ve hangi resmiyet düzeyinde kullanıldığını ayırt etmek gerekir."
        ),
        "watch_out": (
            "Hallo, Guten Morgen ve Guten Tag aynı şey değildir. "
            "Özellikle günün saati değişince kalıbın da değiştiğini erken dönemde yerleştirmek gerekir."
        ),
    },
    "Tanışma için en temel cümleler": {
        "teaching_note": (
            "Bu bölümde cümle mantığı 'özne + kalıp + bilgi' şeklinde kurulur. "
            "İlk hedef uzun cümle kurmak değil, Ich heiße ..., Ich bin ..., Das ist ... gibi çekirdek yapıların yerini bozmadan kullanmaktır."
        ),
        "watch_out": (
            "Ich heiße ad söylemek için kurulu bir kalıptır; Ich bin ise kimlik, durum veya milliyet gibi başka bilgileri de taşır. "
            "İkisini aynı anlamda rastgele kullanmak yerine hangi boşluğu doldurduğunu görmek gerekir."
        ),
    },
    "İlk derste düşülen tipik hatalar": {
        "teaching_note": (
            "Bu kartın amacı yeni kural öğretmek değil, yanlış refleksi erken durdurmaktır. "
            "Başlangıçta yapılan küçük ezber hataları sonraki derslerde büyük zincir hatalara dönüşür."
        ),
        "watch_out": (
            "Bir kelimenin sadece tek Türkçe karşılığı varmış gibi davranmak ve artikeli atlamak en sık iki problemdir. "
            "Her örnekte kelimeyi cümle içindeki görevle birlikte okumak gerekir."
        ),
    },
    "Kişi zamirleri": {
        "teaching_note": (
            "Kişi zamirleri cümlede işi yapanı gösterir ve fiilin çekimini doğrudan belirler. "
            "Bu yüzden zamiri sadece kelime karşılığıyla değil, hangi fiil biçimini çağırdığıyla birlikte öğrenmek gerekir."
        ),
        "watch_out": (
            "sie ve Sie aynı yazıma çok yakın görünür ama aynı şey değildir. "
            "Küçük harfle sie 'o kadın' veya 'onlar', büyük harfle Sie ise resmî hitaptaki 'siz'dir."
        ),
    },
    "sein fiili çekimi": {
        "teaching_note": (
            "sein düzenli çekilmez; bu yüzden kalıbı kuralla üretmek yerine blok halinde tanımak gerekir. "
            "Erken A1'de asıl hedef bin, bist, ist, sind, seid biçimlerini doğru özneyle eşleştirmektir."
        ),
        "watch_out": (
            "Düzenli fiillerde gördüğün ek mantığını sein fiiline uygulayamazsın. "
            "Özellikle ihr seid ve sie/Sie sind biçimleri ayrı ayrı yerleşmelidir."
        ),
    },
    "Temel cümle kalıpları": {
        "teaching_note": (
            "Burada ana omurga 'zamir + sein + bilgi' şeklindedir. "
            "Son kısma ad, meslek, milliyet, duygu ya da basit nitelik gelir; bu yapı A1 boyunca onlarca kez geri döner."
        ),
        "watch_out": (
            "Ich bin ..., Du bist ..., Er ist ..., Sie ist ..., Es ist ..., Wir sind ..., Ihr seid ..., sie sind ..., Sie sind ... çizgisini eksiksiz görmeden ilerlemek doğru olmaz. "
            "Özne değişince fiilin de değiştiğini otomatik fark etmen gerekir."
        ),
    },
    "Kısa hâl-hatır kalıpları": {
        "teaching_note": (
            "Wie geht's?, Mir geht es gut. gibi yapılar bu seviyede tek tek çözülerek değil, hazır konuşma kalıbı olarak alınmalıdır. "
            "Amaç doğal giriş-çıkış refleksi kazanmaktır."
        ),
        "watch_out": (
            "Mir, dir ve Ihnen biçimlerinin ayrıntılı hâl bilgisini bu derste çözmüyoruz. "
            "Şimdilik bunları bozmadan ezberlenmesi gereken sabit ifade parçaları gibi kullan."
        ),
    },
    "İlk dersten farkı ne?": {
        "teaching_note": (
            "İlk derste hazır tanışma kalıpları vardı; burada ise cümlenin çekim iskeleti kuruluyor. "
            "Artık sadece ifade tanımıyor, özneye göre fiili de değiştiriyoruz."
        ),
        "watch_out": (
            "Ders 1'in kalıp mantığını bırakmıyoruz; sadece onun altındaki gramer omurgasını görünür hale getiriyoruz. "
            "Bu yüzden eski kalıpları da yeni çekimle birlikte tekrar etmek gerekir."
        ),
    },
    "0-20 arası temel sayılar": {
        "teaching_note": (
            "Bu sayılar günlük hayatta yaş, telefon, saat ve fiyat gibi alanlara giriş sağlar. "
            "İlk aşamada amaç matematik yapmak değil, sayıyı duyunca tanımak ve kısa cevapta kullanabilmektir."
        ),
        "watch_out": (
            "13-19 aralığında Türkçedeki dizilişi bekleme; Almancada bazı biçimler kulağa yabancı gelebilir. "
            "Sayıları tek tek değil, art arda seri tekrar ederek çalışmak daha hızlı sonuç verir."
        ),
    },
    "Yaş sorma ve söyleme": {
        "teaching_note": (
            "Almancada yaş, sahip olunan bir şey gibi değil, olunan bir durum gibi ifade edilir. "
            "Bu yüzden yaş söylerken haben değil sein kullanılır: Ich bin zwanzig Jahre alt."
        ),
        "watch_out": (
            "Türkçe ve İngilizce etkisiyle 'Benim 20 yaşım var' mantığını kopyalamak sık hatadır. "
            "Yaş ifadesinde çekirdek yapı daima sein fiiliyle kurulur."
        ),
    },
    "aus ve in farkı": {
        "teaching_note": (
            "aus kökeni veya geldiğin yeri, in ise bulunduğun yeri gösterir. "
            "A1'de bu ikisini ayırmak, 'nerelisin?' ile 'neredesin?' sorularını karıştırmamak için kritiktir."
        ),
        "watch_out": (
            "Ich bin aus Berlin ile Ich bin in Berlin aynı cümle değildir. "
            "İlki köken veya çıkış noktası, ikincisi şu anki konum bilgisidir."
        ),
    },
    "Milliyet söylemenin başlangıç kalıpları": {
        "teaching_note": (
            "Bu derste milliyeti en basit yüklem yapısı içinde veriyoruz: Ich bin türkisch. "
            "Amaç önce köken bilgisiyle sıfat benzeri milliyet ifadesini oturtmak, daha ileri nüansları sonraya bırakmaktır."
        ),
        "watch_out": (
            "Ülke adı ile milliyet aynı şey değildir. "
            "Deutschland ülke adıdır; deutsch ise dil veya milliyet niteliği olarak kullanılır."
        ),
    },
    "Önemli istisna: die Türkei": {
        "teaching_note": (
            "Bazı ülke adları artikel alır ve bu yüzden kalıp biraz değişir. "
            "die Türkei örneği, ülke isimlerinin her zaman artikelsiz gelmediğini erken dönemde göstermesi açısından önemlidir."
        ),
        "watch_out": (
            "Bütün ülke adlarına artikel ekleme alışkanlığı kurmak da yanlıştır. "
            "Bu başlık bir genel kural değil, dikkat edilmesi gereken sınırlı istisna mantığıdır."
        ),
    },
    "Düzenli fiil çekim mantığı": {
        "teaching_note": (
            "Düzenli fiillerde kök sabit kalır, kişi eki değişir. "
            "Bu dersi doğru oturtursan daha sonra yüzlerce fiili aynı iskelet üzerinden daha rahat okursun."
        ),
        "watch_out": (
            "Fiilin mastar biçimini ezberlemek yetmez; ich, du, er/sie/es, wir, ihr, sie/Sie çizgisini takip etmek gerekir. "
            "Özellikle du ve er/sie/es ekleri sık karışır."
        ),
    },
    "Sık kullanılan soru kelimeleri": {
        "teaching_note": (
            "Soru kelimesi cümlede hangi bilginin istendiğini belirler. "
            "wer kişi, wo yer, wann zaman, was nesne veya içerik, wie ise biçim veya durum sorar."
        ),
        "watch_out": (
            "Soru kelimelerini sadece Türkçe karşılığıyla değil, hangi bilgi alanını açtığıyla öğrenmek gerekir. "
            "Aksi halde doğru soru kelimesini seçsen bile yanlış türde cevap beklersin."
        ),
    },
    "Soru kelimeli cümle düzeni": {
        "teaching_note": (
            "Almanca soru kelimeli cümlede soru kelimesinden hemen sonra çekimli fiil gelir. "
            "Yani sıra çoğu zaman soru kelimesi + fiil + özne + diğer ögeler biçimindedir."
        ),
        "watch_out": (
            "Türkçedeki serbest sözdizimini Almancaya taşımak en sık hatalardan biridir. "
            "Soru kelimesini gördüğünde fiilin ikinci pozisyonda kalıp kalmadığını özellikle kontrol et."
        ),
    },
    "Evet-hayır soruları": {
        "teaching_note": (
            "Soru kelimesi yoksa fiil ilk sıraya geçerek soru kurar. "
            "Bu yapı kısa ve hızlı konuşmada çok kullanıldığı için erken oturması gerekir."
        ),
        "watch_out": (
            "Düz cümle dizilimini aynen bırakıp yalnız soru işareti eklemek Almanca için yeterli değildir. "
            "Fiilin başa geçtiğini gözle görmen gerekir."
        ),
    },
    "Kısa cevap ve bilgi genişletme": {
        "teaching_note": (
            "Amaç sadece 'evet' veya 'hayır' demek değil, o cevabı bir adım daha bilgiyle büyütebilmektir. "
            "Bu alışkanlık öğrenciyi çok erken safhada gerçek iletişime yaklaştırır."
        ),
        "watch_out": (
            "Tek kelimelik cevaplar faydalıdır ama kalıcı iletişim üretmez. "
            "Mümkün olduğunda Ja/Nein sonrasına kısa bir ikinci cümle eklemeyi alışkanlık haline getir."
        ),
    },
    "haben fiili çekimi": {
        "teaching_note": (
            "haben, sahiplik ve bazı temel nesne cümlelerinin omurgasını kurar. "
            "sein kadar temel olduğu için çekimini erken aşamada ayrı blok halinde görmek gerekir."
        ),
        "watch_out": (
            "sein ile haben görev olarak aynı değildir. "
            "Ben doktorum cümlesinde sein, benim bir kitabım var cümlesinde ise haben kullanılır."
        ),
    },
    "Temel iyelik kelimeleri": {
        "teaching_note": (
            "mein, dein, sein, ihr gibi kelimeler bir şeyin kime ait olduğunu gösterir. "
            "Bu derste onları ayrıntılı çekim tablosu olarak değil, en sık görülen blok biçimleriyle tanıyoruz."
        ),
        "watch_out": (
            "sein kelimesi hem 'olmak' fiilinin mastarı hem de 'onun' anlamındaki iyelik sözü olarak karşına çıkabilir. "
            "Kelimeden önce ya da sonra ne geldiğine bakmadan karar verme."
        ),
    },
    "Aile tanıtımı için iki temel kalıp": {
        "teaching_note": (
            "Aile anlatımında iki omurga öne çıkar: Das ist ... ve Ich habe ... "
            "Biri tanıtma, diğeri sahip olma ilişkisini kurar."
        ),
        "watch_out": (
            "Das ist mein Bruder ile Ich habe einen Bruder aynı bilgiyi farklı açıdan verir. "
            "Birinde tanıtma, diğerinde sahiplik yapısı çalışır."
        ),
    },
    "Günlük nesnelerle sahiplik": {
        "teaching_note": (
            "Sahiplik kalıpları kişi veya aileyle sınırlı değildir; eşyalarda da aynı mantık sürer. "
            "Bu, iyelik kelimelerinin gündelik hayata yayılmasını sağlar."
        ),
        "watch_out": (
            "Öznenin değişmesiyle hem haben çekimi hem de iyelik sözü değişebilir. "
            "Sadece nesneye odaklanıp cümlenin başını ihmal etme."
        ),
    },
    "Önemli ayrım: sein fiili ve sein iyeliği aynı şey değildir": {
        "teaching_note": (
            "Aynı yazılışın iki farklı görev üstlenmesi Almanca başlangıcında kafa karıştırır. "
            "Birinde fiil olarak yüklem kurulur, diğerinde isimden önce gelip sahiplik gösterilir."
        ),
        "watch_out": (
            "sein Buch ifadesindeki sein, 'olmak' anlamına gelmez. "
            "Fiil olup olmadığını anlamak için yanında isim mi yoksa cümlenin çekim merkezi mi olduğuna bak."
        ),
    },
    "Rutin fiilleri": {
        "teaching_note": (
            "Bu bölüm günlük akışı anlatan tekrar eden eylemleri kurar. "
            "Amaç tek tek fiil ezberlemekten çok sabah-kahvaltı-iş-okul-uyku zincirini cümleye çevirebilmektir."
        ),
        "watch_out": (
            "Rutin fiillerde zaman ifadesi sık kullanılır ama cümlenin fiil çekimi yine özneye göre yapılır. "
            "Zaman sözü eklenince fiilin çekimini unutma."
        ),
    },
    "Temel zaman ifadeleri": {
        "teaching_note": (
            "heute, morgen, morgens, abends gibi ifadeler zamanı kaba çerçevede verir. "
            "İlk aşamada bunları hazır zarf grupları gibi tanımak yeterlidir."
        ),
        "watch_out": (
            "Her zaman ifadesinin önüne edat gelmez. "
            "heute ve morgen yalın gelirken, saat ve gün anlatımında başka yapılar devreye girebilir."
        ),
    },
    "am, um ve yalın zaman zarfları": {
        "teaching_note": (
            "am gün ve bazı takvimli zamanları, um saatleri, yalın zaman zarfları ise edatsız genel zamanı anlatır. "
            "Bu ayrım cümleyi doğru kurmanın en temel zaman mantığıdır."
        ),
        "watch_out": (
            "um 8 Uhr, am Montag ve heute biçimleri birbirinin yerine geçmez. "
            "Önce 'saat mi, gün mü, genel zaman mı?' sorusunu sorup sonra kalıbı seç."
        ),
    },
    "Saat sorma ve söyleme": {
        "teaching_note": (
            "Saat dili kısa ama çok sık kullanılan bir alandır. "
            "Başlangıçta önce tam saatleri ve soru-cevap omurgasını temiz kurmak gerekir."
        ),
        "watch_out": (
            "Türkçedeki saat anlatımını birebir taşıma. "
            "Wie spät ist es? sorusuna Alman saat mantığıyla cevap vermeyi ayrı bir kalıp olarak çalış."
        ),
    },
    "Zaman ifadesi öndeyse fiil ikinci sırada kalır": {
        "teaching_note": (
            "Almancada cümlenin başına zaman, yer veya başka bir öğe gelebilir; ama çekimli fiil yine ikinci pozisyonu korur. "
            "Bu, sözdiziminde çok temel ve kalıcı bir kuraldır."
        ),
        "watch_out": (
            "Bugün, sabah, saat sekizde gibi ifadeleri başa alınca özneyi hemen araya sıkıştırma. "
            "Önce fiilin ikinci yerde kalıp kalmadığını kontrol et."
        ),
    },
    "Kısa rutin anlatımı kurma": {
        "teaching_note": (
            "Bu kartta ayrı ayrı öğrendiğin fiil, zaman ve sıra bilgilerini küçük paragraf hâline getiriyoruz. "
            "A1 için önemli olan kusursuz uzunluk değil, düzenli ve anlaşılır akıştır."
        ),
        "watch_out": (
            "Her cümleye aynı yapıyla başlamak metni yapaylaştırır. "
            "Ama çeşitlilik ararken fiilin yerini bozmamak gerekir."
        ),
    },
    "Belirli ve belirsiz artikel farkı": {
        "teaching_note": (
            "Belirli artikel, konuşanın ve dinleyenin hangi nesneden söz edildiğini bildiği durumlarda; belirsiz artikel ise ilk kez tanıtılan veya genel bir nesne için kullanılır. "
            "Bu fark iletişimde 'hangi şeyden bahsediyoruz?' sorusunu netleştirir."
        ),
        "watch_out": (
            "Her isme otomatik olarak bir artikel koymak yeterli değildir; der Tisch ile ein Tisch aynı bilgi yoğunluğunu taşımaz. "
            "Nesnenin bilinirlik derecesine bakmak gerekir."
        ),
    },
    "kein / keine ile isim olumsuzluğu": {
        "teaching_note": (
            "kein/keine, ismin önünde durup 'hiç yok / bir tane bile yok' anlamı kurar. "
            "Bu yapı özellikle var-yok ve sahiplik cümlelerinde çok doğal kullanılır."
        ),
        "watch_out": (
            "nicht ile kein aynı görevde değildir. "
            "Başlangıçta isim olumsuzluğunu görünce ilk refleks olarak kein/keine düşünmek gerekir."
        ),
    },
    "Temel ev ve oda kelimeleri": {
        "teaching_note": (
            "Mekân sorularını kurabilmek için önce ev, oda ve temel eşya kelimelerini blok hâlinde tanımak gerekir. "
            "Bu kelimeler daha sonra yer tarifine ve günlük konuşmaya temel olur."
        ),
        "watch_out": (
            "Özel isimleri kelime kartı gibi ezberlemek yerine gerçek mekân isimlerini örnek cümlede görmeye odaklan. "
            "Kelimeyi mutlaka artikel ve bağlamıyla birlikte al."
        ),
    },
    "Wo ist ...? ve kısa yer cevapları": {
        "teaching_note": (
            "Bu seviyede amaç tam yön tarifi vermek değil, yer sormayı ve kısa cevaplamayı başlatmaktır. "
            "Wo ist ...?, Hier., Dort. gibi küçük kalıplar bunun için yeterlidir."
        ),
        "watch_out": (
            "Yer sormayı köken sorma ile karıştırma; Wo yer, Woher ise köken sorar. "
            "İkisi benzer görünse de aynı bilgi türünü istemez."
        ),
    },
    "Es gibt / Gibt es ...?": {
        "teaching_note": (
            "Es gibt yapısı 'var' demenin en doğal yollarından biridir; soru biçimi ise fiilin başa geçmesiyle kurulur. "
            "Ev, oda ve nesne konuşmalarında bu kalıp çok sık geri döner."
        ),
        "watch_out": (
            "Türkçedeki 'orada bir masa var' mantığını kelime kelime çevirmeye çalışma. "
            "Önce Es gibt ... kalıbını bütün olarak tanı."
        ),
    },
    "Küçük not: maskulin çekim ayrıntısı sonra gelecek": {
        "teaching_note": (
            "Bu dersin amacı belirsiz artikel ve isim olumsuzluğu mantığını kurmak; maskulin değişim ayrıntısını sistematik olarak henüz açmıyoruz. "
            "Böylece öğrenci yeni kavram yükü altında ezilmeden ana farkı görebilir."
        ),
        "watch_out": (
            "ein, kein ve artikel değişimlerinin tamamını aynı derste çözmeye çalışma. "
            "Bu not bilinçli bir ertelemedir; bir sonraki yapıda detaylandırılacaktır."
        ),
    },
    "Tam saatler": {
        "teaching_note": (
            "Saat anlatımının ilk basamağı tam saatleri temiz kurmaktır. "
            "Bu yapı yerleşmeden yarım ve çeyrek saat kalıpları gereksiz karmaşa üretir."
        ),
        "watch_out": (
            "Saat cümlesinde yalnız rakama bakma; Uhr sözcüğü ve cümlenin genel dizilimi de önemlidir. "
            "Özellikle soru-cevap çiftlerini birlikte çalış."
        ),
    },
    "halb, Viertel nach ve Viertel vor": {
        "teaching_note": (
            "Bu üç yapı Almanca saat dilinin temel sıçrama noktalarıdır. "
            "Özellikle halb mantığı Türkçeden farklı işlediği için özel dikkat ister."
        ),
        "watch_out": (
            "halb acht, Türkçedeki gibi sekiz buçuk değil yedi buçuk mantığıyla çalışır. "
            "Yani sonraki saate doğru giden bir yapı olduğunu erken fark etmek gerekir."
        ),
    },
    "Hafta günleri ve am kullanımı": {
        "teaching_note": (
            "Hafta günleri bir rutin veya planın takvim ayağını kurar. "
            "Almancada gün adıyla en doğal başlangıç kalıbı am + gün biçimidir."
        ),
        "watch_out": (
            "Gün adı geldiğinde um kullanılamaz; um saat içindir. "
            "am Montag ile um acht Uhr farklı zaman türlerini gösterir."
        ),
    },
    "von ... bis ...": {
        "teaching_note": (
            "Bu kalıp başlangıç ve bitiş sınırını birlikte verir. "
            "Program, çalışma saati ve günlük plan anlatımında çok işlevlidir."
        ),
        "watch_out": (
            "Sadece iki zamanı yan yana yazmak yeterli değildir; aralık ilişkisini açıkça von ... bis ... ile kurmak gerekir. "
            "Saatler ve günler aynı kalıpta kullanılabilir ama bağlamı tutarlı kalmalıdır."
        ),
    },
    "Ayrılabilen fiillere giriş": {
        "teaching_note": (
            "Bazı fiillerde önek cümlede ayrılır ve sonda görünür. "
            "Bu derste yalnız temel fikri tanıyoruz; ayrıntılı tabloyu sonraya bırakıyoruz."
        ),
        "watch_out": (
            "Mastarı sözlükte tek parça görüp cümlede de aynı yerde kalmasını bekleme. "
            "Özellikle düz cümlede ikinci yerde çekimli fiil, sonda ise ayrılan parça bulunur."
        ),
    },
    "Nominativ nedir?": {
        "teaching_note": (
            "Nominativ, cümlenin öznesini yani işi yapan veya cümlenin merkezi olan ismi gösterir. "
            "Bu ayrımı net kurmadan nesne hâlini anlamak zorlaşır."
        ),
        "watch_out": (
            "İlk bakışta tüm isimleri aynı görme eğilimi vardır. "
            "Özneyi bulmak için 'kim / ne yapıyor?' sorusunu cümleye mutlaka uygula."
        ),
    },
    "Akkusativ nedir?": {
        "teaching_note": (
            "Akkusativ, fiilin doğrudan etkilediği nesneyi gösterir. "
            "Yani kitap okuyan kişi özne, okunan kitap ise çoğu zaman Akkusativ nesnedir."
        ),
        "watch_out": (
            "Her isim nesne değildir. "
            "Önce fiili bul, sonra fiilin doğrudan neyi etkilediğini sor; böylece hâli daha güvenli ayırt edersin."
        ),
    },
    "Artikel değişimi": {
        "teaching_note": (
            "Erken A1'de en kritik dönüşüm maskulin tekilde görünür: der -> den, ein -> einen, kein -> keinen. "
            "Diğer birçok yapı ilk aşamada değişmeden kalabildiği için öğrenci farkı burada daha net görür."
        ),
        "watch_out": (
            "Her artikel her durumda değişmiyor sanıp bütün yapıyı aynı renge boyama. "
            "Özellikle maskulin nesnede değişimin görünür olduğunu akılda tut."
        ),
    },
    "wen / was ile nesneyi bul": {
        "teaching_note": (
            "Ezber yerine soru mantığı kullanmak daha sağlamdır. "
            "Fiilden sonra 'kimi?' veya 'neyi?' diye sorduğunda bulduğun unsur çoğu zaman Akkusativ nesne olur."
        ),
        "watch_out": (
            "Sadece Türkçe çeviriye bakarsan nesneyi kaçırabilirsin. "
            "Soruyu doğrudan cümlenin içinde kurup cevabı işaretlemek daha güvenilir bir yöntemdir."
        ),
    },
    "Akkusativ alan temel fiiller": {
        "teaching_note": (
            "Bu seviyede bütün fiilleri değil, sık geçen birkaç temel fiili hedefliyoruz. "
            "haben, sehen, kaufen, brauchen gibi fiillerle nesne mantığı oturunca daha karmaşık yapılar kolaylaşır."
        ),
        "watch_out": (
            "Her fiili aynı kalıba sokma. "
            "Önce dersin verdiği fiiller üzerinde özne-nesne ayrımını otomatikleştir, sonra kapsamı genişlet."
        ),
    },
    "Yiyecek ve içecek kelimeleri artikel ile öğrenilir": {
        "teaching_note": (
            "Menü kelimeleri de diğer isimler gibi artikel, çoğul ve örnek cümle ile öğrenilir. "
            "Bu özellikle sipariş verirken maskulin nesne dönüşümünü doğru kurmak için gereklidir."
        ),
        "watch_out": (
            "Yiyecek kelimeleri tanıdık olduğu için öğrenci çoğu zaman artikeli ihmal eder. "
            "Ama einen Kaffee ile ein Wasser farkı tam bu bilgiye dayanır."
        ),
    },
    "Siparişte en temel iki kalıp": {
        "teaching_note": (
            "Restoranda ilk hedef kusursuz uzun cümle değil, kısa ve doğal sipariş üretmektir. "
            "Ich nehme ... ve Ich bestelle ... kalıpları bu seviyede en güvenli iki omurgadır."
        ),
        "watch_out": (
            "Sipariş anında sein fiiline ya da sözlükteki yalın isme kaçmak kolaydır. "
            "Doğal iletişim için fiil + nesne yapısını korumak gerekir."
        ),
    },
    "Restoranda temel soru kalıpları": {
        "teaching_note": (
            "Yiyecek-içecek bağlamında iletişim çoğu zaman üç eksende döner: var mı, ne kadar ve hesap. "
            "Bu yüzden az sayıda ama yüksek frekanslı soru kalıbını otomatikleştirmek gerekir."
        ),
        "watch_out": (
            "Her soruyu kelime kelime çevirmeye çalışma. "
            "Haben Sie ...?, Was kostet ...? ve Die Rechnung, bitte. hazır iletişim blokları gibi çalışılmalıdır."
        ),
    },
    "Siparişte Akkusativ nesne": {
        "teaching_note": (
            "Bu başlık, bir önceki dersteki nesne bilgisini gerçek hayata taşır. "
            "Sipariş fiilleri doğrudan nesne istediği için özellikle maskulin isimlerdeki dönüşüm artık işlevsel hale gelir."
        ),
        "watch_out": (
            "Bir önceki derste gördüğün der -> den, ein -> einen mantığını burada atlama. "
            "Restoran cümleleri kısa olduğu için hata çok görünür hale gelir."
        ),
    },
    "Kısa restoran diyaloğu mantığı": {
        "teaching_note": (
            "Gerçek diyalog tek bir büyük paragraf değil, kısa soru-cevap bloklarından oluşur. "
            "Bu yüzden önce sıralamayı kurmak gerekir: soru, sipariş, ek istek, kapanış."
        ),
        "watch_out": (
            "Tek tek güzel cümleler kurmak yetmez; diyalog akışı da mantıklı olmalıdır. "
            "Garsonun sorusuna konu dışı bir cevap vermek, gramer doğru olsa bile iletişimi bozar."
        ),
    },
}


GRAMMAR_USAGE = {
    "Temel artikel tablosu": "Yeni isim öğrenirken, nesneyi ilk kez tanırken ve kelimeyi sözlükte doğru paketle tutmak isterken kullanılır.",
    "Selamlaşma kalıpları": "Güne başlarken, bir konuşmaya giriş yaparken veya vedalaşırken kullanılır.",
    "Tanışma için en temel cümleler": "Adını söylemek, birini tanıtmak veya ilk kez kendini kısaca sunmak istediğinde kullanılır.",
    "İlk derste düşülen tipik hatalar": "Yeni cümle kurduktan sonra kendi üretimini hızlıca kontrol etmek için kullanılır.",
    "Kişi zamirleri": "Cümlede işi kimin yaptığını seçerken ve fiilin çekimini belirlerken kullanılır.",
    "sein fiili çekimi": "Kimlik, meslek, milliyet, durum ve temel nitelik bildirirken kullanılır.",
    "Temel cümle kalıpları": "Kısa ama anlamlı ilk Almanca cümleleri üretirken kullanılır.",
    "Kısa hâl-hatır kalıpları": "Birine nasılsın diye sormak ve kısa cevap vermek için kullanılır.",
    "İlk dersten farkı ne?": "Hazır kalıp bilgisinden fiil çekimli cümle omurgasına geçişi anlamak için kullanılır.",
    "0-20 arası temel sayılar": "Yaş, telefon, saat, fiyat ve temel sayma ihtiyacında kullanılır.",
    "Yaş sorma ve söyleme": "Birinin yaşını sorarken veya kendi yaşını söylerken kullanılır.",
    "aus ve in farkı": "Köken bilgisi ile bulunduğun yer bilgisini ayırmak istediğinde kullanılır.",
    "Milliyet söylemenin başlangıç kalıpları": "Milliyetini ya da dil bilgisini çok basit cümlelerle söylerken kullanılır.",
    "Önemli istisna: die Türkei": "Artikel alan ülke isimlerini görüp genel kalıptan ayrılan örnekleri fark etmek için kullanılır.",
    "Düzenli fiil çekim mantığı": "Yeni düzenli fiilleri özneye göre çekmek ve günlük eylem cümleleri kurmak için kullanılır.",
    "Sık kullanılan soru kelimeleri": "Kişi, yer, zaman, biçim veya içerik sorarken kullanılır.",
    "Soru kelimeli cümle düzeni": "Wer, wo, wann, was, wie gibi kelimelerle bilgi isteyen soru cümleleri kurarken kullanılır.",
    "Evet-hayır soruları": "Kısa onay/red cevabı beklenen sorular kurarken kullanılır.",
    "Kısa cevap ve bilgi genişletme": "Evet-hayır cevabını kısa bir ek bilgiyle büyütmek istediğinde kullanılır.",
    "haben fiili çekimi": "Sahiplik, aile üyeleri ve nesneler hakkında konuşurken kullanılır.",
    "Temel iyelik kelimeleri": "Bir şeyin kime ait olduğunu söylerken kullanılır.",
    "Aile tanıtımı için iki temel kalıp": "Aile üyelerini tanıtırken veya aile hakkında bilgi verirken kullanılır.",
    "Günlük nesnelerle sahiplik": "Kitap, telefon, çanta gibi eşyalardan söz ederken sahiplik kurmak için kullanılır.",
    "Önemli ayrım: sein fiili ve sein iyeliği aynı şey değildir": "Aynı biçimde görünen iki farklı yapıyı ayırmak gerektiğinde kullanılır.",
    "Rutin fiilleri": "Günlük alışkanlıkları ve tekrar eden eylemleri anlatırken kullanılır.",
    "Temel zaman ifadeleri": "Zamanı kaba çerçevede belirtmek ve eylemi gün içine yerleştirmek için kullanılır.",
    "am, um ve yalın zaman zarfları": "Saat, gün ve genel zaman ifadelerini doğru kalıpla seçerken kullanılır.",
    "Saat sorma ve söyleme": "Saat öğrenmek, saat söylemek ve basit zaman planı kurmak için kullanılır.",
    "Zaman ifadesi öndeyse fiil ikinci sırada kalır": "Cümleye zaman ifadesiyle başlarken sözdizimini doğru tutmak için kullanılır.",
    "Kısa rutin anlatımı kurma": "Bir günü birkaç kısa cümle ile akış halinde anlatırken kullanılır.",
    "Belirli ve belirsiz artikel farkı": "Nesnenin bilindiği ya da ilk kez tanıtıldığı durumları ayırırken kullanılır.",
    "kein / keine ile isim olumsuzluğu": "İsimleri ve nesneleri doğrudan olumsuzlamak istediğinde kullanılır.",
    "Temel ev ve oda kelimeleri": "Ev, oda ve eşya konuşmasına giriş yaparken kullanılır.",
    "Wo ist ...? ve kısa yer cevapları": "Bir şeyin nerede olduğunu sormak ve kısa cevap vermek için kullanılır.",
    "Es gibt / Gibt es ...?": "Bir yerde bir şeyin var olup olmadığını söylerken veya sorarken kullanılır.",
    "Küçük not: maskulin çekim ayrıntısı sonra gelecek": "Ana fikri kurup ayrıntıyı sonraki derse bırakman gereken yerde kullanılır.",
    "Tam saatler": "Saati açık ve doğrudan söylemen gereken durumlarda kullanılır.",
    "halb, Viertel nach ve Viertel vor": "Saati daha doğal Alman kullanımına yakın biçimde anlatırken kullanılır.",
    "Hafta günleri ve am kullanımı": "Plan, ders, iş ya da rutin gün belirtirken kullanılır.",
    "von ... bis ...": "Başlangıç ve bitiş zamanı veya gün aralığı verirken kullanılır.",
    "Ayrılabilen fiillere giriş": "Önekli bazı günlük fiillerin cümlede nasıl dağıldığını ilk kez tanırken kullanılır.",
    "Nominativ nedir?": "Özneyi belirlemek ve cümlede işi yapan unsuru ayırmak için kullanılır.",
    "Akkusativ nedir?": "Fiilin doğrudan etkilediği nesneyi bulmak için kullanılır.",
    "Artikel değişimi": "Özellikle maskulin nesnede artikel ve ein/kein biçimlerinin neden değiştiğini görmek için kullanılır.",
    "wen / was ile nesneyi bul": "Nesneyi ezberlemeden soru mantığıyla tespit etmek için kullanılır.",
    "Akkusativ alan temel fiiller": "Nesne alan yaygın fiilleri kullanarak ilk doğru Akkusativ cümlelerini kurarken kullanılır.",
    "Yiyecek ve içecek kelimeleri artikel ile öğrenilir": "Menü, kafe ve günlük yemek konuşmasına girerken kullanılır.",
    "Siparişte en temel iki kalıp": "Bir şey isterken, sipariş verirken veya kısa servis diyalogu kurarken kullanılır.",
    "Restoranda temel soru kalıpları": "Var-yok, fiyat ve hesap isteme durumlarında kullanılır.",
    "Siparişte Akkusativ nesne": "Maskulin yiyecek-içecek isimleriyle sipariş verirken kullanılır.",
    "Kısa restoran diyaloğu mantığı": "Garson-müşteri akışını kısa ama doğal bloklarla kurarken kullanılır.",
}


GRAMMAR_FORMULAS = {
    "Temel artikel tablosu": "artikel + isim",
    "Selamlaşma kalıpları": "selam + (ad / kısa devam cümlesi)",
    "Tanışma için en temel cümleler": "özne + tanışma kalıbı + bilgi",
    "İlk derste düşülen tipik hatalar": "kontrol: artikel + isim / doğru kalıp",
    "Kişi zamirleri": "zamir + çekimli fiil",
    "sein fiili çekimi": "zamir + sein + bilgi",
    "Temel cümle kalıpları": "özne + sein + ad / durum / milliyet",
    "Kısa hâl-hatır kalıpları": "Wie geht ...? / Mir geht es ...",
    "İlk dersten farkı ne?": "hazır kalıp -> zamir + fiil + bilgi",
    "0-20 arası temel sayılar": "sayı kelimesi + bağlam",
    "Yaş sorma ve söyleme": "Wie alt bist du? / Ich bin ... Jahre alt.",
    "aus ve in farkı": "Ich bin aus ... / Ich bin in ...",
    "Milliyet söylemenin başlangıç kalıpları": "Ich bin + milliyet",
    "Önemli istisna: die Türkei": "aus der ... / in der ...",
    "Düzenli fiil çekim mantığı": "özne + fiil kökü + kişi eki",
    "Sık kullanılan soru kelimeleri": "soru kelimesi + fiil + özne",
    "Soru kelimeli cümle düzeni": "soru kelimesi + çekimli fiil + özne + diğer ögeler",
    "Evet-hayır soruları": "çekimli fiil + özne + diğer ögeler",
    "Kısa cevap ve bilgi genişletme": "Ja/Nein + kısa ikinci cümle",
    "haben fiili çekimi": "özne + haben + nesne",
    "Temel iyelik kelimeleri": "iyelik sözü + isim",
    "Aile tanıtımı için iki temel kalıp": "Das ist ... / Ich habe ...",
    "Günlük nesnelerle sahiplik": "özne + haben + iyelik / nesne",
    "Önemli ayrım: sein fiili ve sein iyeliği aynı şey değildir": "sein = fiil / sein + isim = iyelik",
    "Rutin fiilleri": "özne + rutin fiili + zaman",
    "Temel zaman ifadeleri": "zaman zarfı + cümle",
    "am, um ve yalın zaman zarfları": "am + gün / um + saat / yalın zarf",
    "Saat sorma ve söyleme": "Wie spät ist es? / Es ist ... Uhr.",
    "Zaman ifadesi öndeyse fiil ikinci sırada kalır": "zaman + fiil + özne + diğer ögeler",
    "Kısa rutin anlatımı kurma": "zaman + özne + fiil + tamamlayıcı",
    "Belirli ve belirsiz artikel farkı": "der/die/das + isim / ein/eine + isim",
    "kein / keine ile isim olumsuzluğu": "kein / keine + isim",
    "Temel ev ve oda kelimeleri": "artikel + oda / eşya ismi",
    "Wo ist ...? ve kısa yer cevapları": "Wo ist ...? / Hier. / Dort.",
    "Es gibt / Gibt es ...?": "Es gibt + nesne / Gibt es + nesne?",
    "Küçük not: maskulin çekim ayrıntısı sonra gelecek": "önce ana kalıp, sonra maskulin değişim",
    "Tam saatler": "Es ist + saat + Uhr.",
    "halb, Viertel nach ve Viertel vor": "Es ist halb ... / Viertel nach ... / Viertel vor ...",
    "Hafta günleri ve am kullanımı": "am + gün",
    "von ... bis ...": "von + başlangıç + bis + bitiş",
    "Ayrılabilen fiillere giriş": "özne + çekimli fiil ... ayrılan önek",
    "Nominativ nedir?": "özne = Nominativ",
    "Akkusativ nedir?": "doğrudan nesne = Akkusativ",
    "Artikel değişimi": "der -> den / ein -> einen / kein -> keinen",
    "wen / was ile nesneyi bul": "fiil + kimi?/neyi? sorusu",
    "Akkusativ alan temel fiiller": "özne + fiil + Akkusativ nesne",
    "Yiyecek ve içecek kelimeleri artikel ile öğrenilir": "artikel + menü kelimesi",
    "Siparişte en temel iki kalıp": "Ich nehme / Ich bestelle + nesne",
    "Restoranda temel soru kalıpları": "Haben Sie ...? / Was kostet ...? / Die Rechnung, bitte.",
    "Siparişte Akkusativ nesne": "fiil + Akkusativ nesne",
    "Kısa restoran diyaloğu mantığı": "soru -> sipariş -> ek istek -> kapanış",
}


GLOSS_PATTERN = re.compile(r"\[\[(?P<term>.+?)::(?P<tooltip>.+?)\]\]")


def _build_gloss_segments(text):
    segments = []
    cursor = 0

    for match in GLOSS_PATTERN.finditer(text):
        if match.start() > cursor:
            segments.append({"text": text[cursor:match.start()], "tooltip": ""})

        segments.append(
            {
                "text": match.group("term"),
                "tooltip": match.group("tooltip"),
            }
        )
        cursor = match.end()

    if cursor < len(text):
        segments.append({"text": text[cursor:], "tooltip": ""})

    return segments


def _prepare_reading_passages(lesson):
    passages = []

    for passage in lesson.get("reading_passages", []):
        prepared_passage = dict(passage)
        prepared_paragraphs = []

        for paragraph in passage.get("paragraphs", []):
            prepared_paragraphs.append(
                {
                    "segments": _build_gloss_segments(paragraph),
                }
            )

        prepared_passage["paragraphs"] = prepared_paragraphs
        passages.append(prepared_passage)

    lesson["reading_passages"] = passages
    return lesson


def _build_grammar_example_note(title, example):
    lower = title.lower()

    if "artikel" in lower and "belirli ve belirsiz" not in lower:
        return "Burada isim, artikeliyle birlikte veriliyor. Amaç kelimeyi yalın değil, doğru artikel paketiyle görmek."
    if "selamlaşma" in lower:
        return "Örnek, ifadenin tek tek çevrilmeden hazır iletişim kalıbı olarak kullanılmasını gösteriyor."
    if "tanışma" in lower:
        return "Bu cümlede kişi bilgisi doğrudan kısa tanışma kalıbına yerleştiriliyor."
    if "tipik hata" in lower:
        return "Örnek, öğrencinin ilk derste en sık yaptığı kaymayı görünür hale getiriyor."
    if "kişi zamirleri" in lower:
        return "Burada asıl odak, öznenin seçilmesi ve fiil çekiminin o özneye bağlanmasıdır."
    if "sein fiili" in lower:
        return "Örnek, özneye göre değişen sein biçiminin yüklem görevini nasıl kurduğunu gösteriyor."
    if "temel cümle kalıpları" in lower:
        return "Bu yapı, zamir + sein + bilgi omurgasının ilk anlamlı cümleyi nasıl kurduğunu gösterir."
    if "hâl-hatır" in lower:
        return "Burada kalıp çözümlemekten çok, soru ve cevabı blok halinde duymaya alışmak önemlidir."
    if "farkı ne" in lower:
        return "Örnek, önceki dersteki hazır kalıpların artık çekimli cümleye dönüştüğünü gösteriyor."
    if "sayılar" in lower:
        return "Sayı burada soyut değil; günlük bir bağlam içinde duyulup üretilen bilgi olarak kullanılıyor."
    if "yaş" in lower:
        return "Örnek, yaşın haben ile değil sein ile ifade edildiğini netleştirir."
    if "aus ve in" in lower:
        return "Bu cümlede köken ile bulunulan yer arasındaki anlam farkı görünür hale geliyor."
    if "milliyet" in lower:
        return "Örnek, ülke adıyla milliyet sıfatının aynı şey olmadığını uygulama içinde gösteriyor."
    if "türkiye" in lower or "turkei" in lower:
        return "İstisna ülke adı burada artikel aldığı için kalıp normal ülke adlarından biraz farklı kuruluyor."
    if "düzenli fiil" in lower:
        return "Fiil kökü sabit kalıyor; değişen kısım özneye bağlı ek oluyor."
    if "soru kelimeleri" in lower:
        return "Örnek, soru kelimesinin hangi bilgi türünü açtığını cümle içinde gösteriyor."
    if "soru kelimeli cümle düzeni" in lower:
        return "Burada kritik nokta, soru kelimesinden hemen sonra çekimli fiilin gelmesidir."
    if "evet-hayır soruları" in lower:
        return "Soru kelimesi yok; soruyu kuran esas hareket fiilin başa geçmesidir."
    if "kısa cevap ve bilgi genişletme" in lower:
        return "Örnek, tek kelimelik yanıtın nasıl küçük bir ikinci cümleyle büyütülebileceğini gösteriyor."
    if "haben fiili" in lower:
        return "Burada sahiplik anlamı haben üzerinden kuruluyor; nesne cümlenin bilgi yükünü taşıyor."
    if "iyelik" in lower:
        return "Örnek, nesnenin kime ait olduğunu isimden önce gelen iyelik sözüyle kuruyor."
    if "aile tanıtımı" in lower:
        return "Bu cümle aile bilgisini ya tanıtma ya da sahiplik kalıbı üzerinden veriyor."
    if "günlük nesnelerle sahiplik" in lower:
        return "Örnek, iyelik ve nesne bilgisini gündelik eşya alanına taşıyor."
    if "aynı şey değildir" in lower:
        return "Burada aynı yazılan yapının fiil mi iyelik mi olduğunu bağlam belirliyor."
    if "rutin fiilleri" in lower:
        return "Cümle, tekrar eden bir günlük eylemi özne ve zaman ilişkisiyle birlikte kuruyor."
    if "temel zaman ifadeleri" in lower:
        return "Bu örnek, zamanı ayrıntılı saat vermeden genel çerçevede göstermeyi amaçlıyor."
    if "am, um" in lower:
        return "Burada saat, gün veya yalın zaman ifadesi için doğru yapı seçiminin nasıl yapıldığı görülüyor."
    if "saat sorma" in lower:
        return "Örnek, saat sorusu ile saat cevabının birbirine nasıl bağlandığını gösteriyor."
    if "fiil ikinci" in lower:
        return "Zaman ifadesi başa gelse bile çekimli fiilin ikinci yerde kaldığına dikkat et."
    if "rutin anlatımı" in lower:
        return "Bu örnek, tek kuralı değil birkaç küçük kuralın akış içinde nasıl birleştiğini gösteriyor."
    if "belirli ve belirsiz artikel farkı" in lower:
        return "Örnek, bilinen nesne ile ilk kez tanıtılan nesne arasındaki farkı görünür hale getiriyor."
    if "kein / keine" in lower:
        return "Burada olumsuzluk isim üzerinde kuruluyor; yani odak fiil değil nesnenin yokluğu."
    if "ev ve oda kelimeleri" in lower:
        return "Kelime ailesi gerçek mekân konuşmasına temel olacak şekilde blok hâlinde veriliyor."
    if "wo ist" in lower:
        return "Örnek, yer sorusunun kısa ve hızlı cevapla nasıl karşılandığını gösteriyor."
    if "es gibt" in lower:
        return "Bu kalıp, bir yerde bir şeyin var olup olmadığını doğal Almanca akışla anlatır."
    if "maskulin çekim" in lower:
        return "Örnek, ana yapıyı koruyup ayrıntılı maskulin değişimi bilinçli olarak sonraya bıraktığımızı gösteriyor."
    if "tam saatler" in lower:
        return "Burada amaç saati açık, kısa ve hatasız söylemektir."
    if "viertel" in lower or "halb" in lower:
        return "Örnek, Almanca saat mantığının Türkçeden farklı işleyen doğal kullanımını gösteriyor."
    if "hafta günleri" in lower:
        return "Cümle, gün bilgisini am kalıbıyla zaman eksenine yerleştiriyor."
    if "von ... bis ..." in lower:
        return "Burada başlangıç ve bitiş bir aralık ilişkisi içinde birlikte veriliyor."
    if "ayrılabilen fiillere giriş" in lower:
        return "Örnek, fiilin çekimli parçası ile ayrılan önekin cümlede farklı yerlere gittiğini gösteriyor."
    if "nominativ" in lower and "akkusativ" not in lower:
        return "Bu örnek, cümlede işi yapan unsurun özne olarak nasıl tanındığını gösteriyor."
    if "akkusativ nedir" in lower:
        return "Burada fiilin doğrudan etkilediği nesne, cümlede ayrı bir rol üstleniyor."
    if "artikel değişimi" in lower:
        return "Örnek, özellikle maskulin nesnede görünür hale gelen artikel dönüşümünü netleştiriyor."
    if "wen / was" in lower:
        return "Bu cümle, nesneyi ezberlemeden soru mantığıyla bulabileceğini gösterir."
    if "akkusativ alan temel fiiller" in lower:
        return "Örnek, nesne isteyen fiilin ardından doğru hâlde bir isim getirilmesini gösteriyor."

    return "Bu örnek, kuralın cümle içinde hangi görevi üstlendiğini görünür hale getiriyor."


def _build_grammar_contrast(title):
    lower = title.lower()

    if "temel artikel tablosu" in lower:
        return {
            "correct": "der Tisch",
            "wrong": "Tisch",
            "reason": "İsmi artikelsiz almak başlangıçta küçük görünür ama sonraki çekimlerde zemini bozar.",
        }
    if "selamlaşma" in lower:
        return {
            "correct": "Guten Morgen!",
            "wrong": "Guten Morgen! (akşam saatinde)",
            "reason": "Selamlaşma kalıpları günün saatine ve bağlama göre seçilir.",
        }
    if "tanışma" in lower:
        return {
            "correct": "Ich heiße Lara.",
            "wrong": "Ich heiße müde.",
            "reason": "Ich heiße ad vermek için kullanılır; durum ve nitelik için kullanılmaz.",
        }
    if "tipik hata" in lower:
        return {
            "correct": "der Name",
            "wrong": "sadece Name",
            "reason": "Kontrol listesi, kelimeyi doğru paketle öğrenip öğrenmediğini sınar.",
        }
    if "kişi zamirleri" in lower:
        return {
            "correct": "Wir",
            "wrong": "Ihr (biz anlamında)",
            "reason": "Zamir seçimi yanlışsa bütün fiil çekimi de yanlış yola gider.",
        }
    if "sein fiili" in lower:
        return {
            "correct": "Wir sind",
            "wrong": "Wir seid",
            "reason": "sein fiili düzenli çekilmez; biçimleri tek tek doğru özneyle eşleştirmek gerekir.",
        }
    if "temel cümle kalıpları" in lower:
        return {
            "correct": "Sie ist müde.",
            "wrong": "Sie sind müde. (o kadın anlamında)",
            "reason": "Özne tekilse fiil de tekil çekilir; yalnız resmî Sie ile sind kullanılır.",
        }
    if "hâl-hatır" in lower:
        return {
            "correct": "Mir geht es gut.",
            "wrong": "Ich gehe gut.",
            "reason": "Bu başlıkta kullanılan ifade serbest üretim değil, sabit konuşma kalıbıdır.",
        }
    if "farkı ne" in lower:
        return {
            "correct": "Ich bin Can.",
            "wrong": "Ich sein Can.",
            "reason": "Hazır kelimeyi değil, özneye göre çekilmiş fiili kullanmak gerekir.",
        }
    if "sayılar" in lower:
        return {
            "correct": "zwanzig",
            "wrong": "zwansig",
            "reason": "Sayılar hızlı geçtiği için yazım ve telaffuz birlikte tekrar edilmelidir.",
        }
    if "yaş" in lower:
        return {
            "correct": "Ich bin 20 Jahre alt.",
            "wrong": "Ich habe 20 Jahre.",
            "reason": "Almancada yaş, sahip olunan bir nesne gibi değil, olunan bir durum gibi ifade edilir.",
        }
    if "aus ve in" in lower:
        return {
            "correct": "Ich bin aus Ankara.",
            "wrong": "Ich bin in Ankara. (köken anlatmak isterken)",
            "reason": "aus kökeni, in ise bulunduğun yeri bildirir.",
        }
    if "milliyet" in lower:
        return {
            "correct": "Ich bin deutsch.",
            "wrong": "Ich bin Deutschland.",
            "reason": "Ülke adı ile milliyet/dil bilgisi aynı yapı değildir.",
        }
    if "türkiye" in lower or "turkei" in lower:
        return {
            "correct": "Ich komme aus der Türkei.",
            "wrong": "Ich komme aus Türkei.",
            "reason": "Bu ülke adı artikel aldığı için kalıp da artikelli kurulur.",
        }
    if "düzenli fiil" in lower:
        return {
            "correct": "du arbeitest",
            "wrong": "du arbeiten",
            "reason": "Mastar biçimi değil, özneye göre çekilmiş fiil kullanılmalıdır.",
        }
    if "soru kelimeleri" in lower:
        return {
            "correct": "Wo wohnst du?",
            "wrong": "Wer wohnst du?",
            "reason": "Soru kelimesi, sorulan bilgi türüne uygun seçilmelidir.",
        }
    if "soru kelimeli cümle düzeni" in lower:
        return {
            "correct": "Wo wohnst du?",
            "wrong": "Wo du wohnst?",
            "reason": "Soru kelimesinden sonra çekimli fiil gelir.",
        }
    if "evet-hayır soruları" in lower:
        return {
            "correct": "Kommst du aus Izmir?",
            "wrong": "Du kommst aus Izmir?",
            "reason": "Bu tip soruda fiil başa geçerek soru kurar.",
        }
    if "kısa cevap ve bilgi genişletme" in lower:
        return {
            "correct": "Ja. Ich wohne in Bursa.",
            "wrong": "Ja in Bursa.",
            "reason": "Yanıtı küçük ama tam bir ikinci cümleyle genişletmek daha doğru refleks oluşturur.",
        }
    if "haben fiili" in lower:
        return {
            "correct": "Ich habe ein Buch.",
            "wrong": "Ich bin ein Buch.",
            "reason": "Sahiplik cümlesi haben ile kurulur; sein burada yanlış görevde kalır.",
        }
    if "iyelik" in lower:
        return {
            "correct": "mein Buch",
            "wrong": "ich Buch",
            "reason": "Aitlik, zamirle değil isimden önce gelen iyelik sözüyle kurulur.",
        }
    if "aile tanıtımı" in lower:
        return {
            "correct": "Das ist meine Schwester.",
            "wrong": "Ich habe meine Schwester. (tanıtma isterken)",
            "reason": "Tanıtma ve sahiplik kalıpları aynı işlevde kullanılmaz.",
        }
    if "günlük nesnelerle sahiplik" in lower:
        return {
            "correct": "Wir haben einen Tisch.",
            "wrong": "Wir sind einen Tisch.",
            "reason": "Nesneye sahip olma anlamı haben ile kurulur.",
        }
    if "aynı şey değildir" in lower:
        return {
            "correct": "sein Buch",
            "wrong": "sein = her yerde olmak fiili",
            "reason": "Aynı biçim, bağlama göre fiil ya da iyelik sözü olabilir.",
        }
    if "rutin fiilleri" in lower:
        return {
            "correct": "Ich arbeite morgens.",
            "wrong": "Ich arbeiten morgens.",
            "reason": "Rutin anlatırken de fiil özneye göre çekilir.",
        }
    if "temel zaman ifadeleri" in lower:
        return {
            "correct": "Heute lerne ich Deutsch.",
            "wrong": "Am heute lerne ich Deutsch.",
            "reason": "Bazı zaman ifadeleri yalın gelir; her zaman sözü edat almaz.",
        }
    if "am, um" in lower:
        return {
            "correct": "um 8 Uhr / am Montag",
            "wrong": "am 8 Uhr / um Montag",
            "reason": "Saat ve gün için kullanılan yapı aynı değildir.",
        }
    if "saat sorma" in lower:
        return {
            "correct": "Es ist neun Uhr.",
            "wrong": "Es neun Uhr.",
            "reason": "Saat cümlesinde çekimli yapı eksik bırakılamaz.",
        }
    if "fiil ikinci" in lower:
        return {
            "correct": "Heute lerne ich Deutsch.",
            "wrong": "Heute ich lerne Deutsch.",
            "reason": "Cümle başına zaman gelse de çekimli fiil ikinci yerde kalır.",
        }
    if "rutin anlatımı" in lower:
        return {
            "correct": "Am Morgen stehe ich auf und arbeite.",
            "wrong": "Am Morgen ich aufstehe und arbeite.",
            "reason": "Akış kurulurken de fiil yeri ve çekim korunmalıdır.",
        }
    if "belirli ve belirsiz artikel farkı" in lower:
        return {
            "correct": "ein Tisch / der Tisch",
            "wrong": "iki yapıyı aynı anlamda rastgele kullanmak",
            "reason": "Belirlilik derecesi değişince artikel de değişir.",
        }
    if "kein / keine" in lower:
        return {
            "correct": "Ich habe kein Auto.",
            "wrong": "Ich habe nicht Auto.",
            "reason": "İsim olumsuzluğu doğrudan kein/keine ile kurulur.",
        }
    if "ev ve oda kelimeleri" in lower:
        return {
            "correct": "das Zimmer",
            "wrong": "Zimmer",
            "reason": "Mekân kelimeleri de diğer isimler gibi artikel ile öğrenilmelidir.",
        }
    if "wo ist" in lower:
        return {
            "correct": "Wo ist das Buch? Dort.",
            "wrong": "Woher ist das Buch?",
            "reason": "Yer sorma ile köken sorma aynı soru değildir.",
        }
    if "es gibt" in lower:
        return {
            "correct": "Es gibt ein Bad.",
            "wrong": "Es hat ein Bad.",
            "reason": "Var-yok anlatımında Almancanın doğal kalıbı Es gibt yapısıdır.",
        }
    if "maskulin çekim" in lower:
        return {
            "correct": "ein Tisch",
            "wrong": "bu derste hemen einen üzerinden tüm sistemi zorlamak",
            "reason": "Bu noktada ana fikir kuruluyor; ayrıntılı maskulin dönüşüm bilinçli olarak sonraya bırakılıyor.",
        }
    if "tam saatler" in lower:
        return {
            "correct": "Es ist acht Uhr.",
            "wrong": "Es ist acht.",
            "reason": "Başlangıç aşamasında Uhr ile açık saat söylemek daha güvenli zemin kurar.",
        }
    if "viertel" in lower or "halb" in lower:
        return {
            "correct": "Es ist halb acht.",
            "wrong": "halb acht = sekiz buçuk",
            "reason": "halb, bir sonraki saate doğru giden yarım saat mantığıyla çalışır.",
        }
    if "hafta günleri" in lower:
        return {
            "correct": "am Dienstag",
            "wrong": "um Dienstag",
            "reason": "Gün adıyla kullanılan yapı am + gün biçimidir.",
        }
    if "von ... bis ..." in lower:
        return {
            "correct": "von 8 bis 10",
            "wrong": "8 bis zu 10 (bu ders mantığında)",
            "reason": "Başlangıçta aralık kurmak için temiz kalıp von ... bis ... olarak tutulur.",
        }
    if "ayrılabilen fiillere giriş" in lower:
        return {
            "correct": "Ich stehe um 7 Uhr auf.",
            "wrong": "Ich aufstehe um 7 Uhr.",
            "reason": "Çekimli fiil önde kalır, ayrılan parça cümlenin sonuna gider.",
        }
    if "nominativ nedir" in lower:
        return {
            "correct": "Der Mann kauft ein Buch. -> Der Mann = özne",
            "wrong": "ein Buch = özne",
            "reason": "İşi yapan unsur özne, yani Nominativ olarak okunur.",
        }
    if "akkusativ nedir" in lower:
        return {
            "correct": "Der Mann kauft ein Buch. -> ein Buch = nesne",
            "wrong": "Der Mann = Akkusativ nesne",
            "reason": "Fiilin doğrudan etkilediği unsur nesne görevindedir.",
        }
    if "artikel değişimi" in lower:
        return {
            "correct": "Ich kaufe den Tisch.",
            "wrong": "Ich kaufe der Tisch.",
            "reason": "Maskulin nesne Akkusativ olduğunda artikel görünür biçimde değişir.",
        }
    if "wen / was" in lower:
        return {
            "correct": "Wen kaufst du? -> bu soru yanlış / Was kaufst du? -> doğru nesne sorusu",
            "wrong": "Her nesneye otomatik wen demek",
            "reason": "Canlı-cansız ve kişi-nesne ayrımı soruda doğru seçilmelidir.",
        }
    if "akkusativ alan temel fiiller" in lower:
        return {
            "correct": "Ich brauche einen Stuhl.",
            "wrong": "Ich brauche ein Stuhl.",
            "reason": "Maskulin nesne fiilin etkisi altına girdiğinde Akkusativ biçimi gerekir.",
        }
    if "yiyecek ve içecek kelimeleri artikel ile öğrenilir" in lower:
        return {
            "correct": "der Kaffee / die Suppe / das Wasser",
            "wrong": "Kaffee / Suppe / Wasser",
            "reason": "Menü kelimeleri de artikelsiz değil, tam isim paketi olarak öğrenilmelidir.",
        }
    if "siparişte en temel iki kalıp" in lower:
        return {
            "correct": "Ich nehme einen Tee.",
            "wrong": "Ich bin einen Tee.",
            "reason": "Siparişte fiil + nesne yapısı gerekir; sein burada yanlış görevde kalır.",
        }
    if "restoranda temel soru kalıpları" in lower:
        return {
            "correct": "Was kostet der Salat?",
            "wrong": "Wo kostet der Salat?",
            "reason": "Fiyat sorusunda Was kostet ...? kalıbı kullanılır.",
        }
    if "siparişte akkusativ nesne" in lower:
        return {
            "correct": "Ich bestelle den Salat.",
            "wrong": "Ich bestelle der Salat.",
            "reason": "Maskulin nesne fiilin doğrudan nesnesi olduğunda artikel değişir.",
        }
    if "kısa restoran diyaloğu mantığı" in lower:
        return {
            "correct": "Garson: Noch etwas? / Müşteri: Nein, danke.",
            "wrong": "Garson: Noch etwas? / Müşteri: Ich bin Pizza.",
            "reason": "Diyalogta yanıt, sorunun açtığı bağlama uygun olmalıdır.",
        }

    return {
        "correct": "Kuralı örnek cümle içinde uygula",
        "wrong": "Türkçedeki dizilişi doğrudan kopyala",
        "reason": "Bu başlıkta amaç yapıyı Almanca cümle mantığı içinde görmek.",
    }


def _prepare_grammar_sections(lesson):
    prepared_sections = []

    for section in lesson.get("grammar_sections", []):
        prepared_section = dict(section)
        guidance = GRAMMAR_GUIDANCE.get(section.get("title"), {})
        title = section.get("title")

        if guidance.get("teaching_note"):
            prepared_section["teaching_note"] = guidance["teaching_note"]
        else:
            prepared_section["teaching_note"] = (
                f'{section.get("summary", "").strip()} '
                "Bu başlıkta amaç, listedeki kalıbı örnek cümle içinde görüp aynı mantığı kendi cümlelerinde tekrar edebilmektir."
            ).strip()

        if guidance.get("watch_out"):
            prepared_section["watch_out"] = guidance["watch_out"]
        else:
            prepared_section["watch_out"] = (
                "Örneklere bakarken önce çekimli fiili, sonra özneyi ve artikel değişimini kontrol et. "
                "Türkçedeki söz dizimini doğrudan kopyalamamaya dikkat et."
            )

        prepared_section["when_to_use"] = GRAMMAR_USAGE.get(
            title,
            "Bu başlık, dersteki örnek cümleleri gerçek kullanım bağlamına bağlamak ve kuralın nerede devreye girdiğini görmek için kullanılır.",
        )
        prepared_section["formula"] = GRAMMAR_FORMULAS.get(
            title,
            "özne + çekimli yapı + bilgi",
        )
        prepared_section["contrast"] = _build_grammar_contrast(title)

        annotated_examples = []
        for example in section.get("examples", []):
            annotated_examples.append(
                {
                    "text": example,
                    "note": _build_grammar_example_note(title, example),
                }
            )
        prepared_section["annotated_examples"] = annotated_examples

        prepared_sections.append(prepared_section)

    lesson["grammar_sections"] = prepared_sections
    return lesson


GERMAN_LESSONS = {
    "a1": [
        {
            "slug": "ders-1-selamlasma-ve-artikeller",
            "index": 1,
            "title": "Selamlaşma ve Artikeller",
            "duration": "60-75 dk",
            "difficulty": "A1.1",
            "teaser": (
                "İlk derste Almanca'nın en temel iki iskeletini kuruyoruz: "
                "selamlaşma kalıpları ve isimleri artikel ile birlikte öğrenme mantığı. "
                "Ders sonunda hem basit bir tanışma diyalogunu anlayabilecek hem de ilk temel kelime setini artikeliyle hatırlayabileceksin."
            ),
            "status": "active",
            "objectives": [
                "Almanca'da der, die ve das artikellerinin ne yaptığını kavramak.",
                "Resmî ve gayrıresmî selamlaşma arasındaki temel farkı görmek.",
                "Tanışma için gereken en temel kalıpları kullanmak.",
                "18 temel kelimeyi artikeli ve temel anlam alanlarıyla birlikte öğrenmek.",
                "Artikel, anlam ve basit cümle kurulumunda hata payını düşürmek.",
                "Bir A1 başlangıç dersinden beklenen ilk refleksi oluşturmak.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "18"},
                {"label": "Gramer odağı", "value": "Artikel + tanışma"},
                {"label": "Alıştırma", "value": "5 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Almanca'da isimler artikel ile öğrenilir",
                    "body": (
                        "Almanca'da ismi yalnız ezberlemek yerine artikel ile birlikte öğrenmek gerekir. "
                        "der Tisch, die Lampe, das Buch gibi. "
                        "Artikel, kelimenin dil bilgisel cinsiyetini gösterir ve daha sonra cümlenin geri kalanını da etkiler."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "Biyolojik cinsiyet ile her zaman aynı değildir",
                    "body": (
                        "Artikel konusu bazı kelimelerde sezgisel görünür ama her zaman tahmin edilebilir değildir. "
                        "Bu nedenle ilk dersten itibaren kelimeyi artikel ile birlikte alma alışkanlığı kurmak gerekir. "
                        "Aksi halde ileride dativ, akkusativ ve sıfat çekimlerinde sürekli dağınık kalırsın."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Selamlaşma kalıpları ezber değil, kalıp tanıma işidir",
                    "body": (
                        "Hallo, Guten Morgen, Guten Tag ve Guten Abend gibi ifadeler kelime kelime çevrilerek değil, "
                        "hazır kalıp olarak öğrenilir. "
                        "A1 seviyesinde hızlı konuşmaktan önce bu kalıpları tanımak ve doğru yerde kullanmak gerekir."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "İlk cümle iskeletleri çok kısadır",
                    "body": (
                        "Bu derste kuracağın cümleler uzun olmayacak: "
                        "Ich heiße ..., Ich bin ..., Das ist ..., Mein Name ist ... "
                        "gibi çok temel yapılarla başlıyoruz. "
                        "Kısa cümleler, doğru temeli daha hızlı kurar."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Hedef kusursuzluk değil, sağlam ilk refleks",
                    "body": (
                        "İlk derste tüm artikelleri sonsuza kadar hatırlamanı beklemiyoruz. "
                        "Ama artikeli gördüğünde şaşırmamayı, kelimeyi tek başına değil paket halinde öğrenmeyi "
                        "ve selamlaşma ile tanışmayı bir araya getirmeyi hedefliyoruz."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Temel artikel tablosu",
                    "summary": "İlk aşamada sadece tekil belirli artikelleri tanıyoruz.",
                    "items": [
                        "der -> çoğu maskulin isim",
                        "die -> çoğu feminin isim",
                        "das -> çoğu nötr isim",
                        "Her yeni isim mümkünse artikel ile birlikte öğrenilir",
                    ],
                    "examples": [
                        "der Mann = adam",
                        "die Frau = kadın",
                        "das Buch = kitap",
                    ],
                },
                {
                    "title": "Selamlaşma kalıpları",
                    "summary": "Günlük giriş seviyesi iletişimin çekirdeği bu kalıplardır.",
                    "items": [
                        "Hallo! = merhaba",
                        "Guten Morgen! = günaydın",
                        "Guten Tag! = iyi günler",
                        "Guten Abend! = iyi akşamlar",
                        "Tschüss! = hoşça kal",
                    ],
                    "examples": [
                        "Hallo, ich heiße Ece.",
                        "Guten Morgen, ich bin Ali.",
                    ],
                },
                {
                    "title": "Tanışma için en temel cümleler",
                    "summary": "Bu cümleler A1'in ilk dakikalarında sürekli kullanılır.",
                    "items": [
                        "Ich heiße ... = Benim adım ...",
                        "Ich bin ... = Ben ... / bağlama göre ad tanıtımında da kullanılabilir",
                        "Mein Name ist ... = Benim adım ...",
                        "Das ist ... = Bu ...",
                        "Wie heißt du? = Adın ne?",
                    ],
                    "examples": [
                        "Ich heiße Elif.",
                        "Mein Name ist Can.",
                        "Das ist Frau Kaya.",
                    ],
                },
                {
                    "title": "İlk derste düşülen tipik hatalar",
                    "summary": "Bu hataları erkenden fark etmek ileride büyük fayda sağlar.",
                    "items": [
                        "Kelimeyi artikelsiz ezberlemek",
                        "Hallo ile Guten Tag'i her yerde aynı sanmak",
                        "Ich heiße ve Ich bin kalıplarını karıştırmak",
                        "Bir kelimenin Türkçede tek anlamı varmış gibi düşünmek",
                    ],
                    "examples": [
                        "Doğru: der Name / yanlış çalışma: sadece Name",
                        "Doğru: Guten Morgen, ich heiße Derya.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Hallo!", "tr": "Merhaba!", "note": "En genel giriş selamlaması."},
                {"de": "Guten Morgen!", "tr": "Günaydın!", "note": "Sabah saatleri için."},
                {"de": "Guten Tag!", "tr": "İyi günler!", "note": "Gün içinde resmî ve güvenli seçim."},
                {"de": "Guten Abend!", "tr": "İyi akşamlar!", "note": "Akşam saatlerinde kullanılır."},
                {"de": "Ich heiße Zeynep.", "tr": "Benim adım Zeynep.", "note": "En temel tanışma kalıbı."},
                {"de": "Ich bin Murat.", "tr": "Ben Murat'ım.", "note": "Kimlik bildiren kısa yapı."},
                {"de": "Mein Name ist Defne.", "tr": "Benim adım Defne.", "note": "Biraz daha açık ve resmî."},
                {"de": "Das ist Frau Yilmaz.", "tr": "Bu Bayan Yilmaz.", "note": "Birini tanıtırken kullanılır."},
                {"de": "Tschüss!", "tr": "Hoşça kal!", "note": "Gayrıresmî kapanış ifadesi."},
            ],
            "common_mistakes": [
                {
                    "wrong": "Name = isim, yeter",
                    "right": "der Name = isim / ad",
                    "reason": "İsmi artikel ile öğrenmek gerekir.",
                },
                {
                    "wrong": "Hallo yerine her durumda Guten Morgen demek",
                    "right": "Saat ve bağlama göre Hallo, Guten Morgen, Guten Tag ayrımını korumak",
                    "reason": "Selamlaşma kalıpları zamana ve resmîyet derecesine göre değişir.",
                },
                {
                    "wrong": "Ich heiße ile Ich bin arasında gelişigüzel gidip gelmek",
                    "right": "İkisi de doğru olabilir; ama ilk aşamada kalıpları ayrı ayrı oturtmak",
                    "reason": "Temel yapılar erken aşamada net ayrılmazsa cümle refleksi yavaş oturur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Hallo! Ich heiße Eda. Und du?", "text_tr": "Merhaba! Benim adım Eda. Ya sen?"},
                    {"speaker": "B", "text_de": "Guten Tag! Ich bin Kerem. Mein Name ist Kerem Aydin.", "text_tr": "İyi günler! Ben Kerem'im. Benim adım Kerem Aydin."},
                    {"speaker": "A", "text_de": "Das ist Frau Demir.", "text_tr": "Bu Bayan Demir."},
                    {"speaker": "B", "text_de": "Hallo, Frau Demir!", "text_tr": "Merhaba, Bayan Demir!"},
                ],
            },
            "reading_passages": [
                {
                    "title": "İlk tanışma metni",
                    "intro": "İlk derste amaç kelimeleri tek başına değil, kısa cümle içinde görmektir.",
                    "word_focus": "8 kelime / kalıp",
                    "paragraphs": [
                        "[[Hallo::merhaba]]! Ich heiße Ada. Das ist [[der Mann::adam / erkek]] Murat und das ist [[die Frau::kadın / hanım]] Elif.",
                        "[[Der Name::isim / ad]] ist wichtig. [[Das Buch::kitap]] ist neu, die [[Lampe::lamba]] ist klein und der [[Tisch::masa]] ist groß. [[Tschüss::hoşça kal]]!",
                    ],
                },
            ],
            "tips": [
                "Kelimeleri listeden değil, sesli tekrar ederek çalış.",
                "Her kelimeyi artikel + isim olarak görmeye alış.",
                "Türkçe anlamı birden fazla ise bağlama göre değişebileceğini kabul et.",
                "Hallo, Guten Morgen ve Guten Tag ifadelerini gün içinde farklı saatlerde düşünerek tekrar et.",
                "Bir kelimeyi ezberleyemiyorsan onu önce örnek cümle içinde tekrar et.",
            ],
            "vocabulary": [
                {
                    "word": "Mann",
                    "article": "der",
                    "plural": "die Männer",
                    "meanings": ["adam", "erkek", "eş koca bağlamında koca"],
                    "example_de": "Der Mann heißt Murat.",
                    "example_tr": "Adamın adı Murat.",
                    "note": "Kişi bildiren temel maskulin örnek.",
                },
                {
                    "word": "Frau",
                    "article": "die",
                    "plural": "die Frauen",
                    "meanings": ["kadın", "hanım", "eş bağlamında eş"],
                    "example_de": "Die Frau kommt aus Berlin.",
                    "example_tr": "Kadın Berlin'den geliyor.",
                    "note": "Selamlaşma ve tanışma diyaloglarında çok sık geçer.",
                },
                {
                    "word": "Kind",
                    "article": "das",
                    "plural": "die Kinder",
                    "meanings": ["çocuk", "evlat"],
                    "example_de": "Das Kind ist ruhig.",
                    "example_tr": "Çocuk sakin.",
                    "note": "Nötr isimler için iyi bir ilk örnek.",
                },
                {
                    "word": "Name",
                    "article": "der",
                    "plural": "die Namen",
                    "meanings": ["isim", "ad"],
                    "example_de": "Mein Name ist Deniz.",
                    "example_tr": "Benim adım Deniz.",
                    "note": "Tanışma kalıplarıyla birlikte öğrenilmelidir.",
                },
                {
                    "word": "Buch",
                    "article": "das",
                    "plural": "die Bücher",
                    "meanings": ["kitap", "eser"],
                    "example_de": "Das Buch ist neu.",
                    "example_tr": "Kitap yeni.",
                    "note": "Nesne isimlerinde nötr artikel örneği.",
                },
                {
                    "word": "Lampe",
                    "article": "die",
                    "plural": "die Lampen",
                    "meanings": ["lamba", "aydınlatma lambası"],
                    "example_de": "Die Lampe ist klein.",
                    "example_tr": "Lamba küçük.",
                    "note": "Basit ev eşyaları kelime grubuna giriş sağlar.",
                },
                {
                    "word": "Tisch",
                    "article": "der",
                    "plural": "die Tische",
                    "meanings": ["masa", "sıra masa bağlamında sıra"],
                    "example_de": "Der Tisch ist groß.",
                    "example_tr": "Masa büyük.",
                    "note": "Sınıf ve ev eşyalarında çok kullanılır.",
                },
                {
                    "word": "Stuhl",
                    "article": "der",
                    "plural": "die Stühle",
                    "meanings": ["sandalye", "koltuk benzeri oturak bağlamında oturak"],
                    "example_de": "Der Stuhl ist alt.",
                    "example_tr": "Sandalye eski.",
                    "note": "Tisch ile beraber erken dönem eşleştirme kelimesidir.",
                },
                {
                    "word": "Haus",
                    "article": "das",
                    "plural": "die Häuser",
                    "meanings": ["ev", "konut", "bina bağlamında ev yapısı"],
                    "example_de": "Das Haus ist neu.",
                    "example_tr": "Ev yeni.",
                    "note": "Temel gündelik kelime; nötr isim kalıbı için faydalı.",
                },
                {
                    "word": "Schule",
                    "article": "die",
                    "plural": "die Schulen",
                    "meanings": ["okul", "eğitim kurumu"],
                    "example_de": "Die Schule ist groß.",
                    "example_tr": "Okul büyük.",
                    "note": "A1 kelime dünyasının merkez kelimelerinden biridir.",
                },
                {
                    "word": "Lehrer",
                    "article": "der",
                    "plural": "die Lehrer",
                    "meanings": ["öğretmen", "erkek öğretmen"],
                    "example_de": "Der Lehrer heißt Arda.",
                    "example_tr": "Öğretmenin adı Arda.",
                    "note": "Meslek kelimelerine giriş için temel örnek.",
                },
                {
                    "word": "Lehrerin",
                    "article": "die",
                    "plural": "die Lehrerinnen",
                    "meanings": ["öğretmen", "kadın öğretmen"],
                    "example_de": "Die Lehrerin kommt aus Bonn.",
                    "example_tr": "Öğretmen Bonn'dan geliyor.",
                    "note": "Erken aşamada eril-dişil meslek çiftleri faydalıdır.",
                },
                {
                    "word": "Freund",
                    "article": "der",
                    "plural": "die Freunde",
                    "meanings": ["erkek arkadaş", "dost", "arkadaş"],
                    "example_de": "Das ist mein Freund.",
                    "example_tr": "Bu benim arkadaşım.",
                    "note": "Bağlama göre romantik ya da genel arkadaş anlamına gelebilir.",
                },
                {
                    "word": "Freundin",
                    "article": "die",
                    "plural": "die Freundinnen",
                    "meanings": ["kadın arkadaş", "dost", "kız arkadaş"],
                    "example_de": "Das ist meine Freundin.",
                    "example_tr": "Bu benim arkadaşım.",
                    "note": "Türkçe karşılığı bağlama göre değişir.",
                },
                {
                    "word": "Stadt",
                    "article": "die",
                    "plural": "die Städte",
                    "meanings": ["şehir", "kent"],
                    "example_de": "Die Stadt ist klein.",
                    "example_tr": "Şehir küçük.",
                    "note": "Nereden geldiğini söylerken sık geçen bir isimdir.",
                },
                {
                    "word": "Tag",
                    "article": "der",
                    "plural": "die Tage",
                    "meanings": ["gün", "gündüz bağlamında gün"],
                    "example_de": "Guten Tag!",
                    "example_tr": "İyi günler!",
                    "note": "Selamlaşma kalıbının içindeki ismi fark ettirir.",
                },
                {
                    "word": "Morgen",
                    "article": "der",
                    "plural": "die Morgen",
                    "meanings": ["sabah", "ertesi gün bağlamında yarın edebî kullanımlar"],
                    "example_de": "Guten Morgen!",
                    "example_tr": "Günaydın!",
                    "note": "İlk derste kalıp olarak öğrenilir.",
                },
                {
                    "word": "Abend",
                    "article": "der",
                    "plural": "die Abende",
                    "meanings": ["akşam", "gece başlangıcı"],
                    "example_de": "Guten Abend!",
                    "example_tr": "İyi akşamlar!",
                    "note": "Zaman bildiren isimler kelime dairesini büyütür.",
                },
            ],
            "exercises": [
                {
                    "id": "articles",
                    "type": "single_choice",
                    "title": "Artikel Testi",
                    "description": "Kelimenin doğru artikelini seç.",
                    "questions": [
                        {
                            "prompt": "___ Frau",
                            "options": ["der", "die", "das"],
                            "correct_index": 1,
                            "explanation": "Frau feminin bir isimdir, bu yüzden die alır.",
                        },
                        {
                            "prompt": "___ Buch",
                            "options": ["der", "die", "das"],
                            "correct_index": 2,
                            "explanation": "Buch nötr isimdir ve das ile kullanılır.",
                        },
                        {
                            "prompt": "___ Name",
                            "options": ["der", "die", "das"],
                            "correct_index": 0,
                            "explanation": "Name maskulin örnektir; der Name şeklinde öğrenilir.",
                        },
                        {
                            "prompt": "___ Schule",
                            "options": ["der", "die", "das"],
                            "correct_index": 1,
                            "explanation": "Schule feminin isimdir ve die ile gelir.",
                        },
                        {
                            "prompt": "___ Haus",
                            "options": ["der", "die", "das"],
                            "correct_index": 2,
                            "explanation": "Haus nötr isimdir; das Haus şeklinde öğrenilir.",
                        },
                        {
                            "prompt": "___ Lehrer",
                            "options": ["der", "die", "das"],
                            "correct_index": 0,
                            "explanation": "Lehrer için temel kalıp der Lehrer'dir.",
                        },
                    ],
                },
                {
                    "id": "meanings",
                    "type": "single_choice",
                    "title": "Anlam Testi",
                    "description": "Kelimenin bağlama uygun anlam grubunu seç.",
                    "questions": [
                        {
                            "prompt": "das Kind",
                            "options": [
                                "çocuk, evlat",
                                "kadın, hanım",
                                "isim, ad",
                            ],
                            "correct_index": 0,
                            "explanation": "Kind temel olarak çocuk demektir; bazı bağlamlarda evlat anlamı da taşır.",
                        },
                        {
                            "prompt": "die Lampe",
                            "options": [
                                "masa, sıra",
                                "lamba, aydınlatma lambası",
                                "erkek, adam",
                            ],
                            "correct_index": 1,
                            "explanation": "Lampe ev ve sınıf eşyaları içinde geçen bir isimdir.",
                        },
                        {
                            "prompt": "der Mann",
                            "options": [
                                "adam, erkek, koca",
                                "çocuk, genç",
                                "isim, kimlik",
                            ],
                            "correct_index": 0,
                            "explanation": "Mann bağlama göre adam, erkek ya da koca anlamı taşıyabilir.",
                        },
                        {
                            "prompt": "die Freundin",
                            "options": [
                                "kadın arkadaş, dost, kız arkadaş",
                                "öğretmen, eğitmen",
                                "sandalye, oturak",
                            ],
                            "correct_index": 0,
                            "explanation": "Freundin bağlama göre arkadaş veya kız arkadaş anlamına gelebilir.",
                        },
                        {
                            "prompt": "der Tag",
                            "options": [
                                "akşam, gece",
                                "gün, gündüz bağlamında gün",
                                "şehir, kent",
                            ],
                            "correct_index": 1,
                            "explanation": "Tag temel olarak gün demektir; Guten Tag kalıbında da bunu görürsün.",
                        },
                        {
                            "prompt": "die Stadt",
                            "options": [
                                "isim, ad",
                                "okul, eğitim kurumu",
                                "şehir, kent",
                            ],
                            "correct_index": 2,
                            "explanation": "Stadt şehir anlamına gelir; kent karşılığı da uygun olabilir.",
                        },
                    ],
                },
                {
                    "id": "grammar-gaps",
                    "type": "single_choice",
                    "title": "Boşluk Doldurma",
                    "description": "Cümlede boşluğu doğru kelime veya yapıyla tamamla.",
                    "questions": [
                        {
                            "prompt": "Guten Morgen, ich ___ Zeynep.",
                            "options": ["heiße", "kommt", "bist"],
                            "correct_index": 0,
                            "explanation": "Kendi adını söylerken ich heiße kalıbı kullanılır.",
                        },
                        {
                            "prompt": "___ Mann ist Lehrer.",
                            "options": ["Das", "Der", "Die"],
                            "correct_index": 1,
                            "explanation": "Mann kelimesi der ile öğrenilir.",
                        },
                        {
                            "prompt": "Das Buch ist ___.",
                            "options": ["neu", "Name", "Hallo"],
                            "correct_index": 0,
                            "explanation": "Cümlede sıfat gerekir; neu burada doğru tamamlamadır.",
                        },
                        {
                            "prompt": "Guten ___!",
                            "options": ["Frau", "Morgen", "Name"],
                            "correct_index": 1,
                            "explanation": "Guten Morgen kalıbı sabah kullanılır.",
                        },
                        {
                            "prompt": "Mein ___ ist Selin.",
                            "options": ["Lampe", "Name", "Abend"],
                            "correct_index": 1,
                            "explanation": "Kendini tanıtırken Mein Name ist ... kalıbı kurulur.",
                        },
                        {
                            "prompt": "Das ist ___ Lehrerin.",
                            "options": ["die", "der", "das"],
                            "correct_index": 0,
                            "explanation": "Lehrerin feminin olduğu için die alır.",
                        },
                    ],
                },
                {
                    "id": "greetings",
                    "type": "single_choice",
                    "title": "Selamlaşma Seçimi",
                    "description": "Bağlama en uygun kalıbı seç.",
                    "questions": [
                        {
                            "prompt": "Sabah birine selam veriyorsun.",
                            "options": ["Guten Abend!", "Guten Morgen!", "Tschüss!"],
                            "correct_index": 1,
                            "explanation": "Sabah için en uygun kalıp Guten Morgen'dir.",
                        },
                        {
                            "prompt": "Akşam ayrılırken hangisi daha uygun?",
                            "options": ["Tschüss!", "Das ist ...", "Mein Name ist ..."],
                            "correct_index": 0,
                            "explanation": "Tschüss ayrılırken kullanılan basit kapanış ifadesidir.",
                        },
                        {
                            "prompt": "Resmî ve güvenli gün ortası selamlaması hangisi?",
                            "options": ["Hallo!", "Guten Tag!", "Ich bin ..."],
                            "correct_index": 1,
                            "explanation": "Guten Tag daha resmî ve güvenli bir seçimdir.",
                        },
                        {
                            "prompt": "Birini tanıtırken hangi kalıp kullanılır?",
                            "options": ["Das ist ...", "Guten Morgen!", "Ich heiße ..."],
                            "correct_index": 0,
                            "explanation": "Bir başkasını göstermek ve tanıtmak için Das ist ... kalıbı kullanılır.",
                        },
                    ],
                },
                {
                    "id": "lesson-review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Dersin temel mantığını toplu olarak yokla.",
                    "questions": [
                        {
                            "prompt": "En doğru çalışma alışkanlığı hangisi?",
                            "options": [
                                "Kelimeyi sadece Türkçe karşılığıyla ezberlemek",
                                "Kelimeyi artikel ile birlikte öğrenmek",
                                "İlk derste artikelleri tamamen görmezden gelmek",
                            ],
                            "correct_index": 1,
                            "explanation": "Bu dersin ana hedefi kelimeyi artikel ile paket olarak öğrenmektir.",
                        },
                        {
                            "prompt": "Hangisi tanışma cümlesidir?",
                            "options": ["Mein Name ist Ela.", "Guten Abend?", "Der Buch."],
                            "correct_index": 0,
                            "explanation": "Mein Name ist ... doğrudan tanışma için kullanılır.",
                        },
                        {
                            "prompt": "Hangisi nötr artikel örneğidir?",
                            "options": ["die Frau", "das Haus", "der Lehrer"],
                            "correct_index": 1,
                            "explanation": "Haus nötr isimdir; das Haus şeklinde kullanılır.",
                        },
                        {
                            "prompt": "İlk derste en doğru hedef hangisidir?",
                            "options": [
                                "Hemen uzun paragraf yazmak",
                                "Tüm grameri bitirmek",
                                "Doğru temel kalıpları tanımak ve tekrar etmek",
                            ],
                            "correct_index": 2,
                            "explanation": "A1 başlangıç dersinde hedef sağlam refleks kurmaktır.",
                        },
                    ],
                },
            ],
            "homework": [
                "Kelime listesinden 10 kelime seç ve her birini artikel ile birlikte sesli tekrar et.",
                "Hallo, Guten Morgen, Guten Tag, Guten Abend kalıplarını günün farklı saatleriyle eşleştir.",
                "Kendini üç farklı şekilde tanıt: Ich heiße ..., Ich bin ..., Mein Name ist ...",
                "Üç kişiyi Das ist ... kalıbıyla tanıtan mini cümleler yaz.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde hedefin tüm kelimeleri kusursuz ezberlemek değil; "
                "artikel mantığını duymaya, temel tanışma kalıplarını tanımaya ve kelimeyi paket halinde öğrenmeye başlamaktır."
            ),
            "next_lesson": {
                "title": "Ders 2: Kişi zamirleri ve sein fiili",
                "status": "active",
                "slug": "ders-2-kisi-zamirleri-ve-sein-fiili",
            },
        },
        {
            "slug": "ders-2-kisi-zamirleri-ve-sein-fiili",
            "index": 2,
            "title": "Kişi Zamirleri ve sein Fiili",
            "duration": "60-75 dk",
            "difficulty": "A1.1",
            "teaser": (
                "Bu derste Almanca'nın en merkezi fiillerinden biri olan sein ile tanışıyoruz. "
                "Ben, sen, o, biz, siz ve onlar gibi kişi zamirlerini görüp en temel tanıtım ve kimlik cümlelerini kurmaya başlıyoruz."
            ),
            "status": "active",
            "objectives": [
                "ich, du, er, sie, es, wir, ihr, sie ve Sie zamirlerini tanımak.",
                "sein fiilinin temel çekimini öğrenmek.",
                "Ich bin ..., Du bist ..., Er ist ... gibi cümleleri doğru kurmak.",
                "Basit kimlik, meslek ve nereli olma cümlelerini okumak ve tamamlamak.",
                "Kişi zamiri ile fiil uyumunu erken aşamada oturtmak.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "16"},
                {"label": "Gramer odağı", "value": "Kişi zamiri + sein"},
                {"label": "Alıştırma", "value": "5 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Kişi zamiri cümlenin omurgasıdır",
                    "body": (
                        "Almanca'da özneyi doğru seçmek fiili de doğru seçmek demektir. "
                        "ich, du, er, sie, es gibi zamirler daha ilk seviyeden itibaren cümle kurulumunun merkezindedir."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "sein fiili çok erken öğrenilir",
                    "body": (
                        "sein fiili olmak anlamına gelir ve A1 seviyesinde kimlik, meslek, milliyet, şehir ve kısa tanıtım cümlelerinde sürekli kullanılır. "
                        "Bu nedenle ezber değil, refleks haline gelmesi gerekir."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Zamir değişince fiil de değişir",
                    "body": (
                        "Ich bin, du bist, er ist, wir sind... "
                        "Bu değişim ilk bakışta ezber gibi gelir ama çok tekrar edilince otomatikleşir. "
                        "Buradaki hedef tek tek kuralı değil, ses kalıbını tanımaktır."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Resmî ve gayrıresmî hitap ayrımı burada başlar",
                    "body": (
                        "du gayrıresmî hitapta, Sie ise resmî hitapta kullanılır. "
                        "A1 seviyesinde bu ayrımı fark etmek yeterlidir; ayrıntılı kullanım daha sonra gelir."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Kısa ama doğru cümleler kuruyoruz",
                    "body": (
                        "Bu derste Ich bin Student., Du bist müde., Wir sind hier. gibi kısa cümleler kuracağız. "
                        "Uzun cümlelerden önce doğru uyum daha önemlidir."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Kişi zamirleri",
                    "summary": "İlk aşamada özneyi görmek ve cümlede ayırt etmek yeterlidir.",
                    "items": [
                        "ich = ben",
                        "du = sen",
                        "er = o (erkek)",
                        "sie = o (kadın)",
                        "es = o (nötr / cansız / genel durum)",
                        "wir = biz",
                        "ihr = siz (gayrıresmî çoğul)",
                        "sie = onlar",
                        "Sie = Siz (resmî hitap)",
                    ],
                    "examples": [
                        "Ich bin Lara.",
                        "Du bist Emir.",
                        "Es ist gut.",
                        "Wir sind hier.",
                        "Sie sind Herr Demir.",
                    ],
                },
                {
                    "title": "sein fiili çekimi",
                    "summary": "Bu çekim tablosu A1'in en temel ezberlerinden biridir.",
                    "items": [
                        "ich bin",
                        "du bist",
                        "er ist",
                        "sie ist",
                        "es ist",
                        "wir sind",
                        "ihr seid",
                        "sie sind",
                        "Sie sind",
                    ],
                    "examples": [
                        "Ich bin Student.",
                        "Du bist müde.",
                        "Sie ist Studentin.",
                        "Es ist gut.",
                        "Ihr seid hier.",
                        "Sie sind Lehrerin.",
                    ],
                },
                {
                    "title": "Temel cümle kalıpları",
                    "summary": "sein fiili ile ilk anlamlı cümleler burada kurulur.",
                    "items": [
                        "Ich bin ... = Ben ...",
                        "Du bist ... = Sen ...",
                        "Er ist ... = O ...",
                        "Sie ist ... = O ...",
                        "Es ist ... = Bu / O ...",
                        "Wir sind ... = Biz ...",
                        "Ihr seid ... = Siz ...",
                        "sie sind ... = Onlar ...",
                        "Sie sind ... = Siz ...",
                    ],
                    "examples": [
                        "Ich bin in Berlin.",
                        "Sie ist Studentin.",
                        "Es ist gut.",
                        "Er ist Lehrer.",
                        "Wir sind Freunde.",
                        "Ihr seid müde.",
                    ],
                },
                {
                    "title": "Kısa hâl-hatır kalıpları",
                    "summary": "Erken A1 akışında Wie geht's? hattını da net biçimde oturtuyoruz.",
                    "items": [
                        "Wie geht es dir? = Nasılsın?",
                        "Wie geht es Ihnen? = Nasılsınız?",
                        "Mir geht es gut. = İyiyim.",
                        "Mir geht es sehr gut. = Çok iyiyim.",
                        "Es geht so. = İdare eder.",
                        "Mir geht es nicht gut. = İyi değilim.",
                    ],
                    "examples": [
                        "Hallo, wie geht es dir?",
                        "Danke, mir geht es gut.",
                        "Heute geht es mir nicht so gut.",
                    ],
                },
                {
                    "title": "İlk dersten farkı ne?",
                    "summary": "İlk derste isim ve selamlaşma gördük; burada cümle omurgası kuruyoruz.",
                    "items": [
                        "Artikeller isimle ilgilidir",
                        "Kişi zamirleri özneyle ilgilidir",
                        "sein fiili zamire göre şekil değiştirir",
                        "Bu ders tanıtım cümlelerini bir adım ileri taşır",
                    ],
                    "examples": [
                        "Ich bin Ece.",
                        "Das ist Ece. Sie ist Studentin.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Ich bin Ali.", "tr": "Ben Ali'yim.", "note": "En temel kendini tanıtma kalıbı."},
                {"de": "Du bist sehr nett.", "tr": "Sen çok naziksin.", "note": "du ile kurulan basit cümle."},
                {"de": "Er ist Lehrer.", "tr": "O öğretmen.", "note": "Erkek özne ile meslek bildirme."},
                {"de": "Sie ist Studentin.", "tr": "O öğrenci.", "note": "Kadın özne ile temel cümle."},
                {"de": "Es ist gut.", "tr": "Bu iyi.", "note": "Genel durum veya nötr referans için."},
                {"de": "Wir sind hier.", "tr": "Biz buradayız.", "note": "wir ile ilk toplu cümle."},
                {"de": "Ihr seid müde.", "tr": "Siz yorgunsunuz.", "note": "ihr ile gayrıresmî çoğul kullanım."},
                {"de": "Sie sind in Ankara.", "tr": "Onlar Ankara'da.", "note": "Küçük harfli sie = onlar kullanımını gösterir."},
                {"de": "Sie sind Herr Kaya, richtig?", "tr": "Siz Bay Kaya'sınız, değil mi?", "note": "Büyük harfli Sie resmî hitap olabilir."},
                {"de": "Wie geht es dir?", "tr": "Nasılsın?", "note": "Gayrıresmî hâl-hatır sorusu."},
                {"de": "Wie geht es Ihnen?", "tr": "Nasılsınız?", "note": "Resmî hâl-hatır sorusu."},
                {"de": "Mir geht es gut.", "tr": "İyiyim.", "note": "En temel olumlu cevap."},
                {"de": "Es geht so.", "tr": "İdare eder.", "note": "Nötr durum bildirimi."},
            ],
            "common_mistakes": [
                {
                    "wrong": "du bin / ich bist demek",
                    "right": "ich bin, du bist",
                    "reason": "sein fiili özneye göre değişir; zamir-fiil uyumu çok erken oturmalıdır.",
                },
                {
                    "wrong": "sie gördüğünde her zaman yalnızca 'o kadın' anlamını vermek",
                    "right": "sie bazen 'o kadın', bazen 'onlar'; Sie ise resmî 'siz' olabilir",
                    "reason": "Anlam bağlamdan çıkar; ilk seviyede bu çok önemli bir farktır.",
                },
                {
                    "wrong": "Cümleyi sadece kelime yığınına çevirmek",
                    "right": "Önce özne + sein + tamamlayıcı iskeletini koru",
                    "reason": "Almanca'da doğru omurga erken kurulduğunda diğer konular çok daha rahat oturur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Hallo, ich bin Dila. Wer bist du?", "text_tr": "Merhaba, ben Dila'yım. Sen kimsin?"},
                    {"speaker": "B", "text_de": "Ich bin Kerem. Ich bin Student.", "text_tr": "Ben Kerem'im. Öğrenciyim."},
                    {"speaker": "A", "text_de": "Das ist Elif. Sie ist Lehrerin.", "text_tr": "Bu Elif. O öğretmen."},
                    {"speaker": "B", "text_de": "Wir sind aus Izmir.", "text_tr": "Biz İzmirliyiz / İzmir'deniz."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Kimlik ve durum metni",
                    "intro": "Burada ilk dersin isimlerini, bu derste gördüğün zamir ve sein kalıplarıyla birleştiriyoruz.",
                    "word_focus": "10 kelime / kalıp",
                    "paragraphs": [
                        "[[Hallo::merhaba]], ich bin Dila. Ich bin [[Studentin::kadın öğrenci]] und das ist mein [[Freund::arkadaş / erkek arkadaş]] Kerem. Er ist [[Lehrer::öğretmen]].",
                        "[[Wir::biz]] sind in [[Berlin::Berlin]] und [[Herr::Bay / Bey]] Acar ist auch hier. Meine [[Freundin::arkadaş / kız arkadaş]] Elif ist nicht [[müde::yorgun]].",
                    ],
                },
            ],
            "tips": [
                "sein fiilini tablo gibi ezberlemek yerine sesli bloklar halinde tekrar et: ich bin, du bist, er ist...",
                "Her zamiri ayrı renk veya işaretle çalışmak başlangıçta yardımcı olabilir.",
                "Kısa cümleler kur ve özneyi değiştirince fiilin de değiştiğini fark et.",
                "sie ve Sie ayrımını yazıda büyük harf üzerinden fark etmeye başla.",
            ],
            "vocabulary": [
                {
                    "word": "Student",
                    "article": "der",
                    "plural": "die Studenten",
                    "meanings": ["öğrenci", "üniversite öğrencisi"],
                    "example_de": "Ich bin Student.",
                    "example_tr": "Ben öğrenciyim.",
                    "note": "sein fiili ile çok kolay kullanılır.",
                },
                {
                    "word": "Studentin",
                    "article": "die",
                    "plural": "die Studentinnen",
                    "meanings": ["öğrenci", "kadın öğrenci"],
                    "example_de": "Sie ist Studentin.",
                    "example_tr": "O öğrenci.",
                    "note": "Meslek ve rol isimlerinde cinsiyet farkı için ilk örneklerden biridir.",
                },
                {
                    "word": "Lehrer",
                    "article": "der",
                    "plural": "die Lehrer",
                    "meanings": ["öğretmen", "erkek öğretmen"],
                    "example_de": "Er ist Lehrer.",
                    "example_tr": "O öğretmen.",
                    "note": "Meslek bildirimi için temel kelime.",
                },
                {
                    "word": "Lehrerin",
                    "article": "die",
                    "plural": "die Lehrerinnen",
                    "meanings": ["öğretmen", "kadın öğretmen"],
                    "example_de": "Sie ist Lehrerin.",
                    "example_tr": "O öğretmen.",
                    "note": "sein fiiliyle birlikte çok doğal kullanılır.",
                },
                {
                    "word": "Freund",
                    "article": "der",
                    "plural": "die Freunde",
                    "meanings": ["arkadaş", "dost", "erkek arkadaş"],
                    "example_de": "Er ist mein Freund.",
                    "example_tr": "O benim arkadaşım.",
                    "note": "Bağlama göre farklı yakınlık dereceleri taşır.",
                },
                {
                    "word": "Freundin",
                    "article": "die",
                    "plural": "die Freundinnen",
                    "meanings": ["arkadaş", "dost", "kız arkadaş"],
                    "example_de": "Sie ist meine Freundin.",
                    "example_tr": "O benim arkadaşım.",
                    "note": "Türkçede tek kelimeye düşse de Almanca'da bağlam güçlüdür.",
                },
                {
                    "word": "Arzt",
                    "article": "der",
                    "plural": "die Ärzte",
                    "meanings": ["doktor", "hekim"],
                    "example_de": "Er ist Arzt.",
                    "example_tr": "O doktordur.",
                    "note": "Meslek kategorisine yeni bir örnek.",
                },
                {
                    "word": "Ärztin",
                    "article": "die",
                    "plural": "die Ärztinnen",
                    "meanings": ["doktor", "kadın doktor"],
                    "example_de": "Sie ist Ärztin.",
                    "example_tr": "O doktordur.",
                    "note": "Umlautlu çoğul ve meslek çiftleri için yararlıdır.",
                },
                {
                    "word": "müde",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["yorgun", "bitkin"],
                    "example_de": "Ich bin müde.",
                    "example_tr": "Ben yorgunum.",
                    "note": "Bu bir isim değil, sıfat; sein fiili ile çok kullanılır.",
                },
                {
                    "word": "hier",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["burada", "buraya yakın noktada"],
                    "example_de": "Wir sind hier.",
                    "example_tr": "Biz buradayız.",
                    "note": "Yer bildiren temel zarflardan biri.",
                },
                {
                    "word": "aus",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["-den", "-dan", "köken olarak -li"],
                    "example_de": "Ich bin aus Ankara.",
                    "example_tr": "Ben Ankara'danım.",
                    "note": "Nereli olduğunu söylemeye başlangıç verir.",
                },
                {
                    "word": "Deutschland",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["Almanya"],
                    "example_de": "Er ist aus Deutschland.",
                    "example_tr": "O Almanya'dan.",
                    "note": "Ülke isimleriyle ilk temas için.",
                },
                {
                    "word": "Ankara",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["Ankara"],
                    "example_de": "Wir sind in Ankara.",
                    "example_tr": "Biz Ankara'dayız.",
                    "note": "Şehir ismiyle basit yer cümlesi kurulur.",
                },
                {
                    "word": "Berlin",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["Berlin"],
                    "example_de": "Sie ist in Berlin.",
                    "example_tr": "O Berlin'de.",
                    "note": "Yer belirten örnek cümleler için güzel bir şehir adı.",
                },
                {
                    "word": "Herr",
                    "article": "der",
                    "plural": "die Herren",
                    "meanings": ["bay", "bey"],
                    "example_de": "Sie sind Herr Demir.",
                    "example_tr": "Siz Bay Demir'siniz.",
                    "note": "Resmî hitapta kullanılır.",
                },
                {
                    "word": "Frau",
                    "article": "die",
                    "plural": "die Frauen",
                    "meanings": ["bayan", "kadın", "hanım"],
                    "example_de": "Sie sind Frau Kaya.",
                    "example_tr": "Siz Bayan Kaya'siniz.",
                    "note": "Resmî ve genel kullanımda çok geçen kelime.",
                },
            ],
            "exercises": [
                {
                    "id": "pronouns",
                    "type": "single_choice",
                    "title": "Kişi Zamiri Testi",
                    "description": "Bağlama uygun zamiri seç.",
                    "questions": [
                        {
                            "prompt": "Ben öğrenciyim. -> ___ bin Student.",
                            "options": ["Ich", "Du", "Wir"],
                            "correct_index": 0,
                            "explanation": "Birinci tekil kişi için ich kullanılır.",
                        },
                        {
                            "prompt": "O erkek öğretmen. -> ___ ist Lehrer.",
                            "options": ["Sie", "Er", "Es"],
                            "correct_index": 1,
                            "explanation": "Er erkek özne için kullanılır.",
                        },
                        {
                            "prompt": "Biz buradayız. -> ___ sind hier.",
                            "options": ["Ihr", "Wir", "Sie"],
                            "correct_index": 1,
                            "explanation": "Birinci çoğul kişi wir'dir.",
                        },
                        {
                            "prompt": "Siz yorgunsunuz. -> ___ seid müde.",
                            "options": ["Ihr", "Du", "Sie"],
                            "correct_index": 0,
                            "explanation": "Gayrıresmî çoğul siz için ihr kullanılır.",
                        },
                        {
                            "prompt": "Onlar Berlin'de. -> ___ sind in Berlin.",
                            "options": ["Sie", "sie", "es"],
                            "correct_index": 1,
                            "explanation": "Onlar anlamı küçük harfli sie ile kurulur.",
                        },
                    ],
                },
                {
                    "id": "sein",
                    "type": "single_choice",
                    "title": "sein Fiili Testi",
                    "description": "Doğru çekimi seç.",
                    "questions": [
                        {
                            "prompt": "Ich ___ aus Ankara.",
                            "options": ["bist", "bin", "seid"],
                            "correct_index": 1,
                            "explanation": "ich ile bin gelir.",
                        },
                        {
                            "prompt": "Du ___ sehr nett.",
                            "options": ["bist", "bin", "ist"],
                            "correct_index": 0,
                            "explanation": "du ile bist kullanılır.",
                        },
                        {
                            "prompt": "Er ___ Arzt.",
                            "options": ["seid", "sind", "ist"],
                            "correct_index": 2,
                            "explanation": "er ile ist kullanılır.",
                        },
                        {
                            "prompt": "Wir ___ hier.",
                            "options": ["sind", "seid", "ist"],
                            "correct_index": 0,
                            "explanation": "wir ile sind gelir.",
                        },
                        {
                            "prompt": "Ihr ___ in Berlin.",
                            "options": ["bist", "seid", "sind"],
                            "correct_index": 1,
                            "explanation": "ihr ile seid kullanılır.",
                        },
                        {
                            "prompt": "Sie ___ Frau Demir.",
                            "options": ["sind", "ist", "bin"],
                            "correct_index": 0,
                            "explanation": "Resmî hitapta Sie ile sind kullanılır.",
                        },
                    ],
                },
                {
                    "id": "meaning",
                    "type": "single_choice",
                    "title": "Kelime Anlamı Testi",
                    "description": "Kelimenin en uygun anlam grubunu seç.",
                    "questions": [
                        {
                            "prompt": "der Arzt",
                            "options": ["doktor, hekim", "öğrenci, talebe", "arkadaş, dost"],
                            "correct_index": 0,
                            "explanation": "Arzt doktor ya da hekim anlamına gelir.",
                        },
                        {
                            "prompt": "die Studentin",
                            "options": ["kadın öğrenci", "kadın öğretmen", "hanım doktor"],
                            "correct_index": 0,
                            "explanation": "Studentin kadın öğrenci demektir.",
                        },
                        {
                            "prompt": "müde",
                            "options": ["yorgun, bitkin", "genç, yeni", "burada, şimdi"],
                            "correct_index": 0,
                            "explanation": "müde sıfat olarak yorgun anlamına gelir.",
                        },
                        {
                            "prompt": "aus",
                            "options": ["ile", "-den / -dan", "için"],
                            "correct_index": 1,
                            "explanation": "aus temel olarak bir yerden gelmeyi belirtir.",
                        },
                        {
                            "prompt": "Herr",
                            "options": ["bay, bey", "öğretmen", "erkek çocuk"],
                            "correct_index": 0,
                            "explanation": "Herr resmî hitapta bay / bey anlamındadır.",
                        },
                    ],
                },
                {
                    "id": "gaps",
                    "type": "single_choice",
                    "title": "Boşluk Doldurma",
                    "description": "Cümledeki boşluğu en uygun seçenekle tamamla.",
                    "questions": [
                        {
                            "prompt": "Ich ___ Lara.",
                            "options": ["ist", "bin", "seid"],
                            "correct_index": 1,
                            "explanation": "Ich bin Lara en temel tanıtım cümlesidir.",
                        },
                        {
                            "prompt": "Das ist Elif. ___ ist Studentin.",
                            "options": ["Er", "Sie", "Wir"],
                            "correct_index": 1,
                            "explanation": "Elif kadın olduğu için sie kullanılır.",
                        },
                        {
                            "prompt": "Wir ___ Freunde.",
                            "options": ["sind", "bin", "bist"],
                            "correct_index": 0,
                            "explanation": "wir ile sind gelir.",
                        },
                        {
                            "prompt": "Du bist ___ Berlin.",
                            "options": ["aus", "ich", "das"],
                            "correct_index": 0,
                            "explanation": "Bir yerden olma veya gelme için aus kullanılır.",
                        },
                        {
                            "prompt": "Sie ___ Herr Acar, richtig?",
                            "options": ["ist", "bin", "sind"],
                            "correct_index": 2,
                            "explanation": "Resmî hitap Sie olduğunda sind kullanılır.",
                        },
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Zamir + sein mantığını toplu olarak test et.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Du bin Ali.", "Du bist Ali.", "Du seid Ali."],
                            "correct_index": 1,
                            "explanation": "du ile bist kullanılır.",
                        },
                        {
                            "prompt": "Hangisi resmî hitap olabilir?",
                            "options": ["Sie sind Frau Kaya.", "Sie bist Frau Kaya.", "Ihr sind Frau Kaya."],
                            "correct_index": 0,
                            "explanation": "Resmî Sie ile sind gelir.",
                        },
                        {
                            "prompt": "Hangisi bir yer bildiren doğru cümledir?",
                            "options": ["Wir sind in Ankara.", "Wir ist in Ankara.", "Wir bin in Ankara."],
                            "correct_index": 0,
                            "explanation": "wir ile sind kullanılır.",
                        },
                        {
                            "prompt": "sein fiilinin ich çekimi hangisi?",
                            "options": ["bin", "bist", "ist"],
                            "correct_index": 0,
                            "explanation": "ich bin temel cekimdir.",
                        },
                        {
                            "prompt": "Hangisi en doğru ders hedefidir?",
                            "options": [
                                "Tüm fiilleri bu derste bitirmek",
                                "Kişi zamiri ile sein fiili uyumunu oturtmak",
                                "Uzun akademik metin yazmak",
                            ],
                            "correct_index": 1,
                            "explanation": "Bu dersin ana odağı zamir-fiil uyumudur.",
                        },
                    ],
                },
            ],
            "homework": [
                "sein fiili çekimini günde en az 3 kez sesli tekrar et: ich bin, du bist, er ist...",
                "Kendinle ilgili 5 mini cümle kur: adın, şehrin, mesleğin veya rolün.",
                "3 kişi seç ve onlar için Er ist ..., Sie ist ..., Sie sind ... cümleleri yaz.",
                "du ve Sie farkını bir cümle çiftiyle göster.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde hedefin sein fiilini tüm ayrıntılarıyla bitirmek değil; "
                "kişi zamiri ile fiil uyumunu tanımak, kısa kimlik cümlelerini doğru kurmak ve "
                "A1'in ilk gerçek cümle omurgasını oturtmaktır."
            ),
            "next_lesson": {
                "title": "Ders 3: Sayılar, ülkeler ve milliyetler",
                "status": "active",
                "slug": "ders-3-sayilar-ulkeler-ve-milliyetler",
            },
        },
        {
            "slug": "ders-3-sayilar-ulkeler-ve-milliyetler",
            "index": 3,
            "title": "Sayılar, Ülkeler ve Milliyetler",
            "duration": "70-85 dk",
            "difficulty": "A1.1",
            "teaser": (
                "Bu derste 0'dan 20'ye kadar temel sayıları, yaş sormayı, nereli olduğunu söylemeyi "
                "ve ilk milliyet kalıplarını birlikte kuruyoruz. Ders sonunda yaş, ülke, şehir ve milliyet "
                "bilgisiyle daha dolu bir tanışma cümlesi kurabileceksin."
            ),
            "status": "active",
            "objectives": [
                "0-20 arası temel sayıları doğru tanımak ve telaffuz mantığını görmek.",
                "Wie alt bist du? sorusunu anlayıp Ich bin ... Jahre alt kalıbıyla cevap vermek.",
                "aus ve in arasındaki farkı erken aşamada oturtmak.",
                "Ich komme aus ..., Ich wohne in ... kalıplarını kullanmak.",
                "Temel ülke ve milliyet kalıplarını ayırt etmek.",
                "Türkiye gibi artikel alan ülke adlarında sabit kalıbı fark etmek.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "21"},
                {"label": "Gramer odağı", "value": "Sayı + yaş + ülkeler"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Sayıları ezberlemekten çok örüntüyü fark et",
                    "body": (
                        "İlk aşamada sayıları tek tek ezberlemek gerekir; ama 11, 12 ve 20 gibi temel sayıları "
                        "öğrendiğinde diğer yapılar da daha kolay yerleşir. Bu derste önce sık kullanılan küçük sayıları oturtuyoruz."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "Yaş söylerken Almanca farklı düşünür",
                    "body": (
                        "Türkçede '20 yaşındayım' deriz; Almanca'da bu kalıp Ich bin 20 Jahre alt şeklinde kurulur. "
                        "Burada yaş bilgisi sein fiiliyle gelir ve alt kelimesi yapının vazgeçilmez parçasıdır."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "aus ve in aynı şey değildir",
                    "body": (
                        "aus bir yerden gelmeyi veya kökeni anlatır; in ise bir yerde bulunmayı veya yaşamayı anlatır. "
                        "Ich komme aus Deutschland ama Ich wohne in Berlin deriz."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Milliyet söylemenin iki temel yolu vardır",
                    "body": (
                        "Başlangıç seviyesinde en güvenli kalıp Ich komme aus ... yapısıdır. "
                        "Buna ek olarak Ich bin Deutscher / Deutsche, Ich bin Türke / Türkin gibi milliyet kalıplarını da görmeye başlarız."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "İstisnayı erken gör ama boğulma",
                    "body": (
                        "Çoğu ülke adı artikelsiz kullanılır; ama die Türkei gibi bazı ülke adları artikel alır. "
                        "Bu nedenle aus der Türkei kalıbını şimdilik bir bütün olarak öğrenmek en doğru yaklaşımdır."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "0-20 arası temel sayılar",
                    "summary": "Bu derste özellikle günlük konuşmada hızlı geçen temel sayıları tanıyoruz.",
                    "items": [
                        "0 = null",
                        "1 = eins",
                        "2 = zwei",
                        "3 = drei",
                        "4 = vier",
                        "5 = fünf",
                        "10 = zehn",
                        "11 = elf",
                        "12 = zwölf",
                        "20 = zwanzig",
                    ],
                    "examples": [
                        "Ich bin 19 Jahre alt.",
                        "Wir sind zwei Freunde.",
                        "Sie hat zehn Bücher.",
                    ],
                },
                {
                    "title": "Yaş sorma ve söyleme",
                    "summary": "Yaş kalıbı A1 seviyesinde sürekli tekrar edilir.",
                    "items": [
                        "Wie alt bist du? = Kaç yaşındasın?",
                        "Ich bin 18 Jahre alt. = 18 yaşındayım.",
                        "Er ist 20 Jahre alt. = O 20 yaşında.",
                        "Wir sind 19 Jahre alt. = Biz 19 yaşındayız.",
                    ],
                    "examples": [
                        "Wie alt bist du?",
                        "Ich bin zwölf Jahre alt.",
                        "Sie ist zwanzig Jahre alt.",
                    ],
                },
                {
                    "title": "aus ve in farkı",
                    "summary": "Biri kökeni, diğeri bulunduğun yeri anlatır.",
                    "items": [
                        "Ich komme aus Deutschland. = Almanya'dan geliyorum / Almanyalıyım.",
                        "Wir kommen aus Ankara. = Ankara'dan geliyoruz.",
                        "Ich wohne in Berlin. = Berlin'de yaşıyorum.",
                        "Sie wohnt in Wien. = O Viyana'da yaşıyor.",
                    ],
                    "examples": [
                        "Er kommt aus Frankreich.",
                        "Sie wohnt in Spanien.",
                    ],
                },
                {
                    "title": "Milliyet söylemenin başlangıç kalıpları",
                    "summary": "Önce ülke üzerinden düşün, sonra milliyet formunu ekle.",
                    "items": [
                        "Ich komme aus Deutschland.",
                        "Er ist Deutscher.",
                        "Sie ist Deutsche.",
                        "Er ist Türke.",
                        "Sie ist Türkin.",
                    ],
                    "examples": [
                        "Ich komme aus der Türkei.",
                        "Sie ist Türkin und wohnt in Berlin.",
                    ],
                },
                {
                    "title": "Önemli istisna: die Türkei",
                    "summary": "Bu ülke adı artikel alır; bu yüzden kalıp biraz farklı görünür.",
                    "items": [
                        "die Türkei = Türkiye",
                        "aus der Türkei = Türkiye'den",
                        "in der Türkei = Türkiye'de",
                        "Şimdilik bu yapıyı hazır kalıp gibi gör.",
                    ],
                    "examples": [
                        "Ich komme aus der Türkei.",
                        "Meine Familie wohnt in der Türkei.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Wie alt bist du?", "tr": "Kaç yaşındasın?", "note": "Yaş sormanın temel kalıbı."},
                {"de": "Ich bin 18 Jahre alt.", "tr": "18 yaşındayım.", "note": "Yaş söylerken Jahre alt kalıbı birlikte gelir."},
                {"de": "Er ist 20 Jahre alt.", "tr": "O 20 yaşında.", "note": "Üçüncü tekil için örnek yaş cümlesi."},
                {"de": "Ich komme aus Deutschland.", "tr": "Almanya'dan geliyorum / Almanyalıyım.", "note": "Ülke belirtmenin en güvenli başlangıç kalıbı."},
                {"de": "Wir kommen aus der Türkei.", "tr": "Türkiye'den geliyoruz / Türkiyeliyiz.", "note": "Türkiye artikel aldığı için aus der kalıbı gerekir."},
                {"de": "Sie kommt aus Frankreich.", "tr": "O Fransa'dan geliyor.", "note": "Üçüncü tekilde ülke belirtme örneği."},
                {"de": "Ich wohne in Berlin.", "tr": "Berlin'de yaşıyorum.", "note": "in ile bulunulan şehir gösterilir."},
                {"de": "Wir wohnen in Ankara.", "tr": "Ankara'da yaşıyoruz.", "note": "Çoğul özne ile şehir cümlesi."},
                {"de": "Bist du aus Spanien?", "tr": "İspanya'dan mısın?", "note": "Soru cümlesinde aus kullanımı."},
                {"de": "Er ist Deutscher.", "tr": "O Alman.", "note": "Erkek özne için milliyet adı."},
                {"de": "Sie ist Deutsche.", "tr": "O Alman.", "note": "Kadın özne için milliyet adı."},
                {"de": "Sie ist Türkin.", "tr": "O Türk.", "note": "Kadın özne için Türkin kullanılır."},
            ],
            "common_mistakes": [
                {
                    "wrong": "Ich bin 20 alt.",
                    "right": "Ich bin 20 Jahre alt.",
                    "reason": "Yaş kalıbında Jahre alt yapısı birlikte gelir.",
                },
                {
                    "wrong": "Ich komme in Deutschland.",
                    "right": "Ich komme aus Deutschland.",
                    "reason": "aus kökeni ve geldiğin yeri gösterir; in burada doğru değildir.",
                },
                {
                    "wrong": "Ich wohne aus Berlin.",
                    "right": "Ich wohne in Berlin.",
                    "reason": "Yaşadığın şehir için in kullanılır.",
                },
                {
                    "wrong": "Ich komme aus Türkei.",
                    "right": "Ich komme aus der Türkei.",
                    "reason": "die Türkei artikel alan ülke adıdır; doğru kalıp aus der Türkei şeklinde kurulur.",
                },
                {
                    "wrong": "Sie ist Deutscher.",
                    "right": "Sie ist Deutsche.",
                    "reason": "Kadın özneyle Deutsche, erkek özneyle Deutscher kullanılır.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Hallo! Wie alt bist du?", "text_tr": "Merhaba! Kaç yaşındasın?"},
                    {"speaker": "B", "text_de": "Ich bin 19 Jahre alt. Und du?", "text_tr": "19 yaşındayım. Ya sen?"},
                    {"speaker": "A", "text_de": "Ich bin 20 Jahre alt. Ich komme aus Ankara, aus der Türkei.", "text_tr": "20 yaşındayım. Ankara'dan, Türkiye'den geliyorum."},
                    {"speaker": "B", "text_de": "Ich komme aus Berlin. Ich bin Deutscher.", "text_tr": "Ben Berlin'den geliyorum. Almanım."},
                    {"speaker": "A", "text_de": "Schön! Ich bin Türkin und ich wohne in Ankara.", "text_tr": "Güzel! Ben Türküm ve Ankara'da yaşıyorum."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Nereli ve kaç yaşında?",
                    "intro": "Bu metin önceki derslerin kelimelerini sayı, yaş, ülke ve milliyet bilgisiyle genişletir.",
                    "word_focus": "12 kelime / kalıp",
                    "paragraphs": [
                        "[[Hallo::merhaba]]! Ich heiße Ece und ich bin [[zwanzig::yirmi]] Jahre [[alt::yaşında]]. Ich komme aus [[der Türkei::Türkiye / Türkiye'den]] und ich wohne in [[Ankara::Ankara]].",
                        "Meine [[Freundin::arkadaş / kız arkadaş]] Lara kommt aus [[Deutschland::Almanya]]. Sie ist [[Deutsche::Alman (kadın)]]. Mein Freund Can kommt aus [[Österreich::Avusturya]] und er ist sehr nett.",
                        "Wir sind [[zwei::iki]] Freunde und wir sind in [[Berlin::Berlin]].",
                    ],
                },
            ],
            "tips": [
                "Sayıları yalnız görerek değil, yüksek sesle ritim halinde tekrar et.",
                "Yaş kalıbını tek parça gibi çalış: bin + sayı + Jahre alt.",
                "aus ve in için iki ayrı zihin etiketi kur: köken ve bulunulan yer.",
                "Türkiye kalıbını istisna gibi ezberle: aus der Türkei.",
                "Milliyet cümlelerinde öznenin cinsiyetine göre form değişebileceğini erken fark et.",
            ],
            "vocabulary": [
                {
                    "word": "Jahr",
                    "article": "das",
                    "plural": "die Jahre",
                    "meanings": ["yıl", "yaş ifadesindeki yıl"],
                    "example_de": "Ich bin 18 Jahre alt.",
                    "example_tr": "18 yaşındayım.",
                    "note": "Yaş söylerken Jahre alt kalıbının merkez kelimesidir.",
                },
                {
                    "word": "Zahl",
                    "article": "die",
                    "plural": "die Zahlen",
                    "meanings": ["sayı", "rakam grubu bağlamında sayı"],
                    "example_de": "Die Zahl ist klein.",
                    "example_tr": "Sayı küçüktür.",
                    "note": "Dersin temel kavramlarından biridir.",
                },
                {
                    "word": "Land",
                    "article": "das",
                    "plural": "die Länder",
                    "meanings": ["ülke", "memleket"],
                    "example_de": "Das Land ist groß.",
                    "example_tr": "Ülke büyüktür.",
                    "note": "Ülke isimlerini çalışırken temel isim olarak karşına çıkar.",
                },
                {
                    "word": "Stadt",
                    "article": "die",
                    "plural": "die Städte",
                    "meanings": ["şehir", "kent"],
                    "example_de": "Die Stadt ist alt.",
                    "example_tr": "Şehir eskidir.",
                    "note": "Ülke ve şehir ayrımını kurmak için tekrar ederiz.",
                },
                {
                    "word": "Deutscher",
                    "article": "der",
                    "plural": "die Deutschen",
                    "meanings": ["Alman", "Alman erkek"],
                    "example_de": "Er ist Deutscher.",
                    "example_tr": "O Alman.",
                    "note": "Erkek özne ile milliyet adı olarak kullanılır.",
                },
                {
                    "word": "Deutsche",
                    "article": "die",
                    "plural": "die Deutschen",
                    "meanings": ["Alman", "Alman kadın"],
                    "example_de": "Sie ist Deutsche.",
                    "example_tr": "O Alman.",
                    "note": "Kadın özne ile kullanılan milliyet formudur.",
                },
                {
                    "word": "Türke",
                    "article": "der",
                    "plural": "die Türken",
                    "meanings": ["Türk", "Türk erkek"],
                    "example_de": "Er ist Türke.",
                    "example_tr": "O Türk.",
                    "note": "Erkek özne için kullanılan milliyet adıdır.",
                },
                {
                    "word": "Türkin",
                    "article": "die",
                    "plural": "die Türkinnen",
                    "meanings": ["Türk", "Türk kadın"],
                    "example_de": "Sie ist Türkin.",
                    "example_tr": "O Türk.",
                    "note": "Kadın özne için kullanılan milliyet formudur.",
                },
                {
                    "word": "alt",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["yaşında", "yaşlı bağlamında yaşlı"],
                    "example_de": "Ich bin 20 Jahre alt.",
                    "example_tr": "20 yaşındayım.",
                    "note": "Yaş kalıbında sabit parçadır; bu derste sıfat anlamından çok yaş işlevi önemlidir.",
                },
                {
                    "word": "aus",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["-den", "-dan", "köken olarak -li"],
                    "example_de": "Ich komme aus Deutschland.",
                    "example_tr": "Almanya'dan geliyorum.",
                    "note": "Köken ve çıkış noktası bildirir.",
                },
                {
                    "word": "in",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["-de", "-da", "içinde"],
                    "example_de": "Ich wohne in Berlin.",
                    "example_tr": "Berlin'de yaşıyorum.",
                    "note": "Bulunulan yer veya yaşanılan şehir için sık kullanılır.",
                },
                {
                    "word": "null",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["sıfır"],
                    "example_de": "Ich zähle: null, eins, zwei.",
                    "example_tr": "Sayıyorum: sıfır, bir, iki.",
                    "note": "Sayı dizisinin başlangıcıdır.",
                },
                {
                    "word": "eins",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["bir"],
                    "example_de": "Ich zähle: eins, zwei, drei.",
                    "example_tr": "Sayıyorum: bir, iki, üç.",
                    "note": "Sayma sırasındaki biçimi eins olur.",
                },
                {
                    "word": "zwei",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["iki"],
                    "example_de": "Wir sind zwei Freunde.",
                    "example_tr": "Biz iki arkadaşız.",
                    "note": "Çok sık kullanılan temel sayılardan biridir.",
                },
                {
                    "word": "drei",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["üç"],
                    "example_de": "Drei Studenten sind hier.",
                    "example_tr": "Üç öğrenci burada.",
                    "note": "Çoğul isimlerle erken aşamada birlikte görülür.",
                },
                {
                    "word": "vier",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["dört"],
                    "example_de": "Vier Bücher liegen hier.",
                    "example_tr": "Dört kitap burada duruyor.",
                    "note": "Sayılarda ritim kurmak için ilk gruptadır.",
                },
                {
                    "word": "fünf",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["beş"],
                    "example_de": "Ich habe fünf Fragen.",
                    "example_tr": "Beş sorum var.",
                    "note": "Umlautlu telaffuza erken alışmak için iyi bir örnektir.",
                },
                {
                    "word": "zehn",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["on"],
                    "example_de": "Sie hat zehn Bücher.",
                    "example_tr": "Onun on kitabı var.",
                    "note": "İki basamaklı sayılara geçişten önce temel eşiği temsil eder.",
                },
                {
                    "word": "elf",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["on bir"],
                    "example_de": "Er ist elf Jahre alt.",
                    "example_tr": "O on bir yaşında.",
                    "note": "10'dan sonraki ilk istisna biçimlerden biridir.",
                },
                {
                    "word": "zwölf",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["on iki"],
                    "example_de": "Sie ist zwölf Jahre alt.",
                    "example_tr": "O on iki yaşında.",
                    "note": "Umlautlu sayı biçimlerinden biridir.",
                },
                {
                    "word": "zwanzig",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["yirmi"],
                    "example_de": "Ich bin zwanzig Jahre alt.",
                    "example_tr": "Yirmi yaşındayım.",
                    "note": "Onluk sayılara geçişin ilk temel örneğidir.",
                },
            ],
            "exercises": [
                {
                    "id": "numbers",
                    "type": "single_choice",
                    "title": "Sayı Testi",
                    "description": "Verilen sayı veya sayı kelimesi için doğru karşılığı seç.",
                    "questions": [
                        {
                            "prompt": "Almanca'da '3' hangisidir?",
                            "options": ["drei", "zwei", "zwölf"],
                            "correct_index": 0,
                            "explanation": "3 sayısının temel Almanca karşılığı drei olur.",
                        },
                        {
                            "prompt": "'fünf' hangi sayıdır?",
                            "options": ["4", "5", "11"],
                            "correct_index": 1,
                            "explanation": "fünf = 5.",
                        },
                        {
                            "prompt": "Almanca'da '12' hangisidir?",
                            "options": ["zwölf", "zwanzig", "zehn"],
                            "correct_index": 0,
                            "explanation": "12 sayısı zwölf olarak yazılır.",
                        },
                        {
                            "prompt": "'elf' hangi sayıdır?",
                            "options": ["10", "11", "20"],
                            "correct_index": 1,
                            "explanation": "elf = 11.",
                        },
                        {
                            "prompt": "Almanca'da '20' hangisidir?",
                            "options": ["zwölf", "zwanzig", "zwei"],
                            "correct_index": 1,
                            "explanation": "20 sayısı zwanzig olarak verilir.",
                        },
                        {
                            "prompt": "'null' hangi sayıdır?",
                            "options": ["0", "1", "9"],
                            "correct_index": 0,
                            "explanation": "null = 0.",
                        },
                    ],
                },
                {
                    "id": "age",
                    "type": "single_choice",
                    "title": "Yaş Kalıbı Testi",
                    "description": "Wie alt bist du? kalıbının mantığını pekiştir.",
                    "questions": [
                        {
                            "prompt": "Kaç yaşındasın? -> ___",
                            "options": ["Wie alt bist du?", "Wo wohnst du?", "Woher kommst du?"],
                            "correct_index": 0,
                            "explanation": "Yaş sormanın temel kalıbı Wie alt bist du? şeklindedir.",
                        },
                        {
                            "prompt": "Ben 18 yaşındayım. -> Ich bin ___ Jahre alt.",
                            "options": ["achtzehn", "zwanzig", "zwei"],
                            "correct_index": 0,
                            "explanation": "18 = achtzehn; yaş kalıbında sayı + Jahre alt birlikte gelir.",
                        },
                        {
                            "prompt": "Er ___ 20 Jahre alt.",
                            "options": ["ist", "bin", "seid"],
                            "correct_index": 0,
                            "explanation": "Er ile sein fiilinin doğru biçimi ist olur.",
                        },
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Ich bin 20 alt.", "Ich bin 20 Jahre alt.", "Ich habe 20 Jahre."],
                            "correct_index": 1,
                            "explanation": "Yaş söylerken doğru kalıp Ich bin ... Jahre alt olur.",
                        },
                        {
                            "prompt": "Sie ist zwölf Jahre alt. cümlesinin Türkçesi hangisi?",
                            "options": ["O 12 yaşında.", "Onlar 20 yaşında.", "Siz 12 yaşındasınız."],
                            "correct_index": 0,
                            "explanation": "Sie ist zwölf Jahre alt = O 12 yaşında.",
                        },
                    ],
                },
                {
                    "id": "countries",
                    "type": "single_choice",
                    "title": "Ülke ve Şehir Testi",
                    "description": "aus ve in farkını doğru yerde kullan.",
                    "questions": [
                        {
                            "prompt": "Ben Almanya'dan geliyorum. -> Ich komme ___ Deutschland.",
                            "options": ["in", "aus", "mit"],
                            "correct_index": 1,
                            "explanation": "Köken belirtirken aus kullanılır.",
                        },
                        {
                            "prompt": "Ben Berlin'de yaşıyorum. -> Ich wohne ___ Berlin.",
                            "options": ["aus", "in", "zu"],
                            "correct_index": 1,
                            "explanation": "Bulunulan şehir için in kullanılır.",
                        },
                        {
                            "prompt": "Türkiye'den geliyoruz. -> Wir kommen aus ___.",
                            "options": ["die Türkei", "der Türkei", "Türkei"],
                            "correct_index": 1,
                            "explanation": "Türkiye için doğru yapı aus der Türkei kalıbıdır.",
                        },
                        {
                            "prompt": "O Fransa'dan geliyor. -> Sie kommt aus ___.",
                            "options": ["Frankreich", "Frankreichs", "Französisch"],
                            "correct_index": 0,
                            "explanation": "Frankreich artikelsiz kullanılan ülke adıdır.",
                        },
                        {
                            "prompt": "Ankara'da yaşıyoruz. -> Wir wohnen ___ Ankara.",
                            "options": ["aus", "in", "von"],
                            "correct_index": 1,
                            "explanation": "Yaşanılan şehir için in gerekir.",
                        },
                    ],
                },
                {
                    "id": "nationality",
                    "type": "single_choice",
                    "title": "Milliyet Kalıbı Testi",
                    "description": "Temel milliyet ifadelerini özneye göre ayırt et.",
                    "questions": [
                        {
                            "prompt": "O erkek Alman. -> Er ist ___.",
                            "options": ["Deutsche", "Deutscher", "Deutschland"],
                            "correct_index": 1,
                            "explanation": "Erkek özne ile Deutscher kullanılır.",
                        },
                        {
                            "prompt": "O kadın Alman. -> Sie ist ___.",
                            "options": ["Deutsche", "Deutscher", "Deutsch"],
                            "correct_index": 0,
                            "explanation": "Kadın özne ile Deutsche kullanılır.",
                        },
                        {
                            "prompt": "O kadın Türk. -> Sie ist ___.",
                            "options": ["Türke", "Türkin", "Türkei"],
                            "correct_index": 1,
                            "explanation": "Kadın özne için Türkin gerekir.",
                        },
                        {
                            "prompt": "O erkek Türk. -> Er ist ___.",
                            "options": ["Türkin", "Türke", "Türkei"],
                            "correct_index": 1,
                            "explanation": "Erkek özne ile Türke kullanılır.",
                        },
                        {
                            "prompt": "Hangisi ülke değil, milliyet adıdır?",
                            "options": ["Deutschland", "Frankreich", "Deutscher"],
                            "correct_index": 2,
                            "explanation": "Deutscher bir milliyet adıdır; diğer ikisi ülke adıdır.",
                        },
                    ],
                },
                {
                    "id": "meaning",
                    "type": "single_choice",
                    "title": "Anlam Eşleştirme",
                    "description": "Kelime ve kalıpların anlamını ayırt et.",
                    "questions": [
                        {
                            "prompt": "Wie alt bist du?",
                            "options": ["Nerede yaşıyorsun?", "Kaç yaşındasın?", "Nerelisin?"],
                            "correct_index": 1,
                            "explanation": "Bu kalıp yaş sormak için kullanılır.",
                        },
                        {
                            "prompt": "Ich komme aus Deutschland.",
                            "options": ["Almanya'da yaşıyorum.", "Almanya'dan geliyorum.", "Almanca konuşuyorum."],
                            "correct_index": 1,
                            "explanation": "aus kökeni gösterir; cümlenin anlamı Almanya'dan geliyorum olur.",
                        },
                        {
                            "prompt": "Ich wohne in Berlin.",
                            "options": ["Berlin'de yaşıyorum.", "Berlin'den geliyorum.", "Berlin 20 yaşında."],
                            "correct_index": 0,
                            "explanation": "wohnen in = bir yerde yaşamak.",
                        },
                        {
                            "prompt": "Sie ist Türkin.",
                            "options": ["O Türkiye'den geliyor.", "O Türk.", "O Almandır."],
                            "correct_index": 1,
                            "explanation": "Türkin kadın özne için Türk milliyetini verir.",
                        },
                        {
                            "prompt": "zwanzig",
                            "options": ["on bir", "on iki", "yirmi"],
                            "correct_index": 2,
                            "explanation": "zwanzig = yirmi.",
                        },
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Sayı, yaş, ülke ve milliyet mantığını birlikte kontrol et.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğru yaş cümlesidir?",
                            "options": ["Ich bin zehn Jahre alt.", "Ich komme zehn Jahre alt.", "Ich wohne zehn Jahre alt."],
                            "correct_index": 0,
                            "explanation": "Yaş söylerken doğru yapı Ich bin ... Jahre alt olur.",
                        },
                        {
                            "prompt": "Hangisi köken bildirir?",
                            "options": ["Ich wohne in Wien.", "Ich komme aus Wien.", "Ich bin Wien."],
                            "correct_index": 1,
                            "explanation": "aus ile gelen kalıp kökeni bildirir.",
                        },
                        {
                            "prompt": "Hangisi Türkiye için doğru kalıptır?",
                            "options": ["Ich komme aus Türkei.", "Ich komme aus der Türkei.", "Ich komme in der Türkei."],
                            "correct_index": 1,
                            "explanation": "Türkiye için hazır kalıp aus der Türkei şeklindedir.",
                        },
                        {
                            "prompt": "Hangisi kadın özne ile uyumludur?",
                            "options": ["Sie ist Türke.", "Sie ist Türkin.", "Sie ist Deutscher."],
                            "correct_index": 1,
                            "explanation": "Kadın özne için doğru milliyet formu Türkin olur.",
                        },
                        {
                            "prompt": "Hangisi 11 sayısını verir?",
                            "options": ["zehn", "elf", "zwölf"],
                            "correct_index": 1,
                            "explanation": "11 = elf.",
                        },
                    ],
                },
            ],
            "homework": [
                "0'dan 20'ye kadar sayıları sesli olarak üç tur tekrar et.",
                "Kendin için 5 mini bilgi cümlesi yaz: yaşın, şehrin, ülken ve milliyetin.",
                "aus ve in farkını göstermek için 6 kısa cümle üret.",
                "Türkiye kalıbını ayrı tekrar et: Ich komme aus der Türkei. / Ich wohne in der Türkei.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde sayıları yalnız tanımakla kalmayıp yaş sormayı, geldiğin yeri söylemeyi "
                "ve ilk milliyet kalıplarını kullanmayı başarmış olmalısın. Asıl hedef, kısa tanışma cümlesini "
                "artık daha dolu ve daha doğru kurabilmektir."
            ),
            "next_lesson": {
                "title": "Ders 4: Düzenli fiiller ve basit soru cümleleri",
                "status": "active",
                "slug": "ders-4-duzenli-fiiller-ve-basit-soru-cumleleri",
            },
        },
        {
            "slug": "ders-4-duzenli-fiiller-ve-basit-soru-cumleleri",
            "index": 4,
            "title": "Düzenli Fiiller ve Basit Soru Cümleleri",
            "duration": "75-90 dk",
            "difficulty": "A1.1",
            "teaser": (
                "Bu derste düzenli fiillerin şimdiki zaman çekimini, temel soru kelimelerini "
                "ve en kısa soru-cevap iskeletlerini kuruyoruz. Önceki derslerde öğrendiğin kimlik, şehir, "
                "ülke ve sayı bilgisini artık fiillerle birleştireceğiz."
            ),
            "status": "active",
            "objectives": [
                "Düzenli fiillerin temel çekim mantığını görmek.",
                "wohnen, lernen, arbeiten, machen, spielen ve trinken gibi sık fiilleri kullanmak.",
                "wo, woher, was, wer ve wie soru kelimeleriyle basit sorular kurmak.",
                "Evet-hayır sorularında fiilin başa geçtiğini fark etmek.",
                "Önceki derslerin kelimeleriyle daha uzun tanışma metinleri anlayabilmek.",
                "Kısa günlük konuşma akışlarında soru sorma refleksi geliştirmek.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "23"},
                {"label": "Gramer odağı", "value": "Düzenli fiil + soru"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Düzenli fiil kalıbı sabit bir omurga verir",
                    "body": (
                        "A1 seviyesinde en büyük rahatlık, düzenli fiillerin büyük kısmının benzer eklerle çekilmesidir. "
                        "ich lerne, du lernst, er lernt, wir lernen gibi örüntü bir kez oturduğunda yeni fiiller daha hızlı yerleşir."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "Soru kelimesi gelince fiil hemen arkasından gelir",
                    "body": (
                        "Wo wohnst du?, Was machst du?, Wie heißt du? gibi kalıplarda soru kelimesinden sonra çekimli fiil gelir. "
                        "Bu dizilim erken aşamada netleşirse ileride daha uzun cümleler de rahat kurulur."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Evet-hayır sorularında fiil başa geçer",
                    "body": (
                        "Lernst du Deutsch?, Arbeitest du heute?, Trinkst du Kaffee? gibi cümlelerde soru kelimesi yoksa "
                        "çekimli fiil ilk sıraya gelir. Bu küçük değişiklik çok temel bir refleks oluşturur."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Yeni fiilleri eski bilgilerle birleştiriyoruz",
                    "body": (
                        "Artık yalnızca Ben Ali'yim demek yetmez; Ben Berlin'de yaşıyorum, Almanca öğreniyorum, kafede çalışıyorum "
                        "gibi daha dolu cümlelere geçiyoruz."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Soru-cevap akışı dersin merkezidir",
                    "body": (
                        "Bu derste fiilleri tek başına ezberlemek yerine soru-cevap çiftleri halinde çalışmak gerekir. "
                        "Böylece bilgi pasif kalmaz; doğrudan kullanıma dönüşür."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Düzenli fiil çekim mantığı",
                    "summary": "Başlangıç aşamasında önce çekim eklerini tanımak gerekir.",
                    "items": [
                        "ich lerne",
                        "du lernst",
                        "er / sie / es lernt",
                        "wir lernen",
                        "ihr lernt",
                        "sie / Sie lernen",
                    ],
                    "examples": [
                        "Ich wohne in Berlin.",
                        "Du arbeitest heute.",
                        "Wir lernen Deutsch.",
                    ],
                },
                {
                    "title": "Sık kullanılan soru kelimeleri",
                    "summary": "Soru cümlelerini genişleten temel araç bunlardır.",
                    "items": [
                        "wer = kim",
                        "was = ne",
                        "wo = nerede",
                        "woher = nereden",
                        "wie = nasıl / ne şekilde",
                    ],
                    "examples": [
                        "Wer ist das?",
                        "Was machst du?",
                        "Wo wohnst du?",
                        "Woher kommst du?",
                    ],
                },
                {
                    "title": "Soru kelimeli cümle düzeni",
                    "summary": "Soru kelimesinden sonra çekimli fiil gelir.",
                    "items": [
                        "Wo wohnst du?",
                        "Was lernst du?",
                        "Wie heißt du?",
                        "Woher kommt er?",
                    ],
                    "examples": [
                        "Wo wohnst du? Ich wohne in Ankara.",
                        "Was lernst du? Ich lerne Deutsch.",
                    ],
                },
                {
                    "title": "Evet-hayır soruları",
                    "summary": "Soru kelimesi yoksa fiil ilk sıraya geçer.",
                    "items": [
                        "Lernst du Deutsch?",
                        "Arbeitest du heute?",
                        "Trinkst du Kaffee?",
                        "Spielt er Musik?",
                    ],
                    "examples": [
                        "Ja, ich lerne Deutsch.",
                        "Nein, ich arbeite heute nicht.",
                    ],
                },
                {
                    "title": "Kısa cevap ve bilgi genişletme",
                    "summary": "Sadece evet-hayır değil, bir adım daha bilgi vermeyi hedefliyoruz.",
                    "items": [
                        "Ja, ich lerne Deutsch.",
                        "Nein, ich trinke keinen Kaffee. A1 başında sadece kalıp olarak tanı.",
                        "Ich wohne in Berlin und ich arbeite im Café.",
                        "Er kommt aus Deutschland und lernt Türkisch.",
                    ],
                    "examples": [
                        "Was machst du? Ich lerne Deutsch.",
                        "Wo arbeitest du? Ich arbeite in einem Café.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Ich wohne in Berlin.", "tr": "Berlin'de yaşıyorum.", "note": "wohnen fiilinin en temel kullanım biçimi."},
                {"de": "Du lernst Deutsch.", "tr": "Sen Almanca öğreniyorsun.", "note": "lernen fiili ile en temel cümle."},
                {"de": "Er arbeitet im Café.", "tr": "O kafede çalışıyor.", "note": "arbeiten fiilini yer bilgisiyle birleştirir."},
                {"de": "Sie spielt Musik.", "tr": "O müzik yapıyor / müzik çalıyor.", "note": "spielen fiili bağlama göre oynamak veya çalmak olabilir."},
                {"de": "Ihr trinkt Kaffee.", "tr": "Siz kahve içiyorsunuz.", "note": "çoğul özne ile düzenli fiil örneği."},
                {"de": "Was machst du?", "tr": "Ne yapıyorsun?", "note": "was ile kurulan temel soru."},
                {"de": "Wo wohnst du?", "tr": "Nerede yaşıyorsun?", "note": "wo ile kurulan temel soru."},
                {"de": "Woher kommst du?", "tr": "Nereden geliyorsun?", "note": "woher köken sorar; önceki dersle bağlantılıdır."},
                {"de": "Lernst du Deutsch?", "tr": "Almanca öğreniyor musun?", "note": "evet-hayır sorusunda fiil başa gelir."},
                {"de": "Arbeitest du heute?", "tr": "Bugün çalışıyor musun?", "note": "zaman zarfı ile kısa soru örneği."},
                {"de": "Ja, ich lerne Deutsch.", "tr": "Evet, Almanca öğreniyorum.", "note": "kısa olumlu cevap."},
                {"de": "Nein, ich arbeite heute nicht.", "tr": "Hayır, bugün çalışmıyorum.", "note": "olumsuz soruya kısa cevap örneği."},
            ],
            "common_mistakes": [
                {
                    "wrong": "ich lernen / du lerne demek",
                    "right": "ich lerne, du lernst",
                    "reason": "Düzenli fiillerde özneye göre ek değişir; fiilin çıplak hâli cümleye doğrudan girmez.",
                },
                {
                    "wrong": "Wo du wohnst?",
                    "right": "Wo wohnst du?",
                    "reason": "Soru kelimesinden sonra çekimli fiil gelir.",
                },
                {
                    "wrong": "Du lernst Deutsch?",
                    "right": "Lernst du Deutsch?",
                    "reason": "Evet-hayır sorularında fiil başa geçer.",
                },
                {
                    "wrong": "Ich wohne aus Berlin.",
                    "right": "Ich wohne in Berlin.",
                    "reason": "in yaşanılan yeri, aus ise kökeni gösterir.",
                },
                {
                    "wrong": "spielen fiilini her zaman sadece oyun oynamak diye düşünmek",
                    "right": "spielen bazen oyun oynamak, bazen de müzik çalmak bağlamında kullanılır",
                    "reason": "Kelime anlamı bağlama göre genişleyebilir.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Hallo! Wo wohnst du?", "text_tr": "Merhaba! Nerede yaşıyorsun?"},
                    {"speaker": "B", "text_de": "Ich wohne in Berlin. Und du?", "text_tr": "Berlin'de yaşıyorum. Ya sen?"},
                    {"speaker": "A", "text_de": "Ich wohne in Ankara und ich lerne Deutsch.", "text_tr": "Ankara'da yaşıyorum ve Almanca öğreniyorum."},
                    {"speaker": "B", "text_de": "Arbeitest du auch?", "text_tr": "Sen de çalışıyor musun?"},
                    {"speaker": "A", "text_de": "Ja, ich arbeite heute im Café.", "text_tr": "Evet, bugün kafede çalışıyorum."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Daha uzun tanışma metni",
                    "intro": "Bu metin önceki derslerin kelimelerini yeni fiiller ve soru cümleleriyle birleştirir.",
                    "word_focus": "14 kelime / kalıp",
                    "paragraphs": [
                        "[[Hallo::merhaba]]! Ich heiße Lina, ich bin [[zwanzig::yirmi]] Jahre [[alt::yaşında]] und ich komme aus [[der Türkei::Türkiye / Türkiye'den]].",
                        "Ich [[wohne::yaşıyorum / oturuyorum]] in [[Berlin::Berlin]] und ich [[lerne::öğreniyorum]] [[Deutsch::Almanca]]. Mein [[Freund::arkadaş / erkek arkadaş]] Emir [[arbeitet::çalışıyor]] in einem [[Café::kafe]].",
                        "Er [[trinkt::içiyor]] oft [[Kaffee::kahve]] und ich [[mache::yapıyorum]] meine [[Hausaufgabe::ödev]]. Abends [[spielen::oynamak / çalmak]] wir Musik und dann fragen wir: [[Wo wohnst du?::Nerede yaşıyorsun?]]",
                    ],
                },
            ],
            "tips": [
                "Yeni fiili ezberlerken hemen bir özne ile birlikte tekrar et: ich lerne, du lernst, er lernt.",
                "Soru kelimelerini tek başına değil, tam cümle halinde çalış.",
                "Önceki derslerden gelen şehir, ülke ve yaş bilgisini yeni fiillerle birleştir.",
                "Evet-hayır sorularında fiilin başa geçmesini sesli tekrarlarla otomatikleştir.",
                "Okuma metnindeki tooltip kelimeleri tek tek değil, cümle içinde hatırlamaya çalış.",
            ],
            "vocabulary": [
                {
                    "word": "wohnen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["yaşamak", "oturmak"],
                    "example_de": "Ich wohne in Berlin.",
                    "example_tr": "Berlin'de yaşıyorum.",
                    "note": "Şehir ve yer bilgisiyle çok sık kullanılır.",
                },
                {
                    "word": "lernen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["öğrenmek", "ders çalışmak"],
                    "example_de": "Wir lernen Deutsch.",
                    "example_tr": "Biz Almanca öğreniyoruz.",
                    "note": "Dil öğrenimi bağlamında temel fiillerden biridir.",
                },
                {
                    "word": "arbeiten",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["çalışmak", "iş yapmak"],
                    "example_de": "Er arbeitet heute.",
                    "example_tr": "O bugün çalışıyor.",
                    "note": "Günlük rutin anlatımında çok sık geçer.",
                },
                {
                    "word": "machen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["yapmak", "etmek"],
                    "example_de": "Was machst du?",
                    "example_tr": "Ne yapıyorsun?",
                    "note": "Başlangıç seviyesinde çok geniş kullanım alanı vardır.",
                },
                {
                    "word": "spielen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["oynamak", "çalmak"],
                    "example_de": "Sie spielt Musik.",
                    "example_tr": "O müzik çalıyor.",
                    "note": "Bağlama göre oyun oynamak veya müzik çalmak anlamı verebilir.",
                },
                {
                    "word": "trinken",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["içmek"],
                    "example_de": "Ihr trinkt Kaffee.",
                    "example_tr": "Siz kahve içiyorsunuz.",
                    "note": "Gündelik rutin fiillerinden biridir.",
                },
                {
                    "word": "fragen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["sormak"],
                    "example_de": "Ich frage meinen Freund.",
                    "example_tr": "Arkadaşıma soruyorum.",
                    "note": "Soru cümlesi mantığıyla birlikte düşünülmesi gereken fiildir.",
                },
                {
                    "word": "Frage",
                    "article": "die",
                    "plural": "die Fragen",
                    "meanings": ["soru"],
                    "example_de": "Die Frage ist wichtig.",
                    "example_tr": "Soru önemlidir.",
                    "note": "Fiil olan fragen ile birlikte hatırlanması yararlıdır.",
                },
                {
                    "word": "Antwort",
                    "article": "die",
                    "plural": "die Antworten",
                    "meanings": ["cevap", "yanıt"],
                    "example_de": "Die Antwort ist kurz.",
                    "example_tr": "Cevap kısadır.",
                    "note": "Soru-cevap ikilisinin ikinci ana parçasıdır.",
                },
                {
                    "word": "Arbeit",
                    "article": "die",
                    "plural": "die Arbeiten",
                    "meanings": ["iş", "çalışma"],
                    "example_de": "Die Arbeit ist heute schwer.",
                    "example_tr": "İş bugün zor.",
                    "note": "arbeiten fiili ile aynı aileden geldiği için birlikte hatırlanmalıdır.",
                },
                {
                    "word": "Hausaufgabe",
                    "article": "die",
                    "plural": "die Hausaufgaben",
                    "meanings": ["ödev", "ev ödevi"],
                    "example_de": "Ich mache meine Hausaufgabe.",
                    "example_tr": "Ödevimi yapıyorum.",
                    "note": "machen fiiliyle sık eşleşir.",
                },
                {
                    "word": "Universität",
                    "article": "die",
                    "plural": "die Universitäten",
                    "meanings": ["üniversite"],
                    "example_de": "Die Universität ist in Berlin.",
                    "example_tr": "Üniversite Berlin'de.",
                    "note": "Öğrenci ve öğrenme bağlamında doğal bir isimdir.",
                },
                {
                    "word": "Musik",
                    "article": "die",
                    "plural": "-",
                    "meanings": ["müzik"],
                    "example_de": "Wir spielen Musik.",
                    "example_tr": "Müzik yapıyoruz / çalıyoruz.",
                    "note": "spielen fiilinin ikinci anlamını göstermek için yararlıdır.",
                },
                {
                    "word": "Kaffee",
                    "article": "der",
                    "plural": "die Kaffees",
                    "meanings": ["kahve"],
                    "example_de": "Ich trinke Kaffee.",
                    "example_tr": "Kahve içiyorum.",
                    "note": "İçecek cümlelerinde çok sık kullanılır.",
                },
                {
                    "word": "Café",
                    "article": "das",
                    "plural": "die Cafés",
                    "meanings": ["kafe"],
                    "example_de": "Er arbeitet im Café.",
                    "example_tr": "O kafede çalışıyor.",
                    "note": "Yer bildiren basit cümlelerle sık görülür.",
                },
                {
                    "word": "Deutsch",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["Almanca"],
                    "example_de": "Ich lerne Deutsch.",
                    "example_tr": "Almanca öğreniyorum.",
                    "note": "Dil adı olarak başlangıç seviyesinde çok kullanılır.",
                },
                {
                    "word": "heute",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["bugün"],
                    "example_de": "Ich arbeite heute.",
                    "example_tr": "Bugün çalışıyorum.",
                    "note": "Zaman zarfı olarak temel günlük kelimelerden biridir.",
                },
                {
                    "word": "oft",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["sık sık", "çoğu zaman"],
                    "example_de": "Er trinkt oft Kaffee.",
                    "example_tr": "O sık sık kahve içer.",
                    "note": "Sıklık bildiren basit zarflardan biridir.",
                },
                {
                    "word": "wer",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["kim"],
                    "example_de": "Wer ist das?",
                    "example_tr": "Bu kim?",
                    "note": "Kişi hakkında soru sormak için kullanılır.",
                },
                {
                    "word": "was",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["ne"],
                    "example_de": "Was machst du?",
                    "example_tr": "Ne yapıyorsun?",
                    "note": "İş, nesne veya etkinlik sorularında kullanılır.",
                },
                {
                    "word": "wo",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["nerede"],
                    "example_de": "Wo wohnst du?",
                    "example_tr": "Nerede yaşıyorsun?",
                    "note": "Bulunulan yeri sorar.",
                },
                {
                    "word": "woher",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["nereden"],
                    "example_de": "Woher kommst du?",
                    "example_tr": "Nereden geliyorsun?",
                    "note": "Kökeni veya çıkış noktasını sorar.",
                },
                {
                    "word": "wie",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["nasıl", "ne şekilde"],
                    "example_de": "Wie heißt du?",
                    "example_tr": "Adın ne?",
                    "note": "Sık kullanılan soru kelimelerinden biridir.",
                },
            ],
            "exercises": [
                {
                    "id": "regular-verbs",
                    "type": "single_choice",
                    "title": "Düzenli Fiil Çekimi",
                    "description": "Özneye göre doğru fiil biçimini seç.",
                    "questions": [
                        {
                            "prompt": "Ich ___ in Berlin.",
                            "options": ["wohnst", "wohne", "wohnt"],
                            "correct_index": 1,
                            "explanation": "ich ile wohnen fiili wohne olur.",
                        },
                        {
                            "prompt": "Du ___ Deutsch.",
                            "options": ["lernst", "lernen", "lernt"],
                            "correct_index": 0,
                            "explanation": "du ile düzenli fiiller çoğunlukla -st alır: du lernst.",
                        },
                        {
                            "prompt": "Er ___ heute im Café.",
                            "options": ["arbeite", "arbeitet", "arbeiten"],
                            "correct_index": 1,
                            "explanation": "er ile düzenli fiiller -t alır: er arbeitet.",
                        },
                        {
                            "prompt": "Wir ___ Musik.",
                            "options": ["spielen", "spielt", "spielst"],
                            "correct_index": 0,
                            "explanation": "wir ile fiilin temel çoğul biçimi kullanılır: wir spielen.",
                        },
                        {
                            "prompt": "Ihr ___ Kaffee.",
                            "options": ["trinken", "trinkt", "trinkst"],
                            "correct_index": 1,
                            "explanation": "ihr ile düzenli fiiller -t alır: ihr trinkt.",
                        },
                        {
                            "prompt": "Sie ___ die Hausaufgabe.",
                            "options": ["machen", "macht", "machst"],
                            "correct_index": 0,
                            "explanation": "sie / Sie çoğul ya da resmî özneyle machen biçimi gelir.",
                        },
                    ],
                },
                {
                    "id": "question-words",
                    "type": "single_choice",
                    "title": "Soru Kelimesi Testi",
                    "description": "Bağlama göre doğru soru kelimesini seç.",
                    "questions": [
                        {
                            "prompt": "___ wohnst du? -> Nerede yaşıyorsun?",
                            "options": ["Wo", "Was", "Wer"],
                            "correct_index": 0,
                            "explanation": "Yer sormak için wo kullanılır.",
                        },
                        {
                            "prompt": "___ kommst du? -> Nereden geliyorsun?",
                            "options": ["Wie", "Woher", "Wo"],
                            "correct_index": 1,
                            "explanation": "Köken ve çıkış noktası için woher gerekir.",
                        },
                        {
                            "prompt": "___ machst du? -> Ne yapıyorsun?",
                            "options": ["Wer", "Was", "Wie"],
                            "correct_index": 1,
                            "explanation": "Eylem veya nesne sorularında was kullanılır.",
                        },
                        {
                            "prompt": "___ ist das? -> Bu kim?",
                            "options": ["Wer", "Wo", "Wie"],
                            "correct_index": 0,
                            "explanation": "Kişi sorarken wer kullanılır.",
                        },
                        {
                            "prompt": "___ heißt du? -> Adın ne / nasıl adlandırılıyorsun?",
                            "options": ["Wie", "Was", "Woher"],
                            "correct_index": 0,
                            "explanation": "Ad sormanın kalıbı Wie heißt du? şeklindedir.",
                        },
                    ],
                },
                {
                    "id": "question-order",
                    "type": "single_choice",
                    "title": "Soru Cümlesi Düzeni",
                    "description": "Doğru soru cümlesi sırasını seç.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Wo du wohnst?", "Wo wohnst du?", "Du wohnst wo?"],
                            "correct_index": 1,
                            "explanation": "Soru kelimesinden sonra çekimli fiil gelir: Wo wohnst du?",
                        },
                        {
                            "prompt": "Hangisi evet-hayır sorusudur?",
                            "options": ["Du lernst Deutsch?", "Lernst du Deutsch?", "Deutsch lernst du?"],
                            "correct_index": 1,
                            "explanation": "Evet-hayır sorusunda fiil başa gelir: Lernst du Deutsch?",
                        },
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Was du machst?", "Was machst du?", "Du machst was?"],
                            "correct_index": 1,
                            "explanation": "was ile kurulan standart soru kalıbı Was machst du? olur.",
                        },
                        {
                            "prompt": "Hangisi doğru sorudur?",
                            "options": ["Arbeitest du heute?", "Du arbeitest heute?", "Heute du arbeitest?"],
                            "correct_index": 0,
                            "explanation": "Fiil başa geçerek evet-hayır sorusu kurulur.",
                        },
                        {
                            "prompt": "Hangisi doğru sıralamadır?",
                            "options": ["Woher er kommt?", "Woher kommt er?", "Er kommt woher?"],
                            "correct_index": 1,
                            "explanation": "woher sonrasında çekimli fiil gelir: Woher kommt er?",
                        },
                    ],
                },
                {
                    "id": "meaning",
                    "type": "single_choice",
                    "title": "Kelime ve Kalıp Anlamı",
                    "description": "Fiil ve soru kalıplarının anlamını seç.",
                    "questions": [
                        {
                            "prompt": "arbeiten",
                            "options": ["çalışmak", "öğrenmek", "içmek"],
                            "correct_index": 0,
                            "explanation": "arbeiten = çalışmak.",
                        },
                        {
                            "prompt": "Wo wohnst du?",
                            "options": ["Nereden geliyorsun?", "Nerede yaşıyorsun?", "Ne yapıyorsun?"],
                            "correct_index": 1,
                            "explanation": "wo + wohnen = Nerede yaşıyorsun?",
                        },
                        {
                            "prompt": "Kaffee",
                            "options": ["kahve", "kafe", "müzik"],
                            "correct_index": 0,
                            "explanation": "Kaffee içecek olarak kahve anlamına gelir.",
                        },
                        {
                            "prompt": "Was machst du?",
                            "options": ["Ne yapıyorsun?", "Kim bu?", "Bugün çalışıyor musun?"],
                            "correct_index": 0,
                            "explanation": "machen fiiliyle kurulan temel soru Ne yapıyorsun? olur.",
                        },
                        {
                            "prompt": "Hausaufgabe",
                            "options": ["üniversite", "ödev", "cevap"],
                            "correct_index": 1,
                            "explanation": "Hausaufgabe = ödev.",
                        },
                    ],
                },
                {
                    "id": "gaps",
                    "type": "single_choice",
                    "title": "Boşluk Doldurma",
                    "description": "Fiil ve soru kelimesini doğru yerde kullan.",
                    "questions": [
                        {
                            "prompt": "Ich ___ Deutsch.",
                            "options": ["lerne", "lernst", "lernt"],
                            "correct_index": 0,
                            "explanation": "ich ile düzenli fiil -e alır: ich lerne.",
                        },
                        {
                            "prompt": "___ kommst du? Aus Ankara.",
                            "options": ["Wo", "Wer", "Woher"],
                            "correct_index": 2,
                            "explanation": "Köken sorarken woher gerekir.",
                        },
                        {
                            "prompt": "Er ___ Kaffee.",
                            "options": ["trinkt", "trinkst", "trinken"],
                            "correct_index": 0,
                            "explanation": "er ile trinken fiili trinkt olur.",
                        },
                        {
                            "prompt": "Was ___ du heute?",
                            "options": ["mache", "machst", "macht"],
                            "correct_index": 1,
                            "explanation": "du ile machen fiili machst olur.",
                        },
                        {
                            "prompt": "Wir ___ im Café.",
                            "options": ["arbeite", "arbeitet", "arbeiten"],
                            "correct_index": 2,
                            "explanation": "wir ile arbeiten biçimi kullanılır.",
                        },
                        {
                            "prompt": "___ ist das? Das ist mein Lehrer.",
                            "options": ["Wer", "Wo", "Was"],
                            "correct_index": 0,
                            "explanation": "Kişi sorarken wer kullanılır.",
                        },
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Fiil çekimi ve soru mantığını birlikte yokla.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Du wohnen in Berlin.", "Du wohnst in Berlin.", "Du wohnt in Berlin."],
                            "correct_index": 1,
                            "explanation": "du ile wohnen fiili wohnst olur.",
                        },
                        {
                            "prompt": "Hangisi doğru soru kelimesidir?",
                            "options": ["Woher kommst du?", "Wo kommst du?", "Wer kommst du?"],
                            "correct_index": 0,
                            "explanation": "Köken sormanın en doğru kalıbı Woher kommst du? olur.",
                        },
                        {
                            "prompt": "Hangisi evet-hayır sorusudur?",
                            "options": ["Was machst du?", "Lernst du Deutsch?", "Wo wohnst du?"],
                            "correct_index": 1,
                            "explanation": "Soru kelimesi olmadan fiil başa geçtiği için evet-hayır sorusudur.",
                        },
                        {
                            "prompt": "Hangisi doğru anlam eşleşmesidir?",
                            "options": ["fragen = cevap vermek", "arbeiten = çalışmak", "wohnen = gelmek"],
                            "correct_index": 1,
                            "explanation": "arbeiten = çalışmak.",
                        },
                        {
                            "prompt": "Bu dersin ana hedefi nedir?",
                            "options": [
                                "Tüm Almanca fiilleri bitirmek",
                                "Düzenli fiil ve temel soru iskeletini oturtmak",
                                "Uzun akademik paragraf yazmak",
                            ],
                            "correct_index": 1,
                            "explanation": "Bu dersin ana odağı düzenli fiiller ve kısa soru kalıplarıdır.",
                        },
                    ],
                },
            ],
            "homework": [
                "wohnen, lernen, arbeiten, machen, spielen ve trinken fiillerini tüm öznelerle sesli çek.",
                "Kendin hakkında 6 mini cümle yaz: nerede yaşıyorsun, ne öğreniyorsun, bugün ne yapıyorsun, ne içiyorsun.",
                "wo, woher, was ve wer ile en az birer soru üret.",
                "Okuma metnindeki tooltip kelimelerini kapatıp cümleleri kendi başına tekrar kurmaya çalış.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde yalnızca kelime bilmekle kalmayıp düzenli fiillerle kısa bilgi vermeyi, "
                "temel soru kelimeleriyle soru sormayı ve önceki derslerden gelen şehir, yaş ve ülke bilgisini "
                "daha akıcı cümlelere dönüştürmeyi başarmış olmalısın."
            ),
            "next_lesson": {
                "title": "Ders 5: Aile, sahiplik ve günlük nesneler",
                "status": "active",
                "slug": "ders-5-aile-sahiplik-ve-gunluk-nesneler",
            },
        },
        {
            "slug": "ders-5-aile-sahiplik-ve-gunluk-nesneler",
            "index": 5,
            "title": "Aile, Sahiplik ve Günlük Nesneler",
            "duration": "80-95 dk",
            "difficulty": "A1.2",
            "teaser": (
                "Bu derste aile üyelerini, günlük eşyaları ve sahiplik bildiren temel kalıpları kuruyoruz. "
                "haben fiili ile benim, senin, onun gibi iyelik yapıları bir araya geliyor; böylece artık "
                "nesneler ve insanlar arasındaki ilişkiyi daha doğal anlatabiliyoruz."
            ),
            "status": "active",
            "objectives": [
                "haben fiilinin en temel çekimini öğrenmek.",
                "mein, deine, sein, ihr, unser ve euer gibi iyelik kelimelerini tanımak.",
                "Aile bireylerini doğru artikel ile söylemek.",
                "Günlük nesneleri sahiplik ifadesiyle birlikte kullanmak.",
                "İlk kez daha zengin bir aile tanıtım paragrafı okuyabilmek.",
                "Kısa soru-cevap akışında sahiplik sormayı başarmak.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "20"},
                {"label": "Gramer odağı", "value": "haben + iyelik"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "haben ile sahiplik kurulur",
                    "body": (
                        "Almanca'da bir şeye sahip olmayı en temel biçimde haben fiiliyle anlatırız. "
                        "Ich habe ein Handy., Wir haben zwei Bücher. gibi cümleler bu dersin merkezindedir."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "İyelik kelimesi ismin önüne gelir",
                    "body": (
                        "mein Vater, meine Mutter, mein Handy, meine Tasche gibi yapılarda sahiplik kelimesi "
                        "ismin önüne gelir ve ismin türüne göre biçim değiştirir."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Aile kelimeleri cümleyi hızla büyütür",
                    "body": (
                        "Bu benim annem, bu benim kardeşim, benim iki kardeşim var gibi cümleler "
                        "A1 seviyesinde tanıtım konuşmasını bir üst seviyeye taşır."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Günlük nesneler artık bağlamla gelir",
                    "body": (
                        "Telefon, çanta, anahtar, saat gibi kelimeleri çıplak liste olarak değil, "
                        "Benim çantam, senin anahtarın, bizim odamız gibi bağlam içinde çalışıyoruz."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Ayrıntılı hâl bilgisine girmeden kalıbı oturtuyoruz",
                    "body": (
                        "Bu derste bazı yapılarda einen / eine / ein gibi biçimler göreceksin. "
                        "Şimdilik bunları hazır kalıp gibi alıyoruz; ayrıntılı nesne hâli konusu daha sonra gelecek."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "haben fiili çekimi",
                    "summary": "Bu fiil düzenli görünmez; o yüzden temel çekim tablosunu ayrı öğrenmek gerekir.",
                    "items": [
                        "ich habe",
                        "du hast",
                        "er / sie / es hat",
                        "wir haben",
                        "ihr habt",
                        "sie / Sie haben",
                    ],
                    "examples": [
                        "Ich habe eine Schwester.",
                        "Du hast ein Handy.",
                        "Wir haben zwei Bücher.",
                    ],
                },
                {
                    "title": "Temel iyelik kelimeleri",
                    "summary": "İlk aşamada bu yapıları isimle birlikte blok halinde görmek yeterlidir.",
                    "items": [
                        "mein Vater / meine Mutter / mein Handy",
                        "dein Bruder / deine Tasche",
                        "sein Sohn / seine Tochter",
                        "ihr Schlüssel / ihre Uhr",
                        "unser Zimmer / unsere Wohnung",
                        "euer Tisch / eure Bücher",
                    ],
                    "examples": [
                        "Das ist mein Vater.",
                        "Ist das deine Tasche?",
                        "Unsere Wohnung ist klein.",
                    ],
                },
                {
                    "title": "Aile tanıtımı için iki temel kalıp",
                    "summary": "Bu kalıplar dersin omurgasını kurar.",
                    "items": [
                        "Das ist meine Mutter. = Bu benim annem.",
                        "Ich habe einen Bruder. = Bir erkek kardeşim var.",
                        "Ich habe eine Schwester. = Bir kız kardeşim var.",
                        "Wir haben ein Foto. = Bir fotoğrafımız var.",
                    ],
                    "examples": [
                        "Das ist mein Sohn.",
                        "Ich habe zwei Kinder.",
                    ],
                },
                {
                    "title": "Günlük nesnelerle sahiplik",
                    "summary": "Sahiplik artık eşya dünyasında da görünür.",
                    "items": [
                        "Das ist mein Handy.",
                        "Ist das dein Schlüssel?",
                        "Meine Tasche ist groß.",
                        "Unser Zimmer hat einen Tisch.",
                    ],
                    "examples": [
                        "Wo ist meine Uhr?",
                        "Sein Computer ist neu.",
                    ],
                },
                {
                    "title": "Önemli ayrım: sein fiili ve sein iyeliği aynı şey değildir",
                    "summary": "Yazılış benzer görünse de işlev bambaşkadır.",
                    "items": [
                        "Er ist Lehrer. -> ist burada fiildir.",
                        "Sein Bruder ist Lehrer. -> sein burada 'onun' anlamında iyeliktir.",
                        "Sie ist müde. -> ist fiil.",
                        "Ihr Bruder lernt Deutsch. -> ihr burada 'onun' olabilir.",
                    ],
                    "examples": [
                        "Er ist Student. Sein Bruder arbeitet.",
                        "Sie ist in Berlin. Ihre Tasche ist hier.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Das ist meine Familie.", "tr": "Bu benim ailem.", "note": "Aile tanıtımına giriş cümlesi."},
                {"de": "Das ist mein Vater.", "tr": "Bu benim babam.", "note": "mein + der isim örneği."},
                {"de": "Das ist meine Mutter.", "tr": "Bu benim annem.", "note": "meine + die isim örneği."},
                {"de": "Ich habe einen Bruder.", "tr": "Bir erkek kardeşim var.", "note": "haben fiiliyle ilk aile cümlesi."},
                {"de": "Ich habe eine Schwester.", "tr": "Bir kız kardeşim var.", "note": "dişil aile ismiyle kurulan kalıp."},
                {"de": "Hast du Geschwister?", "tr": "Kardeşlerin var mı?", "note": "du ile kurulan evet-hayır sorusu."},
                {"de": "Ja, ich habe zwei Brüder.", "tr": "Evet, iki erkek kardeşim var.", "note": "kısa cevap + sayı tekrarını birleştirir."},
                {"de": "Das ist mein Handy.", "tr": "Bu benim telefonum.", "note": "günlük nesne ile sahiplik."},
                {"de": "Ist das deine Tasche?", "tr": "Bu senin çantan mı?", "note": "eşya sorusu için temel kalıp."},
                {"de": "Wo ist mein Schlüssel?", "tr": "Anahtarım nerede?", "note": "sahiplik + soru kelimesi birleşimi."},
                {"de": "Unsere Wohnung ist klein.", "tr": "Bizim evimiz küçüktür.", "note": "unser / unsere yapısına giriş."},
                {"de": "Sein Computer ist neu.", "tr": "Onun bilgisayarı yeni.", "note": "sein iyeliğini fiilden ayırmak için iyi örnek."},
            ],
            "common_mistakes": [
                {
                    "wrong": "mein Mutter demek",
                    "right": "meine Mutter",
                    "reason": "die ile gelen isimlerde temel iyelik biçimi genelde meine / deine / seine / ihre olur.",
                },
                {
                    "wrong": "du habe / er haben demek",
                    "right": "du hast, er hat",
                    "reason": "haben fiili düzenli çekim izlemez; du ve er biçimleri özellikle dikkat ister.",
                },
                {
                    "wrong": "mein der Bruder gibi çift belirleyici kurmak",
                    "right": "mein Bruder",
                    "reason": "İyelik kelimesi varken ayrıca der / die / das getirilmez.",
                },
                {
                    "wrong": "sein kelimesini her gördüğünde fiil sanmak",
                    "right": "sein bazen fiil, bazen 'onun' anlamında iyelik olabilir",
                    "reason": "İşlev cümledeki yerine göre anlaşılır.",
                },
                {
                    "wrong": "özel isim gibi tekil nesneleri gelişigüzel ezberlemek",
                    "right": "nesneyi sahiplik ve kullanım cümlesiyle öğrenmek",
                    "reason": "Kelime bağlam içinde öğrenildiğinde daha kalıcı olur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Hallo! Ist das deine Tasche?", "text_tr": "Merhaba! Bu senin çantan mı?"},
                    {"speaker": "B", "text_de": "Ja, das ist meine Tasche. Und das ist mein Handy.", "text_tr": "Evet, bu benim çantam. Ve bu da benim telefonum."},
                    {"speaker": "A", "text_de": "Hast du Geschwister?", "text_tr": "Kardeşlerin var mı?"},
                    {"speaker": "B", "text_de": "Ja, ich habe einen Bruder und eine Schwester.", "text_tr": "Evet, bir erkek kardeşim ve bir kız kardeşim var."},
                    {"speaker": "A", "text_de": "Schön. Meine Familie ist in Ankara.", "text_tr": "Güzel. Benim ailem Ankara'da."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Aile ve oda metni",
                    "intro": "Bu metin önceki derslerin şehir, yaş ve fiil bilgisini şimdi aile ve eşyalarla birleştiriyor.",
                    "word_focus": "16 kelime / kalıp",
                    "paragraphs": [
                        "[[Hallo::merhaba]]! Ich heiße Deniz und ich [[wohne::yaşıyorum]] in Berlin. Das ist [[meine Familie::benim ailem]]. Mein [[Vater::baba]] arbeitet heute und meine [[Mutter::anne]] trinkt [[Kaffee::kahve]].",
                        "Ich habe einen [[Bruder::erkek kardeş]] und eine [[Schwester::kız kardeş]]. Mein Bruder lernt Deutsch und meine Schwester spielt Musik. Wir haben auch ein altes [[Foto::foto]].",
                        "In unserer [[Wohnung::ev / daire]] gibt es ein kleines [[Zimmer::oda]], einen [[Tisch::masa]], ein [[Handy::telefon]], eine [[Tasche::çanta]] und einen [[Schlüssel::anahtar]]. [[Wo ist mein Schlüssel?::Anahtarım nerede?]]",
                    ],
                },
            ],
            "tips": [
                "haben fiilini mutlaka sesli tekrar et: ich habe, du hast, er hat...",
                "İyelik kelimelerini tek başına değil isimle birlikte çalış: meine Mutter, mein Vater, meine Tasche.",
                "Aile kelimelerini fotoğraf veya şema ile eşleştirerek tekrar etmek kalıcılığı artırır.",
                "Okuma metnindeki eşya kelimelerini kendi odandaki nesnelerle ilişkilendir.",
                "sein fiili ile sein iyeliğini karıştırmamak için örnek cümleleri karşılaştır.",
            ],
            "vocabulary": [
                {
                    "word": "Familie",
                    "article": "die",
                    "plural": "die Familien",
                    "meanings": ["aile"],
                    "example_de": "Das ist meine Familie.",
                    "example_tr": "Bu benim ailem.",
                    "note": "Dersin merkez isimlerinden biridir.",
                },
                {
                    "word": "Mutter",
                    "article": "die",
                    "plural": "die Mütter",
                    "meanings": ["anne"],
                    "example_de": "Das ist meine Mutter.",
                    "example_tr": "Bu benim annem.",
                    "note": "meine ile çok sık kullanılır.",
                },
                {
                    "word": "Vater",
                    "article": "der",
                    "plural": "die Väter",
                    "meanings": ["baba"],
                    "example_de": "Das ist mein Vater.",
                    "example_tr": "Bu benim babam.",
                    "note": "mein ile kullanılan temel aile ismidir.",
                },
                {
                    "word": "Bruder",
                    "article": "der",
                    "plural": "die Brüder",
                    "meanings": ["erkek kardeş", "erkek kardeş / abi"],
                    "example_de": "Ich habe einen Bruder.",
                    "example_tr": "Bir erkek kardeşim var.",
                    "note": "haben fiiliyle sık görülür.",
                },
                {
                    "word": "Schwester",
                    "article": "die",
                    "plural": "die Schwestern",
                    "meanings": ["kız kardeş", "abla / kız kardeş"],
                    "example_de": "Ich habe eine Schwester.",
                    "example_tr": "Bir kız kardeşim var.",
                    "note": "dişil aile isimleri için iyi bir örnektir.",
                },
                {
                    "word": "Sohn",
                    "article": "der",
                    "plural": "die Söhne",
                    "meanings": ["oğul", "erkek evlat"],
                    "example_de": "Das ist ihr Sohn.",
                    "example_tr": "Bu onun oğludur.",
                    "note": "ihr / sein ayrımında yararlı olur.",
                },
                {
                    "word": "Tochter",
                    "article": "die",
                    "plural": "die Töchter",
                    "meanings": ["kız evlat", "kız çocuk"],
                    "example_de": "Das ist seine Tochter.",
                    "example_tr": "Bu onun kızıdır.",
                    "note": "aile ilişkilerinin genişletilmiş örneğidir.",
                },
                {
                    "word": "Zimmer",
                    "article": "das",
                    "plural": "die Zimmer",
                    "meanings": ["oda"],
                    "example_de": "Unser Zimmer ist klein.",
                    "example_tr": "Bizim odamız küçüktür.",
                    "note": "ev ve eşya bağlamında sık geçer.",
                },
                {
                    "word": "Wohnung",
                    "article": "die",
                    "plural": "die Wohnungen",
                    "meanings": ["ev", "daire"],
                    "example_de": "Unsere Wohnung ist klein.",
                    "example_tr": "Bizim evimiz küçüktür.",
                    "note": "wohnen fiiliyle birlikte düşünülmelidir.",
                },
                {
                    "word": "Handy",
                    "article": "das",
                    "plural": "die Handys",
                    "meanings": ["telefon", "cep telefonu"],
                    "example_de": "Das ist mein Handy.",
                    "example_tr": "Bu benim telefonum.",
                    "note": "günlük nesne olarak çok sık kullanılır.",
                },
                {
                    "word": "Tasche",
                    "article": "die",
                    "plural": "die Taschen",
                    "meanings": ["çanta"],
                    "example_de": "Ist das deine Tasche?",
                    "example_tr": "Bu senin çantan mı?",
                    "note": "soru kalıbıyla birlikte iyi çalışılır.",
                },
                {
                    "word": "Schlüssel",
                    "article": "der",
                    "plural": "die Schlüssel",
                    "meanings": ["anahtar"],
                    "example_de": "Wo ist mein Schlüssel?",
                    "example_tr": "Anahtarım nerede?",
                    "note": "sahiplik ve soru kelimesini birleştirir.",
                },
                {
                    "word": "Stift",
                    "article": "der",
                    "plural": "die Stifte",
                    "meanings": ["kalem"],
                    "example_de": "Mein Stift ist hier.",
                    "example_tr": "Kalemim burada.",
                    "note": "sınıf ve günlük eşya arasında köprü kurar.",
                },
                {
                    "word": "Foto",
                    "article": "das",
                    "plural": "die Fotos",
                    "meanings": ["fotoğraf"],
                    "example_de": "Wir haben ein Foto.",
                    "example_tr": "Bir fotoğrafımız var.",
                    "note": "aile tanıtımı bağlamında doğal bir nesnedir.",
                },
                {
                    "word": "Uhr",
                    "article": "die",
                    "plural": "die Uhren",
                    "meanings": ["saat"],
                    "example_de": "Ihre Uhr ist neu.",
                    "example_tr": "Onun saati yenidir.",
                    "note": "iyelikle sık kullanılan küçük nesnelerdendir.",
                },
                {
                    "word": "Computer",
                    "article": "der",
                    "plural": "die Computer",
                    "meanings": ["bilgisayar"],
                    "example_de": "Sein Computer ist neu.",
                    "example_tr": "Onun bilgisayarı yenidir.",
                    "note": "sein iyeliğini ayırt etmek için yararlıdır.",
                },
                {
                    "word": "Buch",
                    "article": "das",
                    "plural": "die Bücher",
                    "meanings": ["kitap"],
                    "example_de": "Unser Buch ist auf dem Tisch.",
                    "example_tr": "Kitabımız masanın üstünde.",
                    "note": "önceki dersten gelen bir kelimeyi yeni bağlamda tekrar eder.",
                },
                {
                    "word": "Telefon",
                    "article": "das",
                    "plural": "die Telefone",
                    "meanings": ["telefon", "telefon cihazı"],
                    "example_de": "Das Telefon ist alt.",
                    "example_tr": "Telefon eski.",
                    "note": "Handy ile farkı göstermek için yararlıdır.",
                },
                {
                    "word": "Hund",
                    "article": "der",
                    "plural": "die Hunde",
                    "meanings": ["köpek"],
                    "example_de": "Unser Hund ist klein.",
                    "example_tr": "Bizim köpeğimiz küçüktür.",
                    "note": "aile çevresi içinde geçen canlı varlık örneği.",
                },
                {
                    "word": "Katze",
                    "article": "die",
                    "plural": "die Katzen",
                    "meanings": ["kedi"],
                    "example_de": "Ihre Katze ist ruhig.",
                    "example_tr": "Onun kedisi sakindir.",
                    "note": "ev ve sahiplik bağlamında doğal bir isimdir.",
                },
            ],
            "exercises": [
                {
                    "id": "haben",
                    "type": "single_choice",
                    "title": "haben Fiili Testi",
                    "description": "Özneye göre doğru haben çekimini seç.",
                    "questions": [
                        {
                            "prompt": "Ich ___ eine Schwester.",
                            "options": ["hast", "habe", "hat"],
                            "correct_index": 1,
                            "explanation": "ich ile haben fiili habe olur.",
                        },
                        {
                            "prompt": "Du ___ ein Handy.",
                            "options": ["hast", "haben", "habt"],
                            "correct_index": 0,
                            "explanation": "du ile doğru biçim hast olur.",
                        },
                        {
                            "prompt": "Er ___ einen Bruder.",
                            "options": ["habe", "hat", "haben"],
                            "correct_index": 1,
                            "explanation": "er ile haben fiili hat olur.",
                        },
                        {
                            "prompt": "Wir ___ zwei Bücher.",
                            "options": ["habt", "haben", "hat"],
                            "correct_index": 1,
                            "explanation": "wir ile temel çoğul biçim haben kullanılır.",
                        },
                        {
                            "prompt": "Ihr ___ eine Wohnung.",
                            "options": ["habt", "hast", "haben"],
                            "correct_index": 0,
                            "explanation": "ihr ile habt kullanılır.",
                        },
                        {
                            "prompt": "Sie ___ eine Familie.",
                            "options": ["haben", "hat", "habe"],
                            "correct_index": 0,
                            "explanation": "sie / Sie ile çoğul-resmî biçim haben olur.",
                        },
                    ],
                },
                {
                    "id": "possessives",
                    "type": "single_choice",
                    "title": "İyelik Kalıbı Testi",
                    "description": "İsme uygun iyelik biçimini seç.",
                    "questions": [
                        {
                            "prompt": "Bu benim annem. -> Das ist ___ Mutter.",
                            "options": ["mein", "meine", "meinen"],
                            "correct_index": 1,
                            "explanation": "Mutter dişil olduğu için meine gerekir.",
                        },
                        {
                            "prompt": "Bu benim babam. -> Das ist ___ Vater.",
                            "options": ["mein", "meine", "meinen"],
                            "correct_index": 0,
                            "explanation": "Vater eril isimdir; temel biçim mein Vater olur.",
                        },
                        {
                            "prompt": "Bu senin çantan mı? -> Ist das ___ Tasche?",
                            "options": ["dein", "deine", "deinen"],
                            "correct_index": 1,
                            "explanation": "Tasche dişil olduğu için deine gerekir.",
                        },
                        {
                            "prompt": "Onun bilgisayarı yeni. -> ___ Computer ist neu.",
                            "options": ["Sein", "Seine", "Seinen"],
                            "correct_index": 0,
                            "explanation": "Computer eril görünse de burada temel kalıp sein Computer olur.",
                        },
                        {
                            "prompt": "Bizim evimiz küçük. -> ___ Wohnung ist klein.",
                            "options": ["Unser", "Unsere", "Unseren"],
                            "correct_index": 1,
                            "explanation": "Wohnung dişil olduğu için unsere gerekir.",
                        },
                    ],
                },
                {
                    "id": "family",
                    "type": "single_choice",
                    "title": "Aile Kelimeleri Testi",
                    "description": "Aile bireylerini doğru anlam grubuyla eşleştir.",
                    "questions": [
                        {
                            "prompt": "die Mutter",
                            "options": ["anne", "kız kardeş", "kız evlat"],
                            "correct_index": 0,
                            "explanation": "Mutter = anne.",
                        },
                        {
                            "prompt": "der Bruder",
                            "options": ["erkek kardeş", "baba", "oğul"],
                            "correct_index": 0,
                            "explanation": "Bruder = erkek kardeş.",
                        },
                        {
                            "prompt": "die Tochter",
                            "options": ["anne", "kız evlat", "kız kardeş"],
                            "correct_index": 1,
                            "explanation": "Tochter = kız evlat / kız çocuk.",
                        },
                        {
                            "prompt": "der Sohn",
                            "options": ["oğul", "erkek kardeş", "baba"],
                            "correct_index": 0,
                            "explanation": "Sohn = oğul.",
                        },
                        {
                            "prompt": "die Familie",
                            "options": ["aile", "ev", "oda"],
                            "correct_index": 0,
                            "explanation": "Familie = aile.",
                        },
                    ],
                },
                {
                    "id": "objects",
                    "type": "single_choice",
                    "title": "Günlük Nesneler Testi",
                    "description": "Günlük nesne kelimelerini anlamıyla eşleştir.",
                    "questions": [
                        {
                            "prompt": "der Schlüssel",
                            "options": ["anahtar", "çanta", "saat"],
                            "correct_index": 0,
                            "explanation": "Schlüssel = anahtar.",
                        },
                        {
                            "prompt": "das Handy",
                            "options": ["telefon", "fotoğraf", "bilgisayar"],
                            "correct_index": 0,
                            "explanation": "Handy = cep telefonu.",
                        },
                        {
                            "prompt": "die Tasche",
                            "options": ["çanta", "kedi", "kalem"],
                            "correct_index": 0,
                            "explanation": "Tasche = çanta.",
                        },
                        {
                            "prompt": "das Foto",
                            "options": ["fotoğraf", "oda", "ev"],
                            "correct_index": 0,
                            "explanation": "Foto = fotoğraf.",
                        },
                        {
                            "prompt": "die Uhr",
                            "options": ["saat", "ödev", "soru"],
                            "correct_index": 0,
                            "explanation": "Uhr = saat.",
                        },
                    ],
                },
                {
                    "id": "gaps",
                    "type": "single_choice",
                    "title": "Boşluk Doldurma",
                    "description": "Aile, sahiplik ve nesne kalıplarını doğru tamamla.",
                    "questions": [
                        {
                            "prompt": "Das ist ___ Vater.",
                            "options": ["meine", "mein", "meinen"],
                            "correct_index": 1,
                            "explanation": "Vater için mein gerekir.",
                        },
                        {
                            "prompt": "Ich ___ zwei Brüder.",
                            "options": ["habe", "hast", "hat"],
                            "correct_index": 0,
                            "explanation": "ich ile habe kullanılır.",
                        },
                        {
                            "prompt": "Ist das ___ Handy?",
                            "options": ["dein", "deine", "deinen"],
                            "correct_index": 0,
                            "explanation": "Handy nötr isimdir; temel biçim dein Handy olur.",
                        },
                        {
                            "prompt": "Wo ist ___ Tasche?",
                            "options": ["mein", "meine", "meiner"],
                            "correct_index": 1,
                            "explanation": "Tasche dişil olduğu için meine gerekir.",
                        },
                        {
                            "prompt": "Unsere ___ ist klein.",
                            "options": ["Zimmer", "Wohnung", "Computer"],
                            "correct_index": 1,
                            "explanation": "Unsere Wohnung ist klein en doğal tamamlamadır.",
                        },
                        {
                            "prompt": "Sein ___ ist neu.",
                            "options": ["Mutter", "Computer", "Schwester"],
                            "correct_index": 1,
                            "explanation": "Sein Computer ist neu cümlesi bu dersin temel örneklerinden biridir.",
                        },
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "haben, iyelik ve günlük nesne mantığını birlikte kontrol et.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Du habe einen Bruder.", "Du hast einen Bruder.", "Du hat einen Bruder."],
                            "correct_index": 1,
                            "explanation": "du ile doğru biçim hast olur.",
                        },
                        {
                            "prompt": "Hangisi sahiplik cümlesidir?",
                            "options": ["Das ist meine Mutter.", "Meine ist Mutter.", "Das meine Mutter."],
                            "correct_index": 0,
                            "explanation": "Doğru iyelik yapısı Das ist meine Mutter olur.",
                        },
                        {
                            "prompt": "Hangisi doğru soru cümlesidir?",
                            "options": ["Ist das deine Tasche?", "Das ist deine Tasche?", "Deine Tasche ist das?"],
                            "correct_index": 0,
                            "explanation": "Evet-hayır sorusunda fiil başa gelir.",
                        },
                        {
                            "prompt": "Hangisi doğru anlam eşleşmesidir?",
                            "options": ["Schlüssel = çanta", "Wohnung = ev / daire", "Sohn = kız evlat"],
                            "correct_index": 1,
                            "explanation": "Wohnung = ev / daire.",
                        },
                        {
                            "prompt": "Bu dersin ana hedefi nedir?",
                            "options": [
                                "Aile ve sahiplik ilişkisini temel kalıplarla anlatabilmek",
                                "Tüm hâl bilgilerini bitirmek",
                                "Uzun edebî mektup yazmak",
                            ],
                            "correct_index": 0,
                            "explanation": "Bu dersin ana odağı aile, sahiplik ve günlük nesne kalıplarını oturtmaktır.",
                        },
                    ],
                },
            ],
            "homework": [
                "Aileni 6 kısa cümleyle tanıt: anne, baba, kardeş, oda, telefon, çanta gibi kelimeler kullan.",
                "haben fiilini tüm öznelerle sesli tekrar et ve her özne için bir sahiplik cümlesi kur.",
                "mein / meine ve dein / deine çiftlerini örneklerle karşılaştır.",
                "Okuma metnindeki nesneleri kendi odandaki gerçek nesnelerle eşleştir.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde artık yalnız kimlik vermekle kalmayıp aileni tanıtabiliyor, "
                "günlük eşyalar hakkında sahiplik belirtebiliyor ve kısa soru-cevap akışında sahiplik sorabiliyor olmalısın."
            ),
            "next_lesson": {
                "title": "Ders 6: Günlük rutinler ve zaman ifadeleri",
                "status": "active",
                "slug": "ders-6-gunluk-rutinler-ve-zaman-ifadeleri",
            },
        },
        {
            "slug": "ders-6-gunluk-rutinler-ve-zaman-ifadeleri",
            "index": 6,
            "title": "Günlük Rutinler ve Zaman İfadeleri",
            "duration": "85-100 dk",
            "difficulty": "A1.2",
            "teaser": (
                "Bu derste günlük hayatı anlatmaya başlıyoruz: sabah ne yapıyorsun, ne zaman çalışıyorsun, "
                "hafta içi ve hafta sonu nasıl bir rutinin var? Zaman ifadeleri, sıklık zarfları ve kısa rutin cümleleri "
                "bir araya gelerek Almanca'yı daha akışlı kullanmanı sağlayacak."
            ),
            "status": "active",
            "objectives": [
                "Günlük rutin anlatan temel fiilleri kullanmak.",
                "morgens, mittags, abends, heute, jeden Tag ve am Wochenende gibi zaman ifadelerini tanımak.",
                "wann sorusunu anlayıp um ... Uhr kalıbıyla cevap vermek.",
                "Zaman ifadesi başa geldiğinde fiilin ikinci sırada kaldığını fark etmek.",
                "Günlük hayatını 5-6 cümleyle anlatmaya yaklaşmak.",
                "Önceki derslerin kişi, şehir, sahiplik ve nesne bilgisini rutine bağlamak.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "22"},
                {"label": "Gramer odağı", "value": "rutin + zaman"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Rutin anlatmak dili gerçek hayata taşır",
                    "body": (
                        "Kim olduğunu söylemek başlangıçtır; ama dili gerçekten kullanmaya başlamak için ne yaptığını "
                        "ve bunu ne zaman yaptığını anlatabilmelisin. Bu ders tam olarak bu geçişi kurar."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "Zaman kelimesi cümlede yön verici olur",
                    "body": (
                        "heute, morgens, am Abend, um 8 Uhr gibi ifadeler cümlenin zaman eksenini belirler. "
                        "Erken aşamada bunları hazır bloklar olarak duymak gerekir."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "wann sorusu yeni bir kapı açar",
                    "body": (
                        "wo ve was sorularını gördük; şimdi wann ile zaman sormaya başlıyoruz. "
                        "Wann arbeitest du?, Wann lernst du? gibi sorular gündelik konuşmanın temelidir."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Zaman başa geçse bile fiil ikinci sırayı bırakmaz",
                    "body": (
                        "Heute lerne ich Deutsch., Am Abend arbeite ich. gibi cümlelerde zaman ifadesi öne gelebilir; "
                        "ama çekimli fiil yine ikinci sırada kalır. Bu, A1 için kritik bir cümle düzeni kuralıdır."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Sıklık ve saat bilgisi rutini somutlaştırır",
                    "body": (
                        "oft, immer, manchmal, um 7 Uhr, am Wochenende gibi parçalar rutini daha gerçek kılar. "
                        "Böylece artık sadece tek cümle değil, küçük bir gün akışı kurabilirsin."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Rutin fiilleri",
                    "summary": "Bu derste özellikle günlük hayatı anlatan fiillere odaklanıyoruz.",
                    "items": [
                        "lernen = öğrenmek / ders çalışmak",
                        "arbeiten = çalışmak",
                        "frühstücken = kahvaltı yapmak",
                        "kochen = yemek pişirmek",
                        "telefonieren = telefon konuşması yapmak",
                        "schlafen = uyumak",
                    ],
                    "examples": [
                        "Ich frühstücke morgens.",
                        "Wir arbeiten heute.",
                        "Sie telefoniert am Abend.",
                    ],
                },
                {
                    "title": "Temel zaman ifadeleri",
                    "summary": "Önce hazır kalıp olarak tanı; sonra cümle içinde tekrar et.",
                    "items": [
                        "heute = bugün",
                        "morgens = sabahları",
                        "mittags = öğlenleri",
                        "abends = akşamları",
                        "jeden Tag = her gün",
                        "am Wochenende = hafta sonunda",
                    ],
                    "examples": [
                        "Ich lerne heute Deutsch.",
                        "Er arbeitet morgens.",
                        "Wir spielen am Wochenende Musik.",
                    ],
                },
                {
                    "title": "am, um ve yalın zaman zarfları",
                    "summary": "Erken A1'de saat, gün ve genel zaman ifadesini birbirinden ayırmak gerekir.",
                    "items": [
                        "um 8 Uhr = saat 8'de",
                        "am Samstag = cumartesi günü",
                        "am Wochenende = hafta sonunda / hafta sonları",
                        "heute, morgens, abends gibi kelimeler çoğu zaman ek edat istemez",
                    ],
                    "examples": [
                        "Ich arbeite um 8 Uhr.",
                        "Am Samstag koche ich.",
                        "Heute lerne ich Deutsch.",
                    ],
                },
                {
                    "title": "Saat sorma ve söyleme",
                    "summary": "İlk aşamada tam saatleri öğrenmek yeterlidir.",
                    "items": [
                        "Wann ...? = Ne zaman ...?",
                        "um 7 Uhr = saat 7'de",
                        "um 8 Uhr = saat 8'de",
                        "um 10 Uhr = saat 10'da",
                    ],
                    "examples": [
                        "Wann arbeitest du? Um 8 Uhr.",
                        "Wann lernst du? Am Abend.",
                    ],
                },
                {
                    "title": "Zaman ifadesi öndeyse fiil ikinci sırada kalır",
                    "summary": "Bu dersin kritik dizilim kuralı budur.",
                    "items": [
                        "Ich lerne heute Deutsch.",
                        "Heute lerne ich Deutsch.",
                        "Am Abend arbeitet er.",
                        "Morgens frühstücken wir zusammen.",
                    ],
                    "examples": [
                        "Heute arbeite ich im Café.",
                        "Am Wochenende lernt sie Deutsch.",
                    ],
                },
                {
                    "title": "Kısa rutin anlatımı kurma",
                    "summary": "Günün küçük parçalarını art arda koyarak akış oluşturuyoruz.",
                    "items": [
                        "Morgens frühstücke ich.",
                        "Danach lerne ich Deutsch.",
                        "Am Nachmittag arbeite ich.",
                        "Abends telefoniere ich mit meiner Familie.",
                    ],
                    "examples": [
                        "Heute lerne ich Deutsch und arbeite am Abend.",
                        "Am Wochenende koche ich und schlafe lange.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Ich frühstücke morgens.", "tr": "Sabahları kahvaltı yaparım.", "note": "rutin fiili + zaman zarfı örneği."},
                {"de": "Heute lerne ich Deutsch.", "tr": "Bugün Almanca çalışıyorum.", "note": "zaman başa geçtiğinde fiilin ikinci sırada kalmasını gösterir."},
                {"de": "Wann arbeitest du?", "tr": "Ne zaman çalışıyorsun?", "note": "wann sorusunun en temel kullanımı."},
                {"de": "Ich arbeite um 8 Uhr.", "tr": "Saat 8'de çalışıyorum.", "note": "tam saat kalıbı."},
                {"de": "Am Abend telefoniere ich mit meiner Mutter.", "tr": "Akşam annemle telefonda konuşuyorum.", "note": "zaman + fiil + aile bilgisi birleşimi."},
                {"de": "Wir kochen mittags.", "tr": "Öğlenleri yemek yapıyoruz.", "note": "çoğul özne ile rutin cümlesi."},
                {"de": "Er schläft oft lange.", "tr": "O sık sık uzun uyur.", "note": "sıklık zarfı ile rutin cümlesi."},
                {"de": "Spielst du am Wochenende Musik?", "tr": "Hafta sonunda müzik çalıyor musun?", "note": "evet-hayır sorusu + zaman ifadesi."},
                {"de": "Ja, ich spiele am Samstag.", "tr": "Evet, cumartesi çalıyorum / oynuyorum.", "note": "kısa cevap ve zaman bilgisi."},
                {"de": "Meine Schwester lernt jeden Tag.", "tr": "Kız kardeşim her gün çalışır / öğrenir.", "note": "günlük tekrar alışkanlığı."},
                {"de": "Wann telefonierst du?", "tr": "Ne zaman telefonlaşıyorsun?", "note": "soru kalıbını pekiştirir."},
                {"de": "Ich schlafe um 11 Uhr.", "tr": "Saat 11'de uyurum / uyuyorum.", "note": "basit saat bildirimi."},
                {"de": "Am Samstag koche ich zu Hause.", "tr": "Cumartesi günü evde yemek yaparım.", "note": "am ile gün kullanımını açıkça gösterir."},
            ],
            "common_mistakes": [
                {
                    "wrong": "Heute ich lerne Deutsch.",
                    "right": "Heute lerne ich Deutsch.",
                    "reason": "Zaman ifadesi başa geçse bile çekimli fiil ikinci sırada kalır.",
                },
                {
                    "wrong": "Wann du arbeitest?",
                    "right": "Wann arbeitest du?",
                    "reason": "Soru kelimesinden sonra çekimli fiil gelir.",
                },
                {
                    "wrong": "Ich arbeite 8 Uhr.",
                    "right": "Ich arbeite um 8 Uhr.",
                    "reason": "Saat söylerken um edatı gerekir.",
                },
                {
                    "wrong": "um Samstag / um Wochenende demek",
                    "right": "am Samstag / am Wochenende demek",
                    "reason": "Saatlerde um, gün ve hafta sonu gibi zaman bloklarında am kullanılır.",
                },
                {
                    "wrong": "morgens ve Morgen'i aynı şey sanmak",
                    "right": "Morgen çoğu zaman isim veya 'yarın' bağlamı taşır; morgens ise sabahları anlamında zarftır",
                    "reason": "Biçim benzer görünse de işlevleri farklıdır.",
                },
                {
                    "wrong": "Sıklık zarflarını cümleden kopuk ezberlemek",
                    "right": "oft, immer, manchmal gibi kelimeleri tam cümle içinde çalışmak",
                    "reason": "Bu kelimeler bağlam içinde öğrenildiğinde çok daha kalıcı olur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Wann lernst du Deutsch?", "text_tr": "Ne zaman Almanca çalışıyorsun?"},
                    {"speaker": "B", "text_de": "Heute lerne ich am Abend. Und du?", "text_tr": "Bugün akşam çalışıyorum. Ya sen?"},
                    {"speaker": "A", "text_de": "Morgens arbeite ich und mittags koche ich.", "text_tr": "Sabahları çalışıyorum, öğlenleri yemek yapıyorum."},
                    {"speaker": "B", "text_de": "Telefonierst du am Abend mit deiner Familie?", "text_tr": "Akşam ailenle telefonlaşıyor musun?"},
                    {"speaker": "A", "text_de": "Ja, oft telefoniere ich um 9 Uhr.", "text_tr": "Evet, sık sık saat 9'da telefonlaşıyorum."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Bir günün akışı",
                    "intro": "Bu metin önceki derslerin kişi, aile, şehir, sahiplik ve fiil bilgisini zaman ekseniyle birleştirir.",
                    "word_focus": "18 kelime / kalıp",
                    "paragraphs": [
                        "[[Morgens::sabahları]] lerne ich Deutsch und ich [[frühstücke::kahvaltı yapıyorum]] mit meiner [[Mutter::anne]]. Heute [[trinke::içiyorum]] ich [[Kaffee::kahve]] und mein Bruder liest ein Buch.",
                        "[[Um 8 Uhr::saat 8'de]] arbeite ich im [[Café::kafe]]. [[Mittags::öğlenleri]] koche ich manchmal und danach [[telefoniere::telefonlaşıyorum]] ich mit meiner [[Familie::aile]].",
                        "[[Am Abend::akşam]] bin ich in unserer [[Wohnung::ev / daire]]. Meine Schwester [[lernt::öğreniyor]] oft, mein Vater [[schläft::uyuyor]] spät und ich frage: [[Wann arbeitest du?::Ne zaman çalışıyorsun?]]",
                    ],
                },
            ],
            "tips": [
                "Rutin cümlelerini sırayla kur: sabah, öğlen, akşam şeklinde düşün.",
                "wann sorusunu um ... Uhr ve am Abend gibi iki farklı cevap tipiyle çalış.",
                "Zaman başa geçtiğinde fiilin ikinci sırada kaldığını mutlaka sesli tekrar et.",
                "Okuma metnindeki zaman kelimelerini günün gerçek saatleriyle ilişkilendir.",
                "Önceki derslerden gelen aile ve eşya kelimelerini bu derste yeniden kullan.",
            ],
            "vocabulary": [
                {
                    "word": "frühstücken",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["kahvaltı yapmak"],
                    "example_de": "Ich frühstücke morgens.",
                    "example_tr": "Sabahları kahvaltı yaparım.",
                    "note": "Günlük rutinlerin en temel fiillerinden biridir.",
                },
                {
                    "word": "kochen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["yemek yapmak", "pişirmek"],
                    "example_de": "Wir kochen mittags.",
                    "example_tr": "Öğlenleri yemek yapıyoruz.",
                    "note": "Rutin ve ev hayatı bağlamında çok kullanılır.",
                },
                {
                    "word": "telefonieren",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["telefonlaşmak", "telefonla konuşmak"],
                    "example_de": "Ich telefoniere am Abend.",
                    "example_tr": "Akşam telefonlaşırım.",
                    "note": "Aile ve arkadaşlarla rutin iletişim için uygundur.",
                },
                {
                    "word": "schlafen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["uyumak"],
                    "example_de": "Er schläft spät.",
                    "example_tr": "O geç uyur.",
                    "note": "Bu derste gündelik rutin fiili olarak tanıtılır; çekimde biçim değişimi fark edilir.",
                },
                {
                    "word": "morgens",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["sabahları"],
                    "example_de": "Morgens lerne ich Deutsch.",
                    "example_tr": "Sabahları Almanca çalışırım.",
                    "note": "Zaman zarfı olarak sık kullanılır.",
                },
                {
                    "word": "mittags",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["öğlenleri"],
                    "example_de": "Mittags koche ich.",
                    "example_tr": "Öğlenleri yemek yaparım.",
                    "note": "Günün ortasını anlatan zaman zarfıdır.",
                },
                {
                    "word": "abends",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["akşamları"],
                    "example_de": "Abends telefoniere ich.",
                    "example_tr": "Akşamları telefonlaşırım.",
                    "note": "Akşam rutini için kullanılır.",
                },
                {
                    "word": "heute",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["bugün"],
                    "example_de": "Heute arbeite ich.",
                    "example_tr": "Bugün çalışıyorum.",
                    "note": "Zaman ifadesi başa da gelebilir.",
                },
                {
                    "word": "jeden Tag",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["her gün"],
                    "example_de": "Sie lernt jeden Tag.",
                    "example_tr": "O her gün çalışır.",
                    "note": "Sıklık ve alışkanlık bildirir.",
                },
                {
                    "word": "am Wochenende",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["hafta sonunda", "hafta sonları"],
                    "example_de": "Am Wochenende spiele ich Musik.",
                    "example_tr": "Hafta sonunda müzik çalarım.",
                    "note": "Hafta içi / hafta sonu ayrımı için temel kalıptır.",
                },
                {
                    "word": "wann",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["ne zaman"],
                    "example_de": "Wann arbeitest du?",
                    "example_tr": "Ne zaman çalışıyorsun?",
                    "note": "Zaman sormanın temel soru kelimesidir.",
                },
                {
                    "word": "Uhr",
                    "article": "die",
                    "plural": "die Uhren",
                    "meanings": ["saat"],
                    "example_de": "Um 8 Uhr arbeite ich.",
                    "example_tr": "Saat 8'de çalışırım.",
                    "note": "Saat bildirirken um ile birlikte sık geçer.",
                },
                {
                    "word": "spät",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["geç"],
                    "example_de": "Er schläft spät.",
                    "example_tr": "O geç uyur.",
                    "note": "Zaman niteliğini anlatan temel zarflardandır.",
                },
                {
                    "word": "früh",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["erken"],
                    "example_de": "Ich arbeite früh.",
                    "example_tr": "Erken çalışırım.",
                    "note": "spät ile karşıt anlamlıdır.",
                },
                {
                    "word": "immer",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["her zaman", "daima"],
                    "example_de": "Sie lernt immer morgens.",
                    "example_tr": "O her zaman sabahları çalışır.",
                    "note": "Sıklık zarfı olarak çok kullanılır.",
                },
                {
                    "word": "manchmal",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["bazen"],
                    "example_de": "Manchmal koche ich abends.",
                    "example_tr": "Bazen akşamları yemek yaparım.",
                    "note": "Rutin içindeki değişkenliği gösterir.",
                },
                {
                    "word": "danach",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["ondan sonra", "sonrasında"],
                    "example_de": "Danach arbeite ich.",
                    "example_tr": "Ondan sonra çalışırım.",
                    "note": "Olay sıralamak için yararlıdır.",
                },
                {
                    "word": "zusammen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["birlikte"],
                    "example_de": "Wir frühstücken zusammen.",
                    "example_tr": "Birlikte kahvaltı yaparız.",
                    "note": "Aile ve arkadaş rutini anlatımında kullanılır.",
                },
                {
                    "word": "Samstag",
                    "article": "der",
                    "plural": "die Samstage",
                    "meanings": ["cumartesi"],
                    "example_de": "Am Samstag spiele ich Musik.",
                    "example_tr": "Cumartesi müzik çalarım.",
                    "note": "Hafta sonu rutini için ilk gün örneğidir.",
                },
                {
                    "word": "Sonntag",
                    "article": "der",
                    "plural": "die Sonntage",
                    "meanings": ["pazar"],
                    "example_de": "Am Sonntag schlafe ich lange.",
                    "example_tr": "Pazar günü uzun uyurum.",
                    "note": "Hafta sonu akışını kurmak için yararlıdır.",
                },
                {
                    "word": "lesen",
                    "article": "-",
                    "plural": "-",
                    "meanings": ["okumak"],
                    "example_de": "Mein Bruder liest ein Buch.",
                    "example_tr": "Erkek kardeşim kitap okur.",
                    "note": "Okuma rutini ve kitap kelimesiyle bağ kurar.",
                },
                {
                    "word": "Tag",
                    "article": "der",
                    "plural": "die Tage",
                    "meanings": ["gün"],
                    "example_de": "Jeden Tag lerne ich.",
                    "example_tr": "Her gün çalışırım.",
                    "note": "Zaman ifadesi içinde tekrar karşına çıkar.",
                },
            ],
            "exercises": [
                {
                    "id": "routine-verbs",
                    "type": "single_choice",
                    "title": "Rutin Fiilleri Testi",
                    "description": "Özneye göre doğru fiil biçimini seç.",
                    "questions": [
                        {
                            "prompt": "Ich ___ morgens.",
                            "options": ["frühstücke", "frühstückst", "frühstückt"],
                            "correct_index": 0,
                            "explanation": "ich ile doğru biçim frühstücke olur.",
                        },
                        {
                            "prompt": "Du ___ heute?",
                            "options": ["arbeitest", "arbeiten", "arbeitet"],
                            "correct_index": 0,
                            "explanation": "du ile çalışmak fiili arbeitest olur.",
                        },
                        {
                            "prompt": "Er ___ am Abend.",
                            "options": ["telefoniere", "telefoniert", "telefonieren"],
                            "correct_index": 1,
                            "explanation": "er ile telefoniert kullanılır.",
                        },
                        {
                            "prompt": "Wir ___ mittags.",
                            "options": ["kocht", "kochen", "kochst"],
                            "correct_index": 1,
                            "explanation": "wir ile kochen biçimi gelir.",
                        },
                        {
                            "prompt": "Ihr ___ spät.",
                            "options": ["schlaft", "schlafen", "schläft"],
                            "correct_index": 0,
                            "explanation": "ihr ile schlafen fiilinin bu dersteki temel çoğul biçimi schlaft olarak çalışılır.",
                        },
                        {
                            "prompt": "Sie ___ ein Buch.",
                            "options": ["lesen", "liest", "lese"],
                            "correct_index": 0,
                            "explanation": "sie / Sie ile çoğul-resmî biçim lesen kullanılır.",
                        },
                    ],
                },
                {
                    "id": "time-words",
                    "type": "single_choice",
                    "title": "Zaman İfadeleri Testi",
                    "description": "Zaman ifadesini doğru anlamla eşleştir.",
                    "questions": [
                        {
                            "prompt": "morgens",
                            "options": ["sabahları", "öğlenleri", "akşamları"],
                            "correct_index": 0,
                            "explanation": "morgens = sabahları.",
                        },
                        {
                            "prompt": "am Wochenende",
                            "options": ["hafta sonunda", "her gün", "saat 8'de"],
                            "correct_index": 0,
                            "explanation": "am Wochenende = hafta sonunda / hafta sonları.",
                        },
                        {
                            "prompt": "jeden Tag",
                            "options": ["her gün", "bugün", "bazen"],
                            "correct_index": 0,
                            "explanation": "jeden Tag = her gün.",
                        },
                        {
                            "prompt": "wann",
                            "options": ["nasıl", "ne zaman", "nereden"],
                            "correct_index": 1,
                            "explanation": "wann = ne zaman.",
                        },
                        {
                            "prompt": "um 8 Uhr",
                            "options": ["saat 8'de", "8 gün", "8 kere"],
                            "correct_index": 0,
                            "explanation": "um 8 Uhr = saat 8'de.",
                        },
                    ],
                },
                {
                    "id": "word-order",
                    "type": "single_choice",
                    "title": "Cümle Dizimi Testi",
                    "description": "Zaman ifadesi ve fiil sırasını doğru kur.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Heute ich lerne Deutsch.", "Heute lerne ich Deutsch.", "Ich heute lerne Deutsch."],
                            "correct_index": 1,
                            "explanation": "Zaman ifadesi başa geçince fiil ikinci sırada kalır.",
                        },
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Wann du arbeitest?", "Wann arbeitest du?", "Du arbeitest wann?"],
                            "correct_index": 1,
                            "explanation": "wann sonrasında çekimli fiil gelir.",
                        },
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Am Abend telefoniere ich.", "Am Abend ich telefoniere.", "Ich telefoniere am Abend?"],
                            "correct_index": 0,
                            "explanation": "Am Abend + fiil + özne dizilimi burada doğrudur.",
                        },
                        {
                            "prompt": "Hangisi evet-hayır sorusudur?",
                            "options": ["Spielst du am Wochenende Musik?", "Du spielst am Wochenende Musik?", "Am Wochenende du spielst Musik?"],
                            "correct_index": 0,
                            "explanation": "Fiil başa geçtiği için evet-hayır sorusudur.",
                        },
                        {
                            "prompt": "Hangisi doğrudur?",
                            "options": ["Um 8 Uhr arbeite ich.", "Um 8 Uhr ich arbeite.", "Ich um 8 Uhr arbeite."],
                            "correct_index": 0,
                            "explanation": "Saat ifadesi baştayken fiil ikinci sırada kalır.",
                        },
                    ],
                },
                {
                    "id": "meaning",
                    "type": "single_choice",
                    "title": "Kalıp ve Anlam Testi",
                    "description": "Rutin cümlelerini anlamıyla eşleştir.",
                    "questions": [
                        {
                            "prompt": "Wann arbeitest du?",
                            "options": ["Ne zaman çalışıyorsun?", "Nerede çalışıyorsun?", "Neden çalışıyorsun?"],
                            "correct_index": 0,
                            "explanation": "wann zaman sorar.",
                        },
                        {
                            "prompt": "Ich frühstücke morgens.",
                            "options": ["Sabahları kahvaltı yaparım.", "Sabahları çalışırım.", "Sabahları uyurum."],
                            "correct_index": 0,
                            "explanation": "frühstücken = kahvaltı yapmak.",
                        },
                        {
                            "prompt": "Am Wochenende spiele ich Musik.",
                            "options": ["Hafta sonunda müzik çalarım.", "Hafta sonunda kahve içerim.", "Hafta sonunda işe giderim."],
                            "correct_index": 0,
                            "explanation": "spielen Musik burada müzik çalmak / yapmak anlamındadır.",
                        },
                        {
                            "prompt": "Heute lerne ich Deutsch.",
                            "options": ["Bugün Almanca çalışıyorum.", "Bugün Almanya'dan geliyorum.", "Bugün ailemi arıyorum."],
                            "correct_index": 0,
                            "explanation": "Bugün + öğrenmek kalıbı doğru eşleşir.",
                        },
                        {
                            "prompt": "Meine Schwester lernt jeden Tag.",
                            "options": ["Kız kardeşim her gün çalışır.", "Kız kardeşim bugün uyur.", "Kız kardeşim saat 8'de gelir."],
                            "correct_index": 0,
                            "explanation": "jeden Tag = her gün.",
                        },
                    ],
                },
                {
                    "id": "gaps",
                    "type": "single_choice",
                    "title": "Boşluk Doldurma",
                    "description": "Rutin ve zaman kalıplarını doğru tamamla.",
                    "questions": [
                        {
                            "prompt": "Ich arbeite ___ 8 Uhr.",
                            "options": ["in", "um", "am"],
                            "correct_index": 1,
                            "explanation": "Saatten önce um gelir.",
                        },
                        {
                            "prompt": "___ lernst du Deutsch? Am Abend.",
                            "options": ["Wer", "Wann", "Wie"],
                            "correct_index": 1,
                            "explanation": "Zaman sormak için wann gerekir.",
                        },
                        {
                            "prompt": "___ Samstag koche ich zu Hause.",
                            "options": ["Um", "Am", "Heute"],
                            "correct_index": 1,
                            "explanation": "Gün ve hafta sonu gibi zaman bloklarında am kullanılır.",
                        },
                        {
                            "prompt": "Heute ___ ich im Café.",
                            "options": ["arbeite", "arbeitest", "arbeitet"],
                            "correct_index": 0,
                            "explanation": "ich ile arbeite kullanılır.",
                        },
                        {
                            "prompt": "Am Wochenende ___ wir Musik.",
                            "options": ["spiele", "spielen", "spielt"],
                            "correct_index": 1,
                            "explanation": "wir ile spielen biçimi gelir.",
                        },
                        {
                            "prompt": "Morgens ___ ich Kaffee.",
                            "options": ["trinke", "trinkst", "trinkt"],
                            "correct_index": 0,
                            "explanation": "ich ile trinke olur.",
                        },
                        {
                            "prompt": "Meine Mutter ___ abends.",
                            "options": ["telefonierst", "telefoniert", "telefonieren"],
                            "correct_index": 1,
                            "explanation": "Üçüncü tekilde telefoniert gerekir.",
                        },
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Rutin, zaman ve cümle dizimi mantığını topluca yokla.",
                    "questions": [
                        {
                            "prompt": "Hangisi doğru zaman cümlesidir?",
                            "options": ["Heute ich arbeite.", "Heute arbeite ich.", "Ich arbeite heute?"],
                            "correct_index": 1,
                            "explanation": "Zaman ifadesi başa geldiğinde fiil ikinci sırada kalır.",
                        },
                        {
                            "prompt": "Hangisi doğru soru cümlesidir?",
                            "options": ["Wann du kochst?", "Wann kochst du?", "Du kochst wann?"],
                            "correct_index": 1,
                            "explanation": "wann + fiil + özne dizilimi gerekir.",
                        },
                        {
                            "prompt": "Hangisi doğru saat kalıbıdır?",
                            "options": ["Ich lerne 7 Uhr.", "Ich lerne um 7 Uhr.", "Ich um 7 Uhr lerne."],
                            "correct_index": 1,
                            "explanation": "Saat bildirirken um kullanılır.",
                        },
                        {
                            "prompt": "Hangisi doğru gün / zaman eşleşmesidir?",
                            "options": ["um Samstag", "am Samstag", "in Samstag"],
                            "correct_index": 1,
                            "explanation": "Gün adıyla temel kullanım am Samstag olur.",
                        },
                        {
                            "prompt": "Hangisi doğru anlam eşleşmesidir?",
                            "options": ["morgens = akşamları", "abends = akşamları", "wann = nerede"],
                            "correct_index": 1,
                            "explanation": "abends = akşamları.",
                        },
                        {
                            "prompt": "Bu dersin ana hedefi nedir?",
                            "options": [
                                "Rutin ve zaman anlatımında temel akışı kurmak",
                                "Tüm düzensiz fiilleri bitirmek",
                                "Geçmiş zaman yazmak",
                            ],
                            "correct_index": 0,
                            "explanation": "Bu dersin ana odağı günlük rutin ve zaman ifadeleridir.",
                        },
                    ],
                },
            ],
            "homework": [
                "Kendi gününü sabah, öğlen, akşam ve gece olarak 6 cümleyle anlat.",
                "wann sorusunu kullanarak en az 4 soru ve 4 cevap yaz.",
                "Bugün ve hafta sonu için ayrı iki mini rutin paragrafı kur.",
                "Okuma metnindeki zaman ifadelerini gerçek hayatındaki saatlerle eşleştir.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde artık yalnız tek tek bilgi veren cümleler değil, küçük bir gün akışı kurabiliyor "
                "olmalısın. Rutin anlatımı, zaman ifadeleri ve soru düzeni A1 seviyesinde gerçek iletişimin önemli eşiğidir."
            ),
            "next_lesson": {
                "title": "Ders 7: Belirsiz artikeller, olumsuzluk ve mekân soruları",
                "status": "active",
                "slug": "ders-7-belirsiz-artikeller-olumsuzluk-ve-mekan-sorulari",
            },
        },
        {
            "slug": "ders-7-belirsiz-artikeller-olumsuzluk-ve-mekan-sorulari",
            "index": 7,
            "title": "Belirsiz Artikeller, Olumsuzluk ve Mekân Soruları",
            "duration": "85-100 dk",
            "difficulty": "A1.2",
            "teaser": (
                "Bu derste artık sadece bir şeyin ne olduğunu değil, var olup olmadığını ve nerede bulunduğunu da söylemeye başlıyoruz. "
                "ein / eine ile kein / keine kalıpları, ev ve oda kelimeleri, Wo ist ...? soruları ve Es gibt yapısı birlikte çalışıyor."
            ),
            "status": "active",
            "objectives": [
                "Belirli artikel ile belirsiz artikel arasındaki farkı görmek.",
                "ein / eine ve kein / keine kalıplarını temel seviyede oturtmak.",
                "Ev, oda ve eşya kelimelerini bağlam içinde öğrenmek.",
                "Wo ist ...? sorusuna hier / dort ile kısa cevap verebilmek.",
                "Es gibt ... / Gibt es ...? kalıplarıyla var-yok anlatımı kurmak.",
                "Mekân tanıtımında kısa ama doğru cümleler yazabilmek.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "20"},
                {"label": "Gramer odağı", "value": "ein/eine + kein/keine"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Belirli ve belirsiz aynı şey değildir",
                    "body": (
                        "der Tisch belirli bir masayı anlatır; ein Tisch ise herhangi bir masayı anlatır. "
                        "Bu fark, Almanca'da nesneleri tanıtmanın temel yollarından biridir."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "kein ile kontrollü olumsuzluk kurarız",
                    "body": (
                        "Bir ismin var olmadığını ya da o şeyin söz konusu olmadığını söylerken kein kullanırız. "
                        "Das ist kein Bad., Das ist keine Küche. gibi örnekler bu dersin çekirdeğidir."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Mekân kelimeleri liste değil, sahne kurar",
                    "body": (
                        "Haus, Küche, Bad, Wohnzimmer gibi kelimeler birlikte bir alan kurar. "
                        "Bu sayede artık sadece kelime değil, bir evin küçük planını anlatmaya başlarsın."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Wo ist ...? sorusu yer bilgisinin kapısını açar",
                    "body": (
                        "Wo ist das Bad?, Wo ist der Balkon? gibi sorular, nesneleri ve odaları cümle içinde kullanmanın doğal yoludur. "
                        "Burada hedef uzun tarif değil, temel mekân refleksidir."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Es gibt yapısı var-yok bilgisini doğal kılar",
                    "body": (
                        "Bir evde, odada veya şehirde neyin bulunduğunu söylerken Es gibt yapısı çok kullanılır. "
                        "Ayrıntılı hâl bilgisini daha sonra sistematikleştireceğiz; burada önce doğal kullanım refleksi kuruyoruz."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Belirli ve belirsiz artikel farkı",
                    "summary": "Aynı ismi farklı kesinlik dereceleriyle anlatabiliriz.",
                    "items": [
                        "der Tisch = belirli masa",
                        "ein Tisch = bir masa / herhangi bir masa",
                        "die Küche = belirli mutfak",
                        "eine Küche = bir mutfak",
                        "das Bad = belirli banyo",
                        "ein Bad = bir banyo",
                    ],
                    "examples": [
                        "Das ist ein Haus.",
                        "Die Küche ist groß.",
                        "Wir haben ein Wohnzimmer.",
                    ],
                },
                {
                    "title": "kein / keine ile isim olumsuzluğu",
                    "summary": "Olumsuzluğu doğrudan ismin önünde kuruyoruz.",
                    "items": [
                        "kein Balkon",
                        "keine Küche",
                        "kein Bad",
                        "keine Toilette",
                    ],
                    "examples": [
                        "Das ist kein Balkon.",
                        "Hier gibt es keine Toilette.",
                        "Das ist keine Küche.",
                    ],
                },
                {
                    "title": "Temel ev ve oda kelimeleri",
                    "summary": "İlk aşamada yer bildiren en sık isimleri blok halinde öğreniyoruz.",
                    "items": [
                        "das Haus = ev",
                        "das Zimmer = oda",
                        "die Küche = mutfak",
                        "das Bad = banyo",
                        "das Wohnzimmer = oturma odası",
                        "das Schlafzimmer = yatak odası",
                    ],
                    "examples": [
                        "Das Haus ist klein.",
                        "Das Schlafzimmer ist dort.",
                    ],
                },
                {
                    "title": "Wo ist ...? ve kısa yer cevapları",
                    "summary": "Yer sormayı önce çok kısa cevaplarla kuruyoruz.",
                    "items": [
                        "Wo ist das Bad?",
                        "Hier. = Burada.",
                        "Dort. = Orada.",
                        "Die Küche ist dort.",
                        "Der Balkon ist hier.",
                    ],
                    "examples": [
                        "Wo ist das Wohnzimmer? Dort.",
                        "Wo ist der Tisch? Er ist hier.",
                    ],
                },
                {
                    "title": "Es gibt / Gibt es ...?",
                    "summary": "Var-yok anlatımı için en doğal başlangıç kalıplarından biridir.",
                    "items": [
                        "Es gibt ein Bad.",
                        "Es gibt eine Küche.",
                        "Gibt es ein Wohnzimmer?",
                        "Gibt es keine Toilette?",
                    ],
                    "examples": [
                        "Ja, es gibt ein Bad.",
                        "Nein, es gibt kein Wohnzimmer.",
                    ],
                },
                {
                    "title": "Küçük not: maskulin çekim ayrıntısı sonra gelecek",
                    "summary": "Bu derste çekirdeği kuruyoruz; maskulin nesne değişimleri bir sonraki gramer dersinde sistematikleşecek.",
                    "items": [
                        "Şimdilik ein / eine ve kein / keine çekirdeğine odaklan.",
                        "Bazı örneklerde ileride einen / keinen göreceksin.",
                        "Bu değişimi Ders 9'da ayrıntılı işleyeceğiz.",
                    ],
                    "examples": [
                        "Önce: Gibt es ein Bad?",
                        "Sonra: Ich sehe den Balkon.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Das ist ein Haus.", "tr": "Bu bir evdir.", "note": "Belirsiz artikel ile ilk tanıtım cümlesi."},
                {"de": "Das ist keine Küche.", "tr": "Bu bir mutfak değildir.", "note": "Dişil isimde isim olumsuzluğu."},
                {"de": "Hier ist das Bad.", "tr": "Banyo burada.", "note": "Kısa yer bildirimi."},
                {"de": "Dort ist das Wohnzimmer.", "tr": "Oturma odası orada.", "note": "dort ile temel konum cümlesi."},
                {"de": "Wo ist der Balkon?", "tr": "Balkon nerede?", "note": "Maskulin isimle yer sorusu."},
                {"de": "Die Lampe ist dort.", "tr": "Lamba orada.", "note": "Yer bildiren en temel kısa cümlelerden biridir."},
                {"de": "Es gibt ein Bad.", "tr": "Bir banyo var.", "note": "Var-yok yapısının en temel kullanımı."},
                {"de": "Gibt es eine Toilette?", "tr": "Bir tuvalet var mı?", "note": "Evet-hayır sorusuna dönüşmüş Es gibt yapısı."},
                {"de": "Nein, es gibt kein Wohnzimmer.", "tr": "Hayır, bir oturma odası yok.", "note": "kein ile olumsuz cevap."},
                {"de": "Das Schlafzimmer ist groß.", "tr": "Yatak odası büyüktür.", "note": "Oda kelimesini sıfatla birleştirir."},
                {"de": "Ist das ein Garten?", "tr": "Bu bir bahçe mi?", "note": "Basit nesne tanıma sorusu."},
                {"de": "Ja, das ist ein Garten.", "tr": "Evet, bu bir bahçedir.", "note": "Kısa olumlu cevap."},
            ],
            "common_mistakes": [
                {
                    "wrong": "ein Küche demek",
                    "right": "eine Küche demek",
                    "reason": "Küche dişil isimdir; bu yüzden eine gerekir.",
                },
                {
                    "wrong": "kein Bad / keine Bad karıştırmak",
                    "right": "kein Bad",
                    "reason": "Bad nötr isimdir; temel olumsuz biçimi kein Bad olur.",
                },
                {
                    "wrong": "Wo der Balkon ist? diye temel soru kurmak",
                    "right": "Wo ist der Balkon?",
                    "reason": "Soru kelimesinden sonra çekimli fiil gelir.",
                },
                {
                    "wrong": "ein der Tisch gibi çift belirleyici kullanmak",
                    "right": "der Tisch ya da ein Tisch demek",
                    "reason": "Aynı isim önünde iki belirleyici birlikte kullanılmaz.",
                },
                {
                    "wrong": "Es gibt cümlesini yalnız kelime listesi gibi görmek",
                    "right": "Es gibt yapısını gerçek mekân cümlelerinde tekrar etmek",
                    "reason": "Bu kalıp bağlam içinde öğrenildiğinde kalıcı olur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Ist das ein Haus?", "text_tr": "Bu bir ev mi?"},
                    {"speaker": "B", "text_de": "Ja, das ist ein Haus. Die Küche ist hier.", "text_tr": "Evet, bu bir ev. Mutfak burada."},
                    {"speaker": "A", "text_de": "Gibt es ein Wohnzimmer?", "text_tr": "Bir oturma odası var mı?"},
                    {"speaker": "B", "text_de": "Ja, es gibt ein Wohnzimmer, aber es gibt kein Bad.", "text_tr": "Evet, bir oturma odası var ama banyo yok."},
                    {"speaker": "A", "text_de": "Wo ist das Bad?", "text_tr": "Banyo nerede?"},
                    {"speaker": "B", "text_de": "Dort. Das Bad ist dort.", "text_tr": "Orada. Banyo orada."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Ev turu metni",
                    "intro": "Bu metin ev, oda ve var-yok kalıplarını kısa bir tur anlatımına dönüştürüyor.",
                    "word_focus": "18 kelime / kalıp",
                    "paragraphs": [
                        "Das ist ein [[Haus::ev]]. Hier ist der [[Flur::koridor / giriş alanı]] und dort ist die [[Küche::mutfak]]. Es gibt auch ein [[Bad::banyo]] und ein [[Wohnzimmer::oturma odası]].",
                        "Dort stehen ein [[Tisch::masa]], ein [[Stuhl::sandalye]] und eine [[Lampe::lamba]]. Das [[Schlafzimmer::yatak odası]] ist klein, aber der [[Garten::bahçe]] ist groß.",
                        "Ich frage: [[Wo ist der Balkon?::Balkon nerede?]] Mein Freund sagt: [[Hier ist kein Balkon.::Burada balkon yok.]] Aber [[dort::orada]] ist eine [[Toilette::tuvalet]].",
                    ],
                },
            ],
            "tips": [
                "ein / eine ve kein / keine kalıplarını mutlaka isimle birlikte tekrar et.",
                "Ev kelimelerini gerçek evinin planıyla eşleştirirsen kalıcılık artar.",
                "Wo ist ...? sorusunu en az 10 farklı isimle sesli kur.",
                "hier ve dort kelimelerini el hareketiyle çalışmak başlangıçta faydalı olur.",
                "Es gibt yapısını olumlu ve olumsuz iki versiyonla birlikte tekrar et.",
            ],
            "vocabulary": [
                {"word": "Haus", "article": "das", "plural": "die Häuser", "meanings": ["ev", "konut"], "example_de": "Das ist ein Haus.", "example_tr": "Bu bir evdir.", "note": "Mekân anlatımının merkez isimlerinden biridir."},
                {"word": "Zimmer", "article": "das", "plural": "die Zimmer", "meanings": ["oda"], "example_de": "Das Zimmer ist klein.", "example_tr": "Oda küçüktür.", "note": "Genel oda kelimesi olarak erken öğrenilir."},
                {"word": "Küche", "article": "die", "plural": "die Küchen", "meanings": ["mutfak"], "example_de": "Die Küche ist hier.", "example_tr": "Mutfak burada.", "note": "Dişil isimle belirsiz artikel çalışmak için iyi örnektir."},
                {"word": "Bad", "article": "das", "plural": "die Bäder", "meanings": ["banyo"], "example_de": "Es gibt ein Bad.", "example_tr": "Bir banyo vardır.", "note": "Es gibt yapısında çok kullanılır."},
                {"word": "Wohnzimmer", "article": "das", "plural": "die Wohnzimmer", "meanings": ["oturma odası", "salon"], "example_de": "Das Wohnzimmer ist groß.", "example_tr": "Oturma odası büyüktür.", "note": "Ev anlatımında temel odalardandır."},
                {"word": "Schlafzimmer", "article": "das", "plural": "die Schlafzimmer", "meanings": ["yatak odası"], "example_de": "Das Schlafzimmer ist dort.", "example_tr": "Yatak odası oradadır.", "note": "Uzun bileşik isimlere giriş sağlar."},
                {"word": "Flur", "article": "der", "plural": "die Flure", "meanings": ["koridor", "giriş holü"], "example_de": "Der Flur ist hell.", "example_tr": "Koridor aydınlıktır.", "note": "Ev içi yön tarifinde işe yarar."},
                {"word": "Balkon", "article": "der", "plural": "die Balkone", "meanings": ["balkon"], "example_de": "Wo ist der Balkon?", "example_tr": "Balkon nerede?", "note": "Maskulin mekân ismi olarak tekrar edilir."},
                {"word": "Garten", "article": "der", "plural": "die Gärten", "meanings": ["bahçe"], "example_de": "Das ist ein Garten.", "example_tr": "Bu bir bahçedir.", "note": "Ev dışı mekânı da oyuna katar."},
                {"word": "Toilette", "article": "die", "plural": "die Toiletten", "meanings": ["tuvalet"], "example_de": "Gibt es eine Toilette?", "example_tr": "Bir tuvalet var mı?", "note": "Soru kalıbında doğal geçer."},
                {"word": "Tisch", "article": "der", "plural": "die Tische", "meanings": ["masa"], "example_de": "Der Tisch ist dort.", "example_tr": "Masa oradadır.", "note": "Önceki dersten gelen kelimeyi yeni mekân bağlamında tekrar eder."},
                {"word": "Stuhl", "article": "der", "plural": "die Stühle", "meanings": ["sandalye"], "example_de": "Der Stuhl ist hier.", "example_tr": "Sandalye burada.", "note": "Tisch ile birlikte sık kullanılır."},
                {"word": "Lampe", "article": "die", "plural": "die Lampen", "meanings": ["lamba"], "example_de": "Die Lampe ist dort.", "example_tr": "Lamba oradadır.", "note": "Dişil nesne örneği olarak işlevlidir."},
                {"word": "Sofa", "article": "das", "plural": "die Sofas", "meanings": ["kanepe", "koltuk"], "example_de": "Das Sofa ist neu.", "example_tr": "Kanepe yenidir.", "note": "Nötr nesne örneği."},
                {"word": "Bett", "article": "das", "plural": "die Betten", "meanings": ["yatak"], "example_de": "Das Bett ist groß.", "example_tr": "Yatak büyüktür.", "note": "Schlafzimmer ile birlikte kolay bağ kurar."},
                {"word": "Schrank", "article": "der", "plural": "die Schränke", "meanings": ["dolap"], "example_de": "Der Schrank ist alt.", "example_tr": "Dolap eskidir.", "note": "Ev eşyası kümesini genişletir."},
                {"word": "Kühlschrank", "article": "der", "plural": "die Kühlschränke", "meanings": ["buzdolabı"], "example_de": "Der Kühlschrank ist hier.", "example_tr": "Buzdolabı burada.", "note": "Bileşik isim örneğidir."},
                {"word": "Herd", "article": "der", "plural": "die Herde", "meanings": ["ocak"], "example_de": "Der Herd ist dort.", "example_tr": "Ocak oradadır.", "note": "Küche ile doğal bağ kurar."},
                {"word": "hier", "article": "-", "plural": "-", "meanings": ["burada"], "example_de": "Hier ist das Bad.", "example_tr": "Banyo burada.", "note": "En temel yer zarfıdır."},
                {"word": "dort", "article": "-", "plural": "-", "meanings": ["orada"], "example_de": "Dort ist die Küche.", "example_tr": "Mutfak oradadır.", "note": "hier ile birlikte çalışılır."},
            ],
            "exercises": [
                {
                    "id": "indefinite-articles",
                    "type": "single_choice",
                    "title": "Belirsiz Artikel Testi",
                    "description": "İsme uygun ein / eine biçimini seç.",
                    "questions": [
                        {"prompt": "___ Küche", "options": ["ein", "eine", "kein"], "correct_index": 1, "explanation": "Küche dişil isimdir; eine Küche olur."},
                        {"prompt": "___ Haus", "options": ["ein", "eine", "keine"], "correct_index": 0, "explanation": "Haus nötr isimdir; ein Haus kullanılır."},
                        {"prompt": "___ Balkon", "options": ["ein", "eine", "keine"], "correct_index": 0, "explanation": "Balkon maskulin isimdir; temel belirsiz biçim ein Balkon olur."},
                        {"prompt": "___ Toilette", "options": ["ein", "eine", "kein"], "correct_index": 1, "explanation": "Toilette dişil isimdir; eine Toilette gerekir."},
                        {"prompt": "___ Wohnzimmer", "options": ["ein", "eine", "keine"], "correct_index": 0, "explanation": "Wohnzimmer nötr isimdir; ein Wohnzimmer olur."},
                        {"prompt": "___ Lampe", "options": ["ein", "eine", "kein"], "correct_index": 1, "explanation": "Lampe dişil isimdir; eine Lampe kullanılır."},
                    ],
                },
                {
                    "id": "negative-forms",
                    "type": "single_choice",
                    "title": "kein / keine Testi",
                    "description": "İsmi doğru olumsuz biçimle tamamla.",
                    "questions": [
                        {"prompt": "Das ist ___ Bad.", "options": ["kein", "keine", "einen"], "correct_index": 0, "explanation": "Bad nötr olduğu için kein Bad olur."},
                        {"prompt": "Hier gibt es ___ Küche.", "options": ["kein", "keine", "einen"], "correct_index": 1, "explanation": "Küche dişil olduğu için keine Küche gerekir."},
                        {"prompt": "Das ist ___ Balkon.", "options": ["keine", "kein", "eine"], "correct_index": 1, "explanation": "Balkon için bu dersteki temel olumsuz biçim kein Balkon şeklindedir."},
                        {"prompt": "Das ist ___ Toilette.", "options": ["kein", "keine", "einen"], "correct_index": 1, "explanation": "Toilette dişil isimdir; keine Toilette olur."},
                        {"prompt": "Wir haben ___ Wohnzimmer.", "options": ["keine", "kein", "eine"], "correct_index": 1, "explanation": "Wohnzimmer nötr isimdir; kein Wohnzimmer gerekir."},
                        {"prompt": "Hier ist ___ Lampe.", "options": ["kein", "keine", "ein"], "correct_index": 1, "explanation": "Lampe dişil isimdir; keine Lampe denir."},
                    ],
                },
                {
                    "id": "room-meaning",
                    "type": "single_choice",
                    "title": "Oda ve Eşya Anlamları",
                    "description": "Mekân kelimesini doğru anlamla eşleştir.",
                    "questions": [
                        {"prompt": "das Wohnzimmer", "options": ["oturma odası", "yatak", "koridor"], "correct_index": 0, "explanation": "Wohnzimmer = oturma odası / salon."},
                        {"prompt": "der Flur", "options": ["mutfak", "koridor", "bahçe"], "correct_index": 1, "explanation": "Flur = koridor / giriş holü."},
                        {"prompt": "das Schlafzimmer", "options": ["yatak odası", "tuvalet", "buzdolabı"], "correct_index": 0, "explanation": "Schlafzimmer = yatak odası."},
                        {"prompt": "der Schrank", "options": ["masa", "dolap", "ocak"], "correct_index": 1, "explanation": "Schrank = dolap."},
                        {"prompt": "der Herd", "options": ["ocak", "bahçe", "balkon"], "correct_index": 0, "explanation": "Herd = ocak."},
                    ],
                },
                {
                    "id": "where-questions",
                    "type": "single_choice",
                    "title": "Wo ist ...? Soruları",
                    "description": "Yer sorma ve yer gösterme mantığını kur.",
                    "questions": [
                        {"prompt": "___ ist das Bad?", "options": ["Wann", "Wo", "Wer"], "correct_index": 1, "explanation": "Yer sormak için wo kullanılır."},
                        {"prompt": "Wo ist der Balkon? -> ___.", "options": ["Hier.", "Gut.", "Danke."], "correct_index": 0, "explanation": "Kısa yer cevabı burada Hier. olabilir."},
                        {"prompt": "Dort ist ___ Küche.", "options": ["die", "der", "das"], "correct_index": 0, "explanation": "Küche dişil isimdir; die Küche olur."},
                        {"prompt": "Wo ist das Wohnzimmer? -> Es ist ___.", "options": ["dort", "müde", "alt"], "correct_index": 0, "explanation": "Yer bildirirken dort kullanılabilir."},
                        {"prompt": "Hangisi doğru soru cümlesidir?", "options": ["Wo ist der Tisch?", "Wo der Tisch ist?", "Der Tisch wo ist?"], "correct_index": 0, "explanation": "Temel soru kalıbı Wo ist der Tisch? şeklindedir."},
                        {"prompt": "Hangisi doğru cevap cümlesidir?", "options": ["Hier ist das Bad.", "Das Bad hier ist?", "Ist hier das Bad."], "correct_index": 0, "explanation": "Doğru cümle düzeni Hier ist das Bad. olur."},
                    ],
                },
                {
                    "id": "es-gibt",
                    "type": "single_choice",
                    "title": "Es gibt / Gibt es ...?",
                    "description": "Var-yok kalıbını doğru yerde kullan.",
                    "questions": [
                        {"prompt": "___ ein Bad.", "options": ["Es gibt", "Wo ist", "Wie geht"], "correct_index": 0, "explanation": "Var-yok bildirmek için Es gibt kullanılır."},
                        {"prompt": "___ eine Toilette?", "options": ["Gibt es", "Wo ist", "Ist das"], "correct_index": 0, "explanation": "Soru biçimi Gibt es ...? olur."},
                        {"prompt": "Nein, es gibt ___ Wohnzimmer.", "options": ["kein", "keine", "einen"], "correct_index": 0, "explanation": "Wohnzimmer nötr isimdir; kein gerekir."},
                        {"prompt": "Ja, es gibt ___ Küche.", "options": ["eine", "ein", "kein"], "correct_index": 0, "explanation": "Küche dişil isimdir; eine kullanılır."},
                        {"prompt": "Hangisi doğru cümledir?", "options": ["Es gibt ein Haus.", "Ein Haus gibt es?", "Gibt ein Haus es."], "correct_index": 0, "explanation": "Düz cümle biçimi Es gibt ... şeklindedir."},
                        {"prompt": "Hangisi doğru olumsuz cümledir?", "options": ["Es gibt keine Toilette.", "Es gibt kein Toilette.", "Gibt es keine Toilette."], "correct_index": 0, "explanation": "Toilette dişil isimdir; keine Toilette gerekir."},
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Belirsiz artikel, olumsuzluk ve mekân sorularını birlikte yokla.",
                    "questions": [
                        {"prompt": "Hangisi doğrudur?", "options": ["eine Bad", "ein Bad", "keine Bad"], "correct_index": 1, "explanation": "Bad nötr isimdir; ein Bad kullanılır."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Wo ist die Küche?", "Wo die Küche ist?", "Die Küche wo ist?"], "correct_index": 0, "explanation": "Soru kelimesinden sonra fiil gelir."},
                        {"prompt": "Hangisi doğru olumsuzluktur?", "options": ["kein Küche", "keine Küche", "ein Küche"], "correct_index": 1, "explanation": "Küche dişildir; keine Küche olur."},
                        {"prompt": "Hangisi doğru anlam eşleşmesidir?", "options": ["Flur = koridor", "Bad = balkon", "Schrank = bahçe"], "correct_index": 0, "explanation": "Flur = koridor / giriş holü."},
                        {"prompt": "Bu dersin ana hedefi nedir?", "options": ["Mekân ve var-yok cümlelerini kurmak", "Geçmiş zaman yazmak", "Modal fiilleri bitirmek"], "correct_index": 0, "explanation": "Bu dersin ana odağı mekân anlatımı ve isim olumsuzluğudur."},
                    ],
                },
            ],
            "homework": [
                "Kendi evin için en az 8 cümlelik mini tanıtım yaz: odalar, eşyalar ve var-yok bilgisi kullan.",
                "Wo ist ...? sorusunu 10 farklı isimle sor ve kısa cevaplar üret.",
                "ein / eine ve kein / keine için iki sütunlu kişisel tekrar listesi oluştur.",
                "Okuma metnindeki mekân kelimelerini gerçek hayatındaki yerlerle eşleştir.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde artık bir evi veya küçük bir mekânı tanıtabilir, hangi odanın veya eşyanın var olduğunu söyleyebilir "
                "ve Wo ist ...? sorularına kısa ama doğru cevap verebilir olmalısın."
            ),
            "next_lesson": {
                "title": "Ders 8: Saatler, günler ve günlük program",
                "status": "active",
                "slug": "ders-8-saatler-gunler-ve-gunluk-program",
            },
        },
        {
            "slug": "ders-8-saatler-gunler-ve-gunluk-program",
            "index": 8,
            "title": "Saatler, Günler ve Günlük Program",
            "duration": "90-105 dk",
            "difficulty": "A1.2",
            "teaser": (
                "Bu derste zamanı daha ayrıntılı söylemeye başlıyoruz: tam saat, buçuklu saat, çeyrek geçe ve çeyrek kala yapıları, "
                "hafta günleri, von ... bis ... kalıbı ve kısa program anlatımı aynı akış içinde çalışıyor."
            ),
            "status": "active",
            "objectives": [
                "Tam saatleri ve temel dakikalı saat kalıplarını okumak.",
                "halb, Viertel nach, Viertel vor ve vor / nach mantığını kavramak.",
                "Hafta günlerini ve am + gün kullanımını oturtmak.",
                "von ... bis ... ile saat veya gün aralığı söylemek.",
                "Ayrılabilen fiillere ilk hafif girişi yapmak.",
                "Kısa bir günlük programı saat ve gün bilgisiyle anlatabilmek.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "19"},
                {"label": "Gramer odağı", "value": "saat + gün + program"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Saat söylemek ayrı bir dil refleksidir",
                    "body": (
                        "Saatler Almanca'da yalnız sayı bilgisiyle değil, kalıp bilgisiyle söylenir. "
                        "Bu yüzden önce tam saatleri, sonra buçuk ve çeyrek yapıları sistemli şekilde kuruyoruz."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "halb mantığı Türkçe düşünmeyebilir",
                    "body": (
                        "Es ist halb sechs cümlesi tam olarak altı buçuk değil, beş buçuk demektir. "
                        "Bu fark erken aşamada netleşmezse saatler sürekli karışır."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Hafta günleri programa omurga verir",
                    "body": (
                        "Montag, Dienstag, Mittwoch gibi gün adlarıyla artık günlere bağlı alışkanlık veya program cümleleri kuruyoruz."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "von ... bis ... aralık bildirir",
                    "body": (
                        "Bir dersin, işin veya etkinliğin hangi saatler arasında sürdüğünü söylemek için von ... bis ... kalıbı kullanılır. "
                        "Bu, günlük programa doğrudan işlev katar."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Ayrılabilen fiillere yalnız giriş yapıyoruz",
                    "body": (
                        "aufstehen veya anfangen gibi fiillerin tam sistemi daha sonra genişleyecek. "
                        "Bu derste yalnız temel dizilimi fark etmen yeterli."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Tam saatler",
                    "summary": "İlk aşamada saatleri açık ve temiz biçimde söylemek gerekir.",
                    "items": [
                        "Es ist ein Uhr.",
                        "Es ist drei Uhr.",
                        "Es ist acht Uhr.",
                        "Es ist elf Uhr.",
                    ],
                    "examples": [
                        "Es ist neun Uhr.",
                        "Der Kurs ist um zehn Uhr.",
                    ],
                },
                {
                    "title": "halb, Viertel nach ve Viertel vor",
                    "summary": "Bu üç yapı A1'de saat anlatımının çekirdeğini kurar.",
                    "items": [
                        "Es ist halb sechs. = Saat beş buçuk.",
                        "Es ist Viertel nach vier. = Saat dördü çeyrek geçiyor.",
                        "Es ist Viertel vor zwei. = Saat ikiye çeyrek var.",
                        "Es ist zehn nach zwei. = Saat ikiyi on geçiyor.",
                        "Es ist zwanzig vor neun. = Saat dokuza yirmi var.",
                    ],
                    "examples": [
                        "Es ist halb acht.",
                        "Es ist Viertel nach zehn.",
                    ],
                },
                {
                    "title": "Hafta günleri ve am kullanımı",
                    "summary": "Gün adıyla en temel kullanım am + gün biçimidir.",
                    "items": [
                        "am Montag",
                        "am Dienstag",
                        "am Mittwoch",
                        "am Donnerstag",
                        "am Freitag",
                        "am Samstag / am Sonntag",
                    ],
                    "examples": [
                        "Am Montag arbeite ich.",
                        "Am Samstag lerne ich Deutsch.",
                    ],
                },
                {
                    "title": "von ... bis ...",
                    "summary": "Saat veya gün aralığı bildirmek için kullanılır.",
                    "items": [
                        "von 9 Uhr bis 12 Uhr",
                        "von Montag bis Freitag",
                        "Der Kurs ist von 10 Uhr bis 12 Uhr.",
                    ],
                    "examples": [
                        "Ich arbeite von Montag bis Freitag.",
                        "Die Pause ist von eins bis halb zwei.",
                    ],
                },
                {
                    "title": "Ayrılabilen fiillere giriş",
                    "summary": "Yalnız temel dizilimi fark ediyoruz; ayrıntılı sistem daha sonra gelecek.",
                    "items": [
                        "aufstehen -> Ich stehe um 7 Uhr auf.",
                        "anfangen -> Der Kurs fängt um 9 Uhr an.",
                        "einkaufen -> Am Samstag kaufe ich ein.",
                    ],
                    "examples": [
                        "Wann stehst du auf?",
                        "Der Unterricht fängt spät an.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Es ist drei Uhr.", "tr": "Saat üç.", "note": "Tam saat kalıbı."},
                {"de": "Es ist halb sechs.", "tr": "Saat beş buçuk.", "note": "halb yapısının temel örneği."},
                {"de": "Es ist Viertel nach vier.", "tr": "Saat dördü çeyrek geçiyor.", "note": "çeyrek geçe kalıbı."},
                {"de": "Es ist Viertel vor zwei.", "tr": "Saat ikiye çeyrek var.", "note": "çeyrek kala kalıbı."},
                {"de": "Es ist zehn nach zwei.", "tr": "Saat ikiyi on geçiyor.", "note": "nach ile dakikalı saat örneği."},
                {"de": "Es ist zwanzig vor neun.", "tr": "Saat dokuza yirmi var.", "note": "vor ile dakikalı saat örneği."},
                {"de": "Am Montag arbeite ich von 9 Uhr bis 17 Uhr.", "tr": "Pazartesi günü 9'dan 17'ye kadar çalışırım.", "note": "gün + saat aralığı."},
                {"de": "Der Kurs ist von Dienstag bis Freitag.", "tr": "Kurs salıdan cumaya kadar sürer.", "note": "gün aralığı kalıbı."},
                {"de": "Ich stehe um 7 Uhr auf.", "tr": "Saat 7'de kalkarım.", "note": "ayrılabilen fiile giriş örneği."},
                {"de": "Der Unterricht fängt um 8 Uhr an.", "tr": "Ders saat 8'de başlar.", "note": "anfangen fiilinin ayrılmalı kullanımı."},
                {"de": "Am Samstag kaufe ich ein.", "tr": "Cumartesi alışveriş yaparım.", "note": "einkaufen fiilinin temel kullanımı."},
                {"de": "Wann ist die Pause?", "tr": "Ara ne zaman?", "note": "saat bilgisine doğal soru."},
            ],
            "common_mistakes": [
                {
                    "wrong": "Es ist halb sechs = altı buçuk sanmak",
                    "right": "Es ist halb sechs = beş buçuk",
                    "reason": "Almanca yarım saatlerde bir sonraki saate göre düşünür.",
                },
                {
                    "wrong": "am yerine um Montag demek",
                    "right": "am Montag demek",
                    "reason": "Gün adlarıyla temel kullanım am olur; um saatlerde kullanılır.",
                },
                {
                    "wrong": "Ich aufstehe um 7 Uhr demek",
                    "right": "Ich stehe um 7 Uhr auf demek",
                    "reason": "Ayrılabilen fiilde ön ek cümlenin sonuna gider.",
                },
                {
                    "wrong": "von 9 Uhr nach 12 Uhr demek",
                    "right": "von 9 Uhr bis 12 Uhr demek",
                    "reason": "Aralık bitişini bis ile veririz.",
                },
                {
                    "wrong": "Viertel nach / vor kalıplarını düz sayı gibi ezberlemek",
                    "right": "Her kalıbı saat resmi veya gerçek zaman çizelgesiyle çalışmak",
                    "reason": "Zaman kalıpları görsel ilişkiyle daha hızlı oturur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Wie spät ist es?", "text_tr": "Saat kaç?"},
                    {"speaker": "B", "text_de": "Es ist Viertel nach acht.", "text_tr": "Saat sekizi çeyrek geçiyor."},
                    {"speaker": "A", "text_de": "Wann fängt der Kurs an?", "text_tr": "Kurs ne zaman başlıyor?"},
                    {"speaker": "B", "text_de": "Der Kurs fängt um neun Uhr an.", "text_tr": "Kurs saat dokuzda başlıyor."},
                    {"speaker": "A", "text_de": "Und wann stehst du auf?", "text_tr": "Peki ne zaman kalkıyorsun?"},
                    {"speaker": "B", "text_de": "Ich stehe am Montag um sieben Uhr auf.", "text_tr": "Pazartesi saat yedide kalkıyorum."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Haftalık program metni",
                    "intro": "Bu metin saatleri, günleri ve kısa program anlatımını tek akışta birleştiriyor.",
                    "word_focus": "18 kelime / kalıp",
                    "paragraphs": [
                        "[[Am Montag::pazartesi günü]] stehe ich um [[7 Uhr::saat 7'de]] [[auf::kalkarım]] und um acht Uhr beginnt der [[Kurs::kurs]]. Die erste [[Pause::ara]] ist um Viertel nach zehn.",
                        "Von [[Dienstag::salı]] bis [[Freitag::cuma]] arbeite ich von neun Uhr bis fünf Uhr. [[Am Samstag::cumartesi günü]] kaufe ich ein und [[am Sonntag::pazar günü]] schlafe ich lange.",
                        "Mein Freund fragt: [[Wie spät ist es?::Saat kaç?]] Ich sage: [[Es ist halb sechs.::Saat beş buçuk.]] Danach lese ich meinen Plan und frage: [[Wann fängt der Unterricht an?::Ders ne zaman başlıyor?]]",
                    ],
                },
            ],
            "tips": [
                "Saat kalıplarını mutlaka yüksek sesle tekrar et; gözle bakmak yetmez.",
                "halb yapısını saat resmi çizerek çalışırsan daha hızlı oturur.",
                "Gün adlarını am ile birlikte blok halinde ezberle: am Montag, am Dienstag...",
                "von ... bis ... kalıbını hem saat hem gün aralığında ayrı ayrı tekrar et.",
                "Ayrılabilen fiillerde ön ekin cümle sonunda kaldığını fark etmeye başla; şimdilik ayrıntıya boğulma.",
            ],
            "vocabulary": [
                {"word": "Montag", "article": "der", "plural": "die Montage", "meanings": ["pazartesi"], "example_de": "Am Montag arbeite ich.", "example_tr": "Pazartesi günü çalışırım.", "note": "Hafta günlerinin ilkidir."},
                {"word": "Dienstag", "article": "der", "plural": "die Dienstage", "meanings": ["salı"], "example_de": "Am Dienstag lerne ich.", "example_tr": "Salı günü çalışırım.", "note": "Program cümlelerinde sık geçer."},
                {"word": "Mittwoch", "article": "der", "plural": "die Mittwoche", "meanings": ["çarşamba"], "example_de": "Am Mittwoch habe ich Pause.", "example_tr": "Çarşamba günü aram var.", "note": "Hafta içi gün adlarından biridir."},
                {"word": "Donnerstag", "article": "der", "plural": "die Donnerstage", "meanings": ["perşembe"], "example_de": "Am Donnerstag koche ich.", "example_tr": "Perşembe günü yemek yaparım.", "note": "Gün adı olarak am ile kullanılır."},
                {"word": "Freitag", "article": "der", "plural": "die Freitage", "meanings": ["cuma"], "example_de": "Am Freitag telefoniere ich.", "example_tr": "Cuma günü telefonlaşırım.", "note": "Hafta sonuna yakın gün anlatımında geçer."},
                {"word": "Samstag", "article": "der", "plural": "die Samstage", "meanings": ["cumartesi"], "example_de": "Am Samstag kaufe ich ein.", "example_tr": "Cumartesi alışveriş yaparım.", "note": "Hafta sonu rutini için temel gün."},
                {"word": "Sonntag", "article": "der", "plural": "die Sonntage", "meanings": ["pazar"], "example_de": "Am Sonntag schlafe ich lange.", "example_tr": "Pazar günü uzun uyurum.", "note": "Dinlenme günü örneklerinde sık kullanılır."},
                {"word": "Uhr", "article": "die", "plural": "die Uhren", "meanings": ["saat"], "example_de": "Es ist acht Uhr.", "example_tr": "Saat sekiz.", "note": "Saat kalıplarının ana ismidir."},
                {"word": "Viertel", "article": "das", "plural": "die Viertel", "meanings": ["çeyrek"], "example_de": "Es ist Viertel nach vier.", "example_tr": "Saat dördü çeyrek geçiyor.", "note": "Saat kalıplarında kalıp parçası olarak çok kullanılır."},
                {"word": "halb", "article": "-", "plural": "-", "meanings": ["yarım", "buçuk"], "example_de": "Es ist halb sechs.", "example_tr": "Saat beş buçuk.", "note": "Saat anlatımında özel işlev taşır."},
                {"word": "vor", "article": "-", "plural": "-", "meanings": ["kala", "önce"], "example_de": "Es ist zwanzig vor neun.", "example_tr": "Saat dokuza yirmi var.", "note": "Saatlerde kala anlamı verir."},
                {"word": "nach", "article": "-", "plural": "-", "meanings": ["geçe", "sonra"], "example_de": "Es ist zehn nach zwei.", "example_tr": "Saat ikiyi on geçiyor.", "note": "Saatlerde geçe anlamı verir."},
                {"word": "Kurs", "article": "der", "plural": "die Kurse", "meanings": ["kurs"], "example_de": "Der Kurs fängt um neun Uhr an.", "example_tr": "Kurs saat dokuzda başlar.", "note": "Program anlatımında doğal isimdir."},
                {"word": "Pause", "article": "die", "plural": "die Pausen", "meanings": ["ara", "mola"], "example_de": "Die Pause ist um elf Uhr.", "example_tr": "Ara saat on birde.", "note": "Ders ve iş programlarında sık geçer."},
                {"word": "Termin", "article": "der", "plural": "die Termine", "meanings": ["randevu", "takvim zamanı"], "example_de": "Der Termin ist am Freitag.", "example_tr": "Randevu cuma günü.", "note": "Program ve takvim dili için yararlıdır."},
                {"word": "Woche", "article": "die", "plural": "die Wochen", "meanings": ["hafta"], "example_de": "Die Woche ist lang.", "example_tr": "Hafta uzundur.", "note": "Günleri büyük zamana bağlar."},
                {"word": "aufstehen", "article": "-", "plural": "-", "meanings": ["kalkmak"], "example_de": "Ich stehe um sieben Uhr auf.", "example_tr": "Saat yedide kalkarım.", "note": "Ayrılabilen fiillere giriş örneğidir."},
                {"word": "anfangen", "article": "-", "plural": "-", "meanings": ["başlamak"], "example_de": "Der Unterricht fängt um acht Uhr an.", "example_tr": "Ders saat sekizde başlar.", "note": "Ön eki ayrılan fiil örneği."},
                {"word": "einkaufen", "article": "-", "plural": "-", "meanings": ["alışveriş yapmak"], "example_de": "Am Samstag kaufe ich ein.", "example_tr": "Cumartesi alışveriş yaparım.", "note": "Hafta sonu rutini ile kolay bağ kurar."},
            ],
            "exercises": [
                {
                    "id": "clock-basics",
                    "type": "single_choice",
                    "title": "Saat Kalıpları Testi",
                    "description": "Tam saat ve temel saat kalıplarını eşleştir.",
                    "questions": [
                        {"prompt": "Saat 3. ->", "options": ["Es ist drei Uhr.", "Es ist halb drei.", "Es ist Viertel vor drei."], "correct_index": 0, "explanation": "Tam saat için Es ist drei Uhr denir."},
                        {"prompt": "Saat 5:30. ->", "options": ["Es ist halb fünf.", "Es ist halb sechs.", "Es ist fünf nach halb sechs."], "correct_index": 1, "explanation": "halb altı = beş buçuk mantığıyla düşünülür."},
                        {"prompt": "Saat 4:15. ->", "options": ["Es ist Viertel nach vier.", "Es ist Viertel vor vier.", "Es ist halb vier."], "correct_index": 0, "explanation": "4:15 için Viertel nach vier kullanılır."},
                        {"prompt": "Saat 1:45. ->", "options": ["Es ist Viertel nach eins.", "Es ist Viertel vor zwei.", "Es ist halb zwei."], "correct_index": 1, "explanation": "1:45 = ikiye çeyrek var."},
                        {"prompt": "Saat 2:10. ->", "options": ["Es ist zehn nach zwei.", "Es ist zehn vor zwei.", "Es ist Viertel nach zwei."], "correct_index": 0, "explanation": "2:10 için zehn nach zwei denir."},
                        {"prompt": "Saat 8:40. ->", "options": ["Es ist zwanzig nach acht.", "Es ist zwanzig vor neun.", "Es ist halb neun."], "correct_index": 1, "explanation": "8:40 = dokuza yirmi var."},
                    ],
                },
                {
                    "id": "weekdays",
                    "type": "single_choice",
                    "title": "Hafta Günleri Testi",
                    "description": "Gün adlarını ve am kullanımını pekiştir.",
                    "questions": [
                        {"prompt": "am Montag", "options": ["pazartesi günü", "salı günü", "pazar günü"], "correct_index": 0, "explanation": "Montag = pazartesi."},
                        {"prompt": "am Samstag", "options": ["çarşamba günü", "cumartesi günü", "cuma günü"], "correct_index": 1, "explanation": "Samstag = cumartesi."},
                        {"prompt": "___ Dienstag lerne ich.", "options": ["Um", "Am", "Von"], "correct_index": 1, "explanation": "Gün adlarıyla am kullanılır."},
                        {"prompt": "Hangisi pazar günüdür?", "options": ["der Sonntag", "der Donnerstag", "der Mittwoch"], "correct_index": 0, "explanation": "Sonntag = pazar."},
                        {"prompt": "Hangisi doğrudur?", "options": ["am Freitag", "um Freitag", "von Freitag"], "correct_index": 0, "explanation": "Gün adıyla temel kullanım am Freitag olur."},
                    ],
                },
                {
                    "id": "von-bis",
                    "type": "single_choice",
                    "title": "von ... bis ... Testi",
                    "description": "Saat ve gün aralıklarını doğru kur.",
                    "questions": [
                        {"prompt": "9'dan 12'ye kadar ->", "options": ["von 9 Uhr bis 12 Uhr", "von 9 Uhr um 12 Uhr", "bis 9 Uhr von 12 Uhr"], "correct_index": 0, "explanation": "Doğru aralık kalıbı von ... bis ... olur."},
                        {"prompt": "Pazartesiden cumaya kadar ->", "options": ["von Montag bis Freitag", "am Montag bis Freitag", "von Freitag nach Montag"], "correct_index": 0, "explanation": "Gün aralığında da von ... bis ... kullanılır."},
                        {"prompt": "Der Kurs ist ___ Dienstag ___ Freitag.", "options": ["von / bis", "am / bis", "von / um"], "correct_index": 0, "explanation": "Aralık bildirirken von ... bis ... gerekir."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Die Pause ist von eins bis halb zwei.", "Die Pause ist um eins bis halb zwei.", "Die Pause ist halb zwei von eins."], "correct_index": 0, "explanation": "Saat aralığı için von ... bis ... kullanılır."},
                        {"prompt": "Hangisi program aralığıdır?", "options": ["von 10 Uhr bis 12 Uhr", "am 10 Uhr", "Viertel nach zehn"], "correct_index": 0, "explanation": "von ... bis ... doğrudan aralık bildirir."},
                    ],
                },
                {
                    "id": "separable-verbs",
                    "type": "single_choice",
                    "title": "Ayrılabilen Fiillere Giriş",
                    "description": "Ön ekin cümle sonuna gittiğini fark et.",
                    "questions": [
                        {"prompt": "Ich ___ um 7 Uhr ___.", "options": ["stehe / auf", "aufstehe / -", "auf / stehe"], "correct_index": 0, "explanation": "aufstehen fiilinde ön ek sona gider."},
                        {"prompt": "Der Kurs ___ um 9 Uhr ___.", "options": ["fängt / an", "anfängt / -", "an / fängt"], "correct_index": 0, "explanation": "anfangen fiilinde ayrılan ön ek sona gelir."},
                        {"prompt": "Am Samstag ___ ich ___.", "options": ["kaufe / ein", "einkaufe / -", "ein / kaufe"], "correct_index": 0, "explanation": "einkaufen fiili temel cümlede kaufe ... ein biçiminde görünür."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Ich stehe um acht Uhr auf.", "Ich aufstehe um acht Uhr.", "Ich auf um acht Uhr stehe."], "correct_index": 0, "explanation": "Doğru ayrılma bu şekildedir."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Der Unterricht fängt spät an.", "Der Unterricht anfängt spät.", "Der Unterricht an spät fängt."], "correct_index": 0, "explanation": "Ayrılabilen fiilde ön ek sonda kalır."},
                    ],
                },
                {
                    "id": "meaning",
                    "type": "single_choice",
                    "title": "Program ve Anlam Testi",
                    "description": "Saat ve program kalıplarını anlamıyla eşleştir.",
                    "questions": [
                        {"prompt": "Es ist Viertel vor zwei.", "options": ["Saat ikiye çeyrek var.", "Saat ikiyi çeyrek geçiyor.", "Saat bir buçuk."], "correct_index": 0, "explanation": "Viertel vor zwei = ikiye çeyrek var."},
                        {"prompt": "Am Samstag kaufe ich ein.", "options": ["Cumartesi alışveriş yaparım.", "Cumartesi çalışırım.", "Cumartesi erken kalkarım."], "correct_index": 0, "explanation": "einkaufen burada alışveriş yapmak anlamındadır."},
                        {"prompt": "Der Kurs ist von Dienstag bis Freitag.", "options": ["Kurs salıdan cumaya kadar sürer.", "Kurs sadece salıdır.", "Kurs cuma günü başlar."], "correct_index": 0, "explanation": "von ... bis ... aralık bildirir."},
                        {"prompt": "Wie spät ist es?", "options": ["Saat kaç?", "Ders ne zaman?", "Hangi gündeyiz?"], "correct_index": 0, "explanation": "Bu soru doğrudan saati sorar."},
                        {"prompt": "Ich stehe um sieben Uhr auf.", "options": ["Saat yedide kalkarım.", "Saat yedide başlarım.", "Saat yedide yerim."], "correct_index": 0, "explanation": "aufstehen = kalkmak."},
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Saatler, günler ve kısa program mantığını birlikte yokla.",
                    "questions": [
                        {"prompt": "Hangisi doğrudur?", "options": ["Es ist halb sechs.", "Es ist halb fünf.", "Es ist Viertel nach sechs."], "correct_index": 0, "explanation": "5:30 için doğru kalıp halb sechs olur."},
                        {"prompt": "Hangisi doğrudur?", "options": ["am Montag", "um Montag", "von Montag"], "correct_index": 0, "explanation": "Gün adlarıyla am kullanılır."},
                        {"prompt": "Hangisi doğru ayrılma örneğidir?", "options": ["Ich stehe auf.", "Ich aufstehe.", "Ich auf stehe."], "correct_index": 0, "explanation": "Ayrılabilen fiilde ön ek sona geçer."},
                        {"prompt": "Hangisi doğru aralıktır?", "options": ["von 9 Uhr bis 11 Uhr", "am 9 Uhr bis 11 Uhr", "um 9 Uhr von 11 Uhr"], "correct_index": 0, "explanation": "Aralık yapısı von ... bis ... olur."},
                        {"prompt": "Bu dersin ana hedefi nedir?", "options": ["Saat ve program anlatımını kurmak", "Akkusativ çekimini bitirmek", "Geçmiş zaman mektubu yazmak"], "correct_index": 0, "explanation": "Bu dersin ana odağı zaman ve program anlatımıdır."},
                    ],
                },
            ],
            "homework": [
                "Bir haftalık mini program yaz: en az 5 gün adı ve 5 saat bilgisi kullan.",
                "Saat kalıpları için 10 örnek saat seç ve hepsini Almanca yaz.",
                "aufstehen, anfangen ve einkaufen ile en az ikişer cümle kur.",
                "von ... bis ... ile hem saat hem gün aralığı veren 4 cümle üret.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde artık saati yalnız sormak değil, ayrıntılı biçimde söylemek; günlere bağlı program kurmak "
                "ve kısa günlük planları Almanca anlatmak konusunda belirgin bir eşiği geçmiş olmalısın."
            ),
            "next_lesson": {
                "title": "Ders 9: Nominativ ve Akkusativ temeli",
                "status": "active",
                "slug": "ders-9-nominativ-ve-akkusativ-temeli",
            },
        },
        {
            "slug": "ders-9-nominativ-ve-akkusativ-temeli",
            "index": 9,
            "title": "Nominativ ve Akkusativ Temeli",
            "duration": "95-110 dk",
            "difficulty": "A1.2",
            "teaser": (
                "Bu derste özne ile nesnenin farkını sistematik biçimde ayırıyoruz. "
                "Nominativ ve Akkusativ temeli, özellikle der -> den, ein -> einen ve kein -> keinen değişimlerini "
                "doğru görmeni sağlayacak; böylece cümleler daha gerçek Almanca gibi kurulmaya başlayacak."
            ),
            "status": "active",
            "objectives": [
                "Nominativ ile Akkusativ arasındaki temel farkı kavramak.",
                "Maskulin isimlerde der -> den dönüşümünü görmek.",
                "Belirsiz ve olumsuz yapılarda ein -> einen, kein -> keinen farkını öğrenmek.",
                "wen / was sorularını nesne bulmak için kullanmak.",
                "sehen, lesen, kaufen, brauchen, suchen gibi fiillerle nesne kurmak.",
                "A1 seviyesinde kontrollü, basit ama doğru nesne cümleleri yazmak.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "19"},
                {"label": "Gramer odağı", "value": "Nominativ + Akkusativ"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Özne ve nesne aynı rol değildir",
                    "body": (
                        "Der Mann liest die Zeitung cümlesinde der Mann işi yapan öznedir, die Zeitung ise eylemin yöneldiği nesnedir. "
                        "Bu fark Almanca'da artikelleri etkileyebilir."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "Yalnızca bazı biçimler değişir",
                    "body": (
                        "İlk aşamada en kritik fark maskulin yapılarda görünür: der -> den, ein -> einen, kein -> keinen. "
                        "Bu yüzden bütün tabloyu aynı anda değil, en önemli dönüşümü merkeze alıyoruz."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "wen / was sorusu nesneyi gösterir",
                    "body": (
                        "Bir fiilin nesnesini bulmak için kimi / neyi yani wen / was sorularını sorarız. "
                        "Bu refleks, çekimi ezberden daha anlamlı kılar."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Her fiil değil, seçilmiş fiillerle başlıyoruz",
                    "body": (
                        "sehen, lesen, kaufen, suchen, brauchen ve haben gibi yüksek frekanslı fiillerle çalışmak, "
                        "Akkusativ konusunu gereksiz yük olmadan doğal hale getirir."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Dativ'e girmeden çekirdeği netleştiriyoruz",
                    "body": (
                        "Bu ders yalnızca Nominativ ve Akkusativ temelini kurar. "
                        "Dativ ve diğer ayrıntılar daha sonra geleceği için şimdilik odağı dağıtmıyoruz."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Nominativ nedir?",
                    "summary": "Cümlede işi yapan ya da cümlenin temel öznesi olan isim çoğu zaman Nominativ olur.",
                    "items": [
                        "Der Mann liest.",
                        "Die Frau arbeitet.",
                        "Das Kind lernt.",
                        "Die Kinder spielen.",
                    ],
                    "examples": [
                        "Der Lehrer spricht.",
                        "Die Lampe ist neu.",
                    ],
                },
                {
                    "title": "Akkusativ nedir?",
                    "summary": "Fiilin doğrudan etkilediği nesne çoğu zaman Akkusativ olur.",
                    "items": [
                        "Ich sehe den Mann.",
                        "Er liest die Zeitung.",
                        "Wir kaufen das Buch.",
                        "Sie suchen die Tasche.",
                    ],
                    "examples": [
                        "Das Kind hat einen Ball.",
                        "Ich brauche einen Stift.",
                    ],
                },
                {
                    "title": "Artikel değişimi",
                    "summary": "Erken A1 için en kritik dönüşüm maskulin yapılardadır.",
                    "items": [
                        "der -> den",
                        "ein -> einen",
                        "kein -> keinen",
                        "die -> die",
                        "das -> das",
                    ],
                    "examples": [
                        "der Schlüssel -> Ich suche den Schlüssel.",
                        "ein Apfel -> Ich kaufe einen Apfel.",
                        "kein Stift -> Ich habe keinen Stift.",
                    ],
                },
                {
                    "title": "wen / was ile nesneyi bul",
                    "summary": "Ezber yerine soru mantığıyla düşünmek daha sağlamdır.",
                    "items": [
                        "Wen siehst du? -> Den Lehrer.",
                        "Was liest du? -> Das Buch.",
                        "Was kaufst du? -> Einen Apfel.",
                    ],
                    "examples": [
                        "Wen suchst du? Ich suche den Freund.",
                        "Was brauchst du? Ich brauche einen Computer.",
                    ],
                },
                {
                    "title": "Akkusativ alan temel fiiller",
                    "summary": "Başlangıçta en sık gereken fiillerle sınırlı kalıyoruz.",
                    "items": [
                        "sehen = görmek",
                        "lesen = okumak",
                        "kaufen = satın almak",
                        "suchen = aramak",
                        "brauchen = ihtiyaç duymak",
                        "haben = sahip olmak",
                    ],
                    "examples": [
                        "Ich lese das Buch.",
                        "Wir kaufen einen Apfel.",
                        "Sie braucht eine Tasche.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Der Mann liest die Zeitung.", "tr": "Adam gazeteyi okuyor.", "note": "Özne ve nesneyi ayıran temel örnek."},
                {"de": "Ich sehe den Lehrer.", "tr": "Öğretmeni görüyorum.", "note": "der -> den dönüşümünü açık biçimde gösterir."},
                {"de": "Wir kaufen einen Apfel.", "tr": "Bir elma satın alıyoruz.", "note": "ein -> einen dönüşümü."},
                {"de": "Ich habe keinen Stift.", "tr": "Kalemim yok.", "note": "kein -> keinen dönüşümü."},
                {"de": "Sie sucht die Tasche.", "tr": "O çantayı arıyor.", "note": "Dişil isimde artikel değişmez."},
                {"de": "Er findet das Buch.", "tr": "O kitabı buluyor.", "note": "Nötr isimde artikel değişmez."},
                {"de": "Wen suchst du?", "tr": "Kimi arıyorsun?", "note": "İnsan nesnesi için wen sorusu."},
                {"de": "Was kaufst du?", "tr": "Ne satın alıyorsun?", "note": "Nesne sorusu için was kullanılır."},
                {"de": "Ich brauche einen Computer.", "tr": "Bir bilgisayara ihtiyacım var.", "note": "Maskulin belirsiz nesne."},
                {"de": "Wir lesen einen Brief.", "tr": "Bir mektup okuyoruz.", "note": "Bir başka maskulin nesne örneği."},
                {"de": "Das Kind hat einen Ball.", "tr": "Çocuğun bir topu var.", "note": "haben fiiliyle nesne kullanımı."},
                {"de": "Sie kauft keine Tasche.", "tr": "O çanta almıyor.", "note": "Dişil isimde keine yapısı."},
            ],
            "common_mistakes": [
                {
                    "wrong": "Ich sehe der Lehrer demek",
                    "right": "Ich sehe den Lehrer demek",
                    "reason": "Maskulin isim nesne olduğunda der -> den dönüşür.",
                },
                {
                    "wrong": "Bir nesne gördüğünde her artikelin değiştiğini sanmak",
                    "right": "Erken aşamada en kritik değişim maskulinde görülür",
                    "reason": "die ve das temel Akkusativ'de aynı kalır.",
                },
                {
                    "wrong": "Ich habe ein Stift demek",
                    "right": "Ich habe einen Stift demek",
                    "reason": "Maskulin belirsiz nesnede ein -> einen olur.",
                },
                {
                    "wrong": "kein ve nicht'i aynı yerde kullanmak",
                    "right": "İsim olumsuzluğunda önce kein yapısına odaklanmak",
                    "reason": "Bu dersin odağı isim nesneleriyle kurulan olumsuzluktur.",
                },
                {
                    "wrong": "wen / was sorusunu atlayıp yalnız sezgiyle gitmek",
                    "right": "Önce nesneye wen / was sorusu sormak",
                    "reason": "Bu yöntem çekimi daha sistemli oturtur.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "A", "text_de": "Was kaufst du?", "text_tr": "Ne satın alıyorsun?"},
                    {"speaker": "B", "text_de": "Ich kaufe einen Apfel und das Buch.", "text_tr": "Bir elma ve kitabı satın alıyorum."},
                    {"speaker": "A", "text_de": "Wen suchst du?", "text_tr": "Kimi arıyorsun?"},
                    {"speaker": "B", "text_de": "Ich suche den Lehrer.", "text_tr": "Öğretmeni arıyorum."},
                    {"speaker": "A", "text_de": "Hast du einen Stift?", "text_tr": "Bir kalemin var mı?"},
                    {"speaker": "B", "text_de": "Nein, ich habe keinen Stift.", "text_tr": "Hayır, kalemim yok."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Sınıf ve alışveriş metni",
                    "intro": "Bu metin özne-nesne farkını günlük hayat bağlamında açık biçimde gösterir.",
                    "word_focus": "18 kelime / kalıp",
                    "paragraphs": [
                        "Der [[Lehrer::öğretmen]] sieht den [[Schüler::öğrenci / erkek öğrenci]] und der Schüler liest die [[Zeitung::gazete]]. Dann sucht er den [[Schlüssel::anahtar]] und findet das [[Buch::kitap]].",
                        "Im Markt kauft meine [[Mutter::anne]] einen [[Apfel::elma]], einen [[Saft::meyve suyu]] und eine [[Tasche::çanta]]. Ich brauche einen [[Stift::kalem]] und einen [[Brief::mektup]] für den Kurs.",
                        "Mein Freund fragt: [[Wen suchst du?::Kimi arıyorsun?]] Ich sage: [[Ich suche den Lehrer.::Öğretmeni arıyorum.]] Danach fragt er: [[Was brauchst du?::Neye ihtiyacın var?]] Ich brauche keinen [[Ball::top]], aber ich brauche einen [[Computer::bilgisayar]].",
                    ],
                },
            ],
            "tips": [
                "Önce cümlede işi yapanı, sonra etkilenen nesneyi bul.",
                "Maskulin örnekleri özellikle ayrı bir liste halinde tekrar et: der -> den, ein -> einen, kein -> keinen.",
                "wen / was sorusunu sesli sormak, nesne refleksini hızlandırır.",
                "die ve das kelimelerinde değişim beklemediğini fark etmek kafa karışıklığını azaltır.",
                "Bu dersi çalışırken Dativ'i düşünme; odak yalnızca temel nesne yapısı olsun.",
            ],
            "vocabulary": [
                {"word": "Lehrer", "article": "der", "plural": "die Lehrer", "meanings": ["öğretmen", "erkek öğretmen"], "example_de": "Ich sehe den Lehrer.", "example_tr": "Öğretmeni görüyorum.", "note": "Maskulin Akkusativ için çok uygun örnek."},
                {"word": "Schüler", "article": "der", "plural": "die Schüler", "meanings": ["öğrenci", "erkek öğrenci"], "example_de": "Der Lehrer sieht den Schüler.", "example_tr": "Öğretmen öğrenciyi görüyor.", "note": "wen sorusu için iyi bir isimdir."},
                {"word": "Zeitung", "article": "die", "plural": "die Zeitungen", "meanings": ["gazete"], "example_de": "Er liest die Zeitung.", "example_tr": "O gazeteyi okuyor.", "note": "Dişil nesnede artikel değişmediğini gösterir."},
                {"word": "Schlüssel", "article": "der", "plural": "die Schlüssel", "meanings": ["anahtar"], "example_de": "Ich suche den Schlüssel.", "example_tr": "Anahtarı arıyorum.", "note": "der -> den dönüşümünü net gösterir."},
                {"word": "Stift", "article": "der", "plural": "die Stifte", "meanings": ["kalem"], "example_de": "Ich habe einen Stift.", "example_tr": "Bir kalemim var.", "note": "ein -> einen örneği."},
                {"word": "Apfel", "article": "der", "plural": "die Äpfel", "meanings": ["elma"], "example_de": "Wir kaufen einen Apfel.", "example_tr": "Bir elma satın alıyoruz.", "note": "Maskulin nesne dönüşümü için idealdir."},
                {"word": "Saft", "article": "der", "plural": "die Säfte", "meanings": ["meyve suyu", "su"], "example_de": "Sie kauft einen Saft.", "example_tr": "Bir meyve suyu alıyor.", "note": "Gıda dersine geçiş öncesi küçük köprü kurar."},
                {"word": "Ball", "article": "der", "plural": "die Bälle", "meanings": ["top"], "example_de": "Das Kind hat einen Ball.", "example_tr": "Çocuğun bir topu var.", "note": "haben ile maskulin nesne."},
                {"word": "Brief", "article": "der", "plural": "die Briefe", "meanings": ["mektup"], "example_de": "Wir lesen einen Brief.", "example_tr": "Bir mektup okuyoruz.", "note": "Okuma fiiliyle doğal bağ kurar."},
                {"word": "Computer", "article": "der", "plural": "die Computer", "meanings": ["bilgisayar"], "example_de": "Ich brauche einen Computer.", "example_tr": "Bir bilgisayara ihtiyacım var.", "note": "brauchen ile sık kullanılır."},
                {"word": "Buch", "article": "das", "plural": "die Bücher", "meanings": ["kitap"], "example_de": "Er findet das Buch.", "example_tr": "Kitabı buluyor.", "note": "Nötr nesnede artikel değişmediğini gösterir."},
                {"word": "Tasche", "article": "die", "plural": "die Taschen", "meanings": ["çanta"], "example_de": "Sie sucht die Tasche.", "example_tr": "Çantayı arıyor.", "note": "Dişil nesne örneği."},
                {"word": "sehen", "article": "-", "plural": "-", "meanings": ["görmek"], "example_de": "Ich sehe den Lehrer.", "example_tr": "Öğretmeni görüyorum.", "note": "wen / was ile sık kontrol edilir."},
                {"word": "lesen", "article": "-", "plural": "-", "meanings": ["okumak"], "example_de": "Wir lesen einen Brief.", "example_tr": "Bir mektup okuyoruz.", "note": "Nesne alan temel fiillerden biridir."},
                {"word": "kaufen", "article": "-", "plural": "-", "meanings": ["satın almak"], "example_de": "Sie kauft einen Apfel.", "example_tr": "Bir elma satın alıyor.", "note": "Günlük nesne cümlelerinde çok kullanılır."},
                {"word": "suchen", "article": "-", "plural": "-", "meanings": ["aramak"], "example_de": "Ich suche den Schlüssel.", "example_tr": "Anahtarı arıyorum.", "note": "Maskulin nesnelerle sık tekrar edilir."},
                {"word": "brauchen", "article": "-", "plural": "-", "meanings": ["ihtiyaç duymak"], "example_de": "Ich brauche einen Computer.", "example_tr": "Bir bilgisayara ihtiyacım var.", "note": "Nesne ihtiyacını açık anlatır."},
                {"word": "finden", "article": "-", "plural": "-", "meanings": ["bulmak"], "example_de": "Er findet das Buch.", "example_tr": "Kitabı buluyor.", "note": "sehen ve suchen ile doğal bir üçlü kurar."},
                {"word": "wen", "article": "-", "plural": "-", "meanings": ["kimi"], "example_de": "Wen suchst du?", "example_tr": "Kimi arıyorsun?", "note": "İnsan nesnesi için kullanılır."},
            ],
            "exercises": [
                {
                    "id": "article-shift",
                    "type": "single_choice",
                    "title": "Artikel Değişimi Testi",
                    "description": "Maskulin nesnede doğru artikel dönüşümünü seç.",
                    "questions": [
                        {"prompt": "Ich sehe ___ Lehrer.", "options": ["der", "den", "dem"], "correct_index": 1, "explanation": "Maskulin nesne olduğunda der -> den olur."},
                        {"prompt": "Wir suchen ___ Schlüssel.", "options": ["der", "den", "das"], "correct_index": 1, "explanation": "Schlüssel maskulindir; nesnede den gerekir."},
                        {"prompt": "Sie kauft ___ Apfel.", "options": ["der", "den", "die"], "correct_index": 1, "explanation": "Apfel maskulin nesne olduğunda den görür."},
                        {"prompt": "Er findet ___ Buch.", "options": ["das", "den", "dem"], "correct_index": 0, "explanation": "Nötr isimde artikel temel Akkusativ'de değişmez."},
                        {"prompt": "Sie liest ___ Zeitung.", "options": ["die", "den", "das"], "correct_index": 0, "explanation": "Dişil isimde artikel temel Akkusativ'de değişmez."},
                        {"prompt": "Das Kind hat ___ Ball.", "options": ["der", "den", "die"], "correct_index": 1, "explanation": "Ball maskulin nesnedir; den Ball olur."},
                    ],
                },
                {
                    "id": "ein-kein-shift",
                    "type": "single_choice",
                    "title": "ein / keinen Dönüşümü",
                    "description": "Belirsiz ve olumsuz maskulin nesne biçimini seç.",
                    "questions": [
                        {"prompt": "Ich habe ___ Stift.", "options": ["ein", "einen", "keinen"], "correct_index": 1, "explanation": "Maskulin nesnede ein -> einen olur."},
                        {"prompt": "Wir kaufen ___ Apfel.", "options": ["ein", "eine", "einen"], "correct_index": 2, "explanation": "Apfel maskulin nesnedir; einen Apfel gerekir."},
                        {"prompt": "Ich habe ___ Schlüssel.", "options": ["kein", "keinen", "keine"], "correct_index": 1, "explanation": "Maskulin nesnenin olumsuzu keinen olur."},
                        {"prompt": "Sie braucht ___ Tasche.", "options": ["keinen", "keine", "kein"], "correct_index": 1, "explanation": "Tasche dişildir; keine Tasche olur."},
                        {"prompt": "Er findet ___ Buch.", "options": ["ein", "einen", "keinen"], "correct_index": 0, "explanation": "Buch nötr isimdir; ein Buch biçimi korunur."},
                        {"prompt": "Wir lesen ___ Brief.", "options": ["ein", "eine", "einen"], "correct_index": 2, "explanation": "Brief maskulin nesnedir; einen Brief gerekir."},
                    ],
                },
                {
                    "id": "wen-was",
                    "type": "single_choice",
                    "title": "wen / was Testi",
                    "description": "Doğru soru kelimesini seçerek nesneyi bul.",
                    "questions": [
                        {"prompt": "___ suchst du? -> Den Lehrer.", "options": ["Wer", "Wen", "Was"], "correct_index": 1, "explanation": "İnsan nesnesi için wen sorulur."},
                        {"prompt": "___ kaufst du? -> Einen Apfel.", "options": ["Wen", "Was", "Wo"], "correct_index": 1, "explanation": "Nesne için was sorulur."},
                        {"prompt": "___ liest du? -> Das Buch.", "options": ["Was", "Wann", "Wie"], "correct_index": 0, "explanation": "Kitap nesne olduğu için was uygundur."},
                        {"prompt": "___ braucht sie? -> Einen Computer.", "options": ["Wen", "Was", "Wer"], "correct_index": 1, "explanation": "Cansız nesne için was sorulur."},
                        {"prompt": "___ siehst du? -> Den Schüler.", "options": ["Wen", "Was", "Woher"], "correct_index": 0, "explanation": "İnsan nesnesi için wen gerekir."},
                    ],
                },
                {
                    "id": "sentence-meaning",
                    "type": "single_choice",
                    "title": "Cümle Anlamı Testi",
                    "description": "Özne ve nesne farkını anlamla birlikte kontrol et.",
                    "questions": [
                        {"prompt": "Ich sehe den Lehrer.", "options": ["Öğretmeni görüyorum.", "Öğretmen beni görüyor.", "Öğretmene gidiyorum."], "correct_index": 0, "explanation": "den Lehrer nesnedir; gören kişi ben olurum."},
                        {"prompt": "Wir kaufen einen Apfel.", "options": ["Bir elma satın alıyoruz.", "Bir elmayı görüyoruz.", "Elma bizi satın alıyor."], "correct_index": 0, "explanation": "kaufen = satın almak."},
                        {"prompt": "Sie sucht die Tasche.", "options": ["Çantayı arıyor.", "Çantayı okuyor.", "Çantayı satıyor."], "correct_index": 0, "explanation": "suchen = aramak."},
                        {"prompt": "Er findet das Buch.", "options": ["Kitabı buluyor.", "Kitabı yazıyor.", "Kitabı kaybediyor."], "correct_index": 0, "explanation": "finden = bulmak."},
                        {"prompt": "Ich habe keinen Stift.", "options": ["Kalemim yok.", "Kalem alıyorum.", "Kalemi görüyorum."], "correct_index": 0, "explanation": "keinen Stift = kalem yok anlamı taşır."},
                    ],
                },
                {
                    "id": "gaps",
                    "type": "single_choice",
                    "title": "Boşluk Doldurma",
                    "description": "Nominativ ve Akkusativ ilişkisini doğru tamamla.",
                    "questions": [
                        {"prompt": "Der Schüler liest ___ Zeitung.", "options": ["die", "den", "dem"], "correct_index": 0, "explanation": "Zeitung dişil nesnedir; die değişmeden kalır."},
                        {"prompt": "Ich brauche ___ Computer.", "options": ["ein", "einen", "keinen"], "correct_index": 1, "explanation": "Computer maskulin nesnedir; einen gerekir."},
                        {"prompt": "Wir suchen ___ Schlüssel.", "options": ["der", "den", "das"], "correct_index": 1, "explanation": "Maskulin nesne den ile gelir."},
                        {"prompt": "Er hat ___ Ball.", "options": ["einen", "ein", "eine"], "correct_index": 0, "explanation": "Ball maskulin nesnedir; einen Ball olur."},
                        {"prompt": "Sie kauft ___ Tasche.", "options": ["eine", "einen", "kein"], "correct_index": 0, "explanation": "Tasche dişil nesnedir; eine Tasche kullanılır."},
                        {"prompt": "Ich habe ___ Stift.", "options": ["keinen", "keine", "kein"], "correct_index": 0, "explanation": "Stift maskulin nesnedir; keinen Stift olur."},
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Nominativ ve Akkusativ çekirdeğini birlikte yokla.",
                    "questions": [
                        {"prompt": "Hangisi doğrudur?", "options": ["Ich sehe der Mann.", "Ich sehe den Mann.", "Ich sehe dem Mann."], "correct_index": 1, "explanation": "Maskulin nesne den alır."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Ich habe ein Stift.", "Ich habe einen Stift.", "Ich habe keinen Tasche."], "correct_index": 1, "explanation": "Maskulin belirsiz nesnede einen gerekir."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Sie liest die Zeitung.", "Sie liest den Zeitung.", "Sie liest das Zeitung."], "correct_index": 0, "explanation": "Dişil nesnede die korunur."},
                        {"prompt": "Hangisi doğru sorudur?", "options": ["Wen suchst du?", "Wer suchst du?", "Was suchst du?"], "correct_index": 0, "explanation": "İnsan nesnesi için wen gerekir."},
                        {"prompt": "Bu dersin ana hedefi nedir?", "options": ["Özne ve nesneyi ayırmayı öğrenmek", "Saatleri tekrar etmek", "Yalnız yer soruları kurmak"], "correct_index": 0, "explanation": "Bu dersin ana odağı özne-nesne ayrımıdır."},
                    ],
                },
            ],
            "homework": [
                "sehen, lesen, kaufen, suchen ve brauchen fiilleriyle en az ikişer cümle kur.",
                "Maskulin nesneler için der -> den, ein -> einen, kein -> keinen tablosunu 10 örnekle tekrar et.",
                "wen ve was sorularını kullanarak 6 mini soru-cevap çifti yaz.",
                "Okuma metnindeki tüm nesneleri ayır ve hangilerinin Nominativ, hangilerinin Akkusativ olduğunu işaretle.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde artık Almanca cümlede kimin işi yaptığını ve eylemin neye yöneldiğini daha net görebiliyor "
                "olmalı; özellikle maskulin nesnelerdeki çekim değişimini bilinçli biçimde kullanmaya başlamalısın."
            ),
            "next_lesson": {
                "title": "Ders 10: Yiyecekler, içecekler ve sipariş kalıpları",
                "status": "active",
                "slug": "ders-10-yiyecekler-icecekler-ve-siparis-kaliplari",
            },
        },
        {
            "slug": "ders-10-yiyecekler-icecekler-ve-siparis-kaliplari",
            "index": 10,
            "title": "Yiyecekler, İçecekler ve Sipariş Kalıpları",
            "duration": "95-110 dk",
            "difficulty": "A1.2",
            "teaser": (
                "A1 kapanış dersinde günlük hayatta en sık karşılaşılan restoran ve kafe dilini topluyoruz. "
                "Yiyecek-içecek kelimelerini artikel ve anlamla oturtacak, sipariş verirken kullanılan temel kalıpları öğrenecek "
                "ve özellikle Akkusativ nesnenin menü cümlelerinde nasıl göründüğünü fark edeceksin."
            ),
            "status": "active",
            "objectives": [
                "18 temel yiyecek ve içecek kelimesini artikeliyle öğrenmek.",
                "Ich nehme ..., Ich bestelle ... ve Für mich ..., bitte. kalıplarını doğru kullanmak.",
                "Haben Sie ...?, Was kostet ...? ve Die Rechnung, bitte. ifadeleriyle temel restoran iletişimi kurmak.",
                "Maskulin nesnelerde einen / keinen biçimini sipariş bağlamında uygulamak.",
                "Kısa restoran diyaloglarını anlayıp benzer cevaplar üretmek.",
                "A1 seviyesinin kapanışında günlük ihtiyaç cümlelerini daha doğal kurmak.",
            ],
            "hero_stats": [
                {"label": "Kelime", "value": "18"},
                {"label": "Gramer odağı", "value": "Sipariş + Akkusativ"},
                {"label": "Alıştırma", "value": "6 modül"},
            ],
            "lesson_blocks": [
                {
                    "eyebrow": "1. Adım",
                    "title": "Menü kelimeleri artikel ile öğrenilir",
                    "body": (
                        "Apfel, Kaffee, Wasser, Suppe gibi kelimeler günlük hayat için çok önemlidir; ama bunları yalnız anlamıyla değil, "
                        "artikel ve çoğul biçimiyle birlikte öğrenmek gerekir. Böylece sipariş cümlesi kurarken doğru biçim daha hızlı gelir."
                    ),
                },
                {
                    "eyebrow": "2. Adım",
                    "title": "Siparişte kısa ve doğal kalıp gerekir",
                    "body": (
                        "Gerçek hayatta uzun cümle kurmadan da sipariş verirsin. Ich nehme einen Tee., Ich bestelle eine Suppe. "
                        "ve Für mich einen Salat, bitte. gibi yapılar A1 için hem doğal hem güvenli başlangıçtır."
                    ),
                },
                {
                    "eyebrow": "3. Adım",
                    "title": "Akkusativ artık gerçek bağlamda görünür",
                    "body": (
                        "Bir şeyi sipariş ettiğinde fiil doğrudan bir nesneye yönelir. Bu yüzden özellikle maskulin isimlerde "
                        "einen Kaffee, einen Salat, keinen Saft gibi biçimler artık sadece kural değil, gerçek kullanım hâline gelir."
                    ),
                },
                {
                    "eyebrow": "4. Adım",
                    "title": "Restoranda soru kalıpları kısa olur",
                    "body": (
                        "Haben Sie Wasser?, Was kostet die Pizza? ve Kommt der Kaffee jetzt? gibi yapılar gündelik iletişimin çekirdeğidir. "
                        "Burada amaç çok karmaşık konuşmak değil, ihtiyaç anında doğru kalıbı hızlı seçmektir."
                    ),
                },
                {
                    "eyebrow": "5. Adım",
                    "title": "Bu ders A1'i kapatır",
                    "body": (
                        "Önceki derslerde kurduğumuz artikel, fiil çekimi, zaman, nesne ve soru düzeni burada aynı sayfada buluşur. "
                        "Bu yüzden ders sonunda seviye bitirme testine geçmek mantıklı hâle gelir."
                    ),
                },
            ],
            "grammar_sections": [
                {
                    "title": "Yiyecek ve içecek kelimeleri artikel ile öğrenilir",
                    "summary": "Menü kelimeleri de diğer isimler gibi artikel ve çoğul biçimiyle alınmalıdır.",
                    "items": [
                        "der Kaffee, der Tee, der Salat gibi maskulin örnekler vardır",
                        "die Suppe, die Pizza, die Rechnung dişil örneklerdir",
                        "das Wasser, das Brot, das Restaurant nötr örneklerdir",
                        "Sipariş cümlesi kurarken artikel bilgisi özellikle nesne hâlinde önem kazanır",
                    ],
                    "examples": [
                        "der Kaffee = kahve",
                        "die Suppe = çorba",
                        "das Wasser = su",
                    ],
                },
                {
                    "title": "Siparişte en temel iki kalıp",
                    "summary": "A1 seviyesinde sipariş verirken önce kısa ve güvenli cümleler kuruyoruz.",
                    "items": [
                        "Ich nehme ... = ... alıyorum / istiyorum",
                        "Ich bestelle ... = ... sipariş ediyorum",
                        "Für mich ..., bitte. = Benim için ..., lütfen.",
                        "bitte ifadesi siparişi yumuşatır ve doğal hale getirir",
                    ],
                    "examples": [
                        "Ich nehme einen Tee.",
                        "Ich bestelle eine Pizza.",
                        "Für mich einen Salat, bitte.",
                    ],
                },
                {
                    "title": "Restoranda temel soru kalıpları",
                    "summary": "Yoklama, fiyat ve hesap isteme kalıpları günlük iletişimin omurgasını kurar.",
                    "items": [
                        "Haben Sie ...? = ... var mı?",
                        "Was kostet ...? = ... ne kadar?",
                        "Die Rechnung, bitte. = Hesap, lütfen.",
                        "Noch etwas? = Başka bir şey?",
                    ],
                    "examples": [
                        "Haben Sie Wasser?",
                        "Was kostet die Suppe?",
                        "Die Rechnung, bitte.",
                    ],
                },
                {
                    "title": "Siparişte Akkusativ nesne",
                    "summary": "Sipariş cümleleri çoğu zaman doğrudan nesne içerir; bu yüzden maskulin dönüşümler görünür hale gelir.",
                    "items": [
                        "der Kaffee -> einen Kaffee",
                        "der Salat -> einen Salat",
                        "ein Tee -> einen Tee",
                        "kein Saft -> keinen Saft",
                    ],
                    "examples": [
                        "Ich nehme einen Kaffee.",
                        "Wir bestellen einen Salat.",
                        "Ich nehme keinen Saft.",
                    ],
                },
                {
                    "title": "Kısa restoran diyaloğu mantığı",
                    "summary": "Siparişte soru, cevap ve kapanış çok kısa bloklar halinde ilerler.",
                    "items": [
                        "Garson sorar: Was möchten Sie? / Haben Sie ...?",
                        "Müşteri cevap verir: Ich nehme ... / Für mich ..., bitte.",
                        "Gerekirse fiyat sorulur: Was kostet ...?",
                        "Kapanışta hesap istenir: Die Rechnung, bitte.",
                    ],
                    "examples": [
                        "A: Was möchten Sie? / B: Ich nehme einen Tee.",
                        "A: Noch etwas? / B: Nein, danke.",
                    ],
                },
            ],
            "phrase_bank": [
                {"de": "Ich nehme einen Kaffee.", "tr": "Bir kahve alıyorum / istiyorum.", "note": "Siparişte güvenli ve doğal başlangıç kalıbı."},
                {"de": "Ich bestelle eine Pizza.", "tr": "Bir pizza sipariş ediyorum.", "note": "Sipariş vermeyi açıkça söyleyen yapı."},
                {"de": "Für mich einen Tee, bitte.", "tr": "Benim için bir çay, lütfen.", "note": "Kısa ve günlük sipariş kalıbı."},
                {"de": "Haben Sie Wasser?", "tr": "Suyunuz var mı?", "note": "Bir şeyin mevcut olup olmadığını sorar."},
                {"de": "Was kostet der Salat?", "tr": "Salata ne kadar?", "note": "Fiyat sorarken kullanılır."},
                {"de": "Noch etwas?", "tr": "Başka bir şey?", "note": "Garsonun tipik kısa sorusu."},
                {"de": "Nein, danke.", "tr": "Hayır, teşekkürler.", "note": "Kibar ve kısa kapanış cevabı."},
                {"de": "Die Rechnung, bitte.", "tr": "Hesap, lütfen.", "note": "Restoranda en temel kapanış kalıplarından biri."},
                {"de": "Ich nehme keinen Saft.", "tr": "Meyve suyu almıyorum / istemiyorum.", "note": "Olumsuz sipariş örneği."},
                {"de": "Wir bestellen eine Suppe und ein Wasser.", "tr": "Bir çorba ve bir su sipariş ediyoruz.", "note": "Birden fazla nesneli sipariş cümlesi."},
            ],
            "common_mistakes": [
                {
                    "wrong": "Ich bin einen Kaffee.",
                    "right": "Ich nehme einen Kaffee.",
                    "reason": "Sipariş verirken sein değil, nesne alan doğal sipariş fiilleri kullanılır.",
                },
                {
                    "wrong": "Ich bestelle der Salat.",
                    "right": "Ich bestelle den Salat.",
                    "reason": "Maskulin nesne Akkusativ olduğunda artikel değişir.",
                },
                {
                    "wrong": "Ich habe nicht Saft.",
                    "right": "Ich nehme keinen Saft.",
                    "reason": "İsim olumsuzluğunda doğrudan kein/keine/keinen yapısı tercih edilir.",
                },
            ],
            "mini_dialogue": {
                "title": "Mini diyalog",
                "lines": [
                    {"speaker": "Garson", "text_de": "Guten Tag. Was möchten Sie?", "text_tr": "İyi günler. Ne alırsınız?"},
                    {"speaker": "Müşteri", "text_de": "Ich nehme einen Kaffee und einen Salat, bitte.", "text_tr": "Bir kahve ve bir salata alayım, lütfen."},
                    {"speaker": "Garson", "text_de": "Noch etwas?", "text_tr": "Başka bir şey?"},
                    {"speaker": "Müşteri", "text_de": "Nein, danke. Die Rechnung, bitte.", "text_tr": "Hayır, teşekkürler. Hesap, lütfen."},
                ],
            },
            "reading_passages": [
                {
                    "title": "Kafede kısa sipariş",
                    "intro": "Yeni kelimeleri menü bağlamında görmek, ezberden daha kalıcıdır.",
                    "word_focus": "10 kelime / kalıp",
                    "paragraphs": [
                        "Im [[Restaurant::restoran]] liest Ece die [[Speisekarte::menü / yemek listesi]]. Sie nimmt [[einen Kaffee::bir kahve]] und [[einen Salat::bir salata]].",
                        "Der [[Kellner::erkek garson]] fragt: [[Noch etwas?::başka bir şey?]] Ece sagt: [[Nein, danke.::hayır, teşekkürler]] [[Die Rechnung, bitte.::hesap, lütfen]]",
                    ],
                },
            ],
            "tips": [
                "Yiyecek kelimelerini artikel + isim + örnek sipariş cümlesi olarak tekrar et.",
                "Maskulin nesnelerde einen ve keinen biçimini özellikle sesli tekrar et.",
                "Bir sipariş kalıbını tek kelime değil, bütün cümle halinde ezberle.",
                "Haben Sie ...?, Was kostet ...? ve Die Rechnung, bitte. çizgisini günlük konuşma blokları gibi tekrar et.",
                "Okuma parçasını bir garson-müşteri diyaloğu gibi sesli canlandır.",
            ],
            "vocabulary": [
                {"word": "Kaffee", "article": "der", "plural": "die Kaffees", "meanings": ["kahve"], "example_de": "Ich nehme einen Kaffee.", "example_tr": "Bir kahve alıyorum.", "note": "Siparişlerde çok sık geçen maskulin isim."},
                {"word": "Tee", "article": "der", "plural": "die Tees", "meanings": ["çay"], "example_de": "Für mich einen Tee, bitte.", "example_tr": "Benim için bir çay, lütfen.", "note": "Kısa sipariş kalıbı için iyi örnek."},
                {"word": "Salat", "article": "der", "plural": "die Salate", "meanings": ["salata"], "example_de": "Der Salat kostet acht Euro.", "example_tr": "Salata sekiz euro.", "note": "Akkusativ dönüşümü görünür hale getiren maskulin isim."},
                {"word": "Saft", "article": "der", "plural": "die Säfte", "meanings": ["meyve suyu"], "example_de": "Ich nehme keinen Saft.", "example_tr": "Meyve suyu almıyorum.", "note": "keinen biçimi için kullanışlı örnek."},
                {"word": "Apfel", "article": "der", "plural": "die Äpfel", "meanings": ["elma"], "example_de": "Ich kaufe einen Apfel.", "example_tr": "Bir elma satın alıyorum.", "note": "Yiyecek alanında maskulin nesne alıştırmaları için uygun."},
                {"word": "Brot", "article": "das", "plural": "die Brote", "meanings": ["ekmek"], "example_de": "Das Brot ist frisch.", "example_tr": "Ekmek taze.", "note": "Nötr yiyecek ismi örneği."},
                {"word": "Wasser", "article": "das", "plural": "die Wasser", "meanings": ["su"], "example_de": "Haben Sie Wasser?", "example_tr": "Suyunuz var mı?", "note": "Temel içecek kelimesi; soru kalıplarıyla birlikte öğrenilir."},
                {"word": "Restaurant", "article": "das", "plural": "die Restaurants", "meanings": ["restoran"], "example_de": "Das Restaurant ist klein.", "example_tr": "Restoran küçük.", "note": "Bağlam kelimesi; mekân konuşmasını güçlendirir."},
                {"word": "Frühstück", "article": "das", "plural": "die Frühstücke", "meanings": ["kahvaltı"], "example_de": "Das Frühstück ist um acht Uhr.", "example_tr": "Kahvaltı saat sekizde.", "note": "Yemek düzeni ve zaman cümlelerini bağlar."},
                {"word": "Mittagessen", "article": "das", "plural": "die Mittagessen", "meanings": ["öğle yemeği"], "example_de": "Das Mittagessen kostet zehn Euro.", "example_tr": "Öğle yemeği on euro.", "note": "Yemek ve fiyat anlatımı için yararlı."},
                {"word": "Abendessen", "article": "das", "plural": "die Abendessen", "meanings": ["akşam yemeği"], "example_de": "Wir essen das Abendessen um sieben Uhr.", "example_tr": "Akşam yemeğini saat yedide yiyoruz.", "note": "Günlük rutin ile menü alanını bağlar."},
                {"word": "Menü", "article": "das", "plural": "die Menüs", "meanings": ["menü"], "example_de": "Das Menü ist heute kurz.", "example_tr": "Menü bugün kısa.", "note": "Restoran bağlamında sık geçer."},
                {"word": "Suppe", "article": "die", "plural": "die Suppen", "meanings": ["çorba"], "example_de": "Ich bestelle eine Suppe.", "example_tr": "Bir çorba sipariş ediyorum.", "note": "Dişil sipariş nesnesi örneği."},
                {"word": "Pizza", "article": "die", "plural": "die Pizzen", "meanings": ["pizza"], "example_de": "Die Pizza ist groß.", "example_tr": "Pizza büyük.", "note": "Yaygın ve tanıdık yiyecek kelimesi."},
                {"word": "Milch", "article": "die", "plural": "die Milchsorten", "meanings": ["süt"], "example_de": "Die Milch ist kalt.", "example_tr": "Süt soğuk.", "note": "İçecek grubunu genişletir."},
                {"word": "Rechnung", "article": "die", "plural": "die Rechnungen", "meanings": ["hesap", "fatura"], "example_de": "Die Rechnung, bitte.", "example_tr": "Hesap, lütfen.", "note": "Kapanış kalıbının ana kelimesi."},
                {"word": "Kellner", "article": "der", "plural": "die Kellner", "meanings": ["garson", "erkek garson"], "example_de": "Der Kellner kommt jetzt.", "example_tr": "Garson şimdi geliyor.", "note": "Restoran diyaloglarının kişi kelimesi."},
                {"word": "Kellnerin", "article": "die", "plural": "die Kellnerinnen", "meanings": ["garson", "kadın garson"], "example_de": "Die Kellnerin fragt: Noch etwas?", "example_tr": "Garson soruyor: Başka bir şey?", "note": "Kişi kelime çiftlerini tamamlar."},
                {"word": "Speisekarte", "article": "die", "plural": "die Speisekarten", "meanings": ["menü", "yemek listesi"], "example_de": "Ich lese die Speisekarte.", "example_tr": "Menüyü okuyorum.", "note": "Okuma metninde ve nesne cümlelerinde işe yarar."},
            ],
            "exercises": [
                {
                    "id": "menu-articles",
                    "type": "single_choice",
                    "title": "Menü Artikel Testi",
                    "description": "Yiyecek ve içecek kelimelerini doğru artikel ile eşleştir.",
                    "questions": [
                        {"prompt": "___ Kaffee", "options": ["der", "die", "das"], "correct_index": 0, "explanation": "Kaffee maskulin isimdir."},
                        {"prompt": "___ Pizza", "options": ["der", "die", "das"], "correct_index": 1, "explanation": "Pizza dişil isimdir."},
                        {"prompt": "___ Wasser", "options": ["der", "die", "das"], "correct_index": 2, "explanation": "Wasser nötr isimdir."},
                        {"prompt": "___ Rechnung", "options": ["der", "die", "das"], "correct_index": 1, "explanation": "Rechnung dişil isimdir."},
                        {"prompt": "___ Salat", "options": ["der", "die", "das"], "correct_index": 0, "explanation": "Salat maskulin isimdir."},
                        {"prompt": "___ Brot", "options": ["der", "die", "das"], "correct_index": 2, "explanation": "Brot nötr isimdir."},
                    ],
                },
                {
                    "id": "ordering-core",
                    "type": "single_choice",
                    "title": "Sipariş Kalıbı Testi",
                    "description": "Doğru sipariş cümlesini seç.",
                    "questions": [
                        {"prompt": "\"Bir çay alıyorum.\"", "options": ["Ich nehme einen Tee.", "Ich bin einen Tee.", "Ich habe Tee einen."], "correct_index": 0, "explanation": "Siparişte Ich nehme ... doğal ve doğru yapıdır."},
                        {"prompt": "\"Bir pizza sipariş ediyorum.\"", "options": ["Ich bestelle eine Pizza.", "Ich bestelle einen Pizza.", "Ich nehme die Pizza ist."], "correct_index": 0, "explanation": "Pizza dişildir; eine Pizza gerekir."},
                        {"prompt": "\"Benim için bir kahve, lütfen.\"", "options": ["Für mich einen Kaffee, bitte.", "Ich für mich Kaffee.", "Bitte mich einen Kaffee."], "correct_index": 0, "explanation": "Kısa sipariş kalıbı böyle kurulur."},
                        {"prompt": "\"Meyve suyu almıyorum.\"", "options": ["Ich nehme keinen Saft.", "Ich nehme nicht Saft.", "Ich bin keinen Saft."], "correct_index": 0, "explanation": "İsim olumsuzluğunda keinen Saft kullanılır."},
                        {"prompt": "\"Bir salata ve bir su sipariş ediyoruz.\"", "options": ["Wir bestellen einen Salat und ein Wasser.", "Wir bestellen ein Salat und einen Wasser.", "Wir sind einen Salat und ein Wasser."], "correct_index": 0, "explanation": "Salat maskulin, Wasser nötr biçimde gelir."},
                    ],
                },
                {
                    "id": "restaurant-questions",
                    "type": "single_choice",
                    "title": "Restoran Soruları",
                    "description": "Garson veya müşteri olarak doğru soru kalıbını seç.",
                    "questions": [
                        {"prompt": "\"Suyunuz var mı?\"", "options": ["Haben Sie Wasser?", "Sind Sie Wasser?", "Was haben Wasser?"], "correct_index": 0, "explanation": "Bir şeyin varlığını kibarca sormanın temel yollarından biridir."},
                        {"prompt": "\"Salata ne kadar?\"", "options": ["Was kostet der Salat?", "Wie heißt der Salat?", "Wo kostet der Salat?"], "correct_index": 0, "explanation": "Fiyat sormak için Was kostet ...? kullanılır."},
                        {"prompt": "\"Başka bir şey?\"", "options": ["Noch etwas?", "Wie alt?", "Woher?"], "correct_index": 0, "explanation": "Kısa servis sorusu olarak çok sık geçer."},
                        {"prompt": "\"Hesap, lütfen.\"", "options": ["Die Rechnung, bitte.", "Die Speisekarte, bitte.", "Der Kaffee, bitte."], "correct_index": 0, "explanation": "Rechnung hesap anlamı taşır."},
                        {"prompt": "\"Menüde çorba var mı?\"", "options": ["Gibt es eine Suppe?", "Es gibt eine Suppe?", "Wo ist eine Suppe?"], "correct_index": 0, "explanation": "Var mı sorusunda fiil başa geçer: Gibt es ...?"},
                    ],
                },
                {
                    "id": "accusative-ordering",
                    "type": "single_choice",
                    "title": "Siparişte Akkusativ",
                    "description": "Özellikle maskulin nesnelerde doğru biçimi seç.",
                    "questions": [
                        {"prompt": "Ich nehme ___ Kaffee.", "options": ["ein", "einen", "keinen"], "correct_index": 1, "explanation": "Kaffee maskulin nesnedir; einen Kaffee gerekir."},
                        {"prompt": "Wir bestellen ___ Salat.", "options": ["ein", "einen", "eine"], "correct_index": 1, "explanation": "Salat maskulin nesnedir; einen Salat kullanılır."},
                        {"prompt": "Ich nehme ___ Saft.", "options": ["kein", "keinen", "keine"], "correct_index": 1, "explanation": "Saft maskulin olduğu için olumsuz biçim keinen olur."},
                        {"prompt": "Er bestellt ___ Pizza.", "options": ["einen", "eine", "ein"], "correct_index": 1, "explanation": "Pizza dişildir; eine Pizza gerekir."},
                        {"prompt": "Sie nimmt ___ Wasser.", "options": ["ein", "einen", "eine"], "correct_index": 0, "explanation": "Wasser nötr isimdir; ein Wasser olur."},
                        {"prompt": "Ich lese ___ Speisekarte.", "options": ["die", "den", "das"], "correct_index": 0, "explanation": "Speisekarte dişil nesnedir; die korunur."},
                    ],
                },
                {
                    "id": "dialogue-meaning",
                    "type": "single_choice",
                    "title": "Diyalog Anlama",
                    "description": "Kısa restoran diyaloglarının anlamını seç.",
                    "questions": [
                        {"prompt": "Garson: Was möchten Sie? / Müşteri: Ich nehme einen Tee.", "options": ["Bir çay alayım.", "Çayı nerede bulabilirim?", "Ben çayım."], "correct_index": 0, "explanation": "Ich nehme ... siparişte doğal cevap kalıbıdır."},
                        {"prompt": "Garson: Noch etwas? / Müşteri: Nein, danke.", "options": ["Başka bir şey? / Hayır, teşekkürler.", "Bu ne kadar? / Pahalı.", "Nerelisin? / Ankara'danım."], "correct_index": 0, "explanation": "Kısa servis devamı ve kapanış ifadesidir."},
                        {"prompt": "Müşteri: Die Rechnung, bitte.", "options": ["Hesap, lütfen.", "Menü, lütfen.", "Bir kahve, lütfen."], "correct_index": 0, "explanation": "Rechnung = hesap / fatura."},
                        {"prompt": "Müşteri: Haben Sie Wasser?", "options": ["Suyunuz var mı?", "Su nerede?", "Su kaç para?"], "correct_index": 0, "explanation": "Haben Sie ...? mevcut olup olmadığını sorar."},
                        {"prompt": "Müşteri: Für mich einen Salat, bitte.", "options": ["Benim için bir salata, lütfen.", "Salatayı buluyorum.", "Salatayı ödemiyorum."], "correct_index": 0, "explanation": "Kısa ve kibar sipariş kalıbıdır."},
                    ],
                },
                {
                    "id": "review",
                    "type": "single_choice",
                    "title": "Ders Sonu Tekrar",
                    "description": "Yiyecek, içecek, soru ve Akkusativ bilgisini birlikte yokla.",
                    "questions": [
                        {"prompt": "Hangisi doğrudur?", "options": ["Ich bestelle den Salat.", "Ich bestelle der Salat.", "Ich bestelle dem Salat."], "correct_index": 0, "explanation": "Maskulin nesne Akkusativ olduğunda den alır."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Was kostet die Suppe?", "Wie kostet die Suppe?", "Wo kostet die Suppe?"], "correct_index": 0, "explanation": "Fiyat sorusu Was kostet ...? kalıbıyla kurulur."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Für mich einen Tee, bitte.", "Für mich ein Tee bitte ist.", "Ich bin einen Tee, bitte."], "correct_index": 0, "explanation": "Kısa sipariş kalıbı doğal olarak böyle kurulur."},
                        {"prompt": "Hangisi doğrudur?", "options": ["Ich nehme keinen Saft.", "Ich nehme nicht Saft.", "Ich nehme keine Saft."], "correct_index": 0, "explanation": "Maskulin isimlerde olumsuz biçim keinen olur."},
                        {"prompt": "Bu dersin ana hedefi nedir?", "options": ["Akkusativ nesneyi günlük sipariş bağlamında kullanmak", "Sadece saatleri tekrar etmek", "Yalnız milliyet söylemek"], "correct_index": 0, "explanation": "Ders, A1 kapanışında sipariş ve nesne kullanımını birleştirir."},
                    ],
                },
            ],
            "homework": [
                "Kahve, çay, çorba, salata ve pizza ile en az beş sipariş cümlesi yaz.",
                "Haben Sie ...?, Was kostet ...? ve Die Rechnung, bitte. kalıplarıyla üç kısa restoran diyaloğu kur.",
                "Maskulin yiyecek ve içecek isimleriyle einen / keinen biçimini 10 örnek cümlede tekrar et.",
                "Okuma metnindeki tüm nesneleri ayır ve hangilerinin Akkusativ olduğunu işaretle.",
            ],
            "completion_note": (
                "Bu dersi bitirdiğinde artık günlük ihtiyaç diliyle gerçek Almanca arasında daha somut bir bağ kurmuş olmalısın; "
                "özellikle sipariş, soru sorma ve nesne kullanımında A1 omurgası tamamlanmış olur."
            ),
            "next_lesson": {
                "title": "A1 Seviye Bitirme Testi",
                "status": "active",
                "kind": "level_test",
            },
        },
    ]
}
SEIN_PRONOUN_DRILLS = [
    {"pronoun": "ich", "pronoun_tr": "ben", "verb": "bin"},
    {"pronoun": "du", "pronoun_tr": "sen", "verb": "bist"},
    {"pronoun": "er", "pronoun_tr": "o (erkek)", "verb": "ist"},
    {"pronoun": "sie", "pronoun_tr": "o (kadın)", "verb": "ist"},
    {"pronoun": "es", "pronoun_tr": "o (nötr)", "verb": "ist"},
    {"pronoun": "wir", "pronoun_tr": "biz", "verb": "sind"},
    {"pronoun": "ihr", "pronoun_tr": "siz", "verb": "seid"},
    {"pronoun": "sie", "pronoun_tr": "onlar", "verb": "sind"},
    {"pronoun": "Sie", "pronoun_tr": "Siz (resmî)", "verb": "sind"},
]


def _meaning_label(item):
    return ", ".join(item.get("meanings", [])[:2])


def _word_label(item, include_article=True):
    if include_article and item.get("article") not in {"", "-", None}:
        return f"{item['article']} {item['word']}"
    return item["word"]


def _unique_pool(values):
    seen = set()
    unique = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _build_options(correct, pool, rng, option_count=3):
    distractors = [value for value in _unique_pool(pool) if value != correct]
    rng.shuffle(distractors)
    options = [correct] + distractors[: option_count - 1]
    if len(options) < option_count:
        return None
    rng.shuffle(options)
    return options


def _question(prompt, options, correct, explanation):
    return {
        "prompt": prompt,
        "options": options,
        "correct_index": options.index(correct),
        "explanation": explanation,
    }


def _generate_article_module(nouns):
    questions = []
    for item in nouns:
        options = ["der", "die", "das"]
        correct = item["article"]
        questions.append(
            _question(
                f"___ {item['word']}",
                options,
                correct,
                f"{item['word']} kelimesi {correct} ile kullanılır.",
            )
        )

    return {
        "id": "article-marathon",
        "type": "single_choice",
        "title": "Artikel Maratonu",
        "description": "Tüm isimleri hızlıca artikel ile eşleştir.",
        "questions": questions,
    }


def _generate_plural_module(nouns, rng):
    pool = [item["plural"] for item in nouns]
    questions = []

    for item in nouns:
        correct = item["plural"]
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                f"{_word_label(item)} kelimesinin çoğulu hangisi?",
                options,
                correct,
                f"{_word_label(item)} için doğru çoğul {correct} şeklindedir.",
            )
        )

    return {
        "id": "plural-marathon",
        "type": "single_choice",
        "title": "Çoğul Maratonu",
        "description": "Tekil kelimelerin çoğullarını hızlıca tekrar et.",
        "questions": questions,
    }


def _generate_meaning_module(vocabulary, rng):
    pool = [_meaning_label(item) for item in vocabulary]
    questions = []

    for item in vocabulary:
        correct = _meaning_label(item)
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                _word_label(item),
                options,
                correct,
                f"{_word_label(item)} ifadesi en çok '{correct}' anlam grubuna yakındır.",
            )
        )

    return {
        "id": "meaning-marathon",
        "type": "single_choice",
        "title": "Kelime Anlamı Maratonu",
        "description": "Her kelimeyi en yakın anlam grubuyla eşleştir.",
        "questions": questions,
    }


def _generate_reverse_meaning_module(vocabulary, rng):
    pool = [_word_label(item) for item in vocabulary]
    questions = []

    for item in vocabulary:
        correct = _word_label(item)
        prompt = f"'{_meaning_label(item)}' anlamına en uygun Almanca hangisi?"
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                prompt,
                options,
                correct,
                f"Bu anlam grubu için doğru seçenek {correct} olur.",
            )
        )

    return {
        "id": "reverse-meaning-marathon",
        "type": "single_choice",
        "title": "Ters Yönden Kelime Testi",
        "description": "Bu kez Türkçe anlamdan doğru Almanca kelimeyi bul.",
        "questions": questions,
    }


def _generate_example_gap_module(vocabulary, rng):
    pool = [item["word"] for item in vocabulary]
    questions = []

    for item in vocabulary:
        example = item.get("example_de", "")
        if item["word"] not in example:
            continue

        blanked = example.replace(item["word"], "_____", 1)
        prompt = f"{blanked} ({item['example_tr']})"
        correct = item["word"]
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                prompt,
                options,
                correct,
                f"Bu örnekte boşluğa gelen kelime {correct} olur.",
            )
        )

    return {
        "id": "example-gap-marathon",
        "type": "single_choice",
        "title": "Örnek Cümle Tamamlama",
        "description": "Örnek cümlelerde eksik kelimeyi tamamla.",
        "questions": questions,
    }


def _generate_phrase_to_german_module(phrase_bank, rng):
    pool = [item["de"] for item in phrase_bank]
    questions = []

    for item in phrase_bank:
        correct = item["de"]
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                f'Türkçesi "{item["tr"]}" olan ifade hangisi?',
                options,
                correct,
                item.get("note", "") or f"Doğru ifade {correct}.",
            )
        )

    return {
        "id": "phrase-to-german-marathon",
        "type": "single_choice",
        "title": "Kalıp Çeviri Turu",
        "description": "Türkçe ifadelerden doğru Almanca kalıbı seç.",
        "questions": questions,
    }


def _generate_phrase_to_turkish_module(phrase_bank, rng):
    pool = [item["tr"] for item in phrase_bank]
    questions = []

    for item in phrase_bank:
        correct = item["tr"]
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                f'"{item["de"]}" ifadesinin Türkçesi hangisi?',
                options,
                correct,
                item.get("note", "") or f"Bu ifadenin en uygun karşılığı {correct}.",
            )
        )

    return {
        "id": "phrase-to-turkish-marathon",
        "type": "single_choice",
        "title": "Kalıp Anlama Turu",
        "description": "Almanca kalıpların Türkçe karşılığını hızlıca tekrar et.",
        "questions": questions,
    }


def _generate_pronoun_translation_module(rng):
    pool = [item["pronoun"] for item in SEIN_PRONOUN_DRILLS]
    questions = []

    for item in SEIN_PRONOUN_DRILLS:
        correct = item["pronoun"]
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                f'"{item["pronoun_tr"]}" anlamına gelen zamir hangisi?',
                options,
                correct,
                f"Bu anlam grubu için doğru zamir {correct}.",
            )
        )

    return {
        "id": "pronoun-translation-marathon",
        "type": "single_choice",
        "title": "Zamir Anlam Turu",
        "description": "Türkçe kişi anlamlarından doğru zamiri seç.",
        "questions": questions,
    }


def _generate_sein_conjugation_module(rng):
    pool = ["bin", "bist", "ist", "sind", "seid"]
    questions = []

    for item in SEIN_PRONOUN_DRILLS:
        correct = item["verb"]
        options = _build_options(correct, pool, rng)
        if not options:
            continue
        questions.append(
            _question(
                f"{item['pronoun']} ile sein fiilinin doğru çekimi hangisi?",
                options,
                correct,
                f"{item['pronoun']} ile {correct} kullanılır.",
            )
        )

    return {
        "id": "sein-conjugation-marathon",
        "type": "single_choice",
        "title": "sein Çekim Turu",
        "description": "sein fiilini zamire göre hızlıca tekrar et.",
        "questions": questions,
    }


def _build_generated_exercises(lesson, rng):
    generated = []
    vocabulary = lesson.get("vocabulary", [])
    nouns = [
        item for item in vocabulary
        if item.get("article") in {"der", "die", "das"} and item.get("plural") not in {"", "-", None}
    ]
    phrase_bank = lesson.get("phrase_bank", [])

    if nouns:
        generated.append(_generate_article_module(nouns))
        generated.append(_generate_plural_module(nouns, rng))

    if vocabulary:
        generated.append(_generate_meaning_module(vocabulary, rng))
        generated.append(_generate_reverse_meaning_module(vocabulary, rng))
        generated.append(_generate_example_gap_module(vocabulary, rng))

    if phrase_bank:
        generated.append(_generate_phrase_to_german_module(phrase_bank, rng))
        generated.append(_generate_phrase_to_turkish_module(phrase_bank, rng))

    if lesson["slug"] == "ders-2-kisi-zamirleri-ve-sein-fiili":
        generated.append(_generate_pronoun_translation_module(rng))
        generated.append(_generate_sein_conjugation_module(rng))

    return [exercise for exercise in generated if exercise.get("questions")]


def _enrich_lesson_meta(lesson):
    total_questions = sum(len(exercise.get("questions", [])) for exercise in lesson.get("exercises", []))
    total_modules = len(lesson.get("exercises", []))
    lesson["exercise_question_count"] = total_questions
    lesson["exercise_module_count"] = total_modules

    hero_stats = []
    for stat in lesson.get("hero_stats", []):
        updated_stat = dict(stat)
        if updated_stat.get("label", "").lower() in {"alistirma", "alıştırma"}:
            updated_stat["value"] = f"{total_modules} modül"
        hero_stats.append(updated_stat)

    if not any(stat.get("label", "").lower() == "soru" for stat in hero_stats):
        hero_stats.append({"label": "Soru", "value": str(total_questions)})

    lesson["hero_stats"] = hero_stats
    return lesson


def get_german_course_overview():
    levels = []
    for level in GERMAN_COURSE_LEVELS:
        lessons = GERMAN_LESSONS.get(level["slug"], [])
        enriched = dict(level)
        enriched["available_lessons"] = len(lessons)
        enriched["next_open_lesson"] = lessons[0] if lessons else None
        levels.append(enriched)
    return levels


def _shuffle_lesson_exercises(lesson, rng):
    for exercise in lesson.get("exercises", []):
        questions = exercise.get("questions", [])
        if len(questions) > 1:
            original_prompts = [question.get("prompt") for question in questions]
            rng.shuffle(questions)
            if [question.get("prompt") for question in questions] == original_prompts:
                questions.append(questions.pop(0))

        for question in questions:
            options = list(question.get("options", []))
            if len(options) < 2:
                continue

            original_options = list(options)
            correct_option = options[question["correct_index"]]
            rng.shuffle(options)
            if options == original_options:
                options.append(options.pop(0))
            question["options"] = options
            question["correct_index"] = options.index(correct_option)

    return lesson


def get_german_lesson(level_slug, lesson_slug):
    lessons = GERMAN_LESSONS.get(level_slug, [])
    for lesson in lessons:
        if lesson["slug"] == lesson_slug:
            rng = SystemRandom()
            prepared_lesson = deepcopy(lesson)
            prepared_lesson = _prepare_reading_passages(prepared_lesson)
            prepared_lesson = _prepare_grammar_sections(prepared_lesson)
            prepared_lesson["exercises"] = prepared_lesson.get("exercises", []) + _build_generated_exercises(prepared_lesson, rng)
            prepared_lesson = _enrich_lesson_meta(prepared_lesson)
            return _shuffle_lesson_exercises(prepared_lesson, rng)
    return None
