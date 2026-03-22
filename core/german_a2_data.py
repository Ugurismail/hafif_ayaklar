from copy import deepcopy


A2_SCOPE_MATRIX = [
    {"topic": "Perfekt ve geçmiş deneyim anlatımı", "teacher_flow": "Perfekt slaytları ve sein/haben örnekleri", "platform_flow": "Ders 1", "status": "covered"},
    {"topic": "Yer bildirme ve Wechselpräpositionen", "teacher_flow": "Oda konumu ve Wo? alıştırmaları", "platform_flow": "Ders 2", "status": "covered"},
    {"topic": "Restoranda sipariş ve nezaket dili", "teacher_flow": "Menü, sipariş ve servis dili", "platform_flow": "Ders 3", "status": "covered"},
    {"topic": "würde ile yumuşak rica", "teacher_flow": "Rica ve tercih tonunu büyüten slaytlar", "platform_flow": "Ders 4", "status": "covered"},
    {"topic": "Präpositionaladverbien ve da- yapıları", "teacher_flow": "Fiil + edat ve tekrar azaltma mantığı", "platform_flow": "Ders 5", "status": "covered"},
    {"topic": "Modal fiillerin Präteritum biçimleri", "teacher_flow": "konnte / wollte / musste hattı", "platform_flow": "Ders 6", "status": "covered"},
    {"topic": "Kıyafet, betimleme ve temel sıfat sonları", "teacher_flow": "Alışveriş ve ürün betimleme alanı", "platform_flow": "Ders 7", "status": "covered"},
    {"topic": "deshalb ve trotzdem ile bağ kurma", "teacher_flow": "Sebep-sonuç ve beklenti kırılması", "platform_flow": "Ders 8", "status": "covered"},
    {"topic": "Komparativ ve Superlativ", "teacher_flow": "Karşılaştırma ve tercih dili", "platform_flow": "Ders 9", "status": "covered"},
    {"topic": "Vorgangspassiv ve Zustandspassiv girişi", "teacher_flow": "Süreç ve sonuç pasifi örnekleri", "platform_flow": "Ders 10", "status": "covered"},
    {"topic": "im, am, zum, vom ve otel dili", "teacher_flow": "Seyahat, resepsiyon ve kısalmış yapılar", "platform_flow": "Ders 11", "status": "covered"},
    {"topic": "nach, zu, in, auf ile hareket", "teacher_flow": "Wohin? ve yön tarifi çalışmaları", "platform_flow": "Ders 12", "status": "covered"},
    {"topic": "weil, dass, wenn ile yan cümle", "teacher_flow": "Yan cümle ve fiil-sonu örnekleri", "platform_flow": "Ders 13", "status": "covered"},
    {"topic": "werden ile gelecek ve A2 toplama", "teacher_flow": "Gelecek planları ve genel toparlama", "platform_flow": "Ders 14", "status": "covered"},
]


def _v(word, article, plural, meanings, example_de, example_tr, note):
    return {
        "word": word,
        "article": article,
        "plural": plural,
        "meanings": meanings,
        "example_de": example_de,
        "example_tr": example_tr,
        "note": note,
    }


def _p(de, tr, note):
    return {"de": de, "tr": tr, "note": note}


def _g(title, summary, when, formula, logic, warning, examples, contrast=None):
    return {
        "title": title,
        "summary": summary,
        "when_to_use": when,
        "formula": formula,
        "teaching_note": logic,
        "watch_out": warning,
        "examples": [{"text": text, "note": note} for text, note in examples],
        "contrast": contrast,
    }


def _m(wrong, right, reason):
    return {"wrong": wrong, "right": right, "reason": reason}


def _line(speaker, text_de, text_tr):
    return {"speaker": speaker, "text_de": text_de, "text_tr": text_tr}


def _passage(title, word_focus, paragraphs):
    return {"title": title, "word_focus": word_focus, "paragraphs": paragraphs}


def _lesson(index, slug, title, difficulty, teaser, objectives, focus, lesson_blocks, grammar_sections, phrase_bank, common_mistakes, mini_dialogue, reading_passages, tips, vocabulary, completion_note):
    return {
        "slug": slug,
        "index": index,
        "title": title,
        "duration": "80-95 dk",
        "difficulty": difficulty,
        "teaser": teaser,
        "status": "active",
        "objectives": objectives,
        "hero_stats": [
            {"label": "Kelime", "value": str(len(vocabulary))},
            {"label": "Gramer odağı", "value": focus},
            {"label": "Alıştırma", "value": "5+ modül"},
        ],
        "lesson_blocks": lesson_blocks,
        "grammar_sections": grammar_sections,
        "phrase_bank": phrase_bank,
        "common_mistakes": common_mistakes,
        "mini_dialogue": mini_dialogue,
        "reading_passages": reading_passages,
        "tips": tips,
        "vocabulary": vocabulary,
        "completion_note": completion_note,
        "next_lesson": {"title": "Sonraki ders", "status": "planned", "slug": ""},
    }


A2_LESSONS = [
    _lesson(
        1,
        "ders-1-perfekte-giris-ve-gecmis-deneyimler",
        "Perfekt'e Giriş ve Geçmiş Deneyimler",
        "A2.1",
        "A2'nin kapısını geçmiş zaman anlatımıyla açıyoruz. Bu derste Perfekt'in iskeletini, haben-sein ayrımını ve Partizip II mantığını kurup kısa deneyim cümleleri üretmeye başlıyoruz.",
        [
            "Perfekt cümlesinin yardımcı fiil + Partizip II mantığını görmek.",
            "Hangi fiillerin haben, hangilerinin sein ile geldiğini ayırmak.",
            "Ayrılabilen fiillerin Perfekt içindeki yerini fark etmek.",
            "Dün, geçen hafta, az önce gibi geçmiş bağlamlarını kısa cümlede kullanmak.",
            "15+ kelimeyle geçmişte ne olduğunu anlatan basit cümleler kurmak.",
            "A2 seviyesinde ilk geçmiş deneyim paragrafına hazırlanmak.",
        ],
        "Perfekt + haben/sein",
        [
            {"eyebrow": "1. Adım", "title": "Perfekt konuşma dilinin ana geçmiş zamanıdır", "body": "A2 düzeyinde günlük konuşmada en sık duyacağın geçmiş yapı Perfekt'tir. Amaç önce uzun anlatı kurmak değil, dün ne yaptığını, bir yere gidip gitmediğini ve kısa deneyimleri net söylemektir."},
            {"eyebrow": "2. Adım", "title": "Yardımcı fiil cümlenin başında, Partizip II sonda durur", "body": "Perfekt'te çekim yükünü haben veya sein taşır. Asıl eylem bilgisi Partizip II ile cümle sonuna gider. Bu iki parçayı ayırmadan Perfekt mantığı oturmaz."},
            {"eyebrow": "3. Adım", "title": "Hareket ve durum değişimi genelde sein ister", "body": "Gitmek, gelmek, varmak, kalmak gibi yer değiştirme veya durum değişimi anlatan fiiller çoğu kez sein ile gelir. Bu ayrım A2'nin ilk büyük reflekslerinden biridir."},
        ],
        [
            _g(
                "Perfekt cümle iskeleti",
                "Perfekt, çekimli yardımcı fiil ve cümle sonundaki Partizip II ile kurulur.",
                "Dün olan bir işi, yakın geçmişi veya tamamlanmış deneyimi anlatırken kullanılır.",
                "özne + haben/sein + diğer ögeler + Partizip II",
                "Bu yapı sayesinde çekim bilgisi ile eylem bilgisini iki ayrı yere dağıtırsın. Yardımcı fiil kişi bilgisini verir; Partizip II ise asıl eylemi taşır.",
                "Yalnız yardımcı fiili çekmek yetmez; Partizip II'yi cümle sonuna göndermeyi unutursan yapı eksik kalır.",
                [
                    ("Ich habe heute lange gearbeitet.", "Burada kişi ve zaman bilgisi yardımcı fiilde, eylemin tamamlandığı bilgisi ise gearbeitet biçiminde taşınıyor."),
                    ("Wir sind spät nach Hause gekommen.", "Hareket bildiren gelmek fiili burada sein ile kurulduğu için geçmiş yapı daha erken tanınıyor."),
                ],
                {"correct": "Ich habe viel gelernt.", "wrong": "Ich habe viel lernen.", "reason": "Perfekt'te mastar değil Partizip II gerekir."},
            ),
            _g(
                "haben mi sein mi?",
                "Perfekt'te çoğu fiil haben alır; hareket ve durum değişimi bildiren önemli bir grup ise sein ile gelir.",
                "Gitmek, gelmek, kalmak, varmak gibi hareket fiilleriyle yardımcı fiil seçerken kullanılır.",
                "haben = çoğu fiil / sein = hareket ve durum değişimi",
                "Yardımcı fiil seçimi anlamla ilişkilidir. Bu yüzden yalnız ezber değil, fiilin ne anlattığını da görmek gerekir.",
                "Her hareket fiili kesin tek kurala bağlı değil; yine de başlangıçta gehen, kommen, fahren, bleiben, ankommen hattını sağlam kurmak büyük avantaj sağlar.",
                [
                    ("Sie hat die E-Mail geschrieben.", "Yazmak hareket fiili olmadığı için burada haben kullanılıyor."),
                    ("Er ist gestern nach Köln gefahren.", "Yer değiştirme olduğu için sein ile kuruluyor."),
                ],
                {"correct": "Er ist angekommen.", "wrong": "Er hat angekommen.", "reason": "ankommen hareket ve varış anlattığı için sein ile kurulur."},
            ),
            _g(
                "Partizip II ve cümle sonu",
                "Partizip II konuşma akışında cümlenin en sonuna gitmeye eğilimlidir ve Perfekt'i görünür hale getirir.",
                "Uzun cümlelerde yardımcı fiili erkenden, asıl eylemi ise en sonda duymaya alışmak için kullanılır.",
                "yardımcı fiil ... Partizip II",
                "Almanca geçmiş zamanın ritmi burada kurulur: önce kişi ve zaman bilgisi gelir, eylemin tamamlandığı duygu sonda kapanır.",
                "Türkçe etkisiyle Partizip II'yi ortada bırakmak veya yardımcı fiile çok yaklaştırmak özellikle uzun cümlelerde hata üretir.",
                [
                    ("Ich habe am Wochenende meine Freunde besucht.", "Zaman ve nesne ortada kalırken eylemin tamamlanmış biçimi sonda kapanıyor."),
                    ("Wir sind um acht Uhr losgefahren.", "Saat bilgisi araya gelse de Partizip II yine finalde duruyor."),
                ],
            ),
            _g(
                "Ayrılabilen fiillerle Perfekt",
                "Ayrılabilen fiiller Perfekt'te yeniden birleşir ve Partizip II olarak tek blok halinde görünür.",
                "aufstehen, ankommen, losfahren gibi fiillerin geçmişini kurarken kullanılır.",
                "haben/sein + ge...önekli Partizip II",
                "Präsens'te ayrılan önek, Perfekt'te çoğu kez Partizip II içinde yeniden birleşir. Bu yüzden dersler arası fiil davranışını kıyaslamak faydalıdır.",
                "Präsens'teki 'ich stehe auf' yapısını doğrudan Perfekt'e taşıyıp 'ich habe aufgestanden' gibi kırık yapılar kurma.",
                [
                    ("Wir sind pünktlich angekommen.", "ankommen fiilinin öneki burada tekrar birleşip angekommen biçimini oluşturuyor."),
                    ("Der Zug ist um sechs Uhr abgefahren.", "abfahren fiilinin Partizip II'si ayrılan öneği tekrar içeri alıyor."),
                ],
            ),
            _g(
                "Geçmiş zaman zarfları",
                "gestern, letzte Woche, schon, noch nie gibi zarflar Perfekt cümlesine zaman ve deneyim çerçevesi katar.",
                "Bir deneyimin ne zaman olduğunu veya daha önce yaşanıp yaşanmadığını belirtirken kullanılır.",
                "zaman zarfı + yardımcı fiil + ... + Partizip II",
                "A2'de geçmiş zamanı tek başına fiille değil, zaman zarfıyla birlikte vermek anlatımı daha doğal hale getirir.",
                "Yalnız Perfekt kurup zamanı hiç belirtmemek her zaman yanlış değildir; ama öğrenme aşamasında zaman zarfı eklemek anlamı çok netleştirir.",
                [
                    ("Ich habe gestern viel gearbeitet.", "gestern zarfı, işi hangi zaman penceresine yerleştirdiğini açıkça gösterir."),
                    ("Wir sind schon einmal in Wien gewesen.", "schon einmal deneyimin daha önce yaşandığını vurguluyor."),
                ],
            ),
        ],
        [
            _p("Ich habe gestern lange gearbeitet.", "Dün uzun süre çalıştım.", "Perfekt'i zaman zarfıyla birlikte duymak için temel kalıp."),
            _p("Wir sind sehr spät angekommen.", "Çok geç vardık.", "sein alan fiillerle kısa deneyim cümlesi."),
            _p("Hast du das schon gemacht?", "Bunu daha önce yaptın mı?", "Deneyim sormanın doğal yolu."),
            _p("Ich bin am Wochenende zu Hause geblieben.", "Hafta sonunda evde kaldım.", "bleiben fiiliyle sein kullanımını pekiştirir."),
            _p("Er hat seine Freunde besucht.", "Arkadaşlarını ziyaret etti.", "haben alan yaygın bir fiil örneği."),
            _p("Wir haben viele Fotos gemacht.", "Çok fotoğraf çektik.", "sabit Perfekt kalıbı olarak sık geçer."),
            _p("Seid ihr mit dem Zug gefahren?", "Trenle gittiniz mi?", "araç ve hareket fiili birlikte geliyor."),
            _p("Nein, wir sind mit dem Auto gekommen.", "Hayır, arabayla geldik.", "sein ile geçmiş cevap kalıbı."),
            _p("Ich habe mein Ticket schon gekauft.", "Biletimi çoktan aldım.", "schon ile tamamlanmışlık vurgusu."),
            _p("Heute habe ich wenig Zeit gehabt.", "Bugün az vaktim oldu.", "haben ile geçmiş sahiplik/durum kalıbı."),
        ],
        [
            _m("Ich habe nach Hause gegangen.", "Ich bin nach Hause gegangen.", "gehen fiili hareket bildirdiği için sein ile kurulur."),
            _m("Ich habe gearbeitet gestern.", "Ich habe gestern gearbeitet.", "Zaman zarfı ortada kalabilir; Partizip II sona gitmelidir."),
            _m("Wir sind besucht.", "Wir haben besucht.", "besuchen hareket değil, haben alan düz bir fiildir."),
            _m("Ich habe ankommen.", "Ich bin angekommen.", "ankommen hem sein alır hem de Partizip II biçimi gerekir."),
        ],
        {
            "title": "Kısa geçmiş sohbeti",
            "lines": [
                _line("A", "Was hast du gestern gemacht?", "Dün ne yaptın?"),
                _line("B", "Ich habe lange gearbeitet und später meine Schwester besucht.", "Uzun süre çalıştım ve sonra kız kardeşimi ziyaret ettim."),
                _line("A", "Bist du mit dem Bus gefahren?", "Otobüsle mi gittin?"),
                _line("B", "Nein, ich bin zu Fuß gegangen.", "Hayır, yürüyerek gittim."),
            ],
        },
        [
            _passage(
                "Hafta sonu notları",
                "Perfekt'i okurken önce yardımcı fiili, sonra cümle sonundaki Partizip II'yi yakala.",
                [
                    "Am Samstag hat [[Mert::bir erkek adı]] lange [[gearbeitet::çalıştı]] und am Abend seine [[Freunde::arkadaşlar]] [[besucht::ziyaret etti]]. Später hat er viele [[Fotos::fotoğraflar]] gemacht.",
                    "Am Sonntag ist er früh [[aufgestanden::kalktı]] und mit dem [[Zug::tren]] nach [[Ankara::Ankara]] gefahren. Dort ist er am Nachmittag wieder [[angekommen::vardı]].",
                ],
            )
        ],
        [
            "Yardımcı fiili seçmeden önce fiilin anlamına bak.",
            "İlk aşamada Partizip II'yi tek başına ezberleme; tam cümle içinde tekrar et.",
            "sein alan fiilleri küçük bir özel liste gibi ayrı çalış.",
            "Kısa deneyim cümlesi kurarken zaman zarfı eklemeyi alışkanlık yap.",
        ],
        [
            _v("die Reise", "die", "die Reisen", ["seyahat", "yolculuk"], "Die Reise war kurz.", "Seyahat kısaydı.", "Geçmiş deneyim anlatısında çerçeve ismi olarak kullanılır."),
            _v("der Besuch", "der", "die Besuche", ["ziyaret"], "Der Besuch war schön.", "Ziyaret güzeldi.", "Perfekt cümlelerinde besucht ile anlam bağı kurar."),
            _v("das Ticket", "das", "die Tickets", ["bilet"], "Das Ticket ist schon da.", "Bilet zaten burada.", "Alım ve seyahat cümlelerinde doğal nesnedir."),
            _v("der Zug", "der", "die Züge", ["tren"], "Der Zug ist pünktlich angekommen.", "Tren zamanında vardı.", "sein alan hareket fiilleriyle sık geçer."),
            _v("der Bahnhof", "der", "die Bahnhöfe", ["gar", "tren istasyonu"], "Der Bahnhof ist nicht weit.", "Gar uzak değil.", "Seyahat bağlamında temel yer ismidir."),
            _v("das Wochenende", "das", "die Wochenenden", ["hafta sonu"], "Das Wochenende war ruhig.", "Hafta sonu sakindi.", "Geçmiş deneyimlerin en doğal zaman çerçevelerinden biridir."),
            _v("der Koffer", "der", "die Koffer", ["bavul"], "Der Koffer ist schwer.", "Bavul ağır.", "Seyahat cümlelerinin somut nesnesidir."),
            _v("das Foto", "das", "die Fotos", ["fotoğraf"], "Das Foto ist neu.", "Fotoğraf yeni.", "machen fiiliyle sık eşleşir."),
            _v("die Rückfahrt", "die", "die Rückfahrten", ["dönüş yolculuğu"], "Die Rückfahrt war spät.", "Dönüş yolculuğu geç oldu.", "Perfekt sonrası toparlama anlatımında iyi çalışır."),
            _v("die Aufgabe", "die", "die Aufgaben", ["görev", "ödev"], "Die Aufgabe ist fertig.", "Görev hazır.", "haben gemacht kalıbıyla bağ kurar."),
            _v("angekommen", "-", "-", ["varmış", "ulaşmış"], "Wir sind spät angekommen.", "Geç vardık.", "sein ile gelen Partizip II örneği."),
            _v("gefahren", "-", "-", ["gitmiş", "sürmüş"], "Er ist nach Bursa gefahren.", "Bursa'ya gitti.", "hareket fiilinin geçmiş biçimi"),
            _v("geblieben", "-", "-", ["kalmış"], "Ich bin zu Hause geblieben.", "Evde kaldım.", "Durum değişimi olmadan yer değiştirmeme de sein ile kurulabilir."),
            _v("besucht", "-", "-", ["ziyaret etmiş"], "Sie hat ihre Tante besucht.", "Teyzesini ziyaret etti.", "haben ile kurulan düzenli Perfekt örneği."),
            _v("geöffnet", "-", "-", ["açılmış", "açmış"], "Der Laden hat früh geöffnet.", "Dükkan erken açtı.", "Partizip II biçimini görünür hale getirir."),
            _v("abgeschlossen", "-", "-", ["tamamlanmış", "bitirmiş"], "Wir haben das Projekt abgeschlossen.", "Projeyi tamamladık.", "cümle sonunda uzun Partizip II örneği"),
            _v("gestern", "-", "-", ["dün"], "Gestern habe ich wenig geschlafen.", "Dün az uyudum.", "Perfekt'le en sık birleşen zaman zarfı."),
            _v("schon", "-", "-", ["çoktan", "zaten"], "Ich habe schon gegessen.", "Ben çoktan yemek yedim.", "tamamlanmışlık hissini güçlendirir."),
        ],
        "Bu dersin hedefi Perfekt'i kusursuzlaştırmak değil, konuşma dilinde geçmiş anlatım omurgasını kurmaktır. Yardımcı fiili seçebiliyor ve Partizip II'yi sona gönderebiliyorsan A2'nin kapısını doğru yerden açtın.",
    ),
    _lesson(
        2,
        "ders-2-yer-bildirme-ve-wechselpraepositionen",
        "Yer Bildirme ve Wechselpräpositionen",
        "A2.1",
        "Bu derste nesnelerin ve kişilerin nerede olduğunu daha ayrıntılı anlatıyoruz. Wo? sorusuna verilen yer cevaplarıyla Wechselpräpositionen'i gerçek oda düzeni içinde çalışıyoruz.",
        [
            "Wo? sorusuna doğal cevap vermek.",
            "auf, unter, neben, vor, hinter, zwischen, in gibi yer bildiren yapıları tanımak.",
            "stehen, liegen ve hängen fiillerini bağlama göre seçmek.",
            "Bir odadaki nesnelerin konumunu kısa cümlelerle tarif etmek.",
            "Yer cümlelerinde Dativ hissini tanımaya başlamak.",
            "Mekân anlatımında A2 seviyesine uygun ilk ayrıntı katmanını kurmak.",
        ],
        "Wo? + yer bildirme",
        [
            {"eyebrow": "1. Adım", "title": "Wo? sorusu bir konumu sorar", "body": "Bu derste yer değiştirme değil, mevcut konumu anlatıyoruz. Yani soru 'nereye gidiyor?' değil, 'şu an nerede?' mantığıyla çalışıyor."},
            {"eyebrow": "2. Adım", "title": "Aynı edat farklı bağlamda hareket de anlatabilir", "body": "in, auf, unter gibi edatlar başka derste hareketle de kullanılabilir. Burada özellikle Wo? sorusuyla birlikte konum anlatan kullanımını sabitliyoruz."},
            {"eyebrow": "3. Adım", "title": "Nesnenin duruşu fiili de değiştirir", "body": "Bir şey dik duruyorsa stehen, yatık duruyorsa liegen, asılıysa hängen demek daha doğaldır. Bu küçük seçim anlatımı bir anda daha doğal yapar."},
        ],
        [
            _g(
                "Wo? sorusu ve yer cevabı",
                "Wo? sorusu nesnenin veya kişinin bulunduğu konumu sorar.",
                "Bir şeyin şu an nerede olduğunu tarif ederken kullanılır.",
                "Wo ist/steht/liegt ...? + yer ifadesi",
                "A2'de yer anlatımı artık yalnız burada-orada seviyesinde kalmaz; nesnenin tam konumunu verebilmek gerekir.",
                "Wo ile Wohin'i karıştırırsan tüm yapı yön anlatımına kayar. Bu dersin hedefi hareket değil, sabit konumdur.",
                [
                    ("Wo ist der Schlüssel? Er ist auf dem Tisch.", "Soru konumu açıyor; cevap nesneyi bir yüzey üzerinde sabitliyor."),
                    ("Wo liegt das Buch? Es liegt neben der Lampe.", "Yatık duran nesnede liegen fiili doğal seçim oluyor."),
                ],
                {"correct": "Das Handy liegt auf dem Sofa.", "wrong": "Das Handy geht auf das Sofa.", "reason": "Burada hareket değil, mevcut konum anlatılıyor."},
            ),
            _g(
                "Wechselpräpositionen ile konum",
                "in, auf, unter, vor, hinter, neben, zwischen gibi edatlar yer ilişkisini kurar.",
                "Oda düzeni, eşya konumu ve mekân tarifinde kullanılır.",
                "edat + belirli/belirsiz isim",
                "Bu edatlar A2'nin omurgalarından biridir. Aynı kelimeler daha sonra hareket anlatırken başka sorularla yeniden dönecektir.",
                "Şimdilik her edatın her cümlede aynı işi yaptığını düşünme; soru tipi ve fiil hareketi değişince kullanım da değişebilir.",
                [
                    ("Die Tasche ist unter dem Stuhl.", "unter burada nesnenin daha aşağı konumlandığını gösteriyor."),
                    ("Der Schrank steht zwischen dem Bett und dem Fenster.", "zwischen iki referans noktasının arasını kuruyor."),
                ],
            ),
            _g(
                "stehen, liegen, hängen",
                "Bazı nesnelerin konumu anlatılırken genel sein yerine daha doğal yer fiilleri kullanılır.",
                "Dik duran, yatık duran veya asılı duran nesneleri daha doğal ifade etmek için kullanılır.",
                "stehen / liegen / hängen + yer ifadesi",
                "Bu fiiller Almancada mekân tasvirini daha canlı yapar. Aynı nesne için bile duruş değişirse fiil değişebilir.",
                "Her şeyi ist ile çözmek mümkündür ama bu seviyede artık daha doğal fiilleri duymaya alışmak gerekir.",
                [
                    ("Die Lampe hängt über dem Tisch.", "Asılı nesnede hängen seçimi doğal bir ayrıntı verir."),
                    ("Das Sofa steht vor der Wand.", "Büyük ve dik duran eşya için stehen uygun kullanımdır."),
                ],
            ),
            _g(
                "hinter, vor, zwischen farkı",
                "Bu üç ilişki nesnenin referans noktasına göre yönünü ve yerini netleştirir.",
                "Bir nesnenin önünde, arkasında veya iki şeyin arasında olduğunu söylemek istediğinde kullanılır.",
                "hinter / vor / zwischen + isim grubu",
                "Yer anlatımında küçük farklar anlamı tamamen değiştirir. Bu yüzden edatları yalnız çeviriyle değil, zihinsel resimle öğrenmek daha doğrudur.",
                "özellikle zwischen yapısında iki referans noktasını eksik bırakma; kalıp çoğu zaman iki unsur ister.",
                [
                    ("Der Hund liegt vor dem Bett.", "vor, referans nesnenin ön tarafını gösterir."),
                    ("Die Katze sitzt hinter dem Sofa.", "hinter ile görünmeyen arka alan tarif edilir."),
                ],
            ),
        ],
        [
            _p("Wo ist der Schlüssel?", "Anahtar nerede?", "Yer sorusunun temel omurgası."),
            _p("Er liegt auf dem Tisch.", "Masanın üstünde duruyor.", "auf + Dativ yer cevabı."),
            _p("Die Tasche ist unter dem Stuhl.", "Çanta sandalyenin altında.", "alt konum anlatımı."),
            _p("Das Bild hängt über dem Sofa.", "Tablo kanepenin üstünde asılı.", "hängen fiili ile doğal yer tarifi."),
            _p("Der Schrank steht neben der Tür.", "Dolap kapının yanında duruyor.", "büyük eşyalarda stehen kullanımı."),
            _p("Zwischen dem Bett und dem Fenster steht ein Tisch.", "Yatak ile pencere arasında bir masa duruyor.", "iki referans noktalı yer cümlesi."),
            _p("Vor dem Haus steht ein Auto.", "Evin önünde bir araba duruyor.", "mekân dışına da uygulanabilen kalıp."),
            _p("Hinter dem Regal ist noch Platz.", "Rafın arkasında hâlâ yer var.", "soyut değil gerçek yer bildirimi."),
            _p("Im Zimmer ist es sehr ruhig.", "Odada çok sakin.", "iç mekân bağlamı için kısa kalıp."),
            _p("Die Lampe hängt an der Wand.", "Lamba duvarda asılı.", "an + Dativ yer ilişkisi."),
        ],
        [
            _m("Wo gehst du?", "Wo bist du?", "Bu derste hareket değil konum soruyoruz."),
            _m("Das Buch steht auf dem Tisch.", "Das Buch liegt auf dem Tisch.", "Kitap yatık konumda düşünüldüğünde liegen daha doğaldır."),
            _m("Die Tasche ist zwischen dem Stuhl.", "Die Tasche ist zwischen dem Stuhl und dem Sofa.", "zwischen çoğu kez iki referans nokta ister."),
            _m("Die Lampe ist auf die Wand.", "Die Lampe hängt an der Wand.", "duvar üzerindeki konum için an der Wand daha doğal kalıptır."),
        ],
        {
            "title": "Oda tarifi",
            "lines": [
                _line("A", "Wo ist das Buch?", "Kitap nerede?"),
                _line("B", "Es liegt auf dem Tisch, neben der Lampe.", "Masanın üstünde, lambanın yanında duruyor."),
                _line("A", "Und wo steht der Stuhl?", "Peki sandalye nerede duruyor?"),
                _line("B", "Der Stuhl steht vor dem Fenster.", "Sandalye pencerenin önünde duruyor."),
            ],
        },
        [
            _passage(
                "Yeni oda",
                "Okumada önce edatı, sonra referans nesneyi yakala; böylece zihninde küçük bir plan oluşur.",
                [
                    "Im [[Zimmer::oda]] steht ein [[Bett::yatak]] links. Neben dem Bett steht ein [[Stuhl::sandalye]]. Vor dem [[Fenster::pencere]] steht ein kleiner [[Tisch::masa]].",
                    "An der [[Wand::duvar]] hängt eine [[Lampe::lamba]]. Unter dem Tisch liegt eine [[Tasche::çanta]] und hinter dem [[Regal::raf]] ist noch Platz.",
                ],
            )
        ],
        [
            "Yer cümlesini çalışırken küçük bir oda krokisi çizmek işini kolaylaştırır.",
            "Edatı çevirip bırakma; daima referans nesneyle birlikte tekrar et.",
            "stehen, liegen, hängen üçlüsünü ayrı mini grup olarak çalış.",
            "Önce konum anlatımını oturt; hareket anlatımı sonraki derste daha rahat gelir.",
        ],
        [
            _v("das Sofa", "das", "die Sofas", ["kanepe"], "Das Sofa steht vor der Wand.", "Kanepe duvarın önünde duruyor.", "Yer bildirme dersinin temel büyük eşya kelimelerinden biridir."),
            _v("das Regal", "das", "die Regale", ["raf"], "Das Regal steht neben der Tür.", "Raf kapının yanında duruyor.", "hinter / neben kalıplarıyla iyi çalışır."),
            _v("der Schrank", "der", "die Schränke", ["dolap"], "Der Schrank ist groß.", "Dolap büyük.", "oda tarifinde temel mobilya"),
            _v("der Tisch", "der", "die Tische", ["masa"], "Der Tisch steht am Fenster.", "Masa pencerenin yanında duruyor.", "auf kalıbıyla çok tekrar edilir."),
            _v("die Lampe", "die", "die Lampen", ["lamba"], "Die Lampe hängt an der Wand.", "Lamba duvarda asılı.", "hängen fiiline doğal örnek verir."),
            _v("die Wand", "die", "die Wände", ["duvar"], "Die Wand ist weiß.", "Duvar beyaz.", "an der Wand kalıbının temel ismidir."),
            _v("die Ecke", "die", "die Ecken", ["köşe"], "Die Pflanze steht in der Ecke.", "Bitki köşede duruyor.", "mekânı daha ayrıntılı tanımlar."),
            _v("der Teppich", "der", "die Teppiche", ["halı"], "Der Teppich liegt unter dem Tisch.", "Halı masanın altında duruyor.", "liegen fiili için iyi örnek."),
            _v("die Tür", "die", "die Türen", ["kapı"], "Die Tür ist offen.", "Kapı açık.", "vor / hinter ilişkilerinde kullanılır."),
            _v("das Fenster", "das", "die Fenster", ["pencere"], "Das Fenster ist groß.", "Pencere büyük.", "oda tarifinde ikinci referans noktası olur."),
            _v("der Stuhl", "der", "die Stühle", ["sandalye"], "Der Stuhl steht neben dem Tisch.", "Sandalye masanın yanında duruyor.", "küçük mobilya konumu için iyidir."),
            _v("das Bett", "das", "die Betten", ["yatak"], "Das Bett steht links.", "Yatak solda duruyor.", "oda merkezini tarif etmeye yarar."),
            _v("auf", "-", "-", ["üstünde"], "Das Handy liegt auf dem Sofa.", "Telefon kanepenin üstünde duruyor.", "yüzey ilişkisi kurar."),
            _v("unter", "-", "-", ["altında"], "Die Tasche ist unter dem Tisch.", "Çanta masanın altında.", "alt konumu net verir."),
            _v("neben", "-", "-", ["yanında"], "Der Schrank steht neben der Tür.", "Dolap kapının yanında duruyor.", "yakın konum bildirir."),
            _v("zwischen", "-", "-", ["arasında"], "Der Stuhl steht zwischen dem Bett und dem Fenster.", "Sandalye yatakla pencerenin arasında duruyor.", "iki referanslı yer kalıbı."),
            _v("vor", "-", "-", ["önünde"], "Das Auto steht vor dem Haus.", "Araba evin önünde duruyor.", "ön konumu gösterir."),
            _v("hinter", "-", "-", ["arkasında"], "Die Katze ist hinter dem Sofa.", "Kedi kanepenin arkasında.", "arka konumu gösterir."),
        ],
        "Bu derste küçük bir odanın krokisini Almanca cümlelerle tarif edebiliyorsan ana hedefe ulaştın. Wo? sorusu ile konum cümlesi artık sende refleks üretmeye başlamalı.",
    ),
    _lesson(
        3,
        "ders-3-restoranda-siparis-ve-nezaket-kaliplari",
        "Restoranda Sipariş ve Nezaket Kalıpları",
        "A2.1",
        "Bu derste menü okuma, sipariş verme, ek istek bildirme ve hesabı isteme gibi gündelik restoran iletişimini A2 seviyesinde daha doğal hale getiriyoruz.",
        [
            "Restoranda temel sipariş kalıplarını kullanmak.",
            "möchten, nehmen ve ich hätte gern kalıpları arasındaki farkı duymak.",
            "Menü ve fiyat sorma cümleleri kurmak.",
            "Kein / noch / sonst noch etwas gibi servis ifadelerini anlamak.",
            "Yiyecek ve içecek kelimelerini doğal bağlamda tekrar etmek.",
            "Kısa bir restoran diyaloğunu baştan sona yönetebilmek.",
        ],
        "Sipariş dili + nezaket",
        [
            {"eyebrow": "1. Adım", "title": "Sipariş yalnız isim saymak değildir", "body": "A2 seviyesinde yalnız pizza, çorba, çay demek yetmez; nazik bir açılış, ek istek ve kapanış da gerekir. Bu ders küçük bir hizmet konuşmasını tamamlamayı hedefler."},
            {"eyebrow": "2. Adım", "title": "Nezaket cümleyi yumuşatır", "body": "bitte, für mich, ich hätte gern, noch etwas gibi ifadeler konuşmayı kaba listeden çıkarıp gerçek restoran diline yaklaştırır."},
            {"eyebrow": "3. Adım", "title": "Fiyat ve hesap dili de siparişin parçasıdır", "body": "A2'de restoranda yalnız sipariş vermek değil, fiyat sormak ve hesabı istemek de temel iletişim görevidir."},
        ],
        [
            _g(
                "Siparişte en temel üç kalıp",
                "Ich möchte..., Ich nehme... ve Ich hätte gern... restoran dilinin en temel üç giriş yoludur.",
                "Bir yiyecek veya içeceği istemek, almak ya da nazik biçimde rica etmek istediğinde kullanılır.",
                "Ich möchte / Ich nehme / Ich hätte gern + nesne",
                "Bu üç yapı aynı hedefe gider ama tonları farklıdır. Ich nehme daha düz, ich möchte daha standart, ich hätte gern ise biraz daha yumuşak ve kibar tınlar.",
                "Tek bir kalıbı her yerde kullanmak yanlış değildir; ama A2'de ton farkını duymaya başlamak konuşmayı belirgin biçimde doğal yapar.",
                [
                    ("Ich möchte eine Suppe und einen Tee.", "Standart ve güvenli sipariş cümlesi."),
                    ("Für mich hätte ich gern das Tagesmenü.", "Biraz daha yumuşak ve servis odaklı rica kalıbı."),
                ],
            ),
            _g(
                "noch, kein ve sonst noch etwas",
                "Servis dili çoğu zaman ek istek sorusu ve isim olumsuzluğu içerir.",
                "Garsonun ek bir şey isteyip istemediğini sorması veya müşterinin bir şeyi istemediğini belirtmesi gerektiğinde kullanılır.",
                "noch + ek istek / kein + isim olumsuzluğu",
                "A2'de restoran dili tek cümlelik siparişten çıkar ve etkileşimli hale gelir. Ek istek ve reddetme kalıpları konuşmayı daha gerçekçi yapar.",
                "nicht ile kein ayrımını burada karıştırırsan özellikle yiyecek isimlerinde yapay cümleler kurarsın.",
                [
                    ("Noch etwas?", "Servis akışında doğal ek istek sorusudur."),
                    ("Nein danke, ich möchte keinen Saft.", "İsim olumsuzluğunu düzgün kurar."),
                ],
            ),
            _g(
                "Fiyat ve hesap sorma",
                "Restoran dilinde fiyat sormak ve hesabı istemek kısa ama çok sık kullanılan iki iletişim görevidir.",
                "Ne kadar tuttuğunu öğrenmek veya siparişi kapatmak istediğinde kullanılır.",
                "Was kostet ...? / Die Rechnung, bitte.",
                "Bu kalıplar sosyal olarak kısa kalır; uzun cümle zorunlu değildir. Önemli olan doğru sabit ifadeyi zamanında kullanmaktır.",
                "Türkçedeki tam çeviri mantığıyla 'hesabı istiyorum' gibi ağır yapı kurmaya gerek yoktur; sabit formül daha doğaldır.",
                [
                    ("Was kostet der Salat?", "Fiyat sorusunu doğrudan ve net açar."),
                    ("Die Rechnung, bitte.", "Kapanışta yeterince doğal ve kısa bir formüldür."),
                ],
            ),
            _g(
                "Für mich ve ohne ile küçük özelleştirme",
                "Siparişi kişiselleştirmek için çoğu zaman 'benim için' veya 'olmadan' gibi küçük ekler gerekir.",
                "Kendi siparişini başkasınınkinden ayırmak veya bir malzemeyi istemediğini belirtmek için kullanılır.",
                "Für mich ... / ohne + isim",
                "A2'de hizmet dilini doğal yapan şey tam da bu küçük eklemelerdir. Yalnız nesneyi söylemek yerine tercihini biraz açarsın.",
                "Ohne yapısını gereksiz yere uzun cümleye boğma; kısa kullanımı daha doğaldır.",
                [
                    ("Für mich einen Tee, bitte.", "Siparişi kişiye bağlar."),
                    ("Ich nehme den Salat ohne Zwiebeln.", "Küçük özelleştirme yapar."),
                ],
            ),
        ],
        [
            _p("Ich möchte eine Suppe und einen Tee.", "Bir çorba ve bir çay istiyorum.", "standart sipariş açılışı"),
            _p("Für mich das Tagesmenü, bitte.", "Benim için günlük menü, lütfen.", "servis dili"),
            _p("Was kostet die Pizza?", "Pizza ne kadar?", "fiyat sorma"),
            _p("Ich hätte gern Wasser ohne Eis.", "Buzsuz su rica ederim.", "küçük özelleştirme"),
            _p("Noch etwas?", "Başka bir şey?", "garson sorusu"),
            _p("Nein danke, das ist alles.", "Hayır teşekkürler, hepsi bu.", "siparişi kapatma"),
            _p("Haben Sie auch vegetarische Gerichte?", "Vejetaryen yemekleriniz de var mı?", "menü genişletme sorusu"),
            _p("Die Rechnung, bitte.", "Hesap, lütfen.", "kapanış formülü"),
            _p("Kann ich mit Karte zahlen?", "Kartla ödeyebilir miyim?", "ödeme sorusu"),
            _p("Ich nehme keinen Saft, sondern Wasser.", "Meyve suyu almıyorum, su alıyorum.", "olumsuz tercih kalıbı"),
        ],
        [
            _m("Ich bin eine Suppe.", "Ich möchte eine Suppe.", "Siparişte sein değil istek kalıbı gerekir."),
            _m("Ich möchte nicht Saft.", "Ich möchte keinen Saft.", "isim olumsuzluğu kein ile kurulur."),
            _m("Wie viel kostet?", "Was kostet die Pizza?", "nesne eksik olduğunda soru havada kalır."),
            _m("Die Rechnung ich will.", "Die Rechnung, bitte.", "Restoran kapanışında sabit kısa formül daha doğaldır."),
        ],
        {
            "title": "Restoranda kısa servis diyaloğu",
            "lines": [
                _line("Garson", "Guten Abend. Was möchten Sie?", "İyi akşamlar. Ne istersiniz?"),
                _line("Müşteri", "Ich hätte gern eine Suppe und einen Tee.", "Bir çorba ve bir çay rica ederim."),
                _line("Garson", "Noch etwas?", "Başka bir şey?"),
                _line("Müşteri", "Nein danke. Die Rechnung später, bitte.", "Hayır teşekkürler. Hesabı sonra lütfen."),
            ],
        },
        [
            _passage(
                "Küçük akşam yemeği",
                "Yiyecek isimlerine bakarken artikel ve mümkünse fiyat sorusu kalıplarını da birlikte tekrar et.",
                [
                    "Im [[Restaurant::restoran]] liest [[Elif::bir kadın adı]] die [[Speisekarte::menü]]. Sie möchte eine [[Suppe::çorba]] und später einen [[Salat::salata]].",
                    "Der [[Kellner::garson]] fragt: [[Noch etwas::başka bir şey]]? Elif sagt: Für mich noch ein [[Wasser::su]], bitte. Am Ende sagt sie: [[Die Rechnung, bitte::hesap lütfen]].",
                ],
            )
        ],
        [
            "Kalıpları tek tek çevirmek yerine servis akışı içinde blok halinde tekrar et.",
            "Ich möchte ve ich hätte gern arasındaki ton farkını yüksek sesle dene.",
            "Fiyat ve hesap kalıplarını kısa tut; fazla kelime eklemek her zaman daha doğal değildir.",
            "Yemek kelimelerini artikel ile çalışmayı sürdür; restoran dili de isim ağırlıklıdır.",
        ],
        [
            _v("der Kaffee", "der", "die Kaffees", ["kahve"], "Der Kaffee ist heiß.", "Kahve sıcak.", "siparişlerin en sık nesnelerinden biridir."),
            _v("der Tee", "der", "die Tees", ["çay"], "Der Tee ist frisch.", "Çay taze.", "kısa siparişlerde sık geçer."),
            _v("der Salat", "der", "die Salate", ["salata"], "Der Salat kostet neun Euro.", "Salata dokuz euro.", "fiyat cümlesi için doğal maskulin isim."),
            _v("der Saft", "der", "die Säfte", ["meyve suyu"], "Der Saft ist kalt.", "Meyve suyu soğuk.", "keinen yapısı için iyi örnek."),
            _v("das Wasser", "das", "die Wasser", ["su"], "Das Wasser ist ohne Eis.", "Su buzsuz.", "içecek özelleştirme cümlelerinde kullanılır."),
            _v("das Menü", "das", "die Menüs", ["menü"], "Das Menü ist heute kurz.", "Menü bugün kısa.", "servis bağlamının merkez isimlerinden biridir."),
            _v("das Frühstück", "das", "die Frühstücke", ["kahvaltı"], "Das Frühstück ist ab acht Uhr.", "Kahvaltı saat sekizden itibaren.", "yemek zamanına da bağlanır."),
            _v("das Mittagessen", "das", "die Mittagessen", ["öğle yemeği"], "Das Mittagessen ist günstig.", "Öğle yemeği uygun fiyatlı.", "öğün kelime grubunu genişletir."),
            _v("die Suppe", "die", "die Suppen", ["çorba"], "Die Suppe ist heiß.", "Çorba sıcak.", "dişil sipariş nesnesi."),
            _v("die Pizza", "die", "die Pizzen", ["pizza"], "Die Pizza ist groß.", "Pizza büyük.", "tanıdık yemek kelimesi olarak hızlı yerleşir."),
            _v("die Rechnung", "die", "die Rechnungen", ["hesap", "fatura"], "Die Rechnung kommt gleich.", "Hesap birazdan geliyor.", "kapanış kalıbının ana kelimesi."),
            _v("die Speisekarte", "die", "die Speisekarten", ["menü", "yemek listesi"], "Die Speisekarte liegt auf dem Tisch.", "Menü masanın üstünde duruyor.", "okuma ve seçim eylemleriyle bağ kurar."),
            _v("der Kellner", "der", "die Kellner", ["garson"], "Der Kellner kommt sofort.", "Garson hemen geliyor.", "hizmet diyaloğunun kişisidir."),
            _v("die Kellnerin", "die", "die Kellnerinnen", ["kadın garson"], "Die Kellnerin fragt höflich.", "Garson nazikçe soruyor.", "servis dili kişilerini tamamlar."),
            _v("möchte", "-", "-", ["istiyor"], "Ich möchte einen Tee.", "Bir çay istiyorum.", "sipariş fiilinin çekimli biçimi."),
            _v("hätte gern", "-", "-", ["rica ederim", "isterdim"], "Ich hätte gern eine Suppe.", "Bir çorba rica ederim.", "yumuşak sipariş formülü."),
            _v("noch", "-", "-", ["daha", "başka"], "Noch ein Wasser, bitte.", "Bir su daha, lütfen.", "ek isteklerde kullanılır."),
            _v("ohne", "-", "-", ["olmadan"], "Ich nehme den Tee ohne Zucker.", "Çayı şekersiz alıyorum.", "küçük kişiselleştirme kurar."),
        ],
        "Bu dersi bitirdiğinde küçük bir restoranda menüye bakıp sipariş verebiliyor, ek istek bildirebiliyor ve hesabı isteme noktasına kadar konuşmayı taşıyabiliyor olmalısın.",
    ),
    _lesson(
        4,
        "ders-4-wuerde-ile-yumusak-rica-ve-istekler",
        "würde ile Yumuşak Rica ve İstekler",
        "A2.1",
        "Bu derste daha kibar ve yumuşak konuşmak için würde / würden yapısını devreye alıyoruz. Özellikle istek, öneri ve ihtimal cümlelerinde tonu nasıl değiştirdiğini çalışıyoruz.",
        [
            "würde / würden yapısının temel işlevini kavramak.",
            "Direkt cümleyle yumuşak rica arasındaki ton farkını duymak.",
            "Ich hätte gern, Ich würde gern ve Könnten Sie...? yapıları arasında bağ kurmak.",
            "Form doldurma, yardım isteme ve rezervasyon bağlamında nazik cümleler kurmak.",
            "İstek cümlesinde asıl fiilin sonda kalmasına alışmak.",
            "A2 konuşmasında kaba değil kontrollü bir ton kurmak.",
        ],
        "würde / kibar rica",
        [
            {"eyebrow": "1. Adım", "title": "Aynı istek farklı tonlarda söylenebilir", "body": "Ich will yerine ich möchte ya da ich würde gern demek, cümlenin tonunu daha yumuşak ve sosyal olarak daha rahat hale getirir."},
            {"eyebrow": "2. Adım", "title": "würde konuşmada tampon görevi görür", "body": "Bu yapı, doğrudan istemek yerine biraz mesafe ve nezaket ekler. Özellikle hizmet, yardım veya rica durumlarında hızlı fark yaratır."},
            {"eyebrow": "3. Adım", "title": "Asıl fiil yine sona gider", "body": "würde çekimli kısım gibi davranır ve asıl fiil cümle sonunda yalın halde kalır. Bunu baştan doğru kurmak gerekir."},
        ],
        [
            _g(
                "würde / würden ile istek",
                "würde yapısı doğrudan istemek yerine daha yumuşak bir ton kurar.",
                "Bir şey rica etmek, tercih belirtmek veya daha nazik görünmek istediğinde kullanılır.",
                "özne + würde/würden + ... + infinitiv",
                "A2'de ton yönetimi önemli hale gelir. Aynı içeriği daha yumuşak kurabildiğinde konuşma kaba talep hissinden çıkar.",
                "würde kullanınca asıl fiili çekmeyip yalın bırakmak gerekir; iki kez çekim yapma.",
                [
                    ("Ich würde morgen gern früher gehen.", "İstek kibarlaşıyor; asıl fiil gehen sonda yalın kalıyor."),
                    ("Wir würden Ihnen gern helfen.", "Kibar teklif veya yardım cümlesi kurmak için uygun."),
                ],
            ),
            _g(
                "Ich hätte gern ve Ich würde gern farkı",
                "İki kalıp da yumuşak istek kurar ama biri isim, diğeri fiil yapısına daha kolay bağlanır.",
                "Bir nesne istemek veya bir eylem yapmak istediğini nazikçe söylemek istediğinde kullanılır.",
                "Ich hätte gern + isim / Ich würde gern + fiil",
                "Ich hätte gern çoğu zaman sipariş veya somut nesne için çok doğal durur. Ich würde gern ise yapmak istediğin eylemi öne çıkarır.",
                "Bu iki kalıbı birbirinin kötü kopyası gibi düşünme; nesne mi istiyorsun, eylem mi istiyorsun sorusunu sorup seçmek daha doğrudur.",
                [
                    ("Ich hätte gern einen Termin.", "Burada nesne istendiği için isim yapısı doğal."),
                    ("Ich würde gern später kommen.", "Burada yapılacak eylem vurgulanıyor."),
                ],
            ),
            _g(
                "Könnten Sie ...? ile resmî rica",
                "Resmî bağlamda yardım ve bilgi istemenin en yumuşak yollarından biri Könnten Sie ...? kalıbıdır.",
                "Ofis, banka, danışma, kayıt veya müşteri hizmeti bağlamında kullanılır.",
                "Könnten Sie + ... + infinitiv?",
                "Bu yapı doğrudan emir veya çıplak soru yerine daha sosyal bir giriş sağlar. A2 için çok işlevli ve güvenli bir kalıptır.",
                "Sie hitabında fiili yanlış kişiyle eşleştirme; resmî hitapta büyük harfli Sie mantığı korunur.",
                [
                    ("Könnten Sie mir helfen?", "Resmî bağlam için kısa ve doğal rica."),
                    ("Könnten Sie das Formular erklären?", "yardım ve açıklama istemeye uygun örnek."),
                ],
            ),
            _g(
                "Nazik cümlede kelime sırası",
                "Yumuşatma kalıbı geldiğinde cümlede yine çekimli unsur ikinci yerde, asıl fiil sonda kalır.",
                "würde, könnte, hätte gibi kalıplarla daha uzun rica cümlesi kurarken kullanılır.",
                "başlangıç ögesi + çekimli yapı + ... + infinitiv",
                "Nezaket cümlesi uzunlaştıkça sözdizimi daha kolay dağılır. Bu yüzden ikinci pozisyon kuralını özellikle korumak gerekir.",
                "Kibar konuşmaya çalışırken söz dizimini bırakmak A2'de sık görülen bir kaymadır.",
                [
                    ("Ich würde heute gern einen Termin reservieren.", "çekimli parça erkenden geliyor, asıl fiil reservieren sonda kapanıyor."),
                    ("Könnten Sie mir kurz erklären, wo das Büro ist?", "yardım cümlesi uzasa da çekimli yapı başta sabit kalır."),
                ],
            ),
        ],
        [
            _p("Ich würde gern später kommen.", "Daha sonra gelmek isterdim.", "fiil tabanlı yumuşak istek"),
            _p("Ich hätte gern einen Termin.", "Bir randevu rica ederim.", "isim tabanlı nazik rica"),
            _p("Könnten Sie mir helfen?", "Bana yardım edebilir misiniz?", "resmî rica"),
            _p("Wir würden gern reservieren.", "Rezervasyon yapmak isterdik.", "çoğul nezaket kalıbı"),
            _p("Ich würde das Formular heute ausfüllen.", "Bu formu bugün doldurmak isterdim.", "eylem ve nesne birlikte"),
            _p("Könnten Sie das bitte wiederholen?", "Bunu lütfen tekrar edebilir misiniz?", "iletişim kurtarma kalıbı"),
            _p("Ich hätte gern mehr Informationen.", "Daha fazla bilgi rica ederim.", "servis ve ofis dili"),
            _p("Würden Sie mir die Adresse schicken?", "Bana adresi gönderir misiniz?", "resmî rica ve bilgi alma"),
            _p("Ich würde lieber morgen kommen.", "Yarın gelmeyi tercih ederim.", "tercih yumuşatma"),
            _p("Könnten wir einen Platz am Fenster bekommen?", "Pencere kenarında yer alabilir miyiz?", "rezervasyon ve kibar rica"),
        ],
        [
            _m("Ich würde gern komme.", "Ich würde gern kommen.", "würde ile asıl fiil yalın kalır."),
            _m("Ich will einen Termin.", "Ich hätte gern einen Termin.", "resmî bağlamda ton yumuşatılmalıdır."),
            _m("Könnten du mir helfen?", "Könntest du mir helfen? / Könnten Sie mir helfen?", "hitap düzeyi ile fiil uyumu korunmalıdır."),
            _m("Ich hätte gern reservieren.", "Ich würde gern reservieren.", "hätte gern çoğu zaman isim; eylem için würde gern daha uygundur."),
        ],
        {
            "title": "Danışmada kısa konuşma",
            "lines": [
                _line("A", "Guten Tag. Ich hätte gern einen Termin.", "İyi günler. Bir randevu rica ederim."),
                _line("B", "Natürlich. Würden Sie lieber am Montag oder am Dienstag kommen?", "Elbette. Pazartesi mi salı mı gelmeyi tercih edersiniz?"),
                _line("A", "Ich würde lieber am Dienstag kommen.", "Salı gelmeyi tercih ederim."),
                _line("B", "Kein Problem. Ich reserviere einen Platz für Sie.", "Sorun değil. Sizin için bir yer ayırıyorum."),
            ],
        },
        [
            _passage(
                "Ofiste kısa rica",
                "Bu metinde ton farkına dikkat et: aynı istek daha kaba da söylenebilirdi, ama burada yumuşatılmış biçimler seçiliyor.",
                [
                    "[[Deniz::bir erkek adı]] ist heute im [[Büro::ofis]]. Er sagt: Ich [[würde::isterdim]] gern mehr [[Informationen::bilgiler]] bekommen und ich hätte gern einen [[Termin::randevu]].",
                    "Die Frau am [[Schalter::danışma gişesi]] antwortet: Natürlich. [[Könnten Sie::edebilir misiniz]] kurz warten? Ich schicke Ihnen gleich die [[Adresse::adres]].",
                ],
            )
        ],
        [
            "Nazik kalıpları tek başına ezberleme; hangi bağlamda kullanıldığını da tekrar et.",
            "würde ile gelen fiilleri yalın halde sonda yakalamaya çalış.",
            "Aynı isteği üç tonda söyleyip aradaki farkı duymak faydalıdır: will, möchte, würde gern.",
            "Resmî Sie hitabını özellikle yardım ve danışma bağlamında tekrar et.",
        ],
        [
            _v("der Termin", "der", "die Termine", ["randevu", "takvim zamanı"], "Der Termin ist morgen.", "Randevu yarın.", "resmî rica dersinin merkez isimlerinden biridir."),
            _v("die Hilfe", "die", "die Hilfen", ["yardım"], "Die Hilfe ist wichtig.", "Yardım önemli.", "Könnten Sie mir helfen? kalıbıyla bağ kurar."),
            _v("das Formular", "das", "die Formulare", ["form"], "Das Formular ist lang.", "Form uzun.", "ofis ve kayıt dili"),
            _v("der Platz", "der", "die Plätze", ["yer", "koltuk"], "Der Platz am Fenster ist frei.", "Pencere kenarındaki yer boş.", "rezervasyon dilinde kullanılır."),
            _v("die Frage", "die", "die Fragen", ["soru"], "Die Frage ist kurz.", "Soru kısa.", "yardım isteme bağlamında geçer."),
            _v("die Empfehlung", "die", "die Empfehlungen", ["öneri", "tavsiye"], "Die Empfehlung ist gut.", "Tavsiye iyi.", "nazik isteklerle birlikte sık duyulur."),
            _v("die Möglichkeit", "die", "die Möglichkeiten", ["olasılık", "imkân"], "Die Möglichkeit ist interessant.", "İmkân ilginç.", "würde ile olasılık dili kurmaya yardımcı olur."),
            _v("die Reservierung", "die", "die Reservierungen", ["rezervasyon"], "Die Reservierung ist fertig.", "Rezervasyon hazır.", "otel ve restoran derslerine köprü olur."),
            _v("die Auskunft", "die", "die Auskünfte", ["bilgi", "danışma bilgisi"], "Die Auskunft ist hier.", "Danışma burada.", "müşteri hizmeti bağlamında kullanılır."),
            _v("der Wunsch", "der", "die Wünsche", ["istek", "dilek"], "Der Wunsch ist klar.", "İstek açık.", "rica cümlesinin anlam alanını büyütür."),
            _v("würde", "-", "-", ["isterdi", "-erdi"], "Ich würde morgen kommen.", "Yarın gelirdim / gelmek isterdim.", "yumuşatma kalıbının çekimli parçası."),
            _v("hätte gern", "-", "-", ["rica ederim", "isterdim"], "Ich hätte gern mehr Zeit.", "Daha fazla zaman isterdim.", "isim tabanlı kibar rica."),
            _v("könnten", "-", "-", ["edebilir miydiniz"], "Könnten Sie mir helfen?", "Bana yardım edebilir misiniz?", "resmî rica çekimi."),
            _v("lieber", "-", "-", ["tercihen", "daha çok"], "Ich würde lieber morgen kommen.", "Yarın gelmeyi tercih ederim.", "tercih belirtir."),
            _v("bitte", "-", "-", ["lütfen"], "Bitte warten Sie kurz.", "Lütfen kısa bir süre bekleyin.", "nezaketin temel taşı."),
            _v("möglich", "-", "-", ["mümkün"], "Ist das möglich?", "Bu mümkün mü?", "yardım ve rica cümlelerini tamamlar."),
            _v("warten", "-", "-", ["beklemek"], "Könnten Sie kurz warten?", "Kısaca bekleyebilir misiniz?", "rica diliyle birleşir."),
            _v("reservieren", "-", "-", ["rezervasyon yapmak", "ayırtmak"], "Wir würden gern reservieren.", "Rezervasyon yapmak isterdik.", "eylem tabanlı nazik istek."),
        ],
        "Bu derste asıl kazanım, aynı isteği daha yumuşak söyleyebilmek. İçerik küçük görünür ama ton kontrolü A2 iletişimini belirgin biçimde ileri taşır.",
    ),
    _lesson(
        5,
        "ders-5-praepositionaladverbien-ve-da-yapilari",
        "Präpositionaladverbien ve da- Yapıları",
        "A2.1",
        "Bu ders biraz daha kavramsal. Aynı ismi tekrar tekrar söylemek yerine dafür, daran, darüber, damit gibi da- yapılarıyla konuşmayı daha akıcı hale getiriyoruz.",
        [
            "Prepozisyon isteyen fiillerle sık kullanılan da- yapıları tanımak.",
            "Bir önceki isim grubunu tekrar etmeden referans verebilmek.",
            "warten auf, denken an, sprechen über, träumen von gibi kalıpları cümlede kullanmak.",
            "Worauf?, Daran, Darüber gibi soru-cevap çiftlerini görmek.",
            "Metin içinde tekrarları azaltan daha doğal A2 cümleleri kurmak.",
            "Fiil + edat birlikteliklerini kelime paketi gibi ezberleme alışkanlığı geliştirmek.",
        ],
        "da- yapıları + fiil-edat",
        [
            {"eyebrow": "1. Adım", "title": "Bazı fiiller tek başına yetmez", "body": "denken an, warten auf, sprechen über, träumen von gibi fiiller edatla birlikte öğrenilir. A2'de bunları tek kelime gibi görmek daha doğru olur."},
            {"eyebrow": "2. Adım", "title": "Aynı ismi tekrar etmek yerine da- kullanılır", "body": "Bir konudan söz ettikten sonra ona tekrar aynı isimle dönmek yerine dafür, darüber, daran gibi yapılar konuşmayı akıcılaştırır."},
            {"eyebrow": "3. Adım", "title": "Soru biçimi çoğu zaman wo- ile açılır", "body": "Worauf wartest du?, Woran denkst du? gibi sorular fiil-edat ilişkisini görünür hâle getirir. Cevapta da çoğu zaman darauf, daran gelir."},
        ],
        [
            _g(
                "Fiil + edat birliktelikleri",
                "Bazı fiiller belirli bir edatla doğal biçimde birlikte kullanılır.",
                "Bir şey beklemek, bir şeyi düşünmek, bir konuda konuşmak, bir şeyi hayal etmek gibi durumlarda kullanılır.",
                "fiil + sabit edat",
                "Bu başlık çeviri mantığıyla değil, kelime paketi mantığıyla öğrenilmelidir. Fiili tek başına ezberlemek çoğu zaman yetersiz kalır.",
                "Edatı her seferinde serbestçe seçmeye çalışma; hangi fiilin hangi edatla geldiğini blok halinde tekrar etmen gerekir.",
                [
                    ("Ich warte auf den Bus.", "warten fiili burada auf ile doğal eşleşiyor."),
                    ("Wir sprechen über das Problem.", "sprechen fiili bu anlamda über ile bağlanıyor."),
                ],
            ),
            _g(
                "da- yapıları ne işe yarar?",
                "Bir isim grubuna tekrar dönerken aynı sözü yeniden kurmak yerine da- ile başlayan kısa yapılar kullanılır.",
                "Daha önce söz ettiğin bir nesneye, plana ya da konuya yeniden gönderme yapmak istediğinde kullanılır.",
                "da + edat",
                "Bu yapı A2 konuşmasını daha akıcı ve daha az tekrar eden hale getirir. Özellikle yazıda ve uzun cümlede büyük fayda sağlar.",
                "İnsanlardan söz ederken da- yapısını her zaman kullanmazsın; kişi sorularında çoğu zaman preposition + pronoun yapısı daha uygundur.",
                [
                    ("Ich warte auf den Bus. Ich warte schon lange darauf.", "İkinci cümlede aynı nesne tekrar edilmeden referans kuruluyor."),
                    ("Wir sprechen über die Reise. Wir sprechen oft darüber.", "üzerine konuşulan konu tekrar edilmeden korunuyor."),
                ],
            ),
            _g(
                "Worauf?, Woran?, Darüber?",
                "Soru biçiminde çoğu zaman wo- ile başlayan yapı, cevapta ise da- ile başlayan yapı görünür.",
                "Bir fiilin istediği edatı soru ve cevap çiftinde çalışırken kullanılır.",
                "wo + edat / da + edat",
                "Bu çift yapı soru ve cevabın aynı mantık çizgisinde kalmasını sağlar. Böylece fiil-edat ilişkisi daha sağlam yerleşir.",
                "Soru ve cevabın farklı edatlarla kurulması sık hatadır; fiilin açtığı edatı iki tarafta da korumak gerekir.",
                [
                    ("Woran denkst du? Ich denke daran.", "Soru ve cevap aynı edat mantığında ilerliyor."),
                    ("Worauf wartest du? Ich warte darauf.", "fiil-edat bağı soru-cevap zincirinde korunuyor."),
                ],
            ),
            _g(
                "İsim tekrarını azaltma",
                "A2'de aynı isim grubunu üst üste tekrar etmek yerine referans kurma becerisi önem kazanır.",
                "Kısa paragraf ya da iki cümlelik anlatımda akışı daha doğal kılmak için kullanılır.",
                "isim + ikinci cümlede da- yapısı",
                "Bu başlık yalnız gramer değil, aynı zamanda metin ekonomisidir. Gereksiz tekrarı azaltmak anlatım kalitesini artırır.",
                "Her isimden sonra otomatik da- yapısı kullanma; kimi zaman tekrar etmek de daha açık olabilir. Ama aynı kalıbı üç kez tekrarlamak akıcılığı düşürür.",
                [
                    ("Thomas träumt von einer Weltreise. Er denkt oft daran.", "İkinci cümle ilk cümledeki büyük isim grubuna geri dönüyor."),
                    ("Wir freuen uns auf das Wochenende. Alle reden schon darüber.", "aynı konu farklı cümlede kısa referansla sürdürülüyor."),
                ],
            ),
        ],
        [
            _p("Worauf wartest du?", "Neyi bekliyorsun?", "soru tarafı"),
            _p("Ich warte darauf.", "Onu bekliyorum.", "cevap tarafı"),
            _p("Woran denkst du?", "Neyi düşünüyorsun?", "denken an sorusu"),
            _p("Ich denke oft daran.", "Onu sık sık düşünüyorum.", "da- cevabı"),
            _p("Wir sprechen darüber.", "Onun hakkında konuşuyoruz.", "konu tekrarını kısaltır"),
            _p("Er träumt davon.", "Onu hayal ediyor.", "von ile da- yapısı"),
            _p("Ich freue mich darauf.", "Onu dört gözle bekliyorum.", "gelecek planları için çok doğal kalıp"),
            _p("Kannst du damit arbeiten?", "Bununla çalışabilir misin?", "araç / yöntem bağlantısı"),
            _p("Daran habe ich noch nicht gedacht.", "Bunu henüz düşünmedim.", "yüksek frekanslı A2 kalıbı"),
            _p("Darüber können wir später sprechen.", "Bunun hakkında sonra konuşabiliriz.", "toplantı ve plan bağlamında işe yarar"),
        ],
        [
            _m("Ich warte an den Bus.", "Ich warte auf den Bus.", "fiilin açtığı edat doğru seçilmelidir."),
            _m("Ich warte auf den Bus. Ich warte auf den Bus lange.", "Ich warte auf den Bus. Ich warte schon lange darauf.", "gereksiz isim tekrarını da- yapısı kırar."),
            _m("Woran wartest du?", "Worauf wartest du?", "soru yapısı fiilin istediği edata göre kurulur."),
            _m("Ich denke darüber an.", "Ich denke daran.", "denken an için cevap yapısı daran olur."),
        ],
        {
            "title": "Konuya geri dönme",
            "lines": [
                _line("A", "Thomas träumt von einer Weltreise.", "Thomas bir dünya turu hayal ediyor."),
                _line("B", "Ja, er spricht oft darüber.", "Evet, bunun hakkında sık sık konuşuyor."),
                _line("A", "Und wartet er schon darauf?", "Peki bunu şimdiden bekliyor mu?"),
                _line("B", "Natürlich. Er freut sich sehr darauf.", "Elbette. Onu çok heyecanla bekliyor."),
            ],
        },
        [
            _passage(
                "Aynı konuyu tekrar etmeden anlatmak",
                "Bu okumada aynı ismin nasıl kısaltılarak korunduğuna bak. Asıl öğrenilecek nokta tam da bu akış ekonomisi.",
                [
                    "[[Thomas::erkek adı]] träumt von einer [[Weltreise::dünya turu]]. Er denkt oft [[daran::ona / bunu düşünerek]] und spricht mit seinen [[Freunden::arkadaşları]] oft [[darüber::bunun hakkında]].",
                    "Seine Schwester wartet auf den [[Sommer::yaz]] und freut sich schon [[darauf::onu dört gözle bekliyor]]. So wiederholen sie die [[Themen::konular]] nicht jedes Mal neu.",
                ],
            )
        ],
        [
            "Fiil + edat listesini kısa kartlar halinde ayrı tekrar et.",
            "Soru ve cevabı birlikte çalış: Worauf? - Darauf.",
            "Aynı ismi üst üste üç kez kullanıyorsan o noktada da- yapısı düşünülebilir.",
            "İnsan mı şey mi anlattığını ayır; da- yapıları çoğu zaman şeylere geri döner.",
        ],
        [
            _v("die Weltreise", "die", "die Weltreisen", ["dünya turu"], "Die Weltreise ist teuer.", "Dünya turu pahalı.", "da- yapılarına bağlanan güçlü örnek isim."),
            _v("das Problem", "das", "die Probleme", ["problem", "sorun"], "Das Problem ist noch da.", "Sorun hâlâ orada.", "über ve an ile sık bağlanır."),
            _v("der Traum", "der", "die Träume", ["hayal", "rüya"], "Der Traum ist groß.", "Hayal büyük.", "träumen von kalıbına doğal köprü."),
            _v("die Musik", "die", "die Musikstücke", ["müzik"], "Die Musik ist laut.", "Müzik yüksek sesli.", "sprechen über ve denken an bağlamlarına açılabilir."),
            _v("das Gespräch", "das", "die Gespräche", ["konuşma", "sohbet"], "Das Gespräch ist interessant.", "Konuşma ilginç.", "sprechen über ile beraber gelir."),
            _v("der Plan", "der", "die Pläne", ["plan"], "Der Plan ist klar.", "Plan net.", "denken an ve sprechen über ile kullanılır."),
            _v("die Antwort", "die", "die Antworten", ["cevap"], "Die Antwort ist kurz.", "Cevap kısa.", "darauf antworten hissine köprü olur."),
            _v("die Freude", "die", "die Freuden", ["sevinç"], "Die Freude ist groß.", "Sevinç büyük.", "sich freuen auf ile ilişkilidir."),
            _v("die Sorge", "die", "die Sorgen", ["endişe", "kaygı"], "Die Sorge ist neu.", "Endişe yeni.", "denken an ile aynı düşünme alanına bağlanır."),
            _v("die E-Mail", "die", "die E-Mails", ["e-posta"], "Die E-Mail ist wichtig.", "E-posta önemli.", "darauf antworten gibi gelecekteki yapılara köprü kurar."),
            _v("dafür", "-", "-", ["bunun için", "ona karşılık"], "Dafür habe ich keine Zeit.", "Bunun için vaktim yok.", "amaç veya uygunluk bağlamı kurar."),
            _v("darüber", "-", "-", ["bunun hakkında"], "Wir sprechen darüber.", "Bunun hakkında konuşuyoruz.", "über ile geri dönüş yapısı."),
            _v("damit", "-", "-", ["bununla"], "Ich arbeite damit jeden Tag.", "Bununla her gün çalışıyorum.", "araç bildirir."),
            _v("daran", "-", "-", ["onu / bunu düşünerek"], "Ich denke oft daran.", "Bunu sık sık düşünüyorum.", "denken an cevabı."),
            _v("darauf", "-", "-", ["onu bekleyerek", "ona doğru"], "Ich warte darauf.", "Onu bekliyorum.", "warten auf cevabı."),
            _v("warten", "-", "-", ["beklemek"], "Wir warten auf den Zug.", "Treni bekliyoruz.", "sabit edatla öğrenilmesi gereken fiil."),
            _v("denken", "-", "-", ["düşünmek"], "Ich denke an meine Familie.", "Ailemi düşünüyorum.", "an ile sık bağlanır."),
            _v("träumen", "-", "-", ["hayal etmek"], "Er träumt von einer Reise.", "Bir yolculuk hayal ediyor.", "von ile tipik eşleşme."),
        ],
        "Bu ders A2'nin akıcılık tarafını açar. Her şeyi uzun uzun tekrar etmek yerine referans kurabiliyorsan yazı ve konuşma bir anda daha doğal görünmeye başlar.",
    ),
    _lesson(
        6,
        "ders-6-modal-fiillerin-praeteritum-bicimleri",
        "Modal Fiillerin Präteritum Biçimleri",
        "A2.1",
        "Bu derste konnte, wollte, musste, durfte ve sollte biçimleriyle geçmişteki zorunluluk, istek ve imkânları anlatıyoruz. Günlük konuşmada çok sık kullanılan güçlü bir A2 başlığıdır.",
        [
            "Modal fiillerin Präteritum biçimlerini tanımak.",
            "Geçmişte ne yapılabildiğini, ne yapılmak istendiğini ve ne yapılması gerektiğini anlatmak.",
            "Perfekt yerine daha doğal duyulan modal geçmiş kalıplarını görmek.",
            "Olumlu ve olumsuz kısa geçmiş cümleler kurmak.",
            "Dün, geçen gün, geçen hafta bağlamında tavsiye ve zorunluluk cümleleri üretmek.",
            "A2 seviyesinde ilk anlatı kalitesini geçmiş modal yapılarla büyütmek.",
        ],
        "konnte / wollte / musste",
        [
            {"eyebrow": "1. Adım", "title": "Modal fiiller geçmişte çoğu kez Präteritum ile duyulur", "body": "Özellikle konnte, musste, wollte gibi biçimler gündelik dilde çok sık hazır paket gibi gelir. Bu yüzden A2'de yalnız Präsens değil, geçmiş biçimlerini de erken duymak gerekir."},
            {"eyebrow": "2. Adım", "title": "Kısa geçmiş anlatıda çok işlevlidir", "body": "Dün spor yapamadım, mektup yazmalıydım, pizza yemek istedim gibi cümleler günlük hayatın tam içindedir ve A2'de önemli bir sıçramadır."},
            {"eyebrow": "3. Adım", "title": "Asıl fiil yine cümle sonunda kalır", "body": "Modal fiil çekilir; asıl eylem yalın halde sonda durur. Bu sözdizimini korumak geçmiş cümleyi temiz tutar."},
        ],
        [
            _g(
                "konnte, wollte, musste, durfte, sollte",
                "Modal fiiller geçmişte çoğu zaman Präteritum biçimiyle kullanılır.",
                "Geçmişte mümkün olan, istenen, zorunlu olan veya izin verilen şeyleri anlatırken kullanılır.",
                "özne + modal fiilin Präteritum'u + ... + infinitiv",
                "Bu yapı A2 konuşmasını çok doğal hale getirir çünkü günlük anılarda sık sık 'yapabildim / yapamadım / yapmak istedim / yapmak zorundaydım' gibi anlamlar gerekir.",
                "Modal fiili geçmişe taşıyınca asıl fiili de geçmişe çevirmeye çalışma; o hâlâ yalın halde sonda kalır.",
                [
                    ("Ich konnte gestern keinen Sport machen.", "Geçmiş imkân / imkânsızlık burada tek kalıpta kuruluyor."),
                    ("Wir mussten lange warten.", "Zorunluluk geçmişte Präteritum modal ile doğal biçimde duyuluyor."),
                ],
            ),
            _g(
                "Olumsuz geçmiş modal cümleler",
                "kein ve nicht ile birlikte modal fiiller geçmişte çok sık olumsuz anlatım kurar.",
                "Bir şeyi yapamadığını, yapmana izin verilmediğini ya da yapmak istemediğini söylerken kullanılır.",
                "özne + modal Präteritum + nicht/kein + ... + infinitiv",
                "Geçmiş anlatımın gerçek hayattaki en sık parçalarından biri tam da 'olmadı / yapamadım / izin yoktu' eksenidir. Bu yüzden olumsuz biçimleri ayrı çalışmak gerekir.",
                "Olumsuzluğu nereye yerleştirdiğin anlamı etkileyebilir; ama başlangıçta ana hedef, modal fiili ve asıl fiili doğru yerde tutmaktır.",
                [
                    ("Ich durfte gestern nicht ausgehen.", "izin yokluğu doğal bir geçmiş kalıp içinde veriliyor."),
                    ("Er wollte keinen Kaffee trinken.", "isim olumsuzluğu ile modal geçmiş bir arada çalışıyor."),
                ],
            ),
            _g(
                "Tavsiye ve zorunluluk tonu",
                "sollte ve musste aynı şey değildir; biri daha çok tavsiye veya beklenti, diğeri zorunluluk hissi verir.",
                "Geçmişte neyin doğru olduğuna dair yorum yaparken veya zorunlu bir eylemi anlatırken kullanılır.",
                "sollte = yapmalıydı / musste = yapmak zorundaydı",
                "Bu ton farkı A2'de önemlidir çünkü yalnız gramer değil, konuşanın bakışı da cümleye girer.",
                "sollte ile musste'yi eş anlamlı kullanmak, cümledeki baskı derecesini bozar.",
                [
                    ("Du solltest einen Brief schreiben.", "daha çok tavsiye veya beklenti tonudur."),
                    ("Ich musste zum Arzt gehen.", "zorunluluk daha sert biçimde duyulur."),
                ],
            ),
            _g(
                "Perfekt yerine neden Präteritum?",
                "Bazı kısa modal geçmiş cümleleri konuşmada Präteritum ile daha doğal ve daha hafif duyulur.",
                "Gündelik anlatıda modal fiillerin geçmişini kurarken kullanılır.",
                "modal fiilin Präteritum'u + infinitiv",
                "Teoride Perfekt alternatifleri de vardır; ama A2 kullanım refleksi açısından konnte, musste, wollte biçimlerini hazır bloklar gibi tanımak çok daha verimlidir.",
                "Her geçmiş cümleyi otomatik Perfekt'e çevirmek bu başlıkta yapaylık üretir.",
                [
                    ("Ich wollte Pizza essen.", "Bu cümle gündelik konuşmada Perfekt'ten daha doğal duyulur."),
                    ("Sie konnte gestern nicht kommen.", "kısa geçmiş olay cümlesi olarak çok yüksek frekanslıdır."),
                ],
            ),
        ],
        [
            _p("Ich konnte gestern keinen Sport machen.", "Dün spor yapamadım.", "geçmişte imkânsızlık"),
            _p("Ich wollte Pizza essen.", "Pizza yemek istedim.", "geçmiş istek"),
            _p("Du solltest den Brief schreiben.", "Mektubu yazmalıydın.", "geçmiş tavsiye"),
            _p("Wir mussten lange warten.", "Uzun süre beklemek zorunda kaldık.", "zorunluluk"),
            _p("Er durfte nicht ausgehen.", "Dışarı çıkmasına izin yoktu.", "yasak / izin yokluğu"),
            _p("Ich konnte nicht schlafen.", "Uyuyamadım.", "çok sık günlük kalıp"),
            _p("Sie wollte später anrufen.", "Daha sonra aramak istedi.", "gelecek niyetin geçmişte anlatımı"),
            _p("Wir sollten früher kommen.", "Daha erken gelmeliydik.", "beklenti / tavsiye"),
            _p("Ich musste zum Arzt gehen.", "Doktora gitmek zorundaydım.", "sağlık bağlamına köprü"),
            _p("Konntest du mir helfen?", "Bana yardım edebildin mi?", "soru biçimi"),
        ],
        [
            _m("Ich konnte gestern keinen Sport gemacht.", "Ich konnte gestern keinen Sport machen.", "modalden sonra fiil yalın kalır."),
            _m("Ich musste zum Arzt gegangen.", "Ich musste zum Arzt gehen.", "aynı cümlede iki farklı geçmiş yükü kurma."),
            _m("Ich wollte nicht Pizza essen.", "Ich wollte keine Pizza essen.", "isim olumsuzluğu burada kein ile daha doğrudur."),
            _m("Du musstest schreiben einen Brief.", "Du musstest einen Brief schreiben.", "nesne ve fiilin yeri korunmalıdır."),
        ],
        {
            "title": "Dünkü program",
            "lines": [
                _line("A", "Warum bist du so müde?", "Neden bu kadar yorgunsun?"),
                _line("B", "Ich konnte letzte Nacht nicht schlafen.", "Geçen gece uyuyamadım."),
                _line("A", "Und heute?", "Peki bugün?"),
                _line("B", "Heute musste ich trotzdem arbeiten.", "Bugün yine de çalışmak zorundaydım."),
            ],
        },
        [
            _passage(
                "Dün planlandığı gibi gitmedi",
                "Okumada önce modal fiili bul, sonra en sonda kalan eyleme bak. Geçmiş anlatının çekirdeği bu ikiliyle kuruluyor.",
                [
                    "[[Can::erkek adı]] wollte gestern ins [[Kino::sinema]] gehen, aber er [[konnte::yapabildi / yapamadı bağlama göre]] nicht. Er musste lange [[arbeiten::çalışmak]] und später noch einen [[Brief::mektup]] schreiben.",
                    "Am Abend sollte er seine [[Mutter::anne]] anrufen. Das wollte er auch, aber er war so [[müde::yorgun]] und durfte nicht mehr lange aufbleiben.",
                ],
            )
        ],
        [
            "Modal fiilin hangi tonu verdiğini ayrı duy: istek mi, zorunluluk mu, izin mi?",
            "Präteritum modal kalıplarını blok cümle olarak tekrar etmek en verimli yöntemdir.",
            "Bir cümlede yalnız bir geçmiş omurgası kur; modal varsa asıl fiili yeniden geçmişe çevirmeye çalışma.",
            "Soru biçimlerini de ayrıca dene; konntest du, wolltest du gibi açılışlar çok kullanılır.",
        ],
        [
            _v("der Sport", "der", "die Sportarten", ["spor"], "Der Sport ist heute nicht möglich.", "Bugün spor mümkün değil.", "konnte keinen Sport machen kalıbına bağlanır."),
            _v("der Brief", "der", "die Briefe", ["mektup"], "Der Brief ist noch nicht fertig.", "Mektup henüz hazır değil.", "sollte schreiben örneğinde geçer."),
            _v("die Prüfung", "die", "die Prüfungen", ["sınav"], "Die Prüfung ist morgen.", "Sınav yarın.", "zorunluluk ve hazırlık bağlamı kurar."),
            _v("das Auto", "das", "die Autos", ["araba"], "Das Auto ist kaputt.", "Araba bozuk.", "konnte nicht fahren kalıplarına zemin olur."),
            _v("die Einladung", "die", "die Einladungen", ["davet", "davetiye"], "Die Einladung ist nett.", "Davet hoş.", "durfte / wollte ile bağlanabilir."),
            _v("die Hausaufgabe", "die", "die Hausaufgaben", ["ödev"], "Die Hausaufgabe ist schwer.", "Ödev zor.", "musste machen bağlamı."),
            _v("der Termin", "der", "die Termine", ["randevu"], "Der Termin war früh.", "Randevu erkendi.", "sollte / musste ile kullanılabilir."),
            _v("die Arbeit", "die", "die Arbeiten", ["iş", "çalışma"], "Die Arbeit war lang.", "İş uzundu.", "zorunluluk anlatısında geçer."),
            _v("das Geld", "das", "die Gelder", ["para"], "Das Geld war nicht genug.", "Para yeterli değildi.", "durfte/konnte bağlamı yaratır."),
            _v("der Arzt", "der", "die Ärzte", ["doktor"], "Der Arzt war sehr freundlich.", "Doktor çok nazikti.", "sağlık bağlamına köprü."),
            _v("konnte", "-", "-", ["yapabildi", "-ebildi"], "Ich konnte nicht kommen.", "Gelemedim.", "modal geçmiş çekimi."),
            _v("wollte", "-", "-", ["istedi"], "Ich wollte früher gehen.", "Daha erken gitmek istedim.", "niyet ve arzu."),
            _v("musste", "-", "-", ["zorundaydı", "-mek zorunda kaldı"], "Wir mussten warten.", "Beklemek zorunda kaldık.", "zorunluluk tonu."),
            _v("durfte", "-", "-", ["izinliydi", "izin verildi"], "Er durfte mitkommen.", "Onun gelmesine izin verildi.", "izin / yasak alanı."),
            _v("sollte", "-", "-", ["yapmalıydı"], "Du solltest schlafen.", "Uyumalısın / uyumalıydın.", "tavsiye veya beklenti."),
            _v("müde", "-", "-", ["yorgun"], "Ich war sehr müde.", "Çok yorgundum.", "modal geçmişin nedenini açıklayan sıfat."),
            _v("später", "-", "-", ["daha sonra"], "Ich wollte später anrufen.", "Daha sonra aramak istedim.", "planı zamana bağlar."),
            _v("schlafen", "-", "-", ["uyumak"], "Ich konnte nicht schlafen.", "Uyuyamadım.", "yüksek frekanslı modal fiil birleşimi."),
        ],
        "Bu ders A2 anlatısını ciddi biçimde büyütür. Artık sadece ne yaptığını değil, neyi yapabildiğini, yapmak zorunda kaldığını veya yapmayı istediğini de geçmişte anlatabiliyorsun.",
    ),
    _lesson(
        7,
        "ders-7-alisveris-kiyafet-ve-sifatlarla-betimleme",
        "Alışveriş, Kıyafet ve Sıfatlarla Betimleme",
        "A2.1",
        "Bu derste kıyafet ve alışveriş dilini sıfatlarla birleştiriyoruz. Hangi bedenin uygun olduğu, bir ürünün pahalı mı rahat mı olduğu gibi günlük konuşmaların gerçek alanına giriyoruz.",
        [
            "Kıyafet isimlerini ve temel mağaza dilini kullanmak.",
            "Renk, beden, rahatlık ve fiyat gibi betimleyici sıfatlarla daha zengin cümleler kurmak.",
            "Belirsiz artikelden sonra en sık görülen sıfat sonlarını tanımak.",
            "gefällt mir / passt mir gibi sık mağaza kalıplarını duymak.",
            "Bir ürün hakkında kısa değerlendirme yapmak.",
            "A2 düzeyinde alışveriş diyaloğunu daha doğal hale getirmek.",
        ],
        "kıyafet dili + sıfatlar",
        [
            {"eyebrow": "1. Adım", "title": "Ürünü yalnız isimle değil özellikle anlat", "body": "A2'de artık yalnız 'bir ceket' demek değil, 'mavi, rahat, biraz pahalı bir ceket' diyebilmek önemlidir. Bu ayrıntı konuşmayı hemen büyütür."},
            {"eyebrow": "2. Adım", "title": "Sıfat sonları ilk kez görünür hale gelir", "body": "Belirsiz artikelden sonra ein rotes Kleid, eine blaue Jacke gibi küçük değişimler görmeye başlarız. Bu ders sistemin tamamını değil, en sık görülen hissi kurar."},
            {"eyebrow": "3. Adım", "title": "Mağaza dili değerlendirme ister", "body": "gefällt mir, passt mir nicht, ist zu teuer gibi ifadeler alışverişi yalnız soru-cevap olmaktan çıkarıp karar verme konuşmasına dönüştürür."},
        ],
        [
            _g(
                "Sıfat + isim birleşimi",
                "Sıfat ismi niteler ve ürün hakkında daha ayrıntılı bilgi verir.",
                "Renk, büyüklük, rahatlık veya fiyat gibi özellik belirtirken kullanılır.",
                "artikel + sıfat + isim",
                "Bu yapı A2 konuşmasını tek kelimelik tanımlardan çıkarır. Karar verirken ya da tavsiye isterken sıfatlar belirleyici olur.",
                "Sıfatı yalnız tek başına öğrenmek yetmez; isimle birlikte küçük bloklar halinde tekrar etmek gerekir.",
                [
                    ("eine blaue Jacke", "Dişil isim önünde sıfat ürünün rengini belirtiyor."),
                    ("ein rotes Kleid", "Nötr isimle birlikte sık görülen ilk sıfat sonu örneği."),
                ],
            ),
            _g(
                "Belirsiz artikelden sonra temel sıfat sonları",
                "ein / eine ile gelen isimlerde sıfatın sonu küçük biçim değişikliği gösterebilir.",
                "Bir ürünü ilk kez tanıtırken veya genel bir ürün seçeneğinden söz ederken kullanılır.",
                "ein + sıfat + isim / eine + sıfat + isim",
                "Bu başlıkta amaç tüm tabloyu ezberlemek değil, kulağı küçük son değişimlerine açmaktır. Özellikle sık kalıpları blok olarak duymak yeterlidir.",
                "Sıfat sonunu görünce bütün cümleyi bırakma; A2'de önce anlamı ve ana kalıbı güvenceye almak daha önemlidir.",
                [
                    ("Ich suche einen warmen Mantel.", "Maskulin nesnede sıfat sonu farklılaşıyor."),
                    ("Sie kauft eine schwarze Hose.", "Dişil isimle farklı, daha tanıdık bir son duyuyoruz."),
                ],
            ),
            _g(
                "gefällt mir / passt mir",
                "Bir ürünün hoşuna gidip gitmediğini veya üzerine uyup uymadığını söylemek için kullanılır.",
                "Mağazada deneme, seçim yapma veya arkadaşla fikir konuşma sırasında kullanılır.",
                "Das gefällt mir. / Das passt mir gut.",
                "Alışveriş konuşmasının gerçek kalbi değerlendirmedir. Bu iki kalıp ürünle duygusal ve pratik ilişki kurmayı sağlar.",
                "gefallen ile passen aynı şey değildir; biri beğeniyi, diğeri uyumu anlatır.",
                [
                    ("Die Jacke gefällt mir sehr.", "Beğeniyi öne çıkarır."),
                    ("Der Mantel passt mir gut.", "Beden ve uyum bilgisini verir."),
                ],
            ),
            _g(
                "zu teuer, zu groß, sehr bequem",
                "Derece belirten küçük zarflar ve sıfatlar ürün değerlendirmesini daha keskin yapar.",
                "Bir şeyin fazla pahalı, fazla büyük veya oldukça rahat olduğunu söylemek istediğinde kullanılır.",
                "zu + sıfat / sehr + sıfat",
                "A2'de yalnız iyi-kötü demek yerine miktarı veya yoğunluğu da söylemek gerekir. zu ve sehr bu işi hızlıca görür.",
                "zu her zaman olumlu vurgu yapmaz; çoğu kez fazlalık veya sorun anlatır.",
                [
                    ("Die Schuhe sind zu teuer.", "Burada aşırılık ve sorun hissi var."),
                    ("Das T-Shirt ist sehr bequem.", "olumlu güçlendirme örneği."),
                ],
            ),
        ],
        [
            _p("Ich suche eine blaue Jacke.", "Mavi bir ceket arıyorum.", "ürün arama"),
            _p("Haben Sie diese Hose in Größe 38?", "Bu pantolonun 38 bedeni var mı?", "beden sorma"),
            _p("Das Kleid gefällt mir sehr.", "Bu elbise çok hoşuma gidiyor.", "beğeni"),
            _p("Der Mantel passt mir nicht gut.", "Palto üzerime iyi olmuyor.", "uyum sorunu"),
            _p("Die Schuhe sind zu teuer.", "Ayakkabılar fazla pahalı.", "fiyat değerlendirmesi"),
            _p("Ich brauche ein bequemes Hemd.", "Rahat bir gömleğe ihtiyacım var.", "sıfat + isim"),
            _p("Kann ich das anprobieren?", "Bunu deneyebilir miyim?", "mağaza hizmet kalıbı"),
            _p("Haben Sie das auch in Schwarz?", "Bunun siyahı da var mı?", "renk alternatifi"),
            _p("Die Bluse ist elegant, aber ein bisschen teuer.", "Bluz şık ama biraz pahalı.", "karşıt değerlendirme"),
            _p("Für mich ist der Rock zu kurz.", "Bana göre etek fazla kısa.", "kişisel değerlendirme"),
        ],
        [
            _m("Ich suche Jacke blau.", "Ich suche eine blaue Jacke.", "isim ve sıfatı doğru blok içinde kurmak gerekir."),
            _m("Die Jacke passt mich.", "Die Jacke passt mir.", "passen kalıbında mir yapısı korunur."),
            _m("Das gefällt ich.", "Das gefällt mir.", "gefallen kalıbında kişisel yönelme yapısı gerekir."),
            _m("Die Schuhe sind sehr teuer zu.", "Die Schuhe sind zu teuer.", "zu doğrudan sıfatın önüne gelir."),
        ],
        {
            "title": "Mağazada karar verme",
            "lines": [
                _line("A", "Wie findest du die Jacke?", "Ceketi nasıl buluyorsun?"),
                _line("B", "Sie gefällt mir, aber sie ist ein bisschen zu teuer.", "Hoşuma gidiyor ama biraz fazla pahalı."),
                _line("A", "Und passt sie dir?", "Peki üzerine oluyor mu?"),
                _line("B", "Ja, sie passt mir gut, aber ich suche lieber eine schwarze Jacke.", "Evet iyi oluyor ama daha çok siyah bir ceket arıyorum."),
            ],
        },
        [
            _passage(
                "Kısa alışveriş notu",
                "Bu metinde ürün adı, renk, fiyat ve kişisel değerlendirme birlikte ilerliyor. A2 seviyesinde tam olarak ihtiyaç duyulan şey bu birleşik anlatım.",
                [
                    "Im [[Geschäft::mağaza]] sucht [[Aylin::kadın adı]] eine [[schwarze::siyah]] [[Jacke::ceket]]. Sie findet auch ein [[rotes::kırmızı]] [[Kleid::elbise]], aber das Kleid ist ihr zu [[teuer::pahalı]].",
                    "Die Jacke [[gefällt::hoşuna gidiyor]] ihr sehr und sie [[passt::uyuyor]] ihr gut. Trotzdem möchte sie noch eine andere [[Größe::beden]] probieren.",
                ],
            )
        ],
        [
            "Sıfatları yalnız liste olarak değil ürünle birlikte blok halinde tekrar et.",
            "gefallen ve passen kalıplarını ayrı kartlar halinde ezberlemek çok işe yarar.",
            "Renk, beden ve fiyat kelimelerini aynı cümlede birleştirmeyi dene.",
            "zu ve sehr farkını özellikle kulakla çalış; ikisi aynı yoğunluğu anlatmaz.",
        ],
        [
            _v("der Mantel", "der", "die Mäntel", ["palto", "manto"], "Der Mantel ist warm.", "Palto sıcak tutuyor.", "kış alışverişi için temel kelime."),
            _v("die Jacke", "die", "die Jacken", ["ceket"], "Die Jacke ist blau.", "Ceket mavi.", "renk ve uyum cümlelerinde sık geçer."),
            _v("das Kleid", "das", "die Kleider", ["elbise"], "Das Kleid ist elegant.", "Elbise şık.", "nötr isimle sıfat birleşimi."),
            _v("der Pullover", "der", "die Pullover", ["kazak"], "Der Pullover ist bequem.", "Kazak rahat.", "gündelik alışveriş dili."),
            _v("die Hose", "die", "die Hosen", ["pantolon"], "Die Hose ist zu lang.", "Pantolon fazla uzun.", "beden değerlendirmesi."),
            _v("das Hemd", "das", "die Hemden", ["gömlek"], "Das Hemd ist weiß.", "Gömlek beyaz.", "erkek giyim örneği."),
            _v("die Bluse", "die", "die Blusen", ["bluz"], "Die Bluse ist teuer.", "Bluz pahalı.", "dişil ürün ismi."),
            _v("der Rock", "der", "die Röcke", ["etek"], "Der Rock ist modern.", "Etek modern.", "kadın giyim kelime grubu."),
            _v("die Schuhe", "die", "die Schuhe", ["ayakkabılar"], "Die Schuhe sind bequem.", "Ayakkabılar rahat.", "çoğul ürün olarak sık kullanılır."),
            _v("die Größe", "die", "die Größen", ["beden", "ölçü"], "Die Größe ist richtig.", "Beden doğru.", "mağaza konuşmasının çekirdek ismidir."),
            _v("der Preis", "der", "die Preise", ["fiyat"], "Der Preis ist hoch.", "Fiyat yüksek.", "karar verme dili."),
            _v("die Umkleide", "die", "die Umkleiden", ["soyunma kabini"], "Die Umkleide ist dort.", "Deneme kabini orada.", "mağaza mekân diliyle bağ kurar."),
            _v("blau", "-", "-", ["mavi"], "Die Jacke ist blau.", "Ceket mavi.", "renk sıfatı."),
            _v("schwarz", "-", "-", ["siyah"], "Der Mantel ist schwarz.", "Palto siyah.", "yüksek frekanslı renk."),
            _v("teuer", "-", "-", ["pahalı"], "Die Schuhe sind teuer.", "Ayakkabılar pahalı.", "değerlendirme sıfatı."),
            _v("bequem", "-", "-", ["rahat"], "Das Hemd ist bequem.", "Gömlek rahat.", "giyim değerlendirmesi."),
            _v("gefällt", "-", "-", ["hoşa gidiyor"], "Die Bluse gefällt mir.", "Bluz hoşuma gidiyor.", "kişisel beğeni kalıbı."),
            _v("passt", "-", "-", ["uyuyor", "oluyor"], "Der Pullover passt mir gut.", "Kazak bana iyi oluyor.", "beden/uyum kalıbı."),
        ],
        "Bu dersin sonunda bir ürünü yalnız adlandırmıyor; rengi, fiyatı, bedeni ve sana göre uygun olup olmadığını da söyleyebiliyor olmalısın. A2 iletişimi tam burada somutlaşır.",
    ),
    _lesson(
        8,
        "ders-8-deshalb-ve-trotzdem-ile-bag-kurma",
        "deshalb ve trotzdem ile Bağ Kurma",
        "A2.2",
        "Bu derste iki cümle arasındaki sebep-sonuç ve beklenti kırılmasını daha doğal anlatıyoruz. deshalb ve trotzdem, A2 konuşmasına düşünce akışı kazandıran iki güçlü kelimedir.",
        [
            "deshalb ile sonuç anlatmak.",
            "trotzdem ile beklentinin tersine giden durumu göstermek.",
            "Bağlaç sonrası fiilin ikinci pozisyonda kaldığını görmek.",
            "Kısa metinlerde neden-sonuç akışı kurmak.",
            "Modal fiillerle birlikte de bu yapıları kullanabilmek.",
            "Tek cümlelerden küçük paragraf akışına geçmek.",
        ],
        "sebep-sonuç + karşıtlık",
        [
            {"eyebrow": "1. Adım", "title": "deshalb sonucu açar", "body": "İlk cümlede sebep vardır; ikinci cümlede deshalb ile sonuç görünür. Bu yapı iki bağımsız cümleyi birbirine çok doğal biçimde bağlar."},
            {"eyebrow": "2. Adım", "title": "trotzdem beklentiyi kırar", "body": "İlk cümleye bakınca başka bir sonuç beklenir; ama trotzdem ile tersine giden gerçek durum söylenir. Bu, A2 anlatımını çok daha canlı yapar."},
            {"eyebrow": "3. Adım", "title": "Bağlaçtan sonra fiil yine ikinci yerde", "body": "deshalb ve trotzdem yan cümle bağlacı gibi çalışmaz; ardından çekimli fiil ikinci pozisyonda kalır. Bu ayrım çok önemlidir."},
        ],
        [
            _g(
                "deshalb ile sonuç",
                "deshalb bir önceki cümlenin sonucunu başlatır.",
                "Bir sebebin doğal sonucunu ikinci cümlede göstermek istediğinde kullanılır.",
                "Sebep cümlesi. Deshalb + fiil + özne + ...",
                "A2'de düşünce akışı kurmak için yalnız tek cümle yetmez. deshalb, iki cümleyi temiz biçimde bağlayarak anlatımı büyütür.",
                "deshalb sonrasında fiili sona atma; bu yapı yan cümle değil, ana cümle düzeniyle devam eder.",
                [
                    ("Es regnet. Deshalb nehme ich einen Schirm.", "İkinci cümlede sonuç doğrudan açılıyor."),
                    ("Der Zug hat Verspätung. Deshalb kommen wir später.", "sebep önce, sonuç sonra net biçimde bağlanıyor."),
                ],
                {"correct": "Es ist spät. Deshalb gehe ich nach Hause.", "wrong": "Es ist spät. Deshalb ich gehe nach Hause.", "reason": "deshalb sonrası fiil ikinci yerde kalır."},
            ),
            _g(
                "trotzdem ile karşıt sonuç",
                "trotzdem beklenenin tersine giden ikinci cümleyi başlatır.",
                "Bir engel, sorun veya ters durum olsa bile asıl eylemin gerçekleştiğini söylemek istediğinde kullanılır.",
                "Engel cümlesi. Trotzdem + fiil + özne + ...",
                "Bu yapı A2 konuşmasına nüans katar çünkü 'ama yine de' hissini çok kısa ve güçlü biçimde verir.",
                "trotzdem'i cümlenin içine rastgele atmak yerine yeni cümlenin başlangıcında kullanmak daha güvenli ve anlaşılırdır.",
                [
                    ("Ich bin müde. Trotzdem arbeite ich weiter.", "beklenen sonuç dinlenmek olurdu; ama ikinci cümle bunun tersini söylüyor."),
                    ("Das Hotel ist teuer. Trotzdem buchen wir ein Zimmer.", "engel bilgisi ve gerçek karar birlikte veriliyor."),
                ],
            ),
            _g(
                "Fiil yeri: yan cümle değil ana cümle",
                "deshalb ve trotzdem sonrasında fiil ana cümle düzeninde ikinci pozisyondadır.",
                "Bu iki sözcükle yeni cümleye başlarken kullanılır.",
                "deshalb/trotzdem + fiil + özne + ...",
                "Bu ayrım çok değerlidir çünkü öğrenci weil ile deshalb'ı, obwohl ile trotzdem'i sık karıştırır. Yapı tipini cümle düzeninden anlayabilmek gerekir.",
                "Bağlaç gördüğünde otomatik fiili sona atma; önce bunun ana cümle mi yan cümle mi olduğuna karar ver.",
                [
                    ("Es ist kalt. Trotzdem gehen wir raus.", "gehen fiili ikinci yerde kaldı."),
                    ("Ich habe wenig Zeit. Deshalb antworte ich kurz.", "antworten fiili yine ikinci yerde."),
                ],
            ),
            _g(
                "Modal fiillerle birlikte kullanım",
                "deshalb ve trotzdem, modal fiilli cümlelerle de rahatlıkla birleşebilir.",
                "Zorunluluk, istek veya imkân anlatan cümleleri bağlamak istediğinde kullanılır.",
                "deshalb/trotzdem + modal fiil + özne + ... + infinitiv",
                "Bu kullanım gerçek hayatta çok sık çıkar çünkü sebep-sonuç çoğu zaman bir zorunluluk veya tercih cümlesine bağlanır.",
                "Modal fiil varsa yine çekimli parça erkene gelir; asıl fiil sonda kalır.",
                [
                    ("Ich bin krank. Trotzdem muss ich arbeiten.", "karşıtlık ve zorunluluk tek cümlede birleşiyor."),
                    ("Der Bus kommt nicht. Deshalb müssen wir laufen.", "sebep-sonuç modal fiille birleşiyor."),
                ],
            ),
        ],
        [
            _p("Es regnet. Deshalb bleibe ich zu Hause.", "Yağmur yağıyor. Bu yüzden evde kalıyorum.", "sebep-sonuç"),
            _p("Ich bin müde. Trotzdem lerne ich weiter.", "Yorgunum. Yine de çalışmaya devam ediyorum.", "karşıt sonuç"),
            _p("Der Zug ist spät. Deshalb kommen wir später.", "Tren gecikmiş. Bu yüzden daha geç geliyoruz.", "ulaşım bağlamı"),
            _p("Das Hotel ist teuer. Trotzdem buchen wir es.", "Otel pahalı. Yine de onu rezerve ediyoruz.", "karar cümlesi"),
            _p("Ich habe wenig Zeit. Deshalb antworte ich kurz.", "Az vaktim var. Bu yüzden kısa cevap veriyorum.", "zaman baskısı"),
            _p("Er ist krank. Trotzdem arbeitet er heute.", "O hasta. Yine de bugün çalışıyor.", "beklenti kırılması"),
            _p("Wir haben kein Auto. Deshalb fahren wir mit dem Bus.", "Arabamız yok. Bu yüzden otobüsle gidiyoruz.", "sonuç kalıbı"),
            _p("Es ist kalt. Trotzdem gehen wir spazieren.", "Hava soğuk. Yine de yürüyüşe çıkıyoruz.", "karşıtlık kalıbı"),
            _p("Der Laden ist zu. Deshalb kaufen wir morgen ein.", "Dükkan kapalı. Bu yüzden yarın alışveriş yapıyoruz.", "plan değişikliği"),
            _p("Ich bin nervös. Trotzdem spreche ich mit dem Chef.", "Gerginim. Yine de müdürle konuşuyorum.", "duygu + eylem"),
        ],
        [
            _m("Es regnet. Deshalb ich bleibe zu Hause.", "Es regnet. Deshalb bleibe ich zu Hause.", "deshalb sonrası fiil ikinci yerde olmalıdır."),
            _m("Ich bin müde. Trotzdem ich arbeite.", "Ich bin müde. Trotzdem arbeite ich.", "aynı sözdizimi kuralı burada da geçerlidir."),
            _m("Es ist spät, deshalb zu Hause ich gehe.", "Es ist spät. Deshalb gehe ich nach Hause.", "ana cümle düzeni korunmalıdır."),
            _m("Er ist krank. Trotzdem er nicht kommt.", "Er ist krank. Trotzdem kommt er.", "trotzdem sonrası bağımsız cümle olarak kurulmalıdır."),
        ],
        {
            "title": "Plan neden değişti?",
            "lines": [
                _line("A", "Warum kommst du heute später?", "Bugün neden daha geç geliyorsun?"),
                _line("B", "Der Bus hat Verspätung. Deshalb komme ich später.", "Otobüs gecikti. Bu yüzden daha geç geliyorum."),
                _line("A", "Und gehst du danach noch zum Kurs?", "Peki sonra yine de kursa gidiyor musun?"),
                _line("B", "Ja, ich bin müde. Trotzdem gehe ich hin.", "Evet, yorgunum. Yine de gidiyorum."),
            ],
        },
        [
            _passage(
                "Küçük sebep-sonuç zinciri",
                "Önce sebebi oku, sonra deshalb veya trotzdem ile ikinci cümlenin hangi yönde gittiğine bak.",
                [
                    "Heute ist [[Mila::kadın adı]] sehr [[müde::yorgun]]. [[Trotzdem::yine de]] geht sie zum [[Kurs::kurs]], weil morgen eine wichtige [[Prüfung::sınav]] ist.",
                    "Der [[Bus::otobüs]] kommt zu spät. [[Deshalb::bu yüzden]] nimmt sie später ein [[Taxi::taksi]] und kommt doch noch pünktlich an.",
                ],
            )
        ],
        [
            "deshalb ve trotzdem'i aynı iki cümle üzerinde dönüşümlü dene; anlam yönünü hemen fark edersin.",
            "Bu başlıkta noktalama ve yeni cümle başlatma, öğrenmeyi kolaylaştırır.",
            "Çekimli fiilin ikinci yerde kaldığını özellikle yüksek sesle kontrol et.",
            "Modal fiilli örnekler kurarak bu yapıları günlük plan diliyle birleştir.",
        ],
        [
            _v("der Regen", "der", "die Regen", ["yağmur"], "Der Regen ist stark.", "Yağmur kuvvetli.", "deshalb ve trotzdem cümleleri için iyi sebep kaynağı."),
            _v("die Bahn", "die", "die Bahnen", ["tren", "raylı ulaşım"], "Die Bahn kommt spät.", "Tren geç geliyor.", "ulaşım sonuçları kurar."),
            _v("der Stau", "der", "die Staus", ["trafik sıkışıklığı"], "Der Stau ist lang.", "Trafik sıkışıklığı uzun sürüyor.", "gecikme nedeni."),
            _v("die Erkältung", "die", "die Erkältungen", ["soğuk algınlığı"], "Die Erkältung ist stark.", "Soğuk algınlığı ağır.", "trotzdem ile sağlık bağlamı."),
            _v("die Arbeit", "die", "die Arbeiten", ["iş"], "Die Arbeit ist heute schwer.", "İş bugün zor.", "sonuç cümlelerine köprü."),
            _v("das Treffen", "das", "die Treffen", ["buluşma", "toplantı"], "Das Treffen ist wichtig.", "Buluşma önemli.", "sebep-sonuç bağlamı."),
            _v("die Zeit", "die", "die Zeiten", ["zaman"], "Die Zeit ist knapp.", "Zaman dar.", "deshalb cümlelerini doğal kılar."),
            _v("der Plan", "der", "die Pläne", ["plan"], "Der Plan ist anders.", "Plan farklı.", "karşıtlık anlatımında kullanılabilir."),
            _v("die Nachricht", "die", "die Nachrichten", ["haber", "mesaj"], "Die Nachricht ist kurz.", "Mesaj kısa.", "sebep bilgisi taşır."),
            _v("das Problem", "das", "die Probleme", ["sorun"], "Das Problem ist groß.", "Sorun büyük.", "trotzdem yapısına uygun engel kelimesi."),
            _v("deshalb", "-", "-", ["bu yüzden"], "Deshalb bleibe ich heute zu Hause.", "Bu yüzden bugün evde kalıyorum.", "sonuç bağlayıcısı."),
            _v("trotzdem", "-", "-", ["yine de", "buna rağmen"], "Trotzdem komme ich.", "Yine de geliyorum.", "karşıt bağlayıcı."),
            _v("pünktlich", "-", "-", ["dakik", "zamanında"], "Ich komme pünktlich.", "Zamanında geliyorum.", "sonuç cümlelerinde sık geçer."),
            _v("später", "-", "-", ["daha sonra", "daha geç"], "Ich komme später.", "Daha geç geliyorum.", "gecikme sonucu"),
            _v("trotz", "-", "-", ["-e rağmen"], "Trotz des Regens gehe ich raus.", "Yağmura rağmen dışarı çıkıyorum.", "trotzdem ile aynı anlam alanına yakınlaşır."),
            _v("kurz", "-", "-", ["kısa"], "Ich antworte kurz.", "Kısa cevap veriyorum.", "zaman baskısında doğal sonuç."),
            _v("weiter", "-", "-", ["devam ederek", "ileri"], "Ich arbeite trotzdem weiter.", "Yine de çalışmaya devam ediyorum.", "trotzdem ile sık eşleşir."),
            _v("doch", "-", "-", ["yine de", "aslında"], "Er kommt doch.", "Yine de geliyor.", "karşıt beklentiyle ilişkilidir."),
        ],
        "Bu dersi kapattığında iki cümle arasındaki ilişkiyi daha net kurabiliyor olmalısın. A2'nin anlatı kalitesi çoğu zaman tam da bu bağlama kelimeleriyle yükselir.",
    ),
    _lesson(
        9,
        "ders-9-komparativ-ve-superlativ",
        "Komparativ ve Superlativ",
        "A2.2",
        "Bu derste artık şeyleri sadece nitelemiyor, karşılaştırıyoruz. Daha büyük, daha pahalı, en iyi, en yakın gibi yapılar günlük konuşmada çok sık gerekli olduğu için A2'nin merkezindedir.",
        [
            "Komparativ yapısını kurmak.",
            "als ile iki şeyi karşılaştırmak.",
            "am ...-sten ve en + sıfat mantığını görmek.",
            "gut, gern, viel gibi düzensiz karşılaştırmaları tanımak.",
            "Yer, fiyat, kalite ve tercih anlatımında kıyas cümleleri üretmek.",
            "A2 seviyesinde seçim ve görüş bildirmeyi güçlendirmek.",
        ],
        "karşılaştırma dili",
        [
            {"eyebrow": "1. Adım", "title": "A2'de artık yalnız betimlemiyoruz, kıyaslıyoruz", "body": "Bir şehrin diğerinden büyük olduğunu, bir otelin daha ucuz olduğunu, bir seçeneğin en iyisi olduğunu söylemek günlük dilde çok gerekli bir beceridir."},
            {"eyebrow": "2. Adım", "title": "Komparativ ile iki öğe, Superlativ ile bütün grup düşünülür", "body": "Biri diğerinden daha iyi olabilir; ama en iyisi demek tüm seçenekler içinde tepe noktayı gösterir. Bu farkı baştan net görmek gerekir."},
            {"eyebrow": "3. Adım", "title": "Bazı sıfatlar düzenli gitmez", "body": "gut-besser-am besten, viel-mehr-am meisten gibi biçimler kuralı sadece ekleyerek kurulmaz. Bunları ayrı bloklar olarak almak gerekir."},
        ],
        [
            _g(
                "Komparativ",
                "İki şey, kişi veya durumu kıyaslamak için kullanılır.",
                "Bir seçeneğin diğerinden daha büyük, daha ucuz, daha hızlı vb. olduğunu söylerken kullanılır.",
                "sıfat + -er + als",
                "Komparativ A2'de karar verme ve görüş bildirme için çok işlevlidir. Bu yapı olmadan tercihler düz ve sınırlı kalır.",
                "Karşılaştırmanın ikinci parçasını eksik bırakmak anlamı bulanıklaştırır; çoğu zaman als ile ikinci öğeyi vermek gerekir.",
                [
                    ("Berlin ist größer als Bonn.", "iki şehir doğrudan kıyaslanıyor."),
                    ("Dieses Hotel ist billiger als das andere.", "ürün veya hizmet karşılaştırmasında çok doğal."),
                ],
            ),
            _g(
                "Superlativ",
                "Bir grup içinde en yüksek veya en güçlü dereceyi göstermek için kullanılır.",
                "En iyi, en hızlı, en yakın gibi seçim yaparken kullanılır.",
                "am + sıfat-sten / der-die-das + superlativ",
                "Superlativ karar cümlesini netleştirir; artık yalnız iki seçenek değil, tüm seçenekler arasında yargı verirsin.",
                "En yüksek dereceyi anlatırken sadece komparativ biçimini tekrar etmek yeterli değildir; am ...sten kalıbını ayrıca tanımak gerekir.",
                [
                    ("Der Weg ist am kürzesten.", "grup içindeki en kısa seçeneği gösteriyor."),
                    ("Dieses Zimmer ist am ruhigsten.", "birden fazla seçenek arasında zirve belirleniyor."),
                ],
            ),
            _g(
                "als ile kıyas",
                "Komparativ çoğu zaman als ile ikinci öğeye bağlanır.",
                "İki şehri, iki kişiyi, iki ürünü veya iki planı açık karşılaştırmada kullanılır.",
                "komparativ + als + ikinci öge",
                "als, kıyasın ikinci ayağını görünür hale getirir. Böylece cümle yalnız yargı değil, açık karşılaştırma olur.",
                "wie ile als karışabilir; ama bu derste odak açık fark ve üstünlük anlattığı için als kullanılır.",
                [
                    ("Mein Zimmer ist größer als dein Zimmer.", "sahiplik ve kıyas aynı cümlede birleşiyor."),
                    ("Der Kaffee hier ist besser als dort.", "kalite kıyası yapılır."),
                ],
            ),
            _g(
                "Düzensiz biçimler: besser, lieber, mehr",
                "Bazı yüksek frekanslı sıfat ve zarflar düzenli ek alma yolunu izlemez.",
                "Tercih, kalite ve miktar karşılaştırmasında kullanılır.",
                "gut -> besser / gern -> lieber / viel -> mehr",
                "Bu biçimler o kadar sık kullanılır ki kuraldan sapma olmalarına rağmen blok olarak çok erken yerleşmelidir.",
                "guter ya da vieler gibi kural dışı biçimler üretmeye çalışma; düzensiz formları ayrı ezberlemek gerekir.",
                [
                    ("Dieses Essen ist besser.", "gut yerine besser geliyor."),
                    ("Ich fahre lieber mit dem Zug.", "tercih bildirirken gern'in komparativi kullanılıyor."),
                ],
            ),
        ],
        [
            _p("Berlin ist größer als Bonn.", "Berlin Bonn'dan daha büyük.", "şehir kıyası"),
            _p("Dieses Hotel ist billiger als das andere.", "Bu otel diğerinden daha ucuz.", "hizmet kıyası"),
            _p("Welcher Weg ist am kürzesten?", "Hangi yol en kısa?", "superlativ sorusu"),
            _p("Der Kaffee hier ist besser.", "Buradaki kahve daha iyi.", "düzensiz sıfat"),
            _p("Ich fahre lieber mit dem Zug.", "Trenle gitmeyi tercih ederim.", "gern -> lieber"),
            _p("Diese Wohnung ist am teuersten.", "Bu ev en pahalı.", "fiyat süperlativi"),
            _p("Der Park ist näher als die Schule.", "Park okuldan daha yakın.", "yakınlık kıyası"),
            _p("Heute habe ich mehr Zeit.", "Bugün daha fazla vaktim var.", "miktar kıyası"),
            _p("Das ist für mich am besten.", "Bu benim için en iyisi.", "karar verme"),
            _p("Unser Zimmer ist ruhiger als das andere.", "Odamız diğerinden daha sakin.", "otel ve değerlendirme dili"),
        ],
        [
            _m("Berlin ist mehr groß als Bonn.", "Berlin ist größer als Bonn.", "komparativ için sıfatın komparativ biçimi gerekir."),
            _m("Dieses Hotel ist billiger wie das andere.", "Dieses Hotel ist billiger als das andere.", "karşılaştırma kalıbında als kullanılır."),
            _m("Das ist am besser.", "Das ist am besten.", "gut düzensizdir; superlativte besten olur."),
            _m("Ich fahre gern als du.", "Ich fahre lieber als du.", "gern'in komparativi lieber biçimidir."),
        ],
        {
            "title": "İki seçenek arasında karar",
            "lines": [
                _line("A", "Welches Hotel ist besser?", "Hangi otel daha iyi?"),
                _line("B", "Das Hotel am Bahnhof ist billiger, aber das Hotel im Zentrum ist ruhiger.", "İstasyonun yanındaki otel daha ucuz ama merkezdeki otel daha sakin."),
                _line("A", "Und welches ist für dich am besten?", "Peki sence hangisi en iyisi?"),
                _line("B", "Für mich ist das ruhigere Hotel am besten.", "Bence daha sakin otel en iyisi."),
            ],
        },
        [
            _passage(
                "Hangisi daha iyi?",
                "Okumada komparativ ve superlativ biçimlerini tek tek işaretle. A2'de bu yapıların ritmini duymak önemlidir.",
                [
                    "[[Emre::erkek adı]] iki [[Hotel::otel]] arasında karar veriyor. Das erste Hotel ist [[billiger::daha ucuz]], aber das zweite Hotel ist [[ruhiger::daha sakin]] und liegt [[näher::daha yakın]] am Zentrum.",
                    "Am Ende sagt er: Für mich ist das zweite Hotel [[am besten::en iyi]]. Es ist nicht am [[günstigsten::en ucuz]], aber es passt besser zu meinem [[Plan::plan]].",
                ],
            )
        ],
        [
            "Sıfatları pozitif, komparativ ve superlativ olarak küçük üçlü kartlarda çalış.",
            "als ile ikinci öğeyi yüksek sesle söylemek yapıyı oturtur.",
            "besser, lieber, mehr gibi düzensizleri ayrı liste yap.",
            "Karar cümlesi kurarken fiyat, mesafe ve kalite kelimelerini birlikte kullanmayı dene.",
        ],
        [
            _v("das Hotel", "das", "die Hotels", ["otel"], "Das Hotel ist ruhig.", "Otel sakin.", "karşılaştırma örneklerinin ana nesnesi."),
            _v("die Stadt", "die", "die Städte", ["şehir"], "Die Stadt ist groß.", "Şehir büyük.", "şehir kıyası için temel isim."),
            _v("der Weg", "der", "die Wege", ["yol"], "Der Weg ist kurz.", "Yol kısa.", "en kısa yol gibi kalıplarda geçer."),
            _v("der Preis", "der", "die Preise", ["fiyat"], "Der Preis ist hoch.", "Fiyat yüksek.", "ucuz-pahalı kıyasının merkez ismidir."),
            _v("das Zimmer", "das", "die Zimmer", ["oda"], "Das Zimmer ist ruhig.", "Oda sakin.", "otel değerlendirmelerinde kullanılır."),
            _v("die Wohnung", "die", "die Wohnungen", ["ev", "daire"], "Die Wohnung ist modern.", "Daire modern.", "yerleşim bağlamında kıyas"),
            _v("der Film", "der", "die Filme", ["film"], "Der Film ist interessant.", "Film ilginç.", "soyut kıyas örneği sağlar."),
            _v("die Aufgabe", "die", "die Aufgaben", ["görev", "ödev"], "Die Aufgabe ist schwer.", "Görev zor.", "kolay-zor kıyası kurar."),
            _v("groß", "-", "-", ["büyük"], "Berlin ist groß.", "Berlin büyük.", "temel düzenli sıfat."),
            _v("klein", "-", "-", ["küçük"], "Bonn ist klein.", "Bonn küçük.", "komparative kolay girer."),
            _v("teuer", "-", "-", ["pahalı"], "Das Zimmer ist teuer.", "Oda pahalı.", "otel ve alışveriş kıyası."),
            _v("günstig", "-", "-", ["uygun fiyatlı"], "Der Preis ist günstig.", "Fiyat uygun.", "billiger alanına bağlanır."),
            _v("schnell", "-", "-", ["hızlı"], "Der Zug ist schnell.", "Tren hızlı.", "ulaşım kıyası."),
            _v("langsam", "-", "-", ["yavaş"], "Der Bus ist langsam.", "Otobüs yavaş.", "karşıt sıfat."),
            _v("besser", "-", "-", ["daha iyi"], "Der Kaffee ist besser.", "Kahve daha iyi.", "gut'un düzensiz komparativi."),
            _v("lieber", "-", "-", ["tercihen"], "Ich fahre lieber mit dem Zug.", "Trenle gitmeyi tercih ederim.", "gern'in komparativi."),
            _v("mehr", "-", "-", ["daha fazla"], "Ich habe mehr Zeit.", "Daha fazla vaktim var.", "miktar kıyası."),
            _v("am besten", "-", "-", ["en iyi"], "Das ist am besten.", "Bu en iyisi.", "superlativ kararı."),
        ],
        "Bu derste yalnız 'iyi' demekten çıkıp 'daha iyi' ve 'en iyi' demeye geçiyorsun. Karşılaştırma dili açıldığında A2 konuşması ciddi biçimde zenginleşir.",
    ),
    _lesson(
        10,
        "ders-10-passive-giris-vorgang-und-zustand",
        "Passiv'e Giriş: Vorgang ve Zustand",
        "A2.2",
        "Bu ders A2'nin üst ucunda duran bir başlık. Ama öğretmen akışına sadık kalarak olayın kendisini vurgulayan pasif ile sonucun durumunu vurgulayan pasif arasındaki farkı temiz bir giriş olarak kuruyoruz.",
        [
            "Vorgangspassiv ve Zustandspassiv farkını sezmek.",
            "werden + Partizip II ile olay merkezli pasif kurmak.",
            "sein + Partizip II ile sonuç/durum merkezli yapı kurmak.",
            "Kapı açılıyor / kapı açık gibi farkları okumak.",
            "Kısa ve kontrollü pasif cümlelerle nesne merkezli anlatı kurmak.",
            "A2 sonunda pasifi tanıyıp temel örneklerde kullanabilmek.",
        ],
        "werden / sein + Partizip II",
        [
            {"eyebrow": "1. Adım", "title": "Bazen işi yapan kişi değil, olan şey önemlidir", "body": "Pasif yapı, odak noktasını yapan kişiden olaya veya sonuca kaydırır. Özellikle ilan, açıklama ve süreç anlatılarında bunun izini çok görürüz."},
            {"eyebrow": "2. Adım", "title": "Vorgangspassiv olayın akışını anlatır", "body": "Kapı açılıyor, ödev yapılıyor, havuz kapatılıyor gibi cümlelerde eylemin gerçekleşme süreci öne çıkar."},
            {"eyebrow": "3. Adım", "title": "Zustandspassiv sonuçta ortaya çıkan durumu gösterir", "body": "Kapı açık, ödev yapılmış durumda, havuz kapalı gibi yapılarda artık süreçten çok sonucun kendisi görünür hale gelir."},
        ],
        [
            _g(
                "Vorgangspassiv",
                "Olayın gerçekleşmesini veya süreci vurgular.",
                "Bir işin yapıldığını ama yapan kişinin önemli olmadığını anlatırken kullanılır.",
                "werden + Partizip II",
                "Bu yapı eylemi süreç olarak gösterir. A2 için asıl hedef, böyle cümleleri görünce tanıyabilmek ve birkaç basit örneği kendin kurabilmektir.",
                "werden fiilini gelecek zamanla karıştırmamaya dikkat et; burada gelecek değil, pasif süreç kuruluyor.",
                [
                    ("Das Fenster wird geöffnet.", "Odak pencereyi açan kişi değil, açılma sürecidir."),
                    ("Die Hausaufgaben werden gemacht.", "yapan kişi siliniyor, süreç öne geliyor."),
                ],
            ),
            _g(
                "Zustandspassiv",
                "Bir eylemin sonucunda oluşan durumu vurgular.",
                "Bir şeyin yapılmış durumda olduğunu veya sonucunun geçerli olduğunu anlatırken kullanılır.",
                "sein + Partizip II",
                "Bu yapıda süreç değil, son durum önemlidir. Bu yüzden çoğu zaman görünüşte sıfat cümlesine yaklaşır.",
                "Vorgang ile Zustand arasındaki farkı yalnız çeviriyle değil, odak noktasıyla ayırmak gerekir: işlem mi, sonuç mu?",
                [
                    ("Das Fenster ist geöffnet.", "Burada pencerenin açılmış durumda olduğu vurgulanıyor."),
                    ("Das Schwimmbad ist geschlossen.", "kapanma eyleminden çok mevcut kapalı durum anlatılıyor."),
                ],
            ),
            _g(
                "werden mi sein mi?",
                "Aynı Partizip II, werden ile süreç; sein ile sonuç anlatabilir.",
                "İşlem ve durum farkını ayırmak gerektiğinde kullanılır.",
                "werden + Partizip II / sein + Partizip II",
                "Bu iki yapı yan yana görülünce pasif mantığı bir anda netleşir. Aynı kelime farklı yardımcı fiille farklı bakış açısı kurar.",
                "Yalnız Partizip II'ye bakarak karar verme; asıl fark yardımcı fiilde ve cümlenin odak merkezindedir.",
                [
                    ("Die Tür wird geschlossen.", "Kapanma işlemi oluyor."),
                    ("Die Tür ist geschlossen.", "Kapının şu an kapalı olduğu söyleniyor."),
                ],
            ),
            _g(
                "Basit pasif cümleler",
                "A2 seviyesinde pasif kullanımı kısa, açık ve yüksek frekanslı örneklerde tutulmalıdır.",
                "Kapı, ödev, paket, yol, bina gibi somut konularda pasifi tanımak ve denemek için kullanılır.",
                "nesne + werden/sein + Partizip II",
                "Amaç bu derste pasifin tüm zamanlarını öğrenmek değil; ana iki bakış açısını temiz örneklerle görmek.",
                "Fazla uzun nesne veya karmaşık yan cümlelerle başlamak pasifin ana mantığını görünmez hale getirebilir.",
                [
                    ("Das Paket wird heute verschickt.", "süreç odaklı pasif örneği."),
                    ("Die Straße ist gesperrt.", "sonuç/durum odaklı kısa örnek."),
                ],
            ),
        ],
        [
            _p("Das Fenster wird geöffnet.", "Pencere açılıyor.", "olay odaklı pasif"),
            _p("Das Fenster ist geöffnet.", "Pencere açık.", "durum odaklı pasif"),
            _p("Die Hausaufgaben werden gemacht.", "Ödevler yapılıyor.", "süreç anlatımı"),
            _p("Die Straße ist gesperrt.", "Yol kapalı.", "mevcut sonuç"),
            _p("Das Paket wird heute verschickt.", "Paket bugün gönderiliyor.", "işlem vurgusu"),
            _p("Der Vertrag ist unterschrieben.", "Sözleşme imzalanmış durumda.", "tamamlanmış sonuç"),
            _p("Die Tür wird repariert.", "Kapı tamir ediliyor.", "süreç örneği"),
            _p("Das Schwimmbad ist geschlossen.", "Yüzme havuzu kapalı.", "durum örneği"),
            _p("Die E-Mail wird sofort beantwortet.", "E-posta hemen cevaplanıyor.", "iş akışı dili"),
            _p("Das Zimmer ist schon vorbereitet.", "Oda çoktan hazırlanmış durumda.", "hazır olma durumu"),
        ],
        [
            _m("Das Fenster ist geöffnet. (işlem anlatmak isterken)", "Das Fenster wird geöffnet.", "süreç için werden gerekir."),
            _m("Die Tür wird geschlossen. (mevcut durumu anlatmak isterken)", "Die Tür ist geschlossen.", "sonuç/durum için sein gerekir."),
            _m("Das Paket wird verschicken.", "Das Paket wird verschickt.", "pasifte mastar değil Partizip II gerekir."),
            _m("Die Rechnung ist machen.", "Die Rechnung ist gemacht.", "sein ile birlikte Partizip II'nin doğru biçimi gerekir."),
        ],
        {
            "title": "Ne oluyor, ne olmuş durumda?",
            "lines": [
                _line("A", "Warum warten alle hier?", "Neden herkes burada bekliyor?"),
                _line("B", "Die Tür wird repariert.", "Kapı tamir ediliyor."),
                _line("A", "Und ist das Büro schon geöffnet?", "Peki ofis açılmış durumda mı?"),
                _line("B", "Nein, es ist noch geschlossen.", "Hayır, hâlâ kapalı."),
            ],
        },
        [
            _passage(
                "Ofiste küçük duyuru",
                "Burada aynı bağlamda hem süreç hem sonuç pasifi birlikte görüyorsun. Farkı yalnız yardımcı fiilden bile okuyabilmelisin.",
                [
                    "Heute wird das [[Büro::ofis]] früh [[geöffnet::açılıyor]]. Die neuen [[Dokumente::belgeler]] werden am Vormittag [[verschickt::gönderiliyor]].",
                    "Das kleine [[Zimmer::oda]] ist schon [[vorbereitet::hazırlanmış]]. Aber die [[Tür::kapı]] ist noch [[geschlossen::kapalı]].",
                ],
            )
        ],
        [
            "Pasifi öğrenirken önce yapan kişiyi unutup nesneye odaklan.",
            "werden ve sein farkını her örnekte yüksek sesle söylemek çok işe yarar.",
            "Süreç mi sonuç mu sorusunu her pasif cümlede kendine sor.",
            "Bu dersi ileri gramer korkusu olmadan, kısa örneklerle çalışmak daha doğrudur.",
        ],
        [
            _v("das Fenster", "das", "die Fenster", ["pencere"], "Das Fenster ist offen.", "Pencere açık.", "pasif örneklerinde sık geçen nesne."),
            _v("die Tür", "die", "die Türen", ["kapı"], "Die Tür ist neu.", "Kapı yeni.", "süreç-sonuç farkını iyi gösterir."),
            _v("die Hausaufgabe", "die", "die Hausaufgaben", ["ödev"], "Die Hausaufgabe ist fertig.", "Ödev hazır.", "yapılıyor / yapılmış örneği."),
            _v("das Schwimmbad", "das", "die Schwimmbäder", ["yüzme havuzu"], "Das Schwimmbad ist groß.", "Yüzme havuzu büyük.", "kapalı/açık durumu için uygundur."),
            _v("die Straße", "die", "die Straßen", ["yol", "cadde"], "Die Straße ist lang.", "Yol uzun.", "kapalı olma örneği kurulabilir."),
            _v("der Vertrag", "der", "die Verträge", ["sözleşme"], "Der Vertrag ist wichtig.", "Sözleşme önemli.", "imzalanma örneği."),
            _v("die E-Mail", "die", "die E-Mails", ["e-posta"], "Die E-Mail ist kurz.", "E-posta kısa.", "iş akışı örnekleri."),
            _v("das Paket", "das", "die Pakete", ["paket"], "Das Paket ist da.", "Paket burada.", "gönderme pasifi için tipik nesne."),
            _v("die Rechnung", "die", "die Rechnungen", ["fatura", "hesap"], "Die Rechnung ist fertig.", "Fatura hazır.", "yapılmış sonuç dili."),
            _v("der Termin", "der", "die Termine", ["randevu"], "Der Termin ist bestätigt.", "Randevu onaylandı.", "durum pasifine yaklaşır."),
            _v("geöffnet", "-", "-", ["açılmış", "açılıyor bağlamına yakın"], "Die Tür ist geöffnet.", "Kapı açık.", "durum pasifi çekirdeği."),
            _v("geschlossen", "-", "-", ["kapalı", "kapatılmış"], "Das Schwimmbad ist geschlossen.", "Havuz kapalı.", "sonuç vurgusu."),
            _v("repariert", "-", "-", ["tamir ediliyor", "tamir edilmiş"], "Die Tür wird repariert.", "Kapı tamir ediliyor.", "süreç vurgusu."),
            _v("unterschrieben", "-", "-", ["imzalanmış"], "Der Vertrag ist unterschrieben.", "Sözleşme imzalanmış.", "tamamlanmış sonuç."),
            _v("verschickt", "-", "-", ["gönderiliyor", "gönderilmiş"], "Das Paket wird heute verschickt.", "Paket bugün gönderiliyor.", "işlem pasifi örneği."),
            _v("gebaut", "-", "-", ["inşa edilmiş"], "Das Haus wird neu gebaut.", "Ev yeniden inşa ediliyor.", "süreç odaklı pasif."),
            _v("gemacht", "-", "-", ["yapılmış"], "Die Hausaufgaben sind gemacht.", "Ödevler yapılmış durumda.", "sonuç odaklı örnek."),
            _v("kontrolliert", "-", "-", ["kontrol ediliyor", "kontrol edilmiş"], "Die Dokumente werden kontrolliert.", "Belgeler kontrol ediliyor.", "kurumsal süreç örneği."),
        ],
        "Pasifi burada mükemmel öğrenmek gerekmiyor. Ama bir cümlede süreç mi vurgulanıyor, sonuç mu vurgulanıyor ayrımını görmeye başladıysan bu ders görevini yaptı.",
    ),
    _lesson(
        11,
        "ders-11-otel-dili-ve-kisalmis-edatli-yapilar",
        "Otel Dili ve Kısalmış Edatlı Yapılar",
        "A2.2",
        "Bu derste im, am, zum, vom gibi sık birleşen yapılara ve otel bağlamına giriyoruz. Rezervasyon, resepsiyon ve şehir içi hizmet dili burada birleşiyor.",
        [
            "im, am, zum, vom gibi sık birleşen kalıpları tanımak.",
            "Otel ve resepsiyon dilinde temel soruları kurmak.",
            "Rezervasyon, anahtar, kahvaltı ve çıkış işlemi gibi temel ihtiyaçları anlatmak.",
            "Bir yerden gelmek ve bir yere gitmek kalıplarını bağlam içinde kullanmak.",
            "Kısa hizmet diyaloglarında daha akıcı cümleler kurmak.",
            "A2 seyahat dilinin çekirdeğini oluşturmak.",
        ],
        "otel + im/am/zum/vom",
        [
            {"eyebrow": "1. Adım", "title": "Bazı edat-artikel birleşimleri çok sık kalıp halindedir", "body": "im, am, zum, vom gibi yapılar ders kitabı dışında gerçek hayatta da sürekli görünür. Bu yüzden ayrı ayrı çözmek yerine kalıp halinde duymak gerekir."},
            {"eyebrow": "2. Adım", "title": "Otel dili küçük ama işlevsel bir alandır", "body": "Rezervasyon var mı, anahtar hazır mı, kahvaltı ne zaman, odada internet var mı gibi cümleler A2 için çok gerçek iletişim görevleridir."},
            {"eyebrow": "3. Adım", "title": "Yer ve hizmet dili birlikte akar", "body": "Otel konuşması çoğu zaman yalnız oda değil; istasyon, havaalanı, resepsiyon ve şehir merkezi gibi mekânlara da bağlanır."},
        ],
        [
            _g(
                "im, am, zum, vom",
                "Bazı edatlar belirli artikel ile çok sık birleşerek kısa kalıplar oluşturur.",
                "Yer, zaman veya yönelme anlatan günlük cümlelerde çok sık kullanılır.",
                "in dem = im / an dem = am / zu dem = zum / von dem = vom",
                "Bu birleşimler doğallığın parçasıdır. Ayrı ayrı söylemek her zaman imkânsız değildir ama konuşma ve yazıda kısalmış biçim çok daha yaygındır.",
                "Kısalmış biçimi gördüğünde anlamı kaybetme; hangi edat ve hangi artikeli içinde taşıdığını fark etmek gerekir.",
                [
                    ("Wir bleiben im Hotel.", "in dem yapısı doğal olarak im biçimine kısalıyor."),
                    ("Ich warte am Bahnhof.", "an dem yerine am kullanılıyor."),
                ],
            ),
            _g(
                "Otelde temel soru cümleleri",
                "Otel dili çoğu zaman rezervasyon, anahtar, kahvaltı ve hizmet sorularıyla ilerler.",
                "Check-in, bilgi alma veya hizmet isteme bağlamında kullanılır.",
                "Haben Sie ...? / Ist ...? / Wann ist ...?",
                "Otel konuşması güvenli sabit sorularla yürür. A2'de bunları blok olarak bilmek, gerçek seyahat iletişimini büyük ölçüde çözer.",
                "Aşırı uzun ve dolambaçlı cümle kurmaya çalışma; hizmet dilinde netlik çoğu zaman daha doğaldır.",
                [
                    ("Haben Sie eine Reservierung für mich?", "check-in açılışını verir."),
                    ("Wann ist das Frühstück?", "zaman bilgisi sormaya yarar."),
                ],
            ),
            _g(
                "Yer kaynağı ve çıkış noktası",
                "aus dem Hotel, vom Bahnhof gibi yapılar bir yerden çıkış veya kaynak bildirir.",
                "Bir yerden geldiğini veya bir hizmet noktasından çıktığını anlatırken kullanılır.",
                "aus dem ... / vom ...",
                "Seyahat dili yalnız nereye gittiğini değil, nereden geldiğini de taşır. Bu yüzden kaynak yapıları da A2'de netleşmelidir.",
                "aus ile von/vom farkını bağlama göre dinlemek gerekir; hepsi aynı çıkış ilişkisini kurmaz.",
                [
                    ("Ich komme aus dem Hotel.", "iç mekândan çıkış anlatılıyor."),
                    ("Er kommt vom Bahnhof.", "daha noktasal bir yerden geliş hissi veriyor."),
                ],
            ),
            _g(
                "Hizmet rica cümleleri",
                "Otelde ek battaniye, internet bilgisi veya geç çıkış gibi istekler için yumuşak hizmet dili gerekir.",
                "Resepsiyonda yardım istemek veya odadaki bir ihtiyaçtan söz etmek istediğinde kullanılır.",
                "Könnten Sie ...? / Ich brauche ...",
                "Bu ders, önceki yumuşak rica kalıplarını somut seyahat bağlamına taşır. Böylece Almanca artık doğrudan işe yarayan alana bağlanır.",
                "Yalnız isim saymak yerine küçük rica cümlesi kurmak iletişim başarısını çok yükseltir.",
                [
                    ("Könnten Sie mir den Schlüssel geben?", "resepsiyonda doğal yardım isteği."),
                    ("Ich brauche ein ruhiges Zimmer.", "istek ve değerlendirme dili birleşiyor."),
                ],
            ),
        ],
        [
            _p("Wir bleiben im Hotel am Bahnhof.", "İstasyonun yanındaki otelde kalıyoruz.", "kısalmış edatlı yer kalıbı"),
            _p("Ich komme gerade vom Flughafen.", "Az önce havaalanından geliyorum.", "çıkış noktası"),
            _p("Haben Sie eine Reservierung für mich?", "Benim için bir rezervasyonunuz var mı?", "check-in sorusu"),
            _p("Wann ist das Frühstück im Hotel?", "Otelde kahvaltı ne zaman?", "zaman sorusu"),
            _p("Könnten Sie mir den Schlüssel geben?", "Bana anahtarı verebilir misiniz?", "resepsiyon rica kalıbı"),
            _p("Ich brauche ein ruhiges Zimmer.", "Sessiz bir odaya ihtiyacım var.", "oda tercihi"),
            _p("Der Bus fährt zum Zentrum.", "Otobüs merkeze gidiyor.", "zum kullanımı"),
            _p("Am Morgen gehe ich zur Rezeption.", "Sabah resepsiyona gidiyorum.", "zaman ve yönelme kalıbı"),
            _p("Vom Hotel ist der Bahnhof nicht weit.", "Otelden istasyon uzak değil.", "yer ilişkisi"),
            _p("Ist WLAN im Zimmer inklusive?", "Odada internet dahil mi?", "otel hizmet dili"),
        ],
        [
            _m("Wir bleiben in dem Hotel. (her zaman ayrı söylemek)", "Wir bleiben im Hotel.", "kısalmış biçim daha doğal ve daha yaygındır."),
            _m("Ich komme von dem Bahnhof.", "Ich komme vom Bahnhof.", "vom biçimi yüksek frekansta kısa kalıptır."),
            _m("Wann Frühstück ist?", "Wann ist das Frühstück?", "soru cümlesinde çekimli fiil ikinci yerde kalır."),
            _m("Ich brauche ruhiges Zimmer.", "Ich brauche ein ruhiges Zimmer.", "isim grubu artikel ve sıfatla birlikte kurulmalıdır."),
        ],
        {
            "title": "Resepsiyonda kısa konuşma",
            "lines": [
                _line("Misafir", "Guten Tag. Ich habe eine Reservierung.", "İyi günler. Bir rezervasyonum var."),
                _line("Görevli", "Natürlich. Könnten Sie mir bitte Ihren Namen sagen?", "Elbette. Bana adınızı söyler misiniz?"),
                _line("Misafir", "Ja. Und ich hätte gern ein ruhiges Zimmer.", "Evet. Ve sessiz bir oda rica ederim."),
                _line("Görevli", "Kein Problem. Das Zimmer ist im dritten Stock.", "Sorun değil. Oda üçüncü katta."),
            ],
        },
        [
            _passage(
                "Şehre varış",
                "Bu okumada otel ve hareket dili birleşiyor. Kısalmış yapıları ayrı kelime değil, hazır kalıp olarak okumaya çalış.",
                [
                    "[[Selin::kadın adı]] kommt heute [[vom Flughafen::havaalanından]] und bleibt zwei Nächte [[im Hotel::otelde]]. Das [[Hotel::otel]] liegt nicht weit [[am Bahnhof::istasyon yanında]].",
                    "Am Abend geht sie [[zur Rezeption::resepsiyona]] und fragt nach dem [[Frühstück::kahvaltı]] und dem [[Schlüssel::anahtar]]. Danach ruht sie sich im [[Zimmer::oda]] aus.",
                ],
            )
        ],
        [
            "Kısalmış edatlı yapıları küçük kartlar halinde ezberlemek çok verimlidir: im, am, zum, vom.",
            "Otel dili için 8-10 sabit soru kalıbı büyük pratik avantaj sağlar.",
            "Resepsiyon konuşmasını yüksek sesle rol oyunu gibi tekrar et.",
            "Yer ve hizmet cümlelerini birleştir; seyahat dili tek başlıkta değil, akış içinde öğrenilir.",
        ],
        [
            _v("das Hotel", "das", "die Hotels", ["otel"], "Das Hotel ist modern.", "Otel modern.", "seyahat ve hizmet bağlamının ana ismidir."),
            _v("die Rezeption", "die", "die Rezeptionen", ["resepsiyon"], "Die Rezeption ist dort.", "Resepsiyon orada.", "otel hizmet merkezi."),
            _v("das Zimmer", "das", "die Zimmer", ["oda"], "Das Zimmer ist ruhig.", "Oda sakin.", "otel tercihleri için temel kelime."),
            _v("der Schlüssel", "der", "die Schlüssel", ["anahtar"], "Der Schlüssel ist hier.", "Anahtar burada.", "resepsiyon diyaloğunun doğal nesnesi."),
            _v("das Frühstück", "das", "die Frühstücke", ["kahvaltı"], "Das Frühstück ist früh.", "Kahvaltı erken.", "otel rutin diline bağlanır."),
            _v("der Koffer", "der", "die Koffer", ["bavul"], "Der Koffer ist schwer.", "Bavul ağır.", "seyahat kelimesi."),
            _v("der Bahnhof", "der", "die Bahnhöfe", ["istasyon", "gar"], "Der Bahnhof ist nah.", "İstasyon yakın.", "am/vom bağlamı kurar."),
            _v("der Flughafen", "der", "die Flughäfen", ["havaalanı"], "Der Flughafen ist groß.", "Havaalanı büyük.", "seyahat başlangıç noktası."),
            _v("die Reservierung", "die", "die Reservierungen", ["rezervasyon"], "Die Reservierung ist bestätigt.", "Rezervasyon onaylandı.", "check-in dili."),
            _v("die Quittung", "die", "die Quittungen", ["fiş", "makbuz"], "Die Quittung ist da.", "Makbuz burada.", "ödeme ve kapanış diline bağlanır."),
            _v("im", "-", "-", ["-de / içinde"], "Wir bleiben im Hotel.", "Otelde kalıyoruz.", "in dem kısalması."),
            _v("am", "-", "-", ["-de / yanında"], "Das Hotel ist am Bahnhof.", "Otel istasyonun yanında.", "an dem kısalması."),
            _v("zum", "-", "-", ["-e / doğru"], "Wir fahren zum Zentrum.", "Merkeze gidiyoruz.", "zu dem kısalması."),
            _v("vom", "-", "-", ["-den / -dan"], "Ich komme vom Flughafen.", "Havaalanından geliyorum.", "von dem kısalması."),
            _v("aus dem", "-", "-", ["içinden / -den"], "Ich komme aus dem Hotel.", "Otelden geliyorum.", "iç mekân çıkışı"),
            _v("ruhig", "-", "-", ["sakin"], "Das Zimmer ist ruhig.", "Oda sakin.", "oda tercihi kurar."),
            _v("inklusive", "-", "-", ["dahil"], "Das Frühstück ist inklusive.", "Kahvaltı dahil.", "hizmet sorularında geçer."),
            _v("Stock", "der", "die Stockwerke", ["kat"], "Das Zimmer ist im dritten Stock.", "Oda üçüncü katta.", "konum detayını büyütür."),
        ],
        "Bu ders A2'yi doğrudan günlük seyahat becerisine bağlar. Kısalmış yapıları ve otel kalıplarını rahat kullanabiliyorsan pratik Almanca tarafı ciddi biçimde güçlenmiş olur.",
    ),
    _lesson(
        12,
        "ders-12-nach-zu-in-ve-auf-ile-hareket",
        "nach, zu, in ve auf ile Hareket",
        "A2.2",
        "Yer anlatımından sonra şimdi hareket anlatımını netleştiriyoruz. Nereye gidildiğini söylerken hangi edatın seçileceği A2'de çok kritik bir ayrım haline gelir.",
        [
            "Wohin? sorusunu anlamak ve cevaplamak.",
            "nach, zu, in, auf ile temel hareket kalıplarını ayırmak.",
            "Şehir içinde yön tarifi verirken links, rechts, geradeaus ve abbiegen kullanmak.",
            "Araç, hedef ve rota bilgisini bir araya getirmek.",
            "nach Hause / zu Hause farkını görmek.",
            "A2 düzeyinde küçük yön tariflerini yönetebilmek.",
        ],
        "Wohin? + hareket edatları",
        [
            {"eyebrow": "1. Adım", "title": "Wo ile Wohin aynı şey değildir", "body": "Wo mevcut konumu, Wohin ise hareketin yöneldiği hedefi sorar. Bu fark A2'de yer cümlesi ile hareket cümlesini net ayırır."},
            {"eyebrow": "2. Adım", "title": "nach, zu, in, auf farklı hedef türlerine gider", "body": "Şehir, ülke, kurum, kapalı mekân ve açık etkinlik alanları aynı yapıyla kurulmaz. Doğru edatı hedefin türü belirler."},
            {"eyebrow": "3. Adım", "title": "Yön tarifi küçük komutlarla büyür", "body": "geradeaus, links, rechts, dann, an der Ampel gibi ifadeler şehirde yol sormayı A2 seviyesine taşır."},
        ],
        [
            _g(
                "Wohin? sorusu",
                "Wohin? bir hareketin hedef yönünü sorar.",
                "Birinin nereye gittiğini, yöneldiğini veya taşındığını sorarken kullanılır.",
                "Wohin + hareket fiili?",
                "Yer bilgisini artık yalnız sabit konum olarak değil, hareketin hedefi olarak da kurman gerekir. Bu ayrım A2 için temel bir kırılma noktasıdır.",
                "Wo / Wohin karışırsa edat seçimi de bozulur; önce sorunun ne istediğini netleştir.",
                [
                    ("Wohin gehst du?", "hedef yön soruluyor."),
                    ("Wohin fährt der Bus?", "araç hareketi de aynı mantıkla soruluyor."),
                ],
            ),
            _g(
                "nach, zu, in, auf farkı",
                "Hedefe göre farklı hareket edatları kullanılır.",
                "Şehre, ülkeye, kuruma, eve, etkinliğe veya kapalı mekâna gitmeyi anlatırken kullanılır.",
                "nach + şehir/ülke / zu + kişi/kurum / in + kapalı alan / auf + etkinlik/alan",
                "A2'nin en sık karışan konularından biri budur. Tek bir Türkçe 'gitmek' fiili Almancada farklı hedef tiplerine göre farklı yapılar çağırır.",
                "Her yeri in ile anlatmaya çalışma. Hedefin niteliğini tanımak, doğru edatı seçmenin anahtarıdır.",
                [
                    ("Wir fahren nach Hamburg.", "şehir adıyla nach kullanılıyor."),
                    ("Ich gehe zur Bank.", "kuruma yönelmede zu yapısı öne çıkıyor."),
                    ("Sie geht in die Apotheke.", "kapalı mekâna giriş hedefi var."),
                ],
            ),
            _g(
                "nach Hause ve zu Hause",
                "Aynı 'ev' kavramı, hareket ve sabit konumda farklı yapılarla kurulur.",
                "Eve doğru gitmek ile evde bulunmak arasındaki farkı anlatırken kullanılır.",
                "nach Hause / zu Hause",
                "Bu küçük çift A2'de çok yüksek frekanslıdır. Hareket ve konum ayrımını tek örnek içinde çok net gösterir.",
                "nach Hause derken edatlı artikel arama; bu yapı sabit kalıp olarak çalışır.",
                [
                    ("Ich gehe jetzt nach Hause.", "hareket ve yön var."),
                    ("Am Abend bin ich zu Hause.", "sabit bulunma durumu var."),
                ],
            ),
            _g(
                "Yön tarifi için mini komutlar",
                "Şehirde yol gösterirken kısa yön sözleri ve hareket fiilleri birlikte çalışır.",
                "Birine yol tarif ederken veya navigasyon benzeri kısa cümleler kurarken kullanılır.",
                "geradeaus / links / rechts / dann + hareket fiili",
                "A2 iletişimi burada soyuttan somuta geçer. Çok kısa komutlarla bile işlevsel bir yön tarifi verebilmek mümkündür.",
                "Yön sözlerini yalnız tek kelime bırakmak yerine küçük bir fiille bağlamak daha anlaşılır olur.",
                [
                    ("Gehen Sie zuerst geradeaus.", "rota başlangıcını kurar."),
                    ("Dann biegen Sie links ab.", "dönüş noktasını netleştirir."),
                ],
            ),
        ],
        [
            _p("Wohin gehst du jetzt?", "Şimdi nereye gidiyorsun?", "yön sorusu"),
            _p("Ich gehe zur Bank.", "Bankaya gidiyorum.", "kuruma yönelme"),
            _p("Wir fahren nach Hamburg.", "Hamburg'a gidiyoruz.", "şehir adıyla hareket"),
            _p("Sie geht in die Apotheke.", "Eczaneye gidiyor.", "kapalı mekâna giriş"),
            _p("Am Abend gehe ich nach Hause.", "Akşam eve gidiyorum.", "hareket ve ev kalıbı"),
            _p("Jetzt bin ich zu Hause.", "Şimdi evdeyim.", "konum ve ev kalıbı"),
            _p("Gehen Sie zuerst geradeaus.", "Önce dümdüz gidin.", "yön tarifi başlangıcı"),
            _p("Dann biegen Sie rechts ab.", "Sonra sağa dönün.", "dönüş komutu"),
            _p("Die Apotheke ist neben der Bank.", "Eczane bankanın yanında.", "rota hedefi doğrulama"),
            _p("Der Bus fährt zum Zentrum.", "Otobüs merkeze gidiyor.", "araç ve yön bir arada"),
        ],
        [
            _m("Wo gehst du?", "Wohin gehst du?", "hareket hedefi soruluyorsa Wohin gerekir."),
            _m("Ich fahre in Hamburg.", "Ich fahre nach Hamburg.", "şehir adlarıyla hareket için çoğu zaman nach kullanılır."),
            _m("Ich bin nach Hause.", "Ich bin zu Hause.", "sabit konumda nach Hause değil zu Hause kullanılır."),
            _m("Dann Sie biegen links ab.", "Dann biegen Sie links ab.", "yön komutunda çekimli fiil öne alınır."),
        ],
        {
            "title": "Şehirde yol sorma",
            "lines": [
                _line("A", "Entschuldigung, wo ist die Apotheke?", "Affedersiniz, eczane nerede?"),
                _line("B", "Gehen Sie zuerst geradeaus und dann links.", "Önce dümdüz gidin, sonra sola dönün."),
                _line("A", "Ist sie weit?", "Uzak mı?"),
                _line("B", "Nein, sie ist direkt neben der Bank.", "Hayır, doğrudan bankanın yanında."),
            ],
        },
        [
            _passage(
                "Merkeze nasıl gidilir?",
                "Bu metinde önce hedefi, sonra hareket fiilini ve yön sözlerini yakalamaya çalış.",
                [
                    "[[Lara::kadın adı]] fährt heute [[nach::-e / yönelerek]] [[Berlin::Berlin]] und möchte danach [[zum Zentrum::merkeze]] gehen. Vom [[Bahnhof::istasyon]] fährt zuerst ein [[Bus::otobüs]].",
                    "Später geht sie [[in die Apotheke::eczane içine]] und am Abend fährt sie [[nach Hause::eve]]. Am nächsten Morgen bleibt sie lange [[zu Hause::evde]].",
                ],
            )
        ],
        [
            "Hedefin türünü belirlemeden edat seçme; şehir mi kurum mu kapalı alan mı sorusunu önce sor.",
            "nach Hause / zu Hause çiftini her gün bir kez tekrar etmen çok işe yarar.",
            "Yol tarifini harita üstünde hayal ederek çalışmak öğrenmeyi hızlandırır.",
            "Kısa komutlar yön tarifinde tam cümle kadar değerlidir; yeter ki doğru sırayla gelsin.",
        ],
        [
            _v("die Apotheke", "die", "die Apotheken", ["eczane"], "Die Apotheke ist hier.", "Eczane burada.", "yön tarifi için sık hedef."),
            _v("der Supermarkt", "der", "die Supermärkte", ["süpermarket"], "Der Supermarkt ist groß.", "Süpermarket büyük.", "günlük hedef mekân."),
            _v("das Krankenhaus", "das", "die Krankenhäuser", ["hastane"], "Das Krankenhaus ist neu.", "Hastane yeni.", "kurumsal hedef örneği."),
            _v("der Bahnhof", "der", "die Bahnhöfe", ["istasyon"], "Der Bahnhof ist nah.", "İstasyon yakın.", "hareket dilinin merkez yerlerinden biri."),
            _v("die Bank", "die", "die Banken", ["banka"], "Die Bank ist links.", "Banka solda.", "yön tarifinde referans olur."),
            _v("das Kino", "das", "die Kinos", ["sinema"], "Das Kino ist im Zentrum.", "Sinema merkezde.", "eğlence mekânı örneği."),
            _v("die Post", "die", "die Postämter", ["posta", "postane"], "Die Post ist nicht weit.", "Postane uzak değil.", "kurum adı olarak kullanılır."),
            _v("die Kreuzung", "die", "die Kreuzungen", ["kavşak"], "Die Kreuzung ist dort.", "Kavşak orada.", "yön tarifini büyütür."),
            _v("die Ampel", "die", "die Ampeln", ["trafik lambası"], "Die Ampel ist rot.", "Trafik lambası kırmızı.", "an der Ampel kalıbı için iyi örnek."),
            _v("die Brücke", "die", "die Brücken", ["köprü"], "Die Brücke ist alt.", "Köprü eski.", "rota referans noktası."),
            _v("nach", "-", "-", ["-e", "-a doğru"], "Wir fahren nach Köln.", "Köln'e gidiyoruz.", "şehir yönelmesi."),
            _v("zu", "-", "-", ["-e", "yanına"], "Ich gehe zum Arzt.", "Doktora gidiyorum.", "kişi/kurum yönelmesi."),
            _v("in", "-", "-", ["içine", "-e"], "Sie geht in die Apotheke.", "Eczaneye gidiyor.", "kapalı mekâna hareket."),
            _v("auf", "-", "-", ["-e", "üzerine / etkinliğe"], "Wir gehen auf den Markt.", "Pazara gidiyoruz.", "açık alan veya etkinlik."),
            _v("links", "-", "-", ["sola", "solda"], "Dann gehen Sie links.", "Sonra sola gidin.", "yön sözü."),
            _v("rechts", "-", "-", ["sağa", "sağda"], "Biegen Sie rechts ab.", "Sağa dönün.", "yön sözü."),
            _v("geradeaus", "-", "-", ["dümdüz"], "Gehen Sie geradeaus.", "Dümdüz gidin.", "rota başlangıcı."),
            _v("abbiegen", "-", "-", ["dönmek", "sapmak"], "Hier müssen Sie links abbiegen.", "Burada sola dönmeniz gerekiyor.", "şehir içi yön fiili."),
        ],
        "Bu dersle birlikte Almanca artık seni gerçek bir şehirde de taşıyabilir hale gelir. Nereye gidildiğini ve birine yolu nasıl tarif edeceğini söyleyebilmek A2'nin somut becerilerinden biridir.",
    ),
    _lesson(
        13,
        "ders-13-weil-dass-ve-wenn-ile-yan-cumleler",
        "weil, dass ve wenn ile Yan Cümleler",
        "A2.2",
        "Bu derste A2'nin en önemli yapılarından birine giriyoruz: yan cümle. Neden, düşünce ve koşul anlatımı artık fiilin sona gittiği bir yapı üzerinden kuruluyor.",
        [
            "weil ile neden anlatmak.",
            "dass ile düşünce, bilgi ve görüş aktarmak.",
            "wenn ile koşul veya tekrar eden zaman anlatımı kurmak.",
            "Yan cümlede fiilin sona gittiğini net görmek.",
            "Ana cümle ve yan cümleyi birlikte daha rahat okumak.",
            "A2 anlatısında neden-sonuç ve fikir aktarımını büyütmek.",
        ],
        "yan cümle + fiil sonda",
        [
            {"eyebrow": "1. Adım", "title": "A2'de cümle artık tek parçadan çıkıyor", "body": "Bu derste yalnız bir bilgi vermiyor, onu başka bir bilgiye bağlıyoruz. Nedenini açıklıyor, düşündüğümüz şeyi aktarıyor veya koşul koyuyoruz."},
            {"eyebrow": "2. Adım", "title": "Yan cümlenin en görünür işareti fiilin sona gitmesidir", "body": "weil, dass ve wenn sonrası küçük sözdizimi değişikliği olur. Bu değişikliği görmek A2 seviyesinde çok kritik bir adımdır."},
            {"eyebrow": "3. Adım", "title": "Bağlaç anlamı kadar cümle düzenini de değiştirir", "body": "Bu başlıkta sadece kelime öğrenmiyoruz; aynı zamanda o kelimenin tüm cümleyi nasıl yeniden düzenlediğini görüyoruz."},
        ],
        [
            _g(
                "weil ile neden",
                "weil bir durumun nedenini açar.",
                "Bir şeyin sebebini açıklarken kullanılır.",
                "ana cümle + weil + ... + fiil",
                "weil, A2'de en doğal açıklama bağlaçlarından biridir. Kısa bir yargıyı neden bilgisiyle büyütmeni sağlar.",
                "weil gördüğünde fiilin yerinin değiştiğini unutursan cümle hemen A1 düzeyine geri düşer.",
                [
                    ("Ich bleibe zu Hause, weil ich krank bin.", "neden bilgisi yan cümlede sona kayıyor."),
                    ("Wir kommen später, weil der Zug Verspätung hat.", "sebep açıklaması doğal biçimde bağlanıyor."),
                ],
            ),
            _g(
                "dass ile fikir ve bilgi aktarma",
                "dass, düşünülen, bilinen veya söylenen içeriği aktarır.",
                "Bir görüşü, haberi veya düşünceyi ikinci cümlede açmak istediğinde kullanılır.",
                "ana cümle + dass + ... + fiil",
                "Bu yapı A2'de düşünce aktarmayı mümkün kılar. Artık yalnız 'bence' demek değil, bence ne olduğunu da daha uzun söylemek gerekir.",
                "dass sonrası da fiil sona gider; bunu weil yapısından ayırmak için anlam yerine sözdizimini de izle.",
                [
                    ("Ich glaube, dass das Hotel gut ist.", "görüş içeriği yan cümlede açılıyor."),
                    ("Sie sagt, dass sie morgen kommt.", "aktarılan bilgi ikinci cümlede tamamlanıyor."),
                ],
            ),
            _g(
                "wenn ile koşul veya tekrar eden zaman",
                "wenn hem koşul hem de tekrar eden zaman bağlamı kurabilir.",
                "'eğer' anlamı veya 'ne zaman' mantığında tekrar eden olay anlatırken kullanılır.",
                "wenn + ... + fiil, ana cümle",
                "A2'de bir planın hangi durumda gerçekleşeceğini söylemek için çok kullanışlıdır. Bu, konuşmayı şartlı ve esnek hale getirir.",
                "Yan cümle başta gelirse ana cümlede fiilin yine erken geleceğini unutma; iki cümlenin düzeni birlikte düşünülmelidir.",
                [
                    ("Wenn ich Zeit habe, komme ich mit.", "koşul gerçekleşirse ana cümle çalışır."),
                    ("Wenn ich müde bin, trinke ich Kaffee.", "tekrar eden bir durum ve alışkanlık anlatılıyor."),
                ],
            ),
            _g(
                "Yan cümlede fiil sona gider",
                "weil, dass ve wenn ile başlayan yan cümlede çekimli fiil sona kayar.",
                "Bu bağlaçlarla kurulan her yapıda kullanılır.",
                "bağlaç + özne + diğer ögeler + fiil",
                "A2'deki en kalıcı sözdizimi kırılmalarından biri budur. Bunu yalnız kural olarak değil, ritim olarak duymak gerekir.",
                "Yan cümleyi başlatıp sonra ana cümle düzenini aynen sürdürmek en yaygın hatadır.",
                [
                    ("..., weil ich heute keine Zeit habe.", "çekimli fiil habe sona kaydı."),
                    ("..., dass wir morgen fahren.", "fahren çekimli biçim olarak sonda duruyor."),
                ],
            ),
        ],
        [
            _p("Ich bleibe zu Hause, weil ich krank bin.", "Hasta olduğum için evde kalıyorum.", "neden"),
            _p("Wir kommen später, weil der Zug Verspätung hat.", "Tren geciktiği için daha geç geliyoruz.", "neden ve ulaşım"),
            _p("Ich glaube, dass das Zimmer frei ist.", "Odanın boş olduğuna inanıyorum.", "fikir aktarımı"),
            _p("Sie sagt, dass sie morgen anruft.", "Yarın arayacağını söylüyor.", "dolaylı aktarıma giriş"),
            _p("Wenn ich Zeit habe, komme ich mit.", "Vaktim olursa ben de gelirim.", "koşul"),
            _p("Wenn es regnet, bleiben wir zu Hause.", "Yağmur yağarsa evde kalırız.", "koşul + plan"),
            _p("Ich weiß, dass er heute arbeitet.", "Bugün çalıştığını biliyorum.", "bilgi aktarımı"),
            _p("Wir fahren nicht, weil das Auto kaputt ist.", "Araba bozuk olduğu için gitmiyoruz.", "neden ve iptal"),
            _p("Wenn ich müde bin, schlafe ich früh.", "Yorgun olduğumda erken uyurum.", "alışkanlık"),
            _p("Er hofft, dass alles gut wird.", "Her şeyin iyi olacağını umuyor.", "umut ve beklenti"),
        ],
        [
            _m("Ich bleibe zu Hause, weil ich bin krank.", "Ich bleibe zu Hause, weil ich krank bin.", "yan cümlede fiil sona gider."),
            _m("Ich glaube, dass ist das Hotel gut.", "Ich glaube, dass das Hotel gut ist.", "dass sonrası ana cümle düzeni korunmaz."),
            _m("Wenn ich habe Zeit, komme ich.", "Wenn ich Zeit habe, komme ich.", "fiil sona kaymalıdır."),
            _m("Weil der Zug hat Verspätung, wir kommen später.", "Weil der Zug Verspätung hat, kommen wir später.", "yan cümle önde olsa da ikinci kısım ana cümle olarak kurulur."),
        ],
        {
            "title": "Sebep, düşünce ve koşul",
            "lines": [
                _line("A", "Warum kommst du heute nicht?", "Bugün neden gelmiyorsun?"),
                _line("B", "Ich komme nicht, weil ich arbeiten muss.", "Çalışmam gerektiği için gelmiyorum."),
                _line("A", "Glaubst du, dass das Meeting wichtig ist?", "Toplantının önemli olduğunu düşünüyor musun?"),
                _line("B", "Ja. Wenn ich später Zeit habe, komme ich noch vorbei.", "Evet. Daha sonra vaktim olursa yine uğrarım."),
            ],
        },
        [
            _passage(
                "Neden böyle oldu?",
                "Bu metinde bağlaçları bul ve yan cümledeki fiilin sonda durduğunu gör. A2'nin sözdizimi burada belirginleşiyor.",
                [
                    "[[Mina::kadın adı]] bleibt heute zu Hause, [[weil::çünkü]] sie sehr [[müde::yorgun]] ist. Sie sagt, [[dass::-dığı / -diği şeyi açar]] sie morgen wieder zum [[Kurs::kurs]] kommt.",
                    "[[Wenn::eğer / ne zaman]] sie am Abend noch [[Zeit::zaman]] hat, schreibt sie ihrer [[Freundin::arkadaşına]] eine lange [[Nachricht::mesaj]].",
                ],
            )
        ],
        [
            "Bağlacı gördüğünde hemen fiilin nereye gideceğini düşün.",
            "weil, dass ve wenn için üç ayrı mini kart yapıp aynı örnek cümleyi dönüştürmeyi dene.",
            "Yan cümleyi kısaltarak başla; çok uzun cümleler ilk aşamada yapıyı boğabilir.",
            "Yan cümle öndeyse ana cümlenin de yeniden kurulduğunu fark et.",
        ],
        [
            _v("die Zeit", "die", "die Zeiten", ["zaman"], "Die Zeit ist knapp.", "Zaman dar.", "wenn cümlelerinde sık geçer."),
            _v("die Nachricht", "die", "die Nachrichten", ["mesaj", "haber"], "Die Nachricht ist lang.", "Mesaj uzun.", "dass ile aktarılan içerik örneği."),
            _v("das Meeting", "das", "die Meetings", ["toplantı"], "Das Meeting ist wichtig.", "Toplantı önemli.", "görüş aktarma cümlesi."),
            _v("die Freundin", "die", "die Freundinnen", ["kadın arkadaş"], "Die Freundin ist nett.", "Arkadaş nazik.", "mesaj ve plan cümlelerinde geçer."),
            _v("der Kurs", "der", "die Kurse", ["kurs"], "Der Kurs ist heute lang.", "Kurs bugün uzun.", "gelecek plan bağlamı."),
            _v("das Problem", "das", "die Probleme", ["sorun"], "Das Problem ist klar.", "Sorun net.", "neden-sonuç zinciri kurar."),
            _v("die Hoffnung", "die", "die Hoffnungen", ["umut"], "Die Hoffnung ist noch da.", "Umut hâlâ var.", "hoffen dass kalıbına bağlanır."),
            _v("der Grund", "der", "die Gründe", ["sebep", "neden"], "Der Grund ist logisch.", "Sebep mantıklı.", "weil ile anlamsal bağ kurar."),
            _v("die Entscheidung", "die", "die Entscheidungen", ["karar"], "Die Entscheidung ist schwer.", "Karar zor.", "koşul ve düşünce bağlamı."),
            _v("der Plan", "der", "die Pläne", ["plan"], "Der Plan ist neu.", "Plan yeni.", "wenn ve dass cümlelerine açılır."),
            _v("weil", "-", "-", ["çünkü"], "Ich bleibe zu Hause, weil ich krank bin.", "Hasta olduğum için evde kalıyorum.", "neden yan cümlesi."),
            _v("dass", "-", "-", ["-dığını / -diğini"], "Ich glaube, dass er kommt.", "Onun geleceğini düşünüyorum.", "içerik aktarma."),
            _v("wenn", "-", "-", ["eğer", "-dığında"], "Wenn ich Zeit habe, komme ich.", "Vaktim olursa gelirim.", "koşul veya tekrar."),
            _v("wissen", "-", "-", ["bilmek"], "Ich weiß, dass er hier ist.", "Onun burada olduğunu biliyorum.", "dass ile sık eşleşir."),
            _v("hoffen", "-", "-", ["umut etmek"], "Wir hoffen, dass alles gut wird.", "Her şeyin iyi olacağını umuyoruz.", "gelecek ve beklenti."),
            _v("merken", "-", "-", ["fark etmek"], "Ich merke, dass du müde bist.", "Yorgun olduğunu fark ediyorum.", "algı ve aktarım."),
            _v("falls", "-", "-", ["olursa", "şayet"], "Falls du Zeit hast, ruf mich an.", "Vaktin olursa beni ara.", "wenn'e yakın koşul kelimesi."),
            _v("ob", "-", "-", ["olup olmadığını"], "Ich weiß nicht, ob er kommt.", "Onun gelip gelmeyeceğini bilmiyorum.", "yan cümle alanını biraz genişletir."),
        ],
        "Bu ders A2'nin sözdizimi eşiğidir. Fiilin yan cümlede sona gittiğini doğal biçimde okuyabiliyor ve birkaç cümlede üretebiliyorsan A2 yapısal olarak ciddi şekilde oturuyor demektir.",
    ),
    _lesson(
        14,
        "ders-14-werden-ile-gelecek-planlari-ve-a2-toparlama",
        "werden ile Gelecek Planları ve A2 Toparlama",
        "A2.2",
        "A2'yi geleceğe dönük plan anlatımıyla kapatıyoruz. werden ile gelecek kurarken şimdiye kadar öğrendiğin Perfekt, modal fiiller, bağlaçlar ve yer kalıpları da küçük bir bütünlük içinde geri dönüyor.",
        [
            "werden + infinitiv ile gelecek planlarını anlatmak.",
            "yakın plan ile tahmin tonunu ayırt etmek.",
            "gelecek cümlesini zaman zarflarıyla genişletmek.",
            "A2 boyunca öğrenilen yapıların tek bir kısa anlatıda birleştiğini görmek.",
            "sebep, plan, yer ve tercih bilgisini aynı konuşmada taşıyabilmek.",
            "A2 sonunda bağımsız günlük anlatı eşiğine gelmek.",
        ],
        "werden + gelecek",
        [
            {"eyebrow": "1. Adım", "title": "werden geleceği görünür kılar", "body": "Almancada gelecek çoğu zaman Präsens ile de anlatılabilir; ama A2'de werden ile gelecek kurmak plan ve tahmini daha belirgin hale getirir."},
            {"eyebrow": "2. Adım", "title": "Gelecek dili planı toparlar", "body": "Ne zaman, nereye, neden ve kiminle gideceğini söylemek artık A2 sonunda tek konuşma içinde birleşebilir. Bu ders bunu toplar."},
            {"eyebrow": "3. Adım", "title": "A2'nin eski başlıkları burada yeniden görünür", "body": "Yer ifadeleri, modal ton, Perfekt karşılaştırması ve bağlaçlar artık yalnız ayrı dersler değil; tek metin içinde birlikte çalışmaya başlar."},
        ],
        [
            _g(
                "werden + Infinitiv",
                "werden, gelecek planı veya öngörüyü görünür hale getirir.",
                "Bir şeyin gelecekte olacağını, yapılacağını veya planlandığını söylerken kullanılır.",
                "özne + werden + ... + infinitiv",
                "A2 sonunda plan anlatımı artık doğal bir ihtiyaçtır. werden yapısı, gelecek zaman hissini açık biçimde taşıyarak anlatıyı düzenler.",
                "werden ile yine asıl fiili çekmeye çalışma; gelecek cümlede asıl fiil yalın halde sonda kalır.",
                [
                    ("Ich werde morgen früher kommen.", "gelecek planı çekimli werden ile kuruluyor."),
                    ("Wir werden im Sommer nach Wien fahren.", "zaman ve yer bilgisiyle tam plan cümlesi oluşuyor."),
                ],
            ),
            _g(
                "Plan mı, tahmin mi?",
                "werden hem plan hem de öngörü tonu taşıyabilir; bağlam bunu belirler.",
                "Kesin plan, muhtemel sonuç veya geleceğe dair beklenti söylerken kullanılır.",
                "werden + infinitiv / werden + muhtemel sonuç",
                "A2'de aynı yapı farklı tonlar taşıyabilir. Bu yüzden yalnız formüle değil, konuşanın niyetine de bakmak gerekir.",
                "Her werden cümlesini aynı kesinlikte okumak doğru değildir; zaman zarfı ve bağlam ipucu verir.",
                [
                    ("Ich werde am Freitag zum Arzt gehen.", "takvimlenmiş plan hissi güçlü."),
                    ("Es wird morgen regnen.", "tahmin / öngörü tonu öne çıkıyor."),
                ],
            ),
            _g(
                "Gelecek cümlesinde zaman ve yön",
                "Gelecek anlatım çoğu zaman ne zaman ve nereye sorularıyla birlikte gelir.",
                "Planı daha somut ve kullanılabilir hale getirmek istediğinde kullanılır.",
                "zaman zarfı + werden + ... + hedef + infinitiv",
                "A2 sonunda yalnız 'gideceğim' demek değil, ne zaman ve nereye gideceğini de rahatça ekleyebilmek gerekir.",
                "Gelecek cümleyi fazla çıplak bırakma; küçük zaman veya yer bilgisi cümleyi belirgin biçimde güçlendirir.",
                [
                    ("Nächste Woche werde ich ins Hotel fahren.", "zaman ve hedef gelecekle birleşiyor."),
                    ("Am Abend werde ich meine Freundin anrufen.", "gelecek eylem net takvimleniyor."),
                ],
            ),
            _g(
                "A2 tekrar köprüsü",
                "Gelecek cümlesi, önceki A2 yapılarını aynı akışta kullanma fırsatı verir.",
                "Planı neden, tercih, yer ve ihtiyaç bilgisiyle birlikte anlatırken kullanılır.",
                "zaman + werden + ... / weil, dass, wenn ile genişleme",
                "Bu dersin amacı yeni tek bir yapıdan çok, artık birden fazla yapıyı aynı konuşmada yönetebildiğini göstermek.",
                "Yeni yapıyı kurarken eski yapıları unutmamak gerekir; çünkü gerçek akıcılık tek başlıkların toplamından doğar.",
                [
                    ("Wenn ich Zeit habe, werde ich am Wochenende nach Izmir fahren.", "koşul ve gelecek aynı cümle zincirinde çalışıyor."),
                    ("Ich glaube, dass wir dort ein gutes Hotel finden werden.", "yan cümle ve gelecek aynı yapıda birleşiyor."),
                ],
            ),
        ],
        [
            _p("Ich werde morgen früher kommen.", "Yarın daha erken geleceğim.", "temel gelecek planı"),
            _p("Wir werden im Sommer nach Wien fahren.", "Yazın Viyana'ya gideceğiz.", "zaman + yer + gelecek"),
            _p("Am Abend werde ich meine Freundin anrufen.", "Akşam arkadaşımı arayacağım.", "takvimlenmiş plan"),
            _p("Es wird morgen regnen.", "Yarın yağmur yağacak.", "öngörü"),
            _p("Wenn ich Zeit habe, werde ich mitkommen.", "Vaktim olursa ben de geleceğim.", "koşul + gelecek"),
            _p("Ich glaube, dass das Wetter besser wird.", "Havanın daha iyi olacağını düşünüyorum.", "görüş + gelecek"),
            _p("Wir werden ein Zimmer reservieren.", "Bir oda rezerve edeceğiz.", "seyahat planı"),
            _p("Nächste Woche werde ich zum Arzt gehen.", "Gelecek hafta doktora gideceğim.", "takvim ve hedef"),
            _p("Später werde ich dir alles erklären.", "Daha sonra sana her şeyi açıklayacağım.", "gelecek vaat / plan"),
            _p("Ich hoffe, dass alles gut wird.", "Her şeyin iyi olacağını umuyorum.", "umut ve gelecek"),
        ],
        [
            _m("Ich werde komme.", "Ich werde kommen.", "werden ile asıl fiil yalın halde olmalıdır."),
            _m("Ich werde morgen nach Hause gehe.", "Ich werde morgen nach Hause gehen.", "gelecek cümlede fiil sona gider."),
            _m("Es wird morgen regnet.", "Es wird morgen regnen.", "tahmin cümlesinde de yalın fiil gerekir."),
            _m("Wenn ich Zeit habe, ich werde kommen.", "Wenn ich Zeit habe, werde ich kommen.", "yan cümle sonrası ana cümle yeniden kurulur."),
        ],
        {
            "title": "A2 sonrası plan",
            "lines": [
                _line("A", "Was wirst du im Sommer machen?", "Yazın ne yapacaksın?"),
                _line("B", "Ich werde zuerst meine Familie besuchen und dann nach Wien fahren.", "Önce ailemi ziyaret edeceğim, sonra Viyana'ya gideceğim."),
                _line("A", "Und wo wirst du dort wohnen?", "Peki orada nerede kalacaksın?"),
                _line("B", "Ich glaube, dass ich ein kleines Hotel im Zentrum finden werde.", "Merkezde küçük bir otel bulacağımı düşünüyorum."),
            ],
        },
        [
            _passage(
                "A2 kapanış paragrafı",
                "Bu metin kasıtlı olarak birkaç eski A2 yapısını birlikte taşıyor. Amaç, artık bunları tek tek değil birleşik olarak okuyabilmen.",
                [
                    "Nächsten Monat wird [[Mert::erkek adı]] nach [[Hamburg::Hamburg]] fahren, weil er dort ein wichtiges [[Treffen::buluşma]] haben wird. Wenn alles gut läuft, wird er im [[Zentrum::merkez]] ein ruhiges [[Hotel::otel]] finden.",
                    "Er glaubt, dass die [[Reise::seyahat]] nicht zu teuer wird. Trotzdem wird er vorher noch mehr [[Geld::para]] sparen, damit später alles leichter wird.",
                ],
            )
        ],
        [
            "werden yapısını Präsens'ten ayrı duy ama her cümlede zorunlu sanma.",
            "Gelecek cümlelerini zaman zarfı ve yer bilgisiyle birlikte kurmaya çalış.",
            "Bu son derste eski A2 başlıklarını bilinçli olarak karıştırıp mini paragraf üret.",
            "A2'yi bitirirken kısa ama birleşik anlatı hedefle; tek tek doğru cümleler artık başlangıç noktasıdır.",
        ],
        [
            _v("die Reise", "die", "die Reisen", ["seyahat", "yolculuk"], "Die Reise wird lang.", "Yolculuk uzun olacak.", "gelecek planlarının merkez isimlerinden biri."),
            _v("das Treffen", "das", "die Treffen", ["buluşma", "toplantı"], "Das Treffen wird wichtig.", "Toplantı önemli olacak.", "gelecek takvim dili."),
            _v("das Zentrum", "das", "die Zentren", ["merkez"], "Das Zentrum ist nah.", "Merkez yakın.", "yer planı kurar."),
            _v("das Hotel", "das", "die Hotels", ["otel"], "Das Hotel wird ruhig sein.", "Otel sakin olacak.", "seyahat geleceği."),
            _v("das Geld", "das", "die Gelder", ["para"], "Das Geld wird reichen.", "Para yetecek.", "plan ve tahmin dili."),
            _v("die Zukunft", "die", "die Zukünfte", ["gelecek"], "Die Zukunft ist offen.", "Gelecek açık.", "ders temasını taşır."),
            _v("der Sommer", "der", "die Sommer", ["yaz"], "Der Sommer wird heiß.", "Yaz sıcak olacak.", "zaman planı."),
            _v("der Plan", "der", "die Pläne", ["plan"], "Der Plan wird klar.", "Plan netleşecek.", "gelecek anlatısını çerçeveler."),
            _v("die Entscheidung", "die", "die Entscheidungen", ["karar"], "Die Entscheidung wird schwer.", "Karar zor olacak.", "gelecek ve tercih cümlelerine bağlanır."),
            _v("die Einladung", "die", "die Einladungen", ["davet"], "Die Einladung wird kommen.", "Davet gelecek.", "gelecek olay hissi."),
            _v("werden", "-", "-", ["-ecek", "olacak"], "Ich werde morgen anrufen.", "Yarın arayacağım.", "gelecek kuran yardımcı fiil."),
            _v("später", "-", "-", ["daha sonra"], "Später werde ich alles erklären.", "Daha sonra her şeyi açıklayacağım.", "gelecek planı zamanlar."),
            _v("nächstes", "-", "-", ["gelecek", "önümüzdeki"], "Nächstes Jahr werde ich reisen.", "Gelecek yıl seyahat edeceğim.", "gelecek takvim işaretçisi."),
            _v("bald", "-", "-", ["yakında"], "Bald werde ich fertig sein.", "Yakında hazır olacağım.", "yakın gelecek hissi."),
            _v("später", "-", "-", ["daha sonra"], "Später werden wir essen.", "Daha sonra yemek yiyeceğiz.", "oturum sonrası zaman verir."),
            _v("hoffen", "-", "-", ["umut etmek"], "Ich hoffe, dass alles gut wird.", "Her şeyin iyi olacağını umuyorum.", "gelecek ve dass birleşimi."),
            _v("finden", "-", "-", ["bulmak"], "Wir werden ein Zimmer finden.", "Bir oda bulacağız.", "seyahat planı eylemi."),
            _v("sparen", "-", "-", ["biriktirmek", "tasarruf etmek"], "Ich werde mehr Geld sparen.", "Daha fazla para biriktireceğim.", "gelecek hedef dili."),
        ],
        "A2 burada bitiyor ama asıl hedef bu son derste tek bir yeni yapı öğrenmek değil. Amaç, artık geçmiş, şimdi ve gelecek arasında daha kontrollü geçebilen bir konuşma omurgasına sahip olmak.",
    ),
]


for idx, lesson in enumerate(A2_LESSONS):
    if idx + 1 < len(A2_LESSONS):
        next_lesson = A2_LESSONS[idx + 1]
        lesson["next_lesson"] = {
            "title": next_lesson["title"],
            "status": next_lesson["status"],
            "slug": next_lesson["slug"],
        }
    else:
        lesson["next_lesson"] = {
            "title": "A2 seviye bitirme testi",
            "status": "planned",
            "slug": "",
            "kind": "planned",
        }


A2_LESSONS = deepcopy(A2_LESSONS)


def _get_lesson(index):
    for lesson in A2_LESSONS:
        if lesson["index"] == index:
            return lesson
    raise KeyError(f"A2 lesson {index} not found")


def _append_exam_bridge(index, body):
    lesson = _get_lesson(index)
    lesson["lesson_blocks"].append(
        {
            "eyebrow": "Sınav köprüsü",
            "title": "Bu dersi Goethe A2 tarzında nasıl kullanırsın?",
            "body": body,
        }
    )


_get_lesson(1)["tips"].append(
    "Goethe A2 için bu dersi 'geçen hafta sonu ne yaptım?' sorusuna 4-5 cümleyle cevap verecek kadar aktif kullan."
)
_append_exam_bridge(
    1,
    "Goethe A2 yazma ve konuşma bölümlerinde geçmişte yaptığın şeyleri kısaca anlatman gerekebilir. Bu dersin sonunda dünün veya geçen hafta sonunun kısa özetini Perfekt ile 4-5 cümlede kurabiliyor olman gerekir.",
)

_get_lesson(2)["tips"].append(
    "Bir odanın ya da evin krokisine bakıp en az 5 yer cümlesi kurabiliyorsan bu ders sınav kullanımı açısından doğru oturmuştur."
)
_append_exam_bridge(
    2,
    "Goethe A2'de ev, oda ve eşya konumu anlatımı sık gerekir. Bu dersi, bir odadaki üç nesnenin nerede olduğunu yardım almadan tarif edecek seviyeye taşımak gerekir.",
)

_get_lesson(3)["tips"].append(
    "Menüden iki şey isteyip fiyat sorup hesabı isteme zincirini tek akışta tekrar et; bu tam sınavlık iletişim görevidir."
)
_append_exam_bridge(
    3,
    "Bu ders özellikle günlük diyalog görevlerine hizmet eder. Menüden bir şey isteme, ek istek bildirme ve hesabı isteme akışını tek konuşmada sürdürebiliyorsan ders işlevini yerine getiriyor.",
)

_get_lesson(4)["tips"].append(
    "Randevu, bilgi alma ve yardım isteme cümlelerini sert emir gibi değil, yumuşak rica olarak kurmaya odaklan."
)
_append_exam_bridge(
    4,
    "Goethe A2'de doğrudan emir değil, sosyal olarak uygun rica ve istek kalıpları gerekir. Bu dersi danışma, kurs ofisi veya telefon görüşmesi bağlamında kullanabiliyorsan doğru yerdeyiz.",
)

_get_lesson(5)["tips"].append(
    "Bu başlığı yalnız soyut gramer gibi çalışma; 'plan, randevu, sorun, yolculuk' gibi gerçek konular üzerinden daran, darüber, darauf kalıplarını tekrar et."
)
_append_exam_bridge(
    5,
    "Bu ders Goethe A2'de uzun yazı üretmekten çok akıcılığı ve tekrar azaltmayı besler. Aynı konuyu iki cümlede yinelerken isim tekrarını kırabiliyorsan ders doğru çalışmıştır.",
)

_get_lesson(6)["tips"].append(
    "Sağlık, iş ve günlük plan bozulmaları üzerinden 'yapamadım, yapmak zorundaydım, yapmak istedim' zincirlerini sesli tekrar et."
)
_append_exam_bridge(
    6,
    "Goethe A2 konuşmasında geçmişte neden bir şeyi yapamadığını veya yapmak zorunda kaldığını anlatmak çok işlevlidir. Bu dersin hedefi kısa kişisel anlatıda modal geçmişi rahat kullanmaktır.",
)

_get_lesson(7)["tips"].append(
    "Bir ürünü yalnız adlandırma; renk, beden, fiyat ve sana uyup uymadığıyla birlikte değerlendir."
)
_append_exam_bridge(
    7,
    "Bu ders alışveriş ve seçim konuşmaları için doğrudan faydalıdır. Bir ürünü beğenip beğenmediğini, pahalı mı rahat mı olduğunu ve hangi bedeni istediğini tek konuşmada söyleyebilmelisin.",
)

_get_lesson(8)["tips"].append(
    "Sebep ve engel içeren iki cümle kurup bunları deshalb ve trotzdem ile dönüştürmek sınavdaki küçük anlatı görevlerini güçlendirir."
)
_append_exam_bridge(
    8,
    "Goethe A2 yazma ve konuşmada fikirleri yalnız sıralamak yetmez; aralarındaki ilişkiyi göstermek gerekir. deshalb ve trotzdem bunu kısa ama güçlü biçimde sağlar.",
)

_get_lesson(9)["tips"].append(
    "İki otel, iki şehir veya iki ürün arasında seçim yapma egzersizleri yap; bu ders kararsızlığı değil, net tercih dilini öğretir."
)
_append_exam_bridge(
    9,
    "Karşılaştırma dili sınavda karar verme ve öneri verme görevlerini güçlendirir. İki seçenek arasında fiyat, mesafe ve kalite kıyası kurabiliyorsan bu ders hazırdır.",
)

lesson_10 = _get_lesson(10)
lesson_10["teaser"] = (
    "Bu ders A2'nin üst sınırına yakın duran pasif yapıya kontrollü bir giriş sunar. "
    "Amaç tüm pasif sistemini üretmek değil; duyuru, süreç ve sonuç cümlelerinde pasifi tanımak ve birkaç kısa örneği güvenle kurmaktır."
)
lesson_10["objectives"][0] = "Vorgangspassiv ve Zustandspassiv farkını önce tanımak, sonra kısa örneklerde denemek."
lesson_10["completion_note"] = (
    "Bu başlık Goethe A2'nin merkez üretim konusu değildir; yine de günlük duyuru ve süreç cümlelerinde pasifi tanıyabiliyor, "
    "werden ile süreç ve sein ile sonuç farkını okuyabiliyorsan ders amacına ulaşmıştır."
)
lesson_10["tips"].append(
    "Pasifi ezber listesi gibi değil, duyuru ve süreç cümlelerini tanıma aracı gibi çalış; bu dersin asıl hedefi budur."
)
_append_exam_bridge(
    10,
    "Bu ders sınav için çekirdek üretim başlığı değil, tanıma ve kontrollü kullanım başlığıdır. Duyuru, açıklama veya iş akışı cümlesinde pasifi fark edip anlamlandırabiliyorsan yeterli kazanımı elde etmiş olursun.",
)

_get_lesson(11)["tips"].append(
    "Rezervasyon, kahvaltı saati, internet ve oda isteği sorularını rol oyunu halinde tekrar et; bu ders doğrudan günlük iletişim becerisidir."
)
_append_exam_bridge(
    11,
    "Bu ders seyahat ve konaklama görevleri için doğrudan kullanılır. Check-in, oda tercihi ve hizmet sorularını blok halinde kurabiliyorsan Goethe A2 tipi işlevsel iletişim hedefine yaklaşırsın.",
)

_get_lesson(12)["tips"].append(
    "Bir arkadaşına tarif verir gibi 4-5 adımlı mini yol tarifi kur; bu ders ancak böyle aktifleşir."
)
_append_exam_bridge(
    12,
    "Yol sorma ve yol tarif etme A2'nin temel iletişim görevlerinden biridir. Bir hedefe nasıl gidileceğini kısa ve net anlatabiliyorsan ders sınav açısından yeterince işlevseldir.",
)

_get_lesson(13)["tips"].append(
    "weil, dass ve wenn ile aynı temayı üç farklı biçimde anlatmayı dene; yapı farkı en hızlı böyle oturur."
)
_append_exam_bridge(
    13,
    "Bu ders A2'nin yapısal eşiğidir. Bir fikri neden, görüş veya koşul ile genişletebiliyorsan hem yazma hem konuşma görevlerinde ciddi avantaj kazanırsın.",
)

lesson_14 = _get_lesson(14)
lesson_14["tips"].append(
    "Son derste ayrı ayrı doğru cümlelerden çok, kısa ama birleşik bir gelecek planı anlatmaya odaklan."
)
_append_exam_bridge(
    14,
    "Bu kapanış dersi A2 genel tekrar işlevi görür. Gelecek planını neden, yer, tercih ve küçük ayrıntılarla 5-6 cümlede anlatabiliyorsan artık bitirme testine geçmeye hazırsın.",
)


def _q(prompt, options, correct_index, explanation):
    return {
        "prompt": prompt,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
    }


def _module(module_id, title, description, questions):
    return {
        "id": module_id,
        "type": "single_choice",
        "title": title,
        "description": description,
        "questions": questions,
    }


def _replace_dialogue(index, title, lines):
    lesson = _get_lesson(index)
    lesson["mini_dialogue"] = {"title": title, "lines": [_line(*line) for line in lines]}


def _replace_reading(index, title, focus, paragraphs):
    lesson = _get_lesson(index)
    lesson["reading_passages"] = [_passage(title, focus, paragraphs)]


def _extend_phrase_bank(index, phrases):
    lesson = _get_lesson(index)
    lesson["phrase_bank"].extend([_p(*phrase) for phrase in phrases])


def _set_extra_exercises(index, modules):
    lesson = _get_lesson(index)
    lesson["exercises"] = modules


_replace_dialogue(
    1,
    "Hafta sonunu ayrıntılı anlatma",
    [
        ("A", "Was hast du am Wochenende gemacht?", "Hafta sonu ne yaptın?"),
        ("B", "Am Samstag habe ich zuerst lange geschlafen und später mit meiner Schwester gefrühstückt.", "Cumartesi önce uzun uyudum, sonra kız kardeşimle kahvaltı yaptım."),
        ("A", "Bist du danach zu Hause geblieben?", "Sonra evde mi kaldın?"),
        ("B", "Nein, ich bin mit dem Zug ins Zentrum gefahren und habe dort zwei Freunde getroffen.", "Hayır, trenle merkeze gittim ve orada iki arkadaşımla buluştum."),
        ("A", "Und was habt ihr am Abend gemacht?", "Peki akşam ne yaptınız?"),
        ("B", "Wir haben in einem kleinen Café gegessen und sind erst um halb elf nach Hause zurückgekommen.", "Küçük bir kafede yemek yedik ve eve ancak on buçukta döndük."),
    ],
)
_replace_reading(
    1,
    "Yoğun ama güzel bir hafta sonu",
    "12 kelime / kalıp",
    [
        "Am Freitagabend hat [[Leyla::kadın adı değil, anlatının kişisi]] lange für einen [[Test::sınav]] gelernt. Trotzdem hat sie noch ihre [[Tasche::çanta]] vorbereitet, weil sie am nächsten Morgen früh [[losgefahren::yola çıktı]] ist.",
        "Am Samstag hat sie zuerst mit ihrer [[Familie::aile]] [[gefrühstückt::kahvaltı yaptı]] und später ihre Großmutter [[besucht::ziyaret etti]]. Dort haben sie zusammen Kaffee getrunken und alte [[Fotos::fotoğraflar]] angeschaut.",
        "Am Sonntag ist Leyla mit einer Freundin ins [[Museum::müze]] gegangen. Sie haben eine [[Eintrittskarte::giriş bileti]] gekauft, viel geredet und sind am Abend müde, aber zufrieden nach Hause [[zurückgekommen::geri döndü]].",
    ],
)
_extend_phrase_bank(
    1,
    [
        ("Am Samstag habe ich zuerst gefrühstückt.", "Cumartesi önce kahvaltı yaptım.", "A1 zaman zarfları ile A2 Perfekt birlikte çalışır."),
        ("Danach bin ich ins Zentrum gefahren.", "Sonra merkeze gittim.", "A1 hareket dili Perfekt içinde tekrar eder."),
        ("Am Abend bin ich spät zurückgekommen.", "Akşam geç döndüm.", "Saat ve zaman ifadeleri eski dersleri tekrar ettirir."),
        ("Ich war am Montag deshalb sehr müde.", "Bu yüzden pazartesi çok yorgundum.", "A1 sıfatları yeni geçmiş anlatıya bağlanır."),
    ],
)
_set_extra_exercises(
    1,
    [
        _module(
            "a2-l1-dialogue-comprehension",
            "Diyalog Anlama",
            "Diyaloğun içindeki geçmiş olay zincirini takip et.",
            [
                _q("Konuşan kişi cumartesi sabah önce ne yapıyor?", ["Trenle merkeze gidiyor", "Kahvaltı yapıyor", "Müzeye gidiyor"], 1, "Diyalogda önce kız kardeşiyle kahvaltı yaptığını söylüyor."),
                _q("Akşam nereye gidiyorlar?", ["Küçük bir kafeye", "Banka şubesine", "İstasyona"], 0, "Akşam küçük bir kafede yemek yediklerini belirtiyor."),
                _q("Eve ne zaman dönüyorlar?", ["Saat sekizde", "Saat on bir buçukta", "Saat on buçuk civarında"], 2, "Diyalogta yarım on bir civarında döndüğünü söylüyor."),
                _q("Geçmiş yapı hangi yardımcı fiille geliyor: 'bin ... zurückgekommen'?", ["haben", "sein", "werden"], 1, "Hareket bildiren dönmek fiili burada sein ile kuruluyor."),
            ],
        ),
        _module(
            "a2-l1-reading-comprehension",
            "Okuma Anlama",
            "Uzun metindeki olay sırasını doğru oku.",
            [
                _q("Leyla cuma akşamı neden ders çalışıyor?", ["Bir teste hazırlandığı için", "Müzeye gittiği için", "İşten geç çıktığı için"], 0, "İlk paragrafta bir test için çalıştığı söyleniyor."),
                _q("Cumartesi günü kimi ziyaret ediyor?", ["Arkadaşını", "Büyükannesini", "Öğretmenini"], 1, "İkinci paragrafta büyükannesini ziyaret ettiği yazıyor."),
                _q("Müzeye girmek için ne alıyorlar?", ["Bir oda anahtarı", "Bir giriş bileti", "Bir harita"], 1, "Üçüncü paragrafta Eintrittskarte aldıkları belirtiliyor."),
                _q("Metnin sonunda Leyla kendini nasıl hissediyor?", ["Yorgun ama memnun", "Sinirli ve aç", "Kafası karışmış"], 0, "Son cümlede müde, aber zufrieden ifadesi geçiyor."),
            ],
        ),
        _module(
            "a2-l1-a1-review",
            "A1 Köprü Tekrarı",
            "A1 zaman ve günlük hayat kelimelerini Perfekt ile birlikte tekrar et.",
            [
                _q("'Cumartesi sabah' için en doğal açılış hangisi?", ["Am Samstagmorgen", "In Samstagmorgen", "Zu Samstagmorgen"], 0, "Gün ve zaman bloğu am ile kurulur."),
                _q("'Ailemle kahvaltı yaptım' cümlesinde doğru yardımcı fiil hangisi?", ["bin", "habe", "seid"], 1, "frühstücken gibi çoğu fiil Perfekt'te haben alır."),
                _q("'Eve döndüm' cümlesinde doğru yapı hangisi?", ["Ich habe nach Hause zurückgekommen.", "Ich bin nach Hause zurückgekommen.", "Ich werde nach Hause zurückgekommen."], 1, "Hareket bildiren zurückkommen sein ile kurulur."),
                _q("'Çok yorgundum' ifadesi hangisidir?", ["Ich war sehr müde.", "Ich bin sehr müde gewesen sein.", "Ich habe sehr müde."], 0, "A1 sein bilgisi burada geçmiş bağlamda tekrar eder."),
            ],
        ),
    ],
)

_replace_dialogue(
    2,
    "Yeni odada eşya yerleştirme",
    [
        ("A", "Wo steht jetzt der neue Schreibtisch?", "Yeni çalışma masası şimdi nerede duruyor?"),
        ("B", "Er steht zwischen dem Fenster und dem Regal, direkt neben der Lampe.", "Pencereyle rafın arasında, lambanın hemen yanında duruyor."),
        ("A", "Und wo liegt dein Laptop?", "Peki dizüstü bilgisayarın nerede duruyor?"),
        ("B", "Er liegt auf dem Tisch, aber die Tasche liegt noch unter dem Bett.", "Masanın üstünde, ama çanta hâlâ yatağın altında duruyor."),
        ("A", "Hängt das Bild jetzt an der Wand?", "Resim şimdi duvarda asılı mı?"),
        ("B", "Ja, und vor dem Sofa steht jetzt auch eine kleine Pflanze.", "Evet, ayrıca kanepenin önünde artık küçük bir bitki de duruyor."),
    ],
)
_replace_reading(
    2,
    "Bir öğrencinin yeni odası",
    "12 kelime / kalıp",
    [
        "[[Deniz::kişi adı]] yeni [[Wohnung::ev]] taşındıktan sonra odasını yeniden düzenliyor. Das [[Regal::raf]] steht jetzt links, und der [[Schreibtisch::çalışma masası]] steht direkt am [[Fenster::pencere]].",
        "Auf dem Tisch liegt ein [[Wörterbuch::sözlük]], daneben liegt ein [[Heft::defter]] und über dem Tisch hängt eine helle [[Lampe::lamba]]. Unter dem Tisch steht noch eine Kiste mit alten [[Büchern::kitaplar]].",
        "Wenn Freunde zu Besuch kommen, können sie sofort sehen, wo alles ist. Der [[Stuhl::sandalye]] steht vor dem Tisch, die [[Tasche::çanta]] liegt hinter der Tür und in der [[Ecke::köşe]] steht eine grüne Pflanze.",
    ],
)
_extend_phrase_bank(
    2,
    [
        ("Das Wörterbuch liegt neben dem Heft.", "Sözlük defterin yanında duruyor.", "A1 okul nesneleri bu derste geri dönüyor."),
        ("Die Pflanze steht in der Ecke.", "Bitki köşede duruyor.", "A1 temel yer kelimeleri genişliyor."),
        ("Vor der Tür steht ein Stuhl.", "Kapının önünde bir sandalye duruyor.", "A1 mobilya kelimeleri tekrar ediliyor."),
        ("Am Abend ist das Zimmer sehr ruhig.", "Akşam oda çok sakin oluyor.", "A1 zaman ifadesi yer anlatımıyla birleşiyor."),
    ],
)
_set_extra_exercises(
    2,
    [
        _module(
            "a2-l2-dialogue-comprehension",
            "Diyalog Anlama",
            "Eşyaların konumunu dikkatle takip et.",
            [
                _q("Çalışma masası nerede duruyor?", ["Kapının arkasında", "Pencereyle rafın arasında", "Yatağın altında"], 1, "Diyalogta masa pencere ile raf arasında duruyor."),
                _q("Çanta nerede?", ["Yatağın altında", "Masanın üstünde", "Lambanın yanında"], 0, "Çantanın hâlâ yatağın altında olduğu söyleniyor."),
                _q("Resim nerede asılı?", ["Kapıda", "Duvarda", "Yatağın üzerinde"], 1, "Bild cümlesi an der Wand ile kuruluyor."),
                _q("Kanepenin önünde ne var?", ["Bir sözlük", "Küçük bir bitki", "Bir bavul"], 1, "Diyaloğun son satırında küçük bir bitki deniyor."),
            ],
        ),
        _module(
            "a2-l2-reading-comprehension",
            "Okuma Anlama",
            "Uzun odada hangi eşya nerede, bunu ayır.",
            [
                _q("Sözlük nerede duruyor?", ["Masanın üstünde", "Pencerenin arkasında", "Rafın içinde"], 0, "İkinci paragrafta Wörterbuch'un masada olduğu belirtiliyor."),
                _q("Defter hangi eşyanın yanında?", ["Bitkinin", "Sözlüğün", "Kapının"], 1, "Defterin sözlüğün yanında olduğu yazıyor."),
                _q("Eski kitaplar nerede?", ["Sandalyenin üstünde", "Kutunun içinde", "Köşede"], 1, "Eski kitapların bir kutunun içinde olduğu söyleniyor."),
                _q("Arkadaşlar geldiğinde neyi hemen anlayabiliyor?", ["Evin kaç odası olduğunu", "Her şeyin nerede olduğunu", "Pencerenin ne zaman açıldığını"], 1, "Metnin üçüncü paragrafı tam bunu söylüyor."),
            ],
        ),
        _module(
            "a2-l2-a1-review",
            "A1 Köprü Tekrarı",
            "A1'deki mobilya ve yer kelimelerini A2 konum cümleleriyle birleştir.",
            [
                _q("'Masa pencerenin yanında duruyor' cümlesi hangisidir?", ["Der Tisch steht neben dem Fenster.", "Der Tisch geht neben das Fenster.", "Der Tisch ist nach dem Fenster."], 0, "Konum cümlesi stehen + neben dem ile kurulur."),
                _q("'Kitap masanın üstünde' için en doğal fiil hangisi?", ["hängt", "liegt", "fährt"], 1, "Yatık nesneler için liegen doğal seçimdir."),
                _q("'Oda çok sakin' cümlesi hangisidir?", ["Das Zimmer ist sehr ruhig.", "Das Zimmer hat sehr ruhig.", "Das Zimmer wird ruhig."], 0, "A1 sein + sıfat yapısı burada tekrar eder."),
                _q("'Köşe' kelimesinin Almancası hangisi?", ["die Ecke", "die Reise", "der Bahnhof"], 0, "Yer anlatımındaki temel isimlerden biridir."),
            ],
        ),
    ],
)

_replace_dialogue(
    3,
    "Restoranda tam sipariş konuşması",
    [
        ("Garson", "Guten Abend. Haben Sie schon gewählt?", "İyi akşamlar. Seçiminizi yaptınız mı?"),
        ("Müşteri", "Ja, ich hätte gern zuerst eine Tomatensuppe und danach den Salat mit Hähnchen.", "Evet, önce bir domates çorbası, sonra da tavuklu salata rica ederim."),
        ("Garson", "Möchten Sie dazu etwas trinken?", "Bunun yanında içecek ister misiniz?"),
        ("Müşteri", "Ja, für mich einen Tee ohne Zucker und später bitte noch Wasser.", "Evet, benim için şekersiz bir çay ve daha sonra da su lütfen."),
        ("Garson", "Natürlich. Sonst noch etwas?", "Elbette. Başka bir şey?"),
        ("Müşteri", "Nein danke. Können wir später mit Karte zahlen?", "Hayır teşekkürler. Daha sonra kartla ödeyebilir miyiz?"),
    ],
)
_replace_reading(
    3,
    "Akşam yemeğinde küçük sorunlar",
    "12 kelime / kalıp",
    [
        "[[Merve::kişi adı]] bugün işten sonra bir [[Restaurant::restoran]] gidiyor. Sie ist müde, möchte aber trotzdem in Ruhe essen und noch kurz ihre [[E-Mails::e-postalar]] kontrol etmek.",
        "Zuerst bestellt sie eine [[Suppe::çorba]], einen [[Salat::salata]] und ein großes [[Wasser::su]]. Danach merkt sie, dass im Salat zu viele [[Zwiebeln::soğanlar]] sind, deshalb bittet sie höflich um eine andere Portion.",
        "Der [[Kellner::garson]] reagiert freundlich und bringt später noch einen [[Kaffee::kahve]]. Am Ende fragt Merve nach der [[Rechnung::hesap]] und bezahlt mit Karte, weil sie kein Bargeld dabei hat.",
    ],
)
_extend_phrase_bank(
    3,
    [
        ("Ich hätte gern die Suppe ohne Zwiebeln.", "Çorbayı soğansız rica ederim.", "A1 yiyecek kelimeleri nezaket diliyle birleşiyor."),
        ("Für mich bitte noch ein Wasser.", "Benim için bir su daha lütfen.", "A1 içecek kelimeleri tekrar ediyor."),
        ("Wir zahlen heute mit Karte.", "Bugün kartla ödüyoruz.", "A1 günlük fiiller hizmet bağlamında geri dönüyor."),
        ("Am Ende fragen wir nach der Rechnung.", "Sonunda hesabı soruyoruz.", "A1 zaman ve sıra mantığı sürüyor."),
    ],
)
_set_extra_exercises(
    3,
    [
        _module(
            "a2-l3-dialogue-comprehension",
            "Diyalog Anlama",
            "Sipariş akışındaki ayrıntıları takip et.",
            [
                _q("Müşteri önce ne istiyor?", ["Bir çorba", "Bir kahve", "Bir tatlı"], 0, "İlk satırda zuerst eine Tomatensuppe diyor."),
                _q("Çay nasıl isteniyor?", ["Şekerli", "Sütlü", "Şekersiz"], 2, "Tee ohne Zucker istiyor."),
                _q("Daha sonra ne istiyor?", ["Su", "Meyve suyu", "Ekmek"], 0, "Später bitte noch Wasser diyor."),
                _q("Ödeme nasıl yapılmak isteniyor?", ["Nakit", "Kartla", "Telefonla"], 1, "Son satırda mit Karte zahlen soruluyor."),
            ],
        ),
        _module(
            "a2-l3-reading-comprehension",
            "Okuma Anlama",
            "Restorandaki küçük sorunu ve çözümünü oku.",
            [
                _q("Merve neden rahatsız oluyor?", ["Çorba soğuk olduğu için", "Salatada çok soğan olduğu için", "Garson geç geldiği için"], 1, "İkinci paragrafta çok fazla soğan olduğu belirtiliyor."),
                _q("Garson nasıl tepki veriyor?", ["Sinirleniyor", "Dostça davranıyor", "Hesabı hemen getiriyor"], 1, "Üçüncü paragrafta freundlich tepki verdiği yazıyor."),
                _q("Merve neden kartla ödüyor?", ["Nakit parası olmadığı için", "Kart daha ucuz olduğu için", "Garson öyle istediği için"], 0, "Metnin sonunda yanında nakit olmadığı söyleniyor."),
                _q("İşten sonra ne yapmak istiyor?", ["Evde uyumak", "Sakin şekilde yemek yemek ve e-postalara bakmak", "Alışverişe gitmek"], 1, "İlk paragraf bu iki amacı veriyor."),
            ],
        ),
        _module(
            "a2-l3-a1-review",
            "A1 Köprü Tekrarı",
            "A1 yiyecek, içecek ve artikel bilgisini sipariş diliyle tekrar et.",
            [
                _q("'Bir çay' için doğru isim grubu hangisi?", ["ein Tee", "einen Tee", "eine Tee"], 1, "Siparişte maskulin nesne Akkusativ alır."),
                _q("'Bir su daha' için hangisi doğal?", ["Noch ein Wasser", "Wasser ist noch", "Ein Wasser noch?"], 0, "Servis dilinde Noch ein Wasser çok doğal kalıptır."),
                _q("'Hesap lütfen' cümlesi hangisi?", ["Die Rechnung, bitte.", "Die Rechnung ist bitte.", "Bitte die Rechnung ist."], 0, "Bu sabit kapanış formülüdür."),
                _q("'Şekersiz' anlamını burada hangi kelime verir?", ["mit", "ohne", "für"], 1, "Ohne, bir şeyi istemediğini veya çıkarıldığını gösterir."),
            ],
        ),
    ],
)

_replace_dialogue(
    4,
    "Danışmada nazik rica",
    [
        ("Görevli", "Guten Tag. Wie kann ich Ihnen helfen?", "İyi günler. Size nasıl yardımcı olabilirim?"),
        ("Öğrenci", "Ich würde gern einen neuen Termin bekommen, weil ich gestern krank war.", "Yeni bir randevu almak isterdim, çünkü dün hastaydım."),
        ("Görevli", "Kein Problem. Würden Sie lieber am Mittwoch oder am Donnerstag kommen?", "Sorun değil. Çarşamba mı perşembe mi gelmeyi tercih edersiniz?"),
        ("Öğrenci", "Ich würde lieber am Donnerstag kommen. Könnten Sie mir die Uhrzeit noch einmal sagen?", "Perşembe gelmeyi tercih ederim. Saati bana bir kez daha söyleyebilir misiniz?"),
        ("Görevli", "Natürlich. Der Termin ist um halb zehn.", "Elbette. Randevu saat dokuz buçukta."),
        ("Öğrenci", "Vielen Dank. Dann komme ich am Donnerstag pünktlich.", "Çok teşekkür ederim. O halde perşembe günü zamanında gelirim."),
    ],
)
_replace_reading(
    4,
    "Nazik olmak neden fark yaratır?",
    "12 kelime / kalıp",
    [
        "[[Seda::kişi adı]] bugün kurs ofisine gidiyor, weil sie ein neues [[Gespräch::görüşme]] braucht. Sie sagt nicht direkt „Ich will einen Termin“, sondern benutzt höfliche [[Formulierungen::ifadeler]].",
        "Am Schalter sagt sie: Ich [[würde::isterdim]] gern mit der Lehrerin sprechen und ich hätte gern mehr [[Informationen::bilgiler]] über den neuen Kurs. Danach fragt sie: [[Könnten Sie::edebilir misiniz]] mir bitte auch die neue Adresse schicken?",
        "Die Mitarbeiterin antwortet freundlich. Gerade in solchen Situationen merkt Seda, dass ein ruhiger Ton oft schneller zu einer guten [[Lösung::çözüm]] führt.",
    ],
)
_extend_phrase_bank(
    4,
    [
        ("Ich würde gern noch eine Frage stellen.", "Bir soru daha sormak isterdim.", "A1 soru kalıpları yumuşatılıyor."),
        ("Könnten Sie das bitte wiederholen?", "Bunu tekrar edebilir misiniz?", "A1 anlamadım ihtiyacını daha nazik hale getirir."),
        ("Ich hätte gern mehr Informationen.", "Daha fazla bilgi rica ederim.", "A1 temel isimlerle resmî ton kuruluyor."),
        ("Am Donnerstag komme ich pünktlich.", "Perşembe günü zamanında gelirim.", "A1 günler ve saat mantığı geri dönüyor."),
    ],
)
_set_extra_exercises(
    4,
    [
        _module(
            "a2-l4-dialogue-comprehension",
            "Diyalog Anlama",
            "Nazik rica zincirini takip et.",
            [
                _q("Öğrenci neden yeni randevu istiyor?", ["Treni kaçırdığı için", "Dün hasta olduğu için", "Adresini unuttuğu için"], 1, "Diyalogta dün hasta olduğunu söylüyor."),
                _q("Hangi günü tercih ediyor?", ["Salı", "Çarşamba", "Perşembe"], 2, "Donnerstag tercih ediliyor."),
                _q("Randevu saat kaçta?", ["Dokuz buçukta", "On birde", "Sekizde"], 0, "Görevli um halb zehn diyor."),
                _q("Öğrenci görevliye neyi tekrar sormasını istiyor?", ["Adresini", "Uhrzeit bilgisini", "Öğretmenin adını"], 1, "Uhrzeit'i tekrar söylemesini istiyor."),
            ],
        ),
        _module(
            "a2-l4-reading-comprehension",
            "Okuma Anlama",
            "Nazik dilin işlevini oku.",
            [
                _q("Seda neden kurs ofisine gidiyor?", ["Yeni bir görüşmeye ihtiyacı olduğu için", "Kahve içmek için", "Arkadaşını görmek için"], 0, "İlk paragrafta yeni bir görüşmeye ihtiyacı olduğu yazıyor."),
                _q("Seda hangi kaba cümleyi kullanmıyor?", ["Ich will einen Termin.", "Ich brauche Hilfe.", "Wann ist der Kurs?"], 0, "Metin bunu açıkça karşıt örnek olarak veriyor."),
                _q("Mitarbeiterin nasıl tepki veriyor?", ["Kararsız", "Dostça", "Sessiz"], 1, "Üçüncü paragrafta freundlich deniyor."),
                _q("Seda neyi fark ediyor?", ["Sessiz kalmanın daha iyi olduğunu", "Yumuşak tonun çözüme daha hızlı götürdüğünü", "Adresin değiştiğini"], 1, "Son cümle bu dersi veriyor."),
            ],
        ),
        _module(
            "a2-l4-a1-review",
            "A1 Köprü Tekrarı",
            "A1 tanışma ve soru kalıplarını daha nazik tonda tekrar et.",
            [
                _q("'Adresi bana gönderir misiniz?' için en nazik seçenek hangisi?", ["Schicken Sie die Adresse.", "Könnten Sie mir die Adresse schicken?", "Adresse schicken?"], 1, "A2 rica tonu burada tam hedef yapıdır."),
                _q("'Perşembe günü geleceğim' cümlesi hangisi?", ["Ich komme am Donnerstag.", "Ich bin Donnerstag.", "Ich habe Donnerstag kommen."], 0, "A1 gün bilgisi ve düzenli fiil burada temel yapı sağlar."),
                _q("'Bilgi' kelimesinin Almancası hangisi?", ["die Information / Informationen", "das Fenster", "die Reise"], 0, "Resmî konuşmalarda sık geçen temel isimdir."),
                _q("'Lütfen' anlamına gelen kelime hangisi?", ["morgen", "bitte", "später"], 1, "A1'den beri en temel nezaket sözcüğüdür."),
            ],
        ),
    ],
)

_replace_dialogue(
    5,
    "Aynı konuya tekrar dönmek",
    [
        ("A", "Denkst du noch an die Reise nach Wien?", "Viyana yolculuğunu hâlâ düşünüyor musun?"),
        ("B", "Ja, ich denke oft daran und ich spreche fast jeden Tag darüber.", "Evet, onu sık sık düşünüyorum ve neredeyse her gün onun hakkında konuşuyorum."),
        ("A", "Worauf wartest du im Moment am meisten?", "Şu anda en çok neyi bekliyorsun?"),
        ("B", "Ich warte auf die Zusage vom Hotel und freue mich schon sehr darauf.", "Otelden onayı bekliyorum ve bunu şimdiden çok heyecanla bekliyorum."),
        ("A", "Kannst du auch mit den neuen Formularen arbeiten?", "Yeni formlarla da çalışabiliyor musun?"),
        ("B", "Ja, mittlerweile kann ich gut damit arbeiten.", "Evet, artık onlarla iyi çalışabiliyorum."),
    ],
)
_replace_reading(
    5,
    "Tekrarsız konuşmak",
    "12 kelime / kalıp",
    [
        "[[Jonas::kişi adı]] und seine Schwester sprechen oft über ihre nächste [[Reise::seyahat]]. Früher haben sie immer wieder denselben Plan genannt, aber jetzt benutzen sie öfter [[darüber::bunun hakkında]] ve [[daran::onu düşünerek]] gibi yapılar.",
        "Jonas wartet auf eine [[Antwort::cevap]] vom Hotel. Er sagt nicht jedes Mal „Ich warte auf die Antwort“, sondern oft nur: Ich warte schon lange [[darauf::onu bekliyorum]].",
        "Später sprechen beide über yeni bir [[Problem::sorun]] mit den Tickets. Trotzdem bleiben sie ruhig, denken kurz [[darüber::bunun hakkında]] nach und arbeiten am Abend gemeinsam [[damit::bununla]].",
    ],
)
_extend_phrase_bank(
    5,
    [
        ("Ich denke oft daran.", "Bunu sık sık düşünüyorum.", "A1 düşünce ve duygu fiilleri A2 referans yapısıyla birleşir."),
        ("Wir sprechen später darüber.", "Bunun hakkında daha sonra konuşuyoruz.", "A1 zaman zarfları tekrar ediyor."),
        ("Ich warte schon lange darauf.", "Bunu uzun süredir bekliyorum.", "A1 schon kelimesi yeni yapıyla dönüyor."),
        ("Mit dem neuen Plan kann ich gut damit arbeiten.", "Yeni planla bununla iyi çalışabiliyorum.", "A1 araç ve nesne mantığı akıcılığa bağlanıyor."),
    ],
)
_set_extra_exercises(
    5,
    [
        _module(
            "a2-l5-dialogue-comprehension",
            "Diyalog Anlama",
            "Hangi da-yapısının hangi konuya döndüğünü fark et.",
            [
                _q("B kişisi ne hakkında sık sık konuşuyor?", ["Yeni telefonu hakkında", "Viyana yolculuğu hakkında", "Yeni işi hakkında"], 1, "İlk iki satır Viyana yolculuğunu konu ediyor."),
                _q("En çok neyi bekliyor?", ["Otel onayını", "Otobüsü", "Kurs sonuçlarını"], 0, "Otelden gelecek onayı beklediğini söylüyor."),
                _q("'darauf' burada neye dönüyor?", ["Otelden onaya", "Tren garına", "Yeni arkadaşa"], 0, "Bir önceki cümledeki Zusage bilgisini tekrar etmiyor, darauf diyor."),
                _q("'damit arbeiten' ne anlatıyor?", ["Bununla çalışmak", "Oraya gitmek", "Birini aramak"], 0, "mit + araç/nesne referansını taşıyor."),
            ],
        ),
        _module(
            "a2-l5-reading-comprehension",
            "Okuma Anlama",
            "Tekrar kırma mantığını metin içinde izle.",
            [
                _q("Jonas artık neden daha akıcı konuşuyor?", ["Daha yavaş konuştuğu için", "Aynı ismi sürekli tekrar etmediği için", "Cümle kurmadığı için"], 1, "İlk paragraf açıkça bunu söylüyor."),
                _q("'darauf' hangi ismin yerini tutuyor?", ["cevabın", "seyahatin", "sorunun"], 0, "İkinci paragrafta Antwort kelimesine dönüyor."),
                _q("Akşam ne yapıyorlar?", ["Sinemaya gidiyorlar", "Sorun hakkında düşünüp birlikte çalışıyorlar", "Bilet alıyorlar"], 1, "Üçüncü paragraf bunu anlatıyor."),
                _q("Metinde 'trotzdem' neyi gösteriyor?", ["Beklenenin aksine sakin kalmalarını", "Yeni oteli", "Bir fiyat bilgisini"], 0, "Sorun olsa da sakin kalmaya devam ediyorlar."),
            ],
        ),
        _module(
            "a2-l5-a1-review",
            "A1 Köprü Tekrarı",
            "A1 soru ve zaman kalıplarını A2 referans yapılarıyla birleştir.",
            [
                _q("'Daha sonra bunun hakkında konuşacağız' cümlesi hangisi?", ["Wir sprechen später darüber.", "Wir sprechen darüber später sein.", "Später darüber wir sprechen."], 0, "Ana cümle düzeni korunur."),
                _q("'Onu bekliyorum' için doğru cevap hangisi?", ["Ich warte daran.", "Ich warte darauf.", "Ich warte darüber."], 1, "warten auf -> darauf olur."),
                _q("'Onu düşünüyorum' cümlesindeki doğru da-yapısı hangisi?", ["damit", "darauf", "daran"], 2, "denken an -> daran cevabı verir."),
                _q("'Bununla çalışıyorum' cümlesi hangisi?", ["Ich arbeite damit.", "Ich arbeite darauf.", "Ich arbeite daran auf."], 0, "mit ile kurulan araç ilişkisi damit olur."),
            ],
        ),
    ],
)

_replace_dialogue(
    6,
    "Dünkü sorunlu gün",
    [
        ("A", "Warum bist du heute so müde?", "Bugün neden bu kadar yorgunsun?"),
        ("B", "Ich konnte letzte Nacht fast nicht schlafen, weil der Nachbar sehr laut war.", "Geçen gece neredeyse hiç uyuyamadım çünkü komşu çok gürültülüydü."),
        ("A", "Musstest du trotzdem früh aufstehen?", "Yine de erken kalkmak zorunda mıydın?"),
        ("B", "Ja, ich musste um sechs Uhr aufstehen und wollte eigentlich zu Hause bleiben.", "Evet, saat altıda kalkmak zorundaydım ve aslında evde kalmak istiyordum."),
        ("A", "Durftest du später wenigstens früher gehen?", "Sonra hiç değilse daha erken çıkmana izin verildi mi?"),
        ("B", "Leider nicht. Ich sollte noch ein Formular fertig machen.", "Ne yazık ki hayır. Bir formu daha bitirmem gerekiyordu."),
    ],
)
_replace_reading(
    6,
    "Bir gün planlandığı gibi gitmedi",
    "12 kelime / kalıp",
    [
        "[[Murat::kişi adı]] wollte gestern eigentlich früh nach Hause gehen. Er war schon am Morgen sehr [[müde::yorgun]], weil er in der Nacht kaum [[schlafen::uyumak]] konnte.",
        "Im Büro musste er aber länger bleiben, denn eine Kollegin war krank. Deshalb musste er mehrere [[Aufgaben::görevler]] allein machen und durfte die Arbeit nicht einfach verschieben.",
        "Am Abend wollte Murat nur noch essen und schlafen. Trotzdem sollte er noch seine Mutter anrufen, weil sie auf eine wichtige [[Antwort::cevap]] wartete.",
    ],
)
_extend_phrase_bank(
    6,
    [
        ("Ich konnte letzte Nacht nicht schlafen.", "Geçen gece uyuyamadım.", "A1 günlük rutin fiilleri geçmiş modal yapıyla dönüyor."),
        ("Ich musste heute früh aufstehen.", "Bugün erken kalkmak zorundaydım.", "A1 saat ve rutin bilgisi tekrar ediyor."),
        ("Ich wollte am Abend zu Hause bleiben.", "Akşam evde kalmak istedim.", "A1 yer ve tercih dili birleşiyor."),
        ("Später sollte ich noch meine Mutter anrufen.", "Daha sonra annemi aramam gerekiyordu.", "A1 aile kelimeleri A2 geçmiş yapıya bağlanıyor."),
    ],
)
_set_extra_exercises(
    6,
    [
        _module(
            "a2-l6-dialogue-comprehension",
            "Diyalog Anlama",
            "Geçmişte ne mümkün oldu, ne zorunlu oldu, bunu ayır.",
            [
                _q("B kişisi neden uyuyamadı?", ["İşe geç kaldığı için", "Komşu gürültülü olduğu için", "Telefonu bozulduğu için"], 1, "İlk yanıtta komşunun gürültülü olduğu söyleniyor."),
                _q("Saat kaçta kalkmak zorunda kaldı?", ["Altıda", "Yedide", "Dokuzda"], 0, "Um sechs Uhr ifadesi geçiyor."),
                _q("Erken çıkmasına izin verildi mi?", ["Evet", "Hayır", "Sadece öğleden sonra"], 1, "Leider nicht diyor."),
                _q("Bitirmesi gereken şey neydi?", ["Bir mektup", "Bir form", "Bir rezervasyon"], 1, "Formular kelimesi son satırda geçiyor."),
            ],
        ),
        _module(
            "a2-l6-reading-comprehension",
            "Okuma Anlama",
            "Modal geçmiş cümlelerin tonunu doğru oku.",
            [
                _q("Murat aslında ne yapmak istiyordu?", ["Arkadaşlarını ziyaret etmek", "Erken eve gitmek", "Yeni bir iş aramak"], 1, "İlk paragraf bunu açık söylüyor."),
                _q("Neden daha uzun kalmak zorunda kaldı?", ["Treni kaçırdığı için", "Bir meslektaşı hasta olduğu için", "Bankaya gitmesi gerektiği için"], 1, "İkinci paragrafta Kollegin krank bilgisi var."),
                _q("Akşam yine de ne yapması gerekiyordu?", ["Annesini aramak", "Müzeye gitmek", "Yemek siparişi vermek"], 0, "Üçüncü paragrafta annesini araması gerektiği yazıyor."),
                _q("Metindeki 'durfte ... nicht' neyi anlatıyor?", ["Yetenek", "İzin / yasak sınırı", "Gelecek planı"], 1, "İzin verilmemesini anlatıyor."),
            ],
        ),
        _module(
            "a2-l6-a1-review",
            "A1 Köprü Tekrarı",
            "A1 rutin ve aile kelimelerini geçmiş modal yapılarla tekrar et.",
            [
                _q("'Annemi aramak istedim' cümlesi hangisi?", ["Ich wollte meine Mutter anrufen.", "Ich wollte meine Mutter angerufen.", "Ich habe wollte meine Mutter anrufen."], 0, "Modal geçmişte asıl fiil yalın kalır."),
                _q("'Bugün çok yorgundum' için doğru yapı hangisi?", ["Ich war heute sehr müde.", "Ich konnte heute sehr müde.", "Ich habe sehr müde."], 0, "A1 sein + sıfat yapısı burada temel kalıptır."),
                _q("'Saat altıda kalkmak zorundaydım' cümlesi hangisi?", ["Ich musste um sechs Uhr aufstehen.", "Ich musste um sechs Uhr aufgestanden.", "Ich bin um sechs Uhr müssen aufstehen."], 0, "Modal fiil çekilir, asıl fiil sonda yalın kalır."),
                _q("'Komşu' için doğru kelime hangisi?", ["der Nachbar", "die Rechnung", "das Bett"], 0, "Günlük hayat bağlamında sık kullanılan isimdir."),
            ],
        ),
    ],
)

_replace_dialogue(
    7,
    "Mağazada daha bilinçli seçim",
    [
        ("A", "Suchst du etwas Bestimmtes?", "Belirli bir şey mi arıyorsun?"),
        ("B", "Ja, ich brauche eine schwarze Jacke, weil meine alte zu klein geworden ist.", "Evet, siyah bir ceket lazım çünkü eskisi artık küçük geldi."),
        ("A", "Wie findest du diese hier?", "Buradaki hakkında ne düşünüyorsun?"),
        ("B", "Sie gefällt mir, aber sie ist ein bisschen zu teuer und die Ärmel sind zu lang.", "Hoşuma gidiyor ama biraz pahalı ve kolları fazla uzun."),
        ("A", "Dann probier doch die blaue Jacke in Größe 38 an.", "O zaman 38 beden mavi ceketi dene."),
        ("B", "Gute Idee. Wenn sie mir passt, kaufe ich sie heute.", "İyi fikir. Bana olursa bugün onu alırım."),
    ],
)
_replace_reading(
    7,
    "Bir mağazada karar vermek",
    "12 kelime / kalıp",
    [
        "[[Aylin::kişi adı]] möchte heute eine neue [[Jacke::ceket]] kaufen. Sie sucht etwas [[Bequemes::rahat bir şey]] für den Alltag, aber die Farbe soll auch zu ihren schwarzen [[Schuhen::ayakkabılar]] passen.",
        "Im Geschäft probiert sie zuerst einen grauen [[Mantel::palto]] an. Der Mantel ist schön, aber die [[Ärmel::kollar]] sind zu lang und der [[Preis::fiyat]] ist höher als erwartet.",
        "Danach findet sie eine dunkelblaue Jacke. Sie ist nicht am [[günstigsten::en uygun fiyatlı]], aber sie sitzt besser, sieht moderner aus und passt gut zu ihrer Tasche und ihrem [[Kleidungsstil::giyim tarzı]].",
    ],
)
_extend_phrase_bank(
    7,
    [
        ("Die Jacke gefällt mir, aber sie ist zu teuer.", "Ceket hoşuma gidiyor ama fazla pahalı.", "A1 beğeni ve fiyat kelimeleri A2 seçim diline bağlanıyor."),
        ("In Größe 38 passt sie mir besser.", "38 bedende bana daha iyi oluyor.", "A1 sayılar yeni bağlamda tekrar ediyor."),
        ("Meine schwarzen Schuhe passen gut dazu.", "Siyah ayakkabılarım buna iyi uyuyor.", "A1 renk bilgisi korunuyor."),
        ("Wenn sie bequem ist, kaufe ich sie heute.", "Rahatsa onu bugün alırım.", "A1 günlük fiiller ve wenn bir araya geliyor."),
    ],
)
_set_extra_exercises(
    7,
    [
        _module(
            "a2-l7-dialogue-comprehension",
            "Diyalog Anlama",
            "Ürün değerlendirme gerekçelerini ayır.",
            [
                _q("B kişisi neden yeni ceket arıyor?", ["Eskisi kaybolduğu için", "Eskisi küçük geldiği için", "Rengi mavi olmadığı için"], 1, "İlk yanıtta eski ceketin küçük geldiği söyleniyor."),
                _q("İlk cekette sorun ne?", ["Çok geniş olması", "Kollarının kısa olması", "Fazla pahalı ve kollarının uzun olması"], 2, "İki sorun aynı cümlede veriliyor."),
                _q("A kişisi hangi bedeni öneriyor?", ["36", "38", "40"], 1, "Größe 38 öneriliyor."),
                _q("B kişisi hangi durumda ceketi alacak?", ["Rengi siyah olursa", "Bugün ucuzlarsa", "Üzerine olursa"], 2, "Wenn sie mir passt ifadesi bunu veriyor."),
            ],
        ),
        _module(
            "a2-l7-reading-comprehension",
            "Okuma Anlama",
            "Bir ürünü neden seçtiğini dikkatle oku.",
            [
                _q("Aylin önce ne arıyor?", ["Günlük kullanım için rahat bir ceket", "Yeni bir elbise", "Bir bavul"], 0, "İlk paragraf tam olarak bunu söylüyor."),
                _q("Gri palto neden eleniyor?", ["Rengi çok koyu olduğu için", "Kolları uzun ve fiyatı yüksek olduğu için", "Bedeni olmadığı için"], 1, "İkinci paragrafta bu iki neden veriliyor."),
                _q("Sonunda hangi ürün daha uygun görünüyor?", ["Lacivert ceket", "Gri palto", "Kırmızı bluz"], 0, "Üçüncü paragraf lacivert cekete yöneliyor."),
                _q("'Kleidungsstil' kelimesi burada neyi tamamlıyor?", ["Fiyat bilgisini", "Giyim tarzı uyumunu", "Beden tablosunu"], 1, "Ceketin tarz uyumunu anlatıyor."),
            ],
        ),
        _module(
            "a2-l7-a1-review",
            "A1 Köprü Tekrarı",
            "A1 renkler, sayılar ve temel kıyafetleri A2 değerlendirme diliyle tekrar et.",
            [
                _q("'Siyah ceket' için doğru grup hangisi?", ["eine schwarze Jacke", "eine schwarz Jacke", "ein schwarzes Jacke"], 0, "Dişil isimle temel sıfat uyumu burada kuruluyor."),
                _q("'38 beden' ifadesinde sayı hangisi?", ["achtunddreißig", "dreizehn", "zwanzig"], 0, "38 = achtunddreißig."),
                _q("'Ayakkabılarım buna uyuyor' cümlesinde doğru fiil hangisi?", ["gefällt", "passt", "wartet"], 1, "passen uyum ve beden ilişkisini anlatır."),
                _q("'Pahalı' anlamına gelen sıfat hangisi?", ["teuer", "ruhig", "krank"], 0, "Fiyat değerlendirmesinin temel sıfatıdır."),
            ],
        ),
    ],
)

_replace_dialogue(
    8,
    "Gerekçe ve karşıtlıkla konuşma",
    [
        ("A", "Kommst du heute Abend auch zum Kurs?", "Bu akşam kursa sen de geliyor musun?"),
        ("B", "Eigentlich bin ich sehr müde. Trotzdem komme ich, weil morgen die Prüfung ist.", "Aslında çok yorgunum. Yine de geliyorum çünkü yarın sınav var."),
        ("A", "Ich habe heute viel Arbeit. Deshalb komme ich vielleicht zehn Minuten später.", "Bugün çok işim var. Bu yüzden belki on dakika geç geleceğim."),
        ("B", "Kein Problem. Wenn du später kommst, reserviere ich dir einen Platz.", "Sorun değil. Geç gelirsen sana bir yer ayırırım."),
        ("A", "Super. Der Bus hat oft Verspätung, trotzdem möchte ich pünktlich sein.", "Harika. Otobüs sık sık gecikiyor, yine de zamanında olmak istiyorum."),
        ("B", "Dann schreib mir kurz, deshalb warte ich am Eingang auf dich.", "O zaman bana kısaca yaz, böylece girişte seni beklerim."),
    ],
)
_replace_reading(
    8,
    "Bir akşam planı neden değişti?",
    "12 kelime / kalıp",
    [
        "[[Ece::kişi adı]] wollte heute nach der Arbeit direkt nach Hause gehen. Sie war sehr [[müde::yorgun]] und hatte am Morgen schon viel [[Stress::stres]].",
        "Trotzdem bleibt sie nicht zu Hause, weil morgen eine wichtige [[Prüfung::sınav]] ist. Deshalb packt sie ihre Unterlagen schnell ein und fährt später noch zum [[Kurs::kurs]].",
        "Der Bus kommt wie so oft zu spät. Trotzdem bleibt Ece ruhig, schreibt ihrer Freundin eine kurze [[Nachricht::mesaj]] und kommt am Ende doch noch [[pünktlich::zamanında]] an.",
    ],
)
_extend_phrase_bank(
    8,
    [
        ("Ich bin müde. Trotzdem komme ich.", "Yorgunum. Yine de geliyorum.", "A1 hâl-hatır kalıbı bağlayıcılarla büyüyor."),
        ("Der Bus ist spät. Deshalb fahren wir später.", "Otobüs geç. Bu yüzden daha geç gidiyoruz.", "A1 ulaşım dili tekrar ediyor."),
        ("Wenn du später kommst, schreibe mir kurz.", "Geç gelirsen bana kısaca yaz.", "A1 kısa mesaj ve zaman bilgisi birleşiyor."),
        ("Ich möchte trotzdem pünktlich sein.", "Yine de zamanında olmak istiyorum.", "A1 istek dili bu derste sebep-sonuçla bağlanıyor."),
    ],
)
_set_extra_exercises(
    8,
    [
        _module(
            "a2-l8-dialogue-comprehension",
            "Diyalog Anlama",
            "deshalb ve trotzdem yönünü doğru izle.",
            [
                _q("B kişisi neden yine de kursa geliyor?", ["Arkadaşını görmek için", "Yarın sınav olduğu için", "Otobüs zamanında geldiği için"], 1, "Yarın sınav olduğu bilgisi veriliyor."),
                _q("A kişisi neden geç kalabilir?", ["Evde kaldığı için", "Çok işi olduğu için", "Kursa gitmek istemediği için"], 1, "Heute viel Arbeit dediği için."),
                _q("B kişisi ne teklif ediyor?", ["Telefon açmayı", "Yer ayırmayı", "Otobüs çağırmayı"], 1, "Einen Platz reserviere ich diyor."),
                _q("'deshalb warte ich am Eingang' neyi anlatıyor?", ["Sonucu", "Rica tonunu", "Fiyat bilgisini"], 0, "deshalb bir sonuç ilişkisi kuruyor."),
            ],
        ),
        _module(
            "a2-l8-reading-comprehension",
            "Okuma Anlama",
            "Plan değişikliğini neden-sonuç ilişkileriyle çöz.",
            [
                _q("Ece önce ne yapmak istiyordu?", ["Doğrudan eve gitmek", "Sinemaya gitmek", "Bankaya uğramak"], 0, "İlk paragraf bunu söylüyor."),
                _q("Neden planını değiştiriyor?", ["Arkadaşı aradığı için", "Sınav olduğu için", "Yağmur yağdığı için"], 1, "İkinci paragrafta sınav bilgisi var."),
                _q("Otobüs geç gelince ne yapıyor?", ["Eve dönüyor", "Arkadaşına mesaj yazıyor", "Kursu iptal ediyor"], 1, "Üçüncü paragrafta kısa mesaj yazdığı belirtiliyor."),
                _q("'doch noch pünktlich' neyi vurguluyor?", ["Beklenenin aksine zamanında varmayı", "Geç gelmeyi", "Dersin iptal olduğunu"], 0, "Trotzdem mantığını destekliyor."),
            ],
        ),
        _module(
            "a2-l8-a1-review",
            "A1 Köprü Tekrarı",
            "A1 günlük plan kelimelerini bağlayıcılarla tekrar et.",
            [
                _q("'Bu yüzden' kelimesi hangisi?", ["trotzdem", "deshalb", "morgen"], 1, "Sebep-sonuç bağlayıcısı deshalb'tır."),
                _q("'Yine de' anlamı hangisi?", ["pünktlich", "trotzdem", "später"], 1, "Karşıt sonuç için trotzdem kullanılır."),
                _q("'Yorgunum ama geliyorum' anlamına en yakın seçenek hangisi?", ["Ich bin müde. Trotzdem komme ich.", "Ich bin müde. Deshalb komme ich.", "Ich komme müde trotzdem bin."], 0, "Yorgunluk beklenenin aksine gelmeyi engellemiyor."),
                _q("'Otobüs geç geliyor' cümlesi hangisi?", ["Der Bus kommt spät.", "Der Bus ist links.", "Der Bus wartet müde."], 0, "A1 ulaşım cümlesi bu derste tekrar eder."),
            ],
        ),
    ],
)

# A2 final readability pass: remove proper-noun tooltips and deepen lessons 9-14.

_replace_reading(
    1,
    "Yoğun ama güzel bir hafta sonu",
    "14 kelime / kalıp",
    [
        "Am Freitagabend hat eine junge Frau lange für einen [[Test::sınav]] gelernt. Trotzdem hat sie noch ihre [[Tasche::çanta]] vorbereitet, weil sie am nächsten Morgen früh [[losgefahren::yola çıktı]] ist.",
        "Am Samstag hat sie zuerst mit ihrer [[Familie::aile]] [[gefrühstückt::kahvaltı yaptı]] und später ihre Großmutter [[besucht::ziyaret etti]]. Dort haben sie zusammen Kaffee getrunken und alte [[Fotos::fotoğraflar]] angeschaut.",
        "Am Sonntag ist sie mit einer Freundin ins [[Museum::müze]] gegangen. Sie haben eine [[Eintrittskarte::giriş bileti]] gekauft, viel geredet und sind am Abend müde, aber zufrieden nach Hause [[zurückgekommen::geri döndü]].",
    ],
)

_replace_reading(
    2,
    "Bir öğrencinin yeni odası",
    "14 kelime / kalıp",
    [
        "Nach dem Umzug ordnet ein Student seine [[Wohnung::ev]] neu. Das [[Regal::raf]] steht jetzt links, und der [[Schreibtisch::çalışma masası]] steht direkt am [[Fenster::pencere]].",
        "Auf dem Tisch liegt ein [[Wörterbuch::sözlük]], daneben liegt ein [[Heft::defter]] und über dem Tisch hängt eine helle [[Lampe::lamba]]. Unter dem Tisch steht noch eine Kiste mit alten [[Büchern::kitaplar]].",
        "Wenn Freunde zu Besuch kommen, können sie sofort sehen, wo alles ist. Der [[Stuhl::sandalye]] steht vor dem Tisch, die [[Tasche::çanta]] liegt hinter der Tür und in der [[Ecke::köşe]] steht eine grüne Pflanze.",
    ],
)

_replace_reading(
    3,
    "Akşam yemeğinde küçük sorunlar",
    "14 kelime / kalıp",
    [
        "Nach der Arbeit geht eine Angestellte in ein [[Restaurant::restoran]]. Sie ist müde, möchte aber trotzdem in Ruhe essen und noch kurz ihre [[E-Mails::e-postalar]] kontrollieren.",
        "Zuerst bestellt sie eine [[Suppe::çorba]], einen [[Salat::salata]] und ein großes [[Wasser::su]]. Danach merkt sie, dass im Salat zu viele [[Zwiebeln::soğanlar]] sind, deshalb bittet sie höflich um eine andere Portion.",
        "Der [[Kellner::garson]] reagiert freundlich und bringt später noch einen [[Kaffee::kahve]]. Am Ende fragt die Frau nach der [[Rechnung::hesap]] und bezahlt mit Karte, weil sie kein Bargeld dabei hat.",
    ],
)

_replace_reading(
    4,
    "Nazik olmak neden fark yaratır?",
    "14 kelime / kalıp",
    [
        "Eine Kursteilnehmerin geht heute ins Büro der Schule, weil sie ein neues [[Gespräch::görüşme]] braucht. Sie sagt nicht direkt \"Ich will einen Termin\", sondern benutzt höfliche [[Formulierungen::ifadeler]].",
        "Am Schalter sagt sie: Ich [[würde::isterdim]] gern mit der Lehrerin sprechen und ich hätte gern mehr [[Informationen::bilgiler]] über den neuen Kurs. Danach fragt sie: [[Könnten Sie::edebilir misiniz]] mir bitte auch die neue Adresse schicken?",
        "Die Mitarbeiterin antwortet freundlich. Gerade in solchen Situationen merkt die Teilnehmerin, dass ein ruhiger Ton oft schneller zu einer guten [[Lösung::çözüm]] führt.",
    ],
)

_replace_reading(
    5,
    "Tekrarsız konuşmak",
    "14 kelime / kalıp",
    [
        "Zwei Geschwister sprechen oft über ihre nächste [[Reise::seyahat]]. Früher haben sie immer wieder denselben Plan genannt, aber jetzt benutzen sie öfter Verweise wie [[darüber::bunun hakkında]] und [[daran::onu düşünerek]].",
        "Einer von ihnen wartet auf eine [[Antwort::cevap]] vom Hotel. Er sagt nicht jedes Mal \"Ich warte auf die Antwort\", sondern oft nur: Ich warte schon lange [[darauf::onu bekliyorum]].",
        "Später sprechen beide über ein neues [[Problem::sorun]] mit den Tickets. Trotzdem bleiben sie ruhig, denken kurz [[darüber::bunun hakkında]] nach und arbeiten am Abend gemeinsam [[damit::bununla]].",
    ],
)

_replace_reading(
    6,
    "Bir gün planlandığı gibi gitmedi",
    "14 kelime / kalıp",
    [
        "Ein Angestellter wollte gestern eigentlich früh nach Hause gehen. Er war schon am Morgen sehr [[müde::yorgun]], weil er in der Nacht kaum [[schlafen::uyumak]] konnte.",
        "Im Büro musste er aber länger bleiben, denn eine Kollegin war krank. Deshalb musste er mehrere [[Aufgaben::görevler]] allein machen und durfte die Arbeit nicht einfach verschieben.",
        "Am Abend wollte er nur noch essen und schlafen. Trotzdem sollte er noch seine Mutter anrufen, weil sie auf eine wichtige [[Antwort::cevap]] wartete.",
    ],
)

_replace_reading(
    7,
    "Bir mağazada karar vermek",
    "14 kelime / kalıp",
    [
        "Eine Kundin möchte heute eine neue [[Jacke::ceket]] kaufen. Sie sucht etwas [[Bequemes::rahat bir şey]] für den Alltag, aber die Farbe soll auch zu ihren schwarzen [[Schuhen::ayakkabılar]] passen.",
        "Im Geschäft probiert sie zuerst einen grauen [[Mantel::palto]] an. Der Mantel ist schön, aber die [[Ärmel::kollar]] sind zu lang und der [[Preis::fiyat]] ist höher als erwartet.",
        "Danach findet sie eine dunkelblaue Jacke. Sie ist nicht am [[günstigsten::en uygun fiyatlı]], aber sie sitzt besser, sieht moderner aus und passt gut zu ihrer Tasche und ihrem [[Kleidungsstil::giyim tarzı]].",
    ],
)

_replace_reading(
    8,
    "Bir akşam planı neden değişti?",
    "14 kelime / kalıp",
    [
        "Eine Teilnehmerin wollte heute nach der Arbeit direkt nach Hause gehen. Sie war sehr [[müde::yorgun]] und hatte am Morgen schon viel [[Stress::stres]].",
        "Trotzdem bleibt sie nicht zu Hause, weil morgen eine wichtige [[Prüfung::sınav]] ist. Deshalb packt sie ihre Unterlagen schnell ein und fährt später noch zum [[Kurs::kurs]].",
        "Der Bus kommt wie so oft zu spät. Trotzdem bleibt sie ruhig, schreibt ihrer Freundin eine kurze [[Nachricht::mesaj]] und kommt am Ende doch noch [[pünktlich::zamanında]] an.",
    ],
)

_replace_dialogue(
    9,
    "İki seçenek arasında gerçekten karar verme",
    [
        ("A", "Welches Fahrrad findest du besser: das rote oder das schwarze?", "Sence hangi bisiklet daha iyi: kırmızı olan mı siyah olan mı?"),
        ("B", "Das schwarze ist etwas teurer, aber es ist auch leichter und bequemer.", "Siyah olan biraz daha pahalı ama aynı zamanda daha hafif ve daha rahat."),
        ("A", "Ich dachte, das rote sei günstiger und deshalb praktischer für den Alltag.", "Kırmızının daha ucuz olduğu için günlük kullanımda daha pratik olduğunu düşünmüştüm."),
        ("B", "Vielleicht, aber das schwarze fährt schneller und der Sattel ist deutlich besser.", "Belki ama siyah olan daha hızlı gidiyor ve selesi belirgin biçimde daha iyi."),
        ("A", "Welches Modell ist denn am beliebtesten?", "Peki en popüler model hangisi?"),
        ("B", "Der Verkäufer meinte, dass das schwarze im Moment das zuverlässigste Modell ist.", "Satıcı şu anda siyah olanın en güvenilir model olduğunu söyledi."),
    ],
)
_replace_reading(
    9,
    "Hangisi gerçekten daha uygun?",
    "14 kelime / kalıp",
    [
        "Zwei Freunde vergleichen heute drei [[Fahrräder::bisikletler]]. Das erste Modell ist [[günstiger::daha ucuz]], das zweite ist [[leichter::daha hafif]] und das dritte sieht am modernsten aus.",
        "Für den Weg zur Arbeit ist nicht nur der [[Preis::fiyat]] wichtig. Ein Freund achtet mehr auf einen [[bequemen::rahat]] Sattel, der andere denkt eher an die tägliche [[Strecke::güzergâh]].",
        "Am Ende wählen sie nicht das billigste, sondern das [[zuverlässigste::en güvenilir]] Fahrrad. Es kostet etwas mehr, ist aber für den Alltag [[praktischer::daha kullanışlı]] und auf längeren Wegen deutlich angenehmer.",
    ],
)
_extend_phrase_bank(
    9,
    [
        ("Dieses Modell ist günstiger als das andere.", "Bu model diğerinden daha ucuz.", "A1 fiyat dili komparativ ile genişliyor."),
        ("Der schwarze Rucksack ist am praktischsten.", "Siyah sırt çantası en kullanışlı olan.", "A1 renk ve eşya bilgisi superlativ ile birleşiyor."),
        ("Der Weg zur Arbeit ist heute länger als sonst.", "İşe giden yol bugün normalden daha uzun.", "A1 günlük rutin dili kıyaslamaya taşınıyor."),
        ("Am Wochenende fahren wir lieber mit dem bequemeren Zug.", "Hafta sonunda daha rahat trenle gitmeyi tercih ediyoruz.", "A1 ulaşım dili yeniden kullanılıyor."),
    ],
)
_set_extra_exercises(
    9,
    [
        _module(
            "a2-l9-dialogue-comprehension",
            "Diyalog Anlama",
            "Komparativ ve superlativ karar dilini doğru oku.",
            [
                _q("Siyah bisiklet neden tercih ediliyor?", ["Daha ucuz olduğu için", "Daha hafif ve daha rahat olduğu için", "Daha küçük olduğu için"], 1, "İkinci ve dördüncü satırlar bu iki nedeni veriyor."),
                _q("A kişisi önce hangi avantajı vurguluyor?", ["Kırmızı modelin daha ucuz olduğunu", "Siyah modelin daha hafif olduğunu", "Üçüncü modelin en hızlı olduğunu"], 0, "A ilk olarak fiyat avantajını söylüyor."),
                _q("En popüler model hangisi olarak sunuluyor?", ["Kırmızı model", "Siyah model", "Hiçbiri"], 1, "Verkäufer siyah modeli öne çıkarıyor."),
                _q("'zuverlässigste' burada ne anlatıyor?", ["En güvenilir olanı", "En parlak olanı", "En yavaş olanı"], 0, "Superlativ kalıbı güvenilirliği en üst düzeyde veriyor."),
            ],
        ),
        _module(
            "a2-l9-reading-comprehension",
            "Okuma Anlama",
            "Karşılaştırma metninde hangi ölçütün niçin seçildiğini bul.",
            [
                _q("Arkadaşlar kaç bisikleti karşılaştırıyor?", ["İki", "Üç", "Dört"], 1, "İlk cümlede üç model geçtiği söyleniyor."),
                _q("Hangi unsur tek başına yeterli görülmüyor?", ["Renk", "Fiyat", "Yağmur"], 1, "İkinci paragraf fiyatın tek ölçüt olmadığını söylüyor."),
                _q("Sonunda neden en ucuz model seçilmiyor?", ["Çünkü daha az güvenilir", "Çünkü çok büyük", "Çünkü kırmızı değil"], 0, "Son paragraf güvenilirlik ve pratikliği öne çıkarıyor."),
                _q("'praktischer' burada neye karşılık geliyor?", ["Daha pahalı", "Daha kullanışlı", "Daha sessiz"], 1, "Kelime işlevsellik karşılaştırması yapıyor."),
            ],
        ),
        _module(
            "a2-l9-a1-review",
            "A1 Köprü Tekrarı",
            "A1 eşya, renk ve günlük yol kelimelerini kıyaslamayla tekrar et.",
            [
                _q("'Daha uzun' için doğru biçim hangisi?", ["lang", "länger", "am lang"], 1, "lang -> länger olur."),
                _q("'En rahat tren' grubu hangisi?", ["der bequeme Zug", "der bequemste Zug", "am bequem Zug"], 1, "Superlativ sıfat grubu bu şekilde kurulur."),
                _q("'Daha ucuz çanta' için doğru seçenek hangisi?", ["eine günstigere Tasche", "eine günstige Tasche als", "eine am günstig Tasche"], 0, "Dişil isimle komparativ burada böyle kurulur."),
                _q("A1'de öğrenilen hangi alan burada tekrar ediyor?", ["Renkler ve günlük eşyalar", "Sadece ay isimleri", "Sadece telefon numaraları"], 0, "Bu derste A1 renk ve eşya kelimeleri bilinçli olarak dönüyor."),
            ],
        ),
    ],
)

_replace_dialogue(
    10,
    "Ne oluyor, ne olmuş durumda?",
    [
        ("A", "Wird der Besprechungsraum heute noch vorbereitet?", "Toplantı odası bugün hâlâ hazırlanıyor mu?"),
        ("B", "Ja, die Stühle werden schon gestellt und die Präsentation wird gerade getestet.", "Evet, sandalyeler şimdiden yerleştiriliyor ve sunum şu anda test ediliyor."),
        ("A", "Und ist der Vertrag schon unterschrieben?", "Peki sözleşme çoktan imzalanmış durumda mı?"),
        ("B", "Nein, er wird erst am Nachmittag unterschrieben, aber die Kopien sind schon gedruckt.", "Hayır, ancak öğleden sonra imzalanacak ama kopyalar çoktan basılmış durumda."),
        ("A", "Gut, dann können die Gäste pünktlich informiert werden.", "İyi, o zaman misafirler zamanında bilgilendirilebilir."),
        ("B", "Genau. Sobald alles fertig ist, wird die Tür geöffnet.", "Aynen. Her şey hazır olur olmaz kapı açılacak."),
    ],
)
_replace_reading(
    10,
    "Ofiste küçük duyuru",
    "14 kelime / kalıp",
    [
        "Im Büro wird heute ein wichtiger [[Raum::oda]] für Gäste vorbereitet. Die [[Stühle::sandalyeler]] werden gestellt, die Getränke werden gebracht und die Technik wird noch einmal [[getestet::test ediliyor]].",
        "Einige Dokumente sind schon [[gedruckt::basılmış]] und die Namensschilder sind fertig [[geschrieben::yazılmış]]. Der Vertrag ist aber noch nicht [[unterschrieben::imzalanmış]], deshalb wartet das Team auf den Chef.",
        "Am Nachmittag wird alles noch einmal kontrolliert. Erst dann wird die Tür geöffnet und die Gruppe wird offiziell [[begrüßt::karşılanıyor]].",
    ],
)
_extend_phrase_bank(
    10,
    [
        ("Die Tür wird geöffnet.", "Kapı açılıyor.", "İşlemi yapan kişi önemli değilse Vorgangspassiv kurulur."),
        ("Die Unterlagen sind gedruckt.", "Belgeler basılmış durumda.", "Sonuç durumu anlatılırken Zustandspassiv görünür."),
        ("Die Gäste werden informiert.", "Misafirler bilgilendiriliyor.", "A1 kişi ve çoğul bilgisi pasif yapıya taşınır."),
        ("Am Nachmittag wird alles kontrolliert.", "Öğleden sonra her şey kontrol ediliyor.", "A1 zaman zarfı pasif cümlede de korunur."),
    ],
)
_set_extra_exercises(
    10,
    [
        _module(
            "a2-l10-dialogue-comprehension",
            "Diyalog Anlama",
            "Vorgang ve sonuç durumunu ayır.",
            [
                _q("Şu anda test edilen şey nedir?", ["Sunum", "Sözleşme", "Kapı"], 0, "Präsentation wird gerade getestet deniyor."),
                _q("Henüz imzalanmamış olan nedir?", ["Kopyalar", "Sözleşme", "Nametags"], 1, "Erst am Nachmittag unterschrieben deniyor."),
                _q("Çoktan tamamlanmış olan hangisi?", ["Kapının açılması", "Kopyaların basılması", "Misafirlerin gelişi"], 1, "Kopien sind schon gedruckt ifadesi sonuç durumunu veriyor."),
                _q("Kapı ne zaman açılacak?", ["Her şey hazır olunca", "Sabah erkenden", "Hiç açılmayacak"], 0, "Sobald alles fertig ist cümlesi bunu söylüyor."),
            ],
        ),
        _module(
            "a2-l10-reading-comprehension",
            "Okuma Anlama",
            "Pasif yapının neden seçildiğini fark et.",
            [
                _q("Metin neden çoğunlukla pasif kullanıyor?", ["İşi yapan kişi önemsiz olduğu için", "Hiç fiil kullanılmadığı için", "Sadece geçmiş anlatıldığı için"], 0, "Ofis hazırlığında odak süreç ve sonuçlarda."),
                _q("Hangi iki şey zaten hazır durumda?", ["Stühle ve Getränke", "Dokümanlar ve isimlikler", "Chef ve Gäste"], 1, "İkinci paragraf bunu açık veriyor."),
                _q("Takım neden bekliyor?", ["Otobüs geciktiği için", "Şef sözleşmeyi imzalayacağı için", "Oda küçük olduğu için"], 1, "Chef bekleniyor çünkü sözleşme henüz imzalanmadı."),
                _q("'wird offiziell begrüßt' neyi anlatıyor?", ["Sonuç durumunu", "Karşılama sürecini", "Emir kipini"], 1, "Burada bir işlem gerçekleşiyor."),
            ],
        ),
        _module(
            "a2-l10-a1-review",
            "A1 Köprü Tekrarı",
            "A1 oda, zaman ve çoğul kelimelerini pasif içinde tekrar et.",
            [
                _q("'Sandalyeler yerleştiriliyor' cümlesi hangisi?", ["Die Stühle werden gestellt.", "Die Stühle sind stellen.", "Die Stühle werden gestellt sein."], 0, "Vorgangspassiv temel kalıbı burada görülür."),
                _q("'Belgeler basılmış durumda' cümlesi hangisi?", ["Die Unterlagen werden drucken.", "Die Unterlagen sind gedruckt.", "Die Unterlagen haben gedruckt."], 1, "Sonuç durumunu anlatır."),
                _q("A1'deki hangi alan bu derste tekrar ediyor?", ["Oda ve eşya kelimeleri", "Sadece mevsimler", "Sadece aile üyeleri"], 0, "Raum, Stühle gibi kelimeler bilinçli olarak dönüyor."),
                _q("'Öğleden sonra' Almanca hangisi?", ["am Nachmittag", "im morgen", "zu Abend"], 0, "A1 zaman ifadisi burada da aynı kalır."),
            ],
        ),
    ],
)

_replace_dialogue(
    11,
    "Resepsiyonda daha doğal konuşma",
    [
        ("A", "Guten Abend. Ich habe ein Zimmer auf den Namen Kaya reserviert.", "İyi akşamlar. Kaya adına bir oda ayırttım."),
        ("B", "Willkommen. Möchten Sie ein ruhiges Zimmer im dritten Stock oder lieber eins näher am Aufzug?", "Hoş geldiniz. Üçüncü katta sakin bir oda mı istersiniz yoksa asansöre daha yakın bir tane mi?"),
        ("A", "Ein ruhiges Zimmer wäre besser, weil ich morgen früh abreise.", "Sakin bir oda daha iyi olur çünkü yarın erken ayrılacağım."),
        ("B", "Kein Problem. Das Frühstück ist ab sieben Uhr im Restaurant und der Wellnessbereich ist bis zehn Uhr geöffnet.", "Sorun değil. Kahvaltı saat yediden itibaren restoranda ve wellness bölümü ona kadar açık."),
        ("A", "Super. Ist das Hotel weit vom Bahnhof entfernt?", "Harika. Otel istasyondan uzak mı?"),
        ("B", "Nein, es ist nur zehn Minuten zu Fuß und direkt im Zentrum.", "Hayır, yürüyerek sadece on dakika ve doğrudan merkezde."),
    ],
)
_replace_reading(
    11,
    "Şehre varış",
    "14 kelime / kalıp",
    [
        "Nach einer langen Reise kommt ein Gast am Abend im [[Hotel::otel]] an. Das Zimmer liegt im dritten [[Stock::kat]] und ist glücklicherweise nicht weit vom [[Aufzug::asansör]] entfernt.",
        "An der [[Rezeption::resepsiyon]] bekommt der Gast noch wichtige Informationen: Das Frühstück ist ab sieben Uhr im Restaurant, und das kleine [[Fitnessstudio::spor salonu]] im Haus ist bis zehn Uhr geöffnet.",
        "Später schreibt der Gast einer Freundin, dass das Hotel direkt im [[Zentrum::merkez]] liegt und man vom [[Bahnhof::istasyon]] aus alles schnell erreichen kann. So beginnt der Aufenthalt deutlich ruhiger als erwartet.",
    ],
)
_extend_phrase_bank(
    11,
    [
        ("Das Hotel liegt direkt im Zentrum.", "Otel doğrudan merkezde bulunuyor.", "A1 yer ifadeleri yeni konaklama diliyle bağlanıyor."),
        ("Das Frühstück ist ab sieben Uhr.", "Kahvaltı saat yediden itibaren.", "A1 saat bilgisi hizmet diliyle birleşiyor."),
        ("Der Bahnhof ist nur zehn Minuten entfernt.", "İstasyon sadece on dakika uzaklıkta.", "A1 ulaşım alanı A2 yolculuk diline taşınıyor."),
        ("Ich habe ein ruhiges Zimmer reserviert.", "Sakin bir oda ayırttım.", "A1 oda ve sıfat bilgisi yeniden kullanılıyor."),
    ],
)
_set_extra_exercises(
    11,
    [
        _module(
            "a2-l11-dialogue-comprehension",
            "Diyalog Anlama",
            "Resepsiyon konuşmasındaki hizmet detaylarını yakala.",
            [
                _q("Misafir nasıl bir oda istiyor?", ["Asansöre yakın", "Sakin", "Daha ucuz"], 1, "Ruhiges Zimmer istediğini söylüyor."),
                _q("Kahvaltı ne zaman başlıyor?", ["Altıda", "Yedide", "Sekizde"], 1, "Ab sieben Uhr ifadesi veriliyor."),
                _q("Otel istasyondan ne kadar uzak?", ["On dakika yaya", "Yarım saat otobüsle", "Çok uzak"], 0, "Nur zehn Minuten zu Fuß deniyor."),
                _q("'im Zentrum' burada neyi anlatıyor?", ["Merkezde bulunmayı", "Merkezden çıkmayı", "Merkeze koşmayı"], 0, "Yer bildiren kısalmış edatlı yapı kullanılıyor."),
            ],
        ),
        _module(
            "a2-l11-reading-comprehension",
            "Okuma Anlama",
            "Konaklama metninde konum ve hizmet bilgilerini çöz.",
            [
                _q("Misafir otele ne zaman varıyor?", ["Sabah erken", "Akşam", "Öğle arasında"], 1, "İlk cümle Abend diyor."),
                _q("Hangi alan saate kadar açık?", ["Restoran", "Fitness alanı", "Resepsiyon"], 1, "İkinci paragrafta fitness alanı geçiyor."),
                _q("Misafir arkadaşına hangi avantajı yazıyor?", ["Otelin merkezde olduğunu", "Odada mutfak bulunduğunu", "Bilet fiyatını"], 0, "Üçüncü paragraf merkez konumunu vurguluyor."),
                _q("'vom Bahnhof aus' neyi kolaylaştırıyor?", ["Her yere hızlı ulaşmayı", "Kahvaltıyı kaçırmayı", "Check-out yapmayı"], 0, "İstasyondan her yere hızlı erişimden bahsediyor."),
            ],
        ),
        _module(
            "a2-l11-a1-review",
            "A1 Köprü Tekrarı",
            "A1 yer, saat ve yolculuk kelimelerini otel bağlamında tekrar et.",
            [
                _q("'Saat yediden itibaren' ifadesi hangisi?", ["ab sieben Uhr", "um sieben später", "seit sieben Uhr nur"], 0, "ab + saat kalıbı burada kullanılıyor."),
                _q("'Merkezde' için doğru seçenek hangisi?", ["im Zentrum", "zu Zentrum", "am Zentrume"], 0, "im = in dem kısalmasıdır."),
                _q("'İstasyondan' anlamına en yakın yapı hangisi?", ["vom Bahnhof", "im Bahnhof", "zum Bahnhof"], 0, "von dem -> vom olur."),
                _q("A1'den hangi alan burada bilinçli dönüyor?", ["Ulaşım ve saatler", "Sadece renkler", "Sadece beden ölçüleri"], 0, "Bahnhof ve saat kalıpları tekrar ediyor."),
            ],
        ),
    ],
)

_replace_dialogue(
    12,
    "Şehir içinde nereye nasıl gidilir?",
    [
        ("A", "Entschuldigung, wie komme ich am schnellsten zum Museum?", "Affedersiniz, müzeye en hızlı nasıl gidebilirim?"),
        ("B", "Gehen Sie zuerst bis zur Ampel und dann nach links zur Brücke.", "Önce ışıklara kadar gidin ve sonra köprüye doğru sola dönün."),
        ("A", "Fahre ich danach mit dem Bus oder gehe ich lieber zu Fuß?", "Bundan sonra otobüsle mi gitsem yoksa yürümem mi daha iyi?"),
        ("B", "Mit dem Bus geht es schneller, aber zu Fuß sehen Sie mehr von der Altstadt.", "Otobüsle daha hızlı olur ama yürürseniz eski şehri daha çok görürsünüz."),
        ("A", "Und wie komme ich später zum Bahnhof?", "Peki sonra istasyona nasıl giderim?"),
        ("B", "Vom Museum aus fahren Sie am besten mit der U-Bahn zum Bahnhof.", "Müzeden sonra en iyisi metro ile istasyona gitmeniz."),
    ],
)
_replace_reading(
    12,
    "Merkeze nasıl gidilir?",
    "14 kelime / kalıp",
    [
        "Wer neu in einer Stadt ist, muss oft fragen, wie man zum [[Zentrum::merkez]] kommt. Manchmal fährt man zuerst [[mit dem Bus::otobüsle]], später geht man zu Fuß weiter und biegt dann an einer [[Brücke::köprü]] ab.",
        "Für manche Orte fährt man direkt [[zum Bahnhof::istasyona]], für andere geht man erst [[zur Apotheke::eczane yönüne]] oder [[in die Altstadt::eski şehre]]. Welche Präposition passt, hängt oft davon ab, ob man zu einer Person, in ein Gebäude oder auf eine Fläche geht.",
        "Wer die Wege ruhig übt, versteht bald den Unterschied zwischen [[nach::...e doğru/...'a]], [[zu::...e/...'ya]] und [[in::...e/...'ya içeri]]. So werden kurze Alltagswege leichter und lange Wege weniger stressig.",
    ],
)
_extend_phrase_bank(
    12,
    [
        ("Ich fahre heute zum Bahnhof.", "Bugün istasyona gidiyorum.", "A1 ulaşım ve yön dili A2 edat seçimiyle birleşiyor."),
        ("Am Wochenende gehen wir in die Altstadt.", "Hafta sonunda eski şehre gidiyoruz.", "A1 gün bilgisi yeni hareket yapısıyla tekrar ediyor."),
        ("Nach dem Kurs gehe ich zur Apotheke.", "Kurstan sonra eczaneye gidiyorum.", "A1 rutin ve sıra bildiren yapı sürüyor."),
        ("Zum Museum fahren wir lieber mit der U-Bahn.", "Müzeye metroyla gitmeyi tercih ediyoruz.", "A1 ulaşım ve tercih dili korunuyor."),
    ],
)
_set_extra_exercises(
    12,
    [
        _module(
            "a2-l12-dialogue-comprehension",
            "Diyalog Anlama",
            "Hedefe göre hangi hareket yapısının seçildiğini ayır.",
            [
                _q("Müzeye giderken ilk yönlendirme nedir?", ["Köprüden sonra sağa dönmek", "Işıklara kadar gidip sola dönmek", "Doğrudan metroya binmek"], 1, "İlk iki adım bu şekilde veriliyor."),
                _q("B kişisi neden yürümeyi de seçenek olarak sunuyor?", ["Daha ucuz olduğu için", "Eski şehri daha fazla görmek için", "Otobüs olmadığı için"], 1, "Altstadt'ı daha çok görmeyi söylüyor."),
                _q("İstasyona gitmek için en iyi yol ne olarak veriliyor?", ["Taksi", "Otobüs", "U-Bahn"], 2, "Son satırda U-Bahn öneriliyor."),
                _q("'zum Museum' neyi gösteriyor?", ["Bir şehre gitmeyi", "Belirli bir yere yönelmeyi", "Bir odanın içinde bulunmayı"], 1, "zu + dativ yönelimi veriyor."),
            ],
        ),
        _module(
            "a2-l12-reading-comprehension",
            "Okuma Anlama",
            "Hareket edatlarının mantığını gerçek rota üzerinden çöz.",
            [
                _q("Metin hangi soruyla başlıyor?", ["Nasıl daha az çalışılır?", "Merkeze nasıl gidilir?", "Hangi tren daha pahalı?"], 1, "İlk paragraf yeni şehirde yön sormadan söz ediyor."),
                _q("'in die Altstadt' hangi durumu anlatıyor?", ["Bir yüzeye çıkmayı", "Bir bölgeye giriş yönünü", "Bir kişiye gitmeyi"], 1, "Bölge/alan içine hareketi anlatıyor."),
                _q("Hangi edat şehirler ve ülkeler yönünde sık kullanılır?", ["nach", "zu", "auf"], 0, "Son paragraf bunu karşılaştırıyor."),
                _q("Metne göre düzenli pratik ne sağlar?", ["Daha çok bilet almayı", "Yolları daha az stresli hale getirmeyi", "Oteli büyütmeyi"], 1, "Son cümlede bu sonuç veriliyor."),
            ],
        ),
        _module(
            "a2-l12-a1-review",
            "A1 Köprü Tekrarı",
            "A1 şehir, ulaşım ve gün kelimelerini yön edatlarıyla tekrar et.",
            [
                _q("'Hafta sonunda istasyona gidiyoruz' cümlesi hangisi?", ["Am Wochenende gehen wir zum Bahnhof.", "Am Wochenende gehen wir Bahnhof.", "Wir zum Bahnhof am Wochenende gehen."], 0, "A1 zaman + A2 yön yapısı birlikte korunuyor."),
                _q("'Şehre gidiyorum' için en tipik edat hangisi?", ["nach", "mit", "unter"], 0, "Şehir ve ülke adlarında çoğu zaman nach kullanılır."),
                _q("'Eczaneye gidiyorum' cümlesinde doğru yapı hangisi?", ["ich gehe zur Apotheke", "ich gehe in Apotheke", "ich gehe nach Apotheke"], 0, "Belirli kuruma/kişiye yönelimde zu kullanılır."),
                _q("A1'den hangi alan burada tekrar ediyor?", ["Ulaşım, şehir ve gün ifadeleri", "Sadece renkler", "Sadece hava durumu"], 0, "Bu ders bilinçli olarak eski ulaşım alanını tekrar ettiriyor."),
            ],
        ),
    ],
)

_replace_dialogue(
    13,
    "Sebep, düşünce ve koşulla plan kurma",
    [
        ("A", "Warum lernst du heute länger als sonst?", "Bugün neden normalden daha uzun çalışıyorsun?"),
        ("B", "Weil ich morgen ein Gespräch habe und ich möchte, dass alles klar klingt.", "Çünkü yarın bir görüşmem var ve her şeyin net duyulmasını istiyorum."),
        ("A", "Denkst du, dass du schon gut vorbereitet bist?", "Sence şimdiden iyi hazırlanmış mısın?"),
        ("B", "Ja, aber wenn ich nervös werde, spreche ich manchmal zu schnell.", "Evet ama heyecanlanırsam bazen fazla hızlı konuşuyorum."),
        ("A", "Dann übe heute noch ein paar Beispiele, weil ruhiges Sprechen viel hilft.", "O zaman bugün birkaç örnek daha çalış, çünkü sakin konuşmak çok yardımcı olur."),
        ("B", "Gute Idee. Ich hoffe, dass ich morgen sicherer klinge.", "İyi fikir. Umarım yarın daha güvenli duyulurum."),
    ],
)
_replace_reading(
    13,
    "Neden böyle oldu?",
    "14 kelime / kalıp",
    [
        "Viele Lernende merken erst später, [[dass::...ki]] Nebensätze den Alltag viel natürlicher machen. Man sagt nicht nur kurze Hauptsätze, sondern verbindet Gründe, Gedanken und Bedingungen klarer.",
        "Ein Beispiel: Jemand lernt heute länger, [[weil::çünkü]] morgen ein wichtiges Gespräch stattfindet. Später sagt dieselbe Person, dass sie hofft, ruhiger zu sprechen, und sie übt weiter, [[wenn::eğer/ne zaman]] sie am Abend noch Zeit hat.",
        "Mit solchen Sätzen wiederholt man A1-Wörter wie Uhrzeiten, Familie, Arbeit oder Kurs, aber man baut sie jetzt in längere [[Strukturen::yapılar]] ein. Genau das macht A2-Sprechen flüssiger und schriftlich deutlich präziser.",
    ],
)
_extend_phrase_bank(
    13,
    [
        ("Ich lerne heute länger, weil ich morgen eine Prüfung habe.", "Bugün daha uzun çalışıyorum çünkü yarın sınavım var.", "A1 sınav ve zaman dili yan cümleyle büyüyor."),
        ("Ich denke, dass der Plan gut ist.", "Planın iyi olduğunu düşünüyorum.", "A1 temel düşünce fiilleri artık dass ile bağlanıyor."),
        ("Wenn ich Zeit habe, rufe ich meine Mutter an.", "Vaktim olursa annemi ararım.", "A1 aile ve günlük rutin dili wenn ile tekrar ediyor."),
        ("Wir bleiben zu Hause, weil es heute spät wird.", "Bugün geç olacağı için evde kalıyoruz.", "A1 ev ve zaman bilgisi sebep cümlesine taşınıyor."),
    ],
)
_set_extra_exercises(
    13,
    [
        _module(
            "a2-l13-dialogue-comprehension",
            "Diyalog Anlama",
            "weil, dass ve wenn yönünü ayırt et.",
            [
                _q("B kişisi neden daha uzun çalışıyor?", ["Çünkü yarın görüşmesi var", "Çünkü otobüsü kaçırdı", "Çünkü tatilde"], 0, "İlk cevapta morgen ein Gespräch geçiyor."),
                _q("Hangi cümlede düşünce/umut aktarılıyor?", ["wenn ich nervös werde", "dass ich morgen sicherer klinge", "weil ruhiges Sprechen hilft"], 1, "dass yan cümlesi içerik aktarır."),
                _q("'wenn ich nervös werde' neyi anlatıyor?", ["Koşulu", "Geçmiş olayı", "Emri"], 0, "Bir durum gerçekleşirse ne olduğunu anlatıyor."),
                _q("A kişisinin önerisi nedir?", ["Daha hızlı konuşmak", "Birkaç örnek daha çalışmak", "Görüşmeyi iptal etmek"], 1, "Dann übe ... derken bunu söylüyor."),
            ],
        ),
        _module(
            "a2-l13-reading-comprehension",
            "Okuma Anlama",
            "Yan cümlelerin işlevini metin içinde çöz.",
            [
                _q("Metne göre öğrenenler neyi geç fark ediyor?", ["Nebensatzların konuşmayı doğal yaptığını", "Bilet fiyatlarını", "Yeni öğretmeni"], 0, "İlk paragraf bunu açık söylüyor."),
                _q("İkinci paragrafta kişi neden daha uzun çalışıyor?", ["Çünkü kurs iptal oldu", "Çünkü yarın önemli bir görüşme var", "Çünkü yağmur yağıyor"], 1, "weil cümlesi bunu taşıyor."),
                _q("'wenn sie am Abend noch Zeit hat' neyi ekliyor?", ["Şart/olasılık", "Yer bilgisi", "Fiyat karşılaştırması"], 0, "Koşullu devam bilgisini verir."),
                _q("Son paragrafta A1'den hangi alanların döndüğü söyleniyor?", ["Saat, aile, iş, kurs", "Sadece renkler", "Sadece mevsimler"], 0, "Metin bunu açıkça listeliyor."),
            ],
        ),
        _module(
            "a2-l13-a1-review",
            "A1 Köprü Tekrarı",
            "A1 zaman, aile ve sınav dilini yan cümlelerle tekrar et.",
            [
                _q("'Çünkü' bağlacı hangisi?", ["weil", "dass", "wenn"], 0, "Sebep bildiren temel bağlaç weil'dir."),
                _q("'... olduğunu düşünüyorum' yapısında en tipik bağlaç hangisi?", ["wenn", "dass", "als"], 1, "İçerik aktaran yan cümlede dass kullanılır."),
                _q("'Vaktim olursa annemi ararım' için doğru seçenek hangisi?", ["Wenn ich Zeit habe, rufe ich meine Mutter an.", "Weil ich Zeit habe, rufe ich meine Mutter an wenn.", "Dass ich Zeit habe, rufe meine Mutter an."], 0, "Koşul + ana cümle düzeni bu şekildedir."),
                _q("A1'den hangi kelime alanı burada tekrar ediyor?", ["Aile ve günlük rutin", "Sadece şehirler", "Sadece otel dili"], 0, "Anneyi aramak gibi A1 kalıpları döndürülüyor."),
            ],
        ),
    ],
)

_replace_dialogue(
    14,
    "A2 sonrası planı somutlaştırma",
    [
        ("A", "Was wirst du nach diesem Kurs als Erstes machen?", "Bu kurstan sonra ilk olarak ne yapacaksın?"),
        ("B", "Ich werde zuerst jeden Morgen zwanzig Minuten wiederholen und danach mehr lesen.", "Önce her sabah yirmi dakika tekrar yapacağım ve sonra daha çok okuyacağım."),
        ("A", "Wirst du auch Sprechen üben?", "Konuşma çalışması da yapacak mısın?"),
        ("B", "Ja, ich werde einmal pro Woche mit einer Freundin nur Deutsch sprechen.", "Evet, haftada bir kez bir arkadaşımla sadece Almanca konuşacağım."),
        ("A", "Und wann willst du die Goethe-Prüfung machen?", "Peki Goethe sınavını ne zaman yapmak istiyorsun?"),
        ("B", "Wenn ich bis zum Sommer sicherer werde, werde ich mich anmelden.", "Yaza kadar daha güvenli olursam kayıt yaptıracağım."),
    ],
)
_replace_reading(
    14,
    "A2 kapanış paragrafı",
    "14 kelime / kalıp",
    [
        "Nach A2 können Lernende schon viel mehr erzählen: was sie gestern gemacht haben, wohin sie morgen [[fahren::gidecekler]], warum etwas schwierig war und welche Lösung am Ende am [[besten::en iyi]] passt.",
        "Im nächsten Schritt werden viele ihr Deutsch im Alltag bewusster benutzen. Sie werden mehr [[lesen::okumak]], kurze Nachrichten schreiben, im Kurs aktiver sprechen und alte A1-Themen wie Familie, Arbeit, Essen oder Reisen regelmäßig [[wiederholen::tekrar etmek]].",
        "Genau dadurch wird aus vielen einzelnen Regeln ein stabiles System. Wer dranbleibt, wird auch in der Prüfung ruhiger reagieren, längere Texte besser verstehen und eigene Antworten klarer [[formulieren::ifade etmek]].",
    ],
)
_extend_phrase_bank(
    14,
    [
        ("Ich werde jeden Tag zwanzig Minuten wiederholen.", "Her gün yirmi dakika tekrar yapacağım.", "A1 saat ve rutin bilgisi gelecek planına taşınıyor."),
        ("Wir werden im Sommer mehr reisen.", "Yazın daha çok seyahat edeceğiz.", "A1 seyahat alanı gelecek zamanla yeniden kuruluyor."),
        ("Wenn ich sicherer werde, melde ich mich an.", "Daha güvenli hale gelirsem kayıt yaptırırım.", "A2 yan cümle bilgisi gelecek planına bağlanıyor."),
        ("Ich werde zuerst lesen und danach sprechen üben.", "Önce okuyacağım sonra konuşma çalışacağım.", "A1 sıra zarfları A2 öğrenme planında tekrar ediyor."),
    ],
)
_set_extra_exercises(
    14,
    [
        _module(
            "a2-l14-dialogue-comprehension",
            "Diyalog Anlama",
            "Gelecek planını ve koşullu hedefi ayır.",
            [
                _q("B kişisi her sabah ne yapacak?", ["Yirmi dakika tekrar yapacak", "Bir saat koşacak", "Sadece film izleyecek"], 0, "İlk planı yirmi dakikalık tekrar."),
                _q("Konuşma pratiğini nasıl yapacak?", ["Her gün tek başına", "Haftada bir arkadaşıyla", "Ayda bir öğretmeniyle"], 1, "Haftada bir arkadaşla konuşacağını söylüyor."),
                _q("Goethe sınavına hangi şartta başvuracak?", ["Yaza kadar daha güvenli olursa", "Hemen bu akşam", "Sadece arkadaşları isterse"], 0, "Wenn ich bis zum Sommer sicherer werde diyor."),
                _q("Buradaki 'werde mich anmelden' neyi anlatıyor?", ["Geçmiş alışkanlığı", "Gelecekteki niyeti", "Yasaklamayı"], 1, "werden gelecek niyet kuruyor."),
            ],
        ),
        _module(
            "a2-l14-reading-comprehension",
            "Okuma Anlama",
            "A2 sonunda nelerin birleştiğini metinden çıkar.",
            [
                _q("Metne göre A2 sonrası neleri daha rahat anlatabiliriz?", ["Sadece renkleri", "Geçmiş, gelecek, nedenler ve çözümleri", "Sadece hava durumunu"], 1, "İlk paragraf bunu özetliyor."),
                _q("Sonraki adımda hangi alışkanlık özellikle öneriliyor?", ["Eski konuları düzenli tekrar etmek", "Sadece yeni kelime ezberlemek", "Dersleri bırakmak"], 0, "İkinci paragraf düzenli tekrarı vurguluyor."),
                _q("'stabiles System' neye gönderme yapıyor?", ["Kuralların bütünleşmesine", "Yeni bir bavula", "Sınıf kapısına"], 0, "Üçüncü paragrafta parçaların sistem haline gelmesi anlatılıyor."),
                _q("Metne göre sınavda ne gelişir?", ["Daha sakin tepki verme ve uzun metin anlama", "Sadece hızlı koşma", "Sadece rakam yazma"], 0, "Son paragraf sınav faydasını bu şekilde özetliyor."),
            ],
        ),
        _module(
            "a2-l14-a1-review",
            "A1 Köprü Tekrarı",
            "A1 rutin, seyahat ve zaman ifadelerini A2 kapanışında tekrar et.",
            [
                _q("'Her gün' ifadesi hangisi?", ["jeden Tag", "im Hotel", "nach links"], 0, "A1 temel zaman ifadesidir."),
                _q("'Yazın daha çok seyahat edeceğiz' cümlesi hangisi?", ["Wir werden im Sommer mehr reisen.", "Wir reisen im Sommer mehr werden.", "Wir haben im Sommer mehr reisen."], 0, "werden ile gelecek planı doğru kurulmuş."),
                _q("A1'den hangi alan burada tekrar ediyor?", ["Zaman, rutin ve seyahat", "Sadece otel resepsiyonu", "Sadece pasif yapı"], 0, "Kapanış dersi eski temel alanları tekrar topluyor."),
                _q("'Önce ... sonra ...' dizisi hangisi?", ["zuerst ... danach ...", "weil ... dass ...", "nach ... zu ..."], 0, "A1 sıra zarfları burada yeniden kullanılıyor."),
            ],
        ),
    ],
)

# A2 lesson 1 refinement: add question/experience usage layer for Goethe-style speaking.
_get_lesson(1)["lesson_blocks"].append(
    {
        "title": "Perfekt ile deneyim soruları da kurmalısın",
        "body": "Goethe A2'de sadece ne yaptığını anlatman yetmez; başkasına 'Hafta sonu ne yaptın?', 'Daha önce oraya gittin mi?' gibi sorular da yöneltebilmen gerekir. Bu yüzden Perfekt'i soru kalıbı, schon/noch nicht ve schon einmal ile birlikte görmek gerekir.",
    }
)
_extend_phrase_bank(
    1,
    [
        ("Hast du schon gegessen?", "Yemek yedin mi?", "schon günlük konuşmada 'çoktan / daha önce bu noktaya kadar' tonunu verir."),
        ("Ich habe noch nicht angerufen.", "Henüz aramadım.", "noch nicht eksik kalan eylemi net anlatır."),
        ("Bist du schon einmal in Berlin gewesen?", "Daha önce hiç Berlin'de bulundun mu?", "schon einmal deneyim sormada çok kullanılır."),
        ("Wir haben am Sonntag nicht gearbeitet.", "Pazar günü çalışmadık.", "Perfekt'te olumsuzluk da erken oturmalıdır."),
    ],
)
_get_lesson(1).setdefault("common_mistakes", []).append(
    {
        "wrong": "Hast du gestern ins Kino gegangen?",
        "right": "Bist du gestern ins Kino gegangen?",
        "why": "gehen hareket fiili olduğu için soru cümlesinde de sein ile kurulur.",
    }
)
_get_lesson(1).setdefault("exercises", []).append(
    _module(
        "a2-l1-experience-questions",
        "Deneyim ve Soru Kalıpları",
        "Perfekt'te soru kurma, schon/noch nicht ve schon einmal kullanımını pekiştir.",
        [
            _q("`Daha önce hiç trenle gittin mi?` sorusu hangisi?", ["Hast du schon einmal mit dem Zug gefahren?", "Bist du schon einmal mit dem Zug gefahren?", "Bist du mit dem Zug schon einmal fahren?"], 1, "fahren hareket fiili olduğu için sein ile kurulur."),
            _q("`Henüz annemi aramadım` cümlesi hangisi?", ["Ich habe meine Mutter noch nicht angerufen.", "Ich bin meine Mutter noch nicht angerufen.", "Ich habe noch nicht meine Mutter anrufen."], 0, "angrufen Partizip II ile ve haben ile kurulur."),
            _q("`Yemek yedin mi?` sorusunda doğru başlangıç hangisi?", ["Hast du ...", "Bist du ...", "Wirst du ..."], 0, "essen çoğu fiil gibi haben alır."),
            _q("`schon einmal` en çok neyi anlatır?", ["Bir deneyimi / daha önce yapmış olmayı", "Sadece geleceği", "Sadece emir vermeyi"], 0, "Deneyim sorularında doğal bir işaretleyicidir."),
        ],
    )
)

# A2 lesson 2 refinement: make the dative-only location logic explicit and replace placeholder contrasts.
_get_lesson(2)["lesson_blocks"].append(
    {
        "title": "Bu derste yön değil, konum anlatıyorsun",
        "body": "Başlıkta Wechselpräpositionen geçse de bu derste asıl hedef hareket değil konum anlatımıdır. Yani şimdilik Wo? sorusuna cevap veriyor ve çoğu örnekte dativ tarafını güçlendiriyorsun; Wohin? ve hareket yönü sonraki adımda daha açık işlenecek.",
    }
)
_get_lesson(2)["grammar_sections"][1].update(
    {
        "summary": "in, auf, unter, vor, hinter, neben, zwischen gibi Wechselpräpositionen bu derste Wo? sorusuna cevap verirken çoğunlukla dativ ile görünür.",
        "formula": "Wo? + edat + dativ isim grubu",
        "teaching_note": "Aynı edatlar daha sonra hareket anlatırken başka biçime kayabilir. Ama bu derste güvenli refleks şudur: sabit konum anlatıyorsan önce dativ düşün.",
        "watch_out": "Wechselpräpositionen adını görüp her seferinde iki ihtimali birden kurmaya çalışma. Önce odak soruyu netleştir: Wo? ise bu derste konum anlatıyorsun.",
        "contrast": {
            "correct": "Der Laptop liegt auf dem Tisch.",
            "wrong": "Der Laptop liegt auf den Tisch.",
            "reason": "Burada hareket yok, sadece mevcut konum var; bu yüzden dativ gerekir.",
        },
        "annotated_examples": [
            {
                "text": "Das Bild hängt an der Wand.",
                "note": "an der Wand ifadesi duvar yüzeyine sabit konumu anlatır; burada hedef bir hareket değil, hazır durumdur.",
            },
            {
                "text": "Die Schlüssel liegen in der Schublade.",
                "note": "Çekmecenin içine hareket anlatılmıyor; ana fikir anahtarların şu an orada bulunmasıdır.",
            },
        ],
        "examples": [
            {
                "text": "Das Bild hängt an der Wand.",
                "note": "an der Wand ifadesi duvar yüzeyine sabit konumu anlatır; burada hedef bir hareket değil, hazır durumdur.",
            },
            {
                "text": "Die Schlüssel liegen in der Schublade.",
                "note": "Çekmecenin içine hareket anlatılmıyor; ana fikir anahtarların şu an orada bulunmasıdır.",
            },
        ],
    }
)
_get_lesson(2)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Das Bild hängt über dem Sofa.",
            "wrong": "Das Bild liegt über dem Sofa.",
            "reason": "Asılı nesnede hängen doğal fiildir; liegen yatay duran nesneler için beklenir.",
        }
    }
)
_get_lesson(2)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Die Lampe steht zwischen dem Fenster und der Tür.",
            "wrong": "Die Lampe steht zwischen dem Fenster.",
            "reason": "zwischen çoğu zaman iki referans noktasını birlikte ister; tek unsurla yapı eksik kalır.",
        }
    }
)
_get_lesson(2).setdefault("common_mistakes", []).append(
    {
        "wrong": "Die Bücher sind in den Regal.",
        "right": "Die Bücher sind im Regal.",
        "why": "Konum anlatırken edattan sonra dativ gerekir; ayrıca in dem çoğu zaman im olarak kısalır.",
    }
)
_extend_phrase_bank(
    2,
    [
        ("Die Schlüssel sind in der Schublade.", "Anahtarlar çekmecede.", "A1 ev ve eşya kelimeleri dativ konumla büyüyor."),
        ("Die Tasche liegt hinter der Tür.", "Çanta kapının arkasında duruyor.", "A1 çanta kelimesi yer tarifinde yeniden kullanılıyor."),
        ("Am Abend sitze ich am Schreibtisch.", "Akşam çalışma masasının başında oturuyorum.", "A1 zaman zarfları konum cümlesine bağlanıyor."),
        ("Neben dem Bett steht eine Lampe.", "Yatağın yanında bir lamba duruyor.", "A1 oda kelimeleri bu derste tekrar ediliyor."),
    ],
)
_get_lesson(2).setdefault("exercises", []).append(
    _module(
        "a2-l2-dative-location-focus",
        "Dativ ile Konum Odağı",
        "Wo? sorusunda doğru edat ve dativ grubunu seç.",
        [
            _q("'Laptop masanın üstünde' cümlesi hangisi?", ["Der Laptop liegt auf dem Tisch.", "Der Laptop liegt auf den Tisch.", "Der Laptop steht auf dem Tisch."], 0, "Konum + yatık nesne için liegen ve dativ gerekir."),
            _q("'Resim duvarda asılı' cümlesi hangisi?", ["Das Bild hängt an der Wand.", "Das Bild hängt an die Wand.", "Das Bild liegt an der Wand."], 0, "Asılı nesnede hängen ve konumda dativ kullanılır."),
            _q("'Çekmecede' anlamına en doğal seçenek hangisi?", ["in der Schublade", "in die Schublade", "zu der Schublade"], 0, "Konum anlattığımız için dativ gerekir."),
            _q("'İki sandalyenin arasında' yapısı hangisi?", ["zwischen dem Stuhl und dem Stuhl", "zwischen der Stuhl", "vor dem Stuhl und dem Tisch"], 0, "zwischen iki referans nokta ister."),
        ],
    )
)

# A2 lesson 3 refinement: replace generic contrasts and strengthen complaint/payment flow.
_get_lesson(3)["lesson_blocks"].append(
    {
        "title": "Sipariş kadar küçük sorunları çözmek de hedefin parçası",
        "body": "Goethe A2 restoran senaryosunda sadece sipariş vermek yetmez. Eksik, fazla, yanlış ya da değiştirilmesini istediğin bir şey olduğunda bunu kısa ama nazik cümlelerle söyleyebilmen gerekir; bu dersin gerçek iletişim değeri burada başlar.",
    }
)
_get_lesson(3)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Ich hätte gern eine Tomatensuppe und einen Tee.",
            "wrong": "Ich bin gern eine Tomatensuppe und einen Tee.",
            "reason": "Siparişte istek kalıbı gerekir; sein fiili nesne istemek için kullanılmaz.",
        }
    }
)
_get_lesson(3)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Nein danke, ich möchte keinen Saft.",
            "wrong": "Nein danke, ich möchte nicht Saft.",
            "reason": "İsim olumsuzluğu burada nicht ile değil kein ile kurulur.",
        },
        "annotated_examples": [
            {
                "text": "Sonst noch etwas zu trinken?",
                "note": "Garsonun servis akışında ek istek açmak için kullandığı en doğal kısa sorulardan biridir.",
            },
            {
                "text": "Nein danke, ich möchte keinen Nachtisch.",
                "note": "kein burada isim grubunu doğrudan olumsuzlar; cümle kısa kaldığı için daha doğal duyulur.",
            },
        ],
        "examples": [
            {
                "text": "Sonst noch etwas zu trinken?",
                "note": "Garsonun servis akışında ek istek açmak için kullandığı en doğal kısa sorulardan biridir.",
            },
            {
                "text": "Nein danke, ich möchte keinen Nachtisch.",
                "note": "kein burada isim grubunu doğrudan olumsuzlar; cümle kısa kaldığı için daha doğal duyulur.",
            },
        ],
    }
)
_get_lesson(3)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Zusammen oder getrennt?",
            "wrong": "Die Rechnung ich will jetzt.",
            "reason": "Hesap ve ödeme dili sabit kısa kalıplarla daha doğal kurulur.",
        }
    }
)
_get_lesson(3)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Ich nehme den Salat ohne Zwiebeln.",
            "wrong": "Ich nehme den Salat nicht mit Zwiebeln.",
            "reason": "Malzeme çıkarmada kısa ve doğal kalıp ohne + isim yapısıdır.",
        }
    }
)
_get_lesson(3).setdefault("common_mistakes", []).append(
    {
        "wrong": "Ich möchte die Suppe ohne.",
        "right": "Ich möchte die Suppe ohne Zwiebeln.",
        "why": "ohne yapısından sonra neyin çıkarıldığını açıkça söylemek gerekir.",
    }
)
_extend_phrase_bank(
    3,
    [
        ("Entschuldigung, in meinem Salat sind zu viele Zwiebeln.", "Affedersiniz, salatamda fazla soğan var.", "Küçük bir şikâyeti nazikçe açmak için güvenli kalıptır."),
        ("Könnten Sie mir bitte eine andere Portion bringen?", "Bana başka bir porsiyon getirebilir misiniz?", "Sorun sonrası çözüm istemeyi öğretir."),
        ("Zahlen wir zusammen oder getrennt?", "Birlikte mi ayrı ayrı mı ödeyelim?", "Restoran kapanışında çok sık gerekir."),
        ("Ich nehme heute keinen Nachtisch.", "Bugün tatlı almayacağım.", "kein ile isim olumsuzluğunu menü bağlamında tekrar ettirir."),
    ],
)
_get_lesson(3).setdefault("exercises", []).append(
    _module(
        "a2-l3-complaint-and-payment",
        "Şikâyet ve Ödeme Akışı",
        "Siparişten sonra küçük sorun bildirme ve hesabı tamamlama dilini pekiştir.",
        [
            _q("`Salatada çok soğan var` cümlesine en yakın seçenek hangisi?", ["In meinem Salat sind zu viele Zwiebeln.", "Mein Salat ist keine Zwiebeln.", "Ich bin zu viele Zwiebeln im Salat."], 0, "Şikâyet cümlesi kısa ve doğrudan kurulmalı."),
            _q("`Bana başka bir porsiyon getirebilir misiniz?` cümlesi hangisi?", ["Könnten Sie mir bitte eine andere Portion bringen?", "Sie bringen mir andere Portion?", "Ich möchte bringen eine Portion andere."], 0, "Nazik çözüm isteme kalıbı böyledir."),
            _q("`Ayrı ayrı mı ödeyelim?` fikri için doğru soru hangisi?", ["Zahlen wir zusammen oder getrennt?", "Kosten wir getrennt?", "Wir bezahlen Rechnung oder?"], 0, "Restoranda doğal ödeme sorusu bu kalıpla gelir."),
            _q("`Bugün tatlı istemiyorum` için doğru seçenek hangisi?", ["Ich möchte nicht Nachtisch.", "Ich nehme heute keinen Nachtisch.", "Ich habe keinen Nachtisch nehmen."], 1, "İsim olumsuzluğu yine kein ile kurulur."),
        ],
    )
)

# A2 lesson 4 refinement: make politeness contrasts explicit and add realistic follow-up requests.
_get_lesson(4)["lesson_blocks"].append(
    {
        "title": "Nazik olmak sadece dil bilgisi değil, sosyal stratejidir",
        "body": "A2'de aynı isteği hem doğrudan hem yumuşatarak kurabilmen gerekir. Özellikle danışma, kayıt, ofis ve müşteri hizmeti bağlamlarında tonu yumuşatmak sadece kibar görünmek için değil, iletişimi açık ve işlevsel tutmak için de önemlidir.",
    }
)
_get_lesson(4)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Ich würde gern den Termin verschieben.",
            "wrong": "Ich verschiebe den Termin jetzt.",
            "reason": "İkinci cümle kaba emir gibi duyulabilir; würde gern isteği yumuşatır ve karşı tarafa alan bırakır.",
        }
    }
)
_get_lesson(4)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich hätte gern einen neuen Termin.",
            "wrong": "Ich würde gern einen neuen Termin.",
            "reason": "Nesne istemede hätte gern daha doğal durur; würde gern daha çok eylem isteğine yaslanır.",
        },
        "annotated_examples": [
            {
                "text": "Ich hätte gern eine schriftliche Bestätigung.",
                "note": "Burada somut bir belge istendiği için isim odaklı kalıp doğaldır.",
            },
            {
                "text": "Ich würde gern später kommen.",
                "note": "Burada yapılacak eylem öne çıktığı için fiil odaklı kalıp seçilir.",
            },
        ],
        "examples": [
            {
                "text": "Ich hätte gern eine schriftliche Bestätigung.",
                "note": "Burada somut bir belge istendiği için isim odaklı kalıp doğaldır.",
            },
            {
                "text": "Ich würde gern später kommen.",
                "note": "Burada yapılacak eylem öne çıktığı için fiil odaklı kalıp seçilir.",
            },
        ],
    }
)
_get_lesson(4)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Könnten Sie mir bitte die Adresse noch einmal schicken?",
            "wrong": "Schicken Sie mir die Adresse noch einmal.",
            "reason": "Doğrudan emir biçimi iş görse de resmî yardım istemede yumuşatılmış soru çok daha uygundur.",
        }
    }
)
_get_lesson(4)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Ich würde heute gern einen Termin reservieren.",
            "wrong": "Ich würde gern reservieren heute einen Termin.",
            "reason": "würde ikinci pozisyonda kalır; infinitiv sona gider, diğer ögeler arada yerleşir.",
        }
    }
)
_get_lesson(4).setdefault("common_mistakes", []).append(
    {
        "wrong": "Könnten Sie sagen mir die Uhrzeit?",
        "right": "Könnten Sie mir die Uhrzeit sagen?",
        "why": "Nazik soru cümlesinde fiilden sonra nesne ve diğer ögelerin sırası korunmalıdır.",
    }
)
_extend_phrase_bank(
    4,
    [
        ("Könnten Sie mir das bitte noch einmal erklären?", "Bunu bana bir kez daha açıklayabilir misiniz?", "Bilgi eksikse en güvenli resmî rica kalıplarından biridir."),
        ("Ich hätte gern eine schriftliche Bestätigung.", "Yazılı bir onay rica ediyorum.", "Belge ve çıktı isteme dilini güçlendirir."),
        ("Ich würde den Termin gern auf Freitag verschieben.", "Randevuyu cumaya almak isterim.", "A1 gün bilgisi nazik randevu diliyle birleşiyor."),
        ("Würden Sie mir bitte kurz helfen?", "Bana kısaca yardım eder misiniz?", "Resmî bağlamda hızlı yardım isteme kalıbıdır."),
    ],
)
_get_lesson(4).setdefault("exercises", []).append(
    _module(
        "a2-l4-polite-follow-up",
        "Nazik Takip ve Düzeltme",
        "Randevu değişikliği, yeniden açıklama isteme ve teyit alma dilini pekiştir.",
        [
            _q("`Bunu bana tekrar açıklar mısınız?` cümlesi hangisi?", ["Könnten Sie mir das bitte noch einmal erklären?", "Sie erklären mir das wieder.", "Erklären Sie das mir bitte noch einmal können?"], 0, "Resmî rica için Könnten Sie kalıbı en doğal seçimdir."),
            _q("`Yazılı bir onay rica ederim` cümlesine en yakın seçenek hangisi?", ["Ich würde gern bestätigen.", "Ich hätte gern eine schriftliche Bestätigung.", "Ich will schriftliche bestätigen."], 1, "Somut belge/çıktı istemede hätte gern daha doğaldır."),
            _q("`Randevuyu cumaya almak isterim` için doğru seçenek hangisi?", ["Ich würde den Termin gern auf Freitag verschieben.", "Ich hätte gern auf Freitag verschieben.", "Ich würde auf Freitag den Termin verschiebe."], 0, "würde + infinitiv kalıbı doğru yerleşmiş durumda."),
            _q("Hangi cümle ton olarak en yumuşaktır?", ["Schicken Sie mir die Adresse.", "Könnten Sie mir bitte die Adresse schicken?", "Sie schicken mir jetzt die Adresse."], 1, "Yumuşatılmış soru yapısı burada en uygun tondur."),
        ],
    )
)

# A2 lesson 5 refinement: replace generic contrasts and make person-vs-thing distinction explicit.
_get_lesson(5)["lesson_blocks"].append(
    {
        "title": "Buradaki asıl beceri tekrar kırmak ama anlamı korumak",
        "body": "Bu dersin değeri tek tek daran, darauf, darüber ezberlemek değil. Asıl hedef, aynı ismi tekrar tekrar söylemeden konuşmayı akıcı tutmak ve yine de neye gönderme yaptığının anlaşılır kalmasını sağlamaktır.",
    }
)
_get_lesson(5)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Wir sprechen über das Problem.",
            "wrong": "Wir sprechen auf das Problem.",
            "reason": "sprechen bu anlamda über ile gelir; edatı serbestçe değiştiremezsin.",
        }
    }
)
_get_lesson(5)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich warte auf die Antwort. Ich warte schon lange darauf.",
            "wrong": "Ich warte auf die Antwort. Ich warte schon lange auf sie.",
            "reason": "Bir nesneye/konuya geri dönerken Almancada burada çoğu zaman da- yapısı daha doğal olur.",
        }
    }
)
_get_lesson(5)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Worauf wartest du? Ich warte darauf.",
            "wrong": "Worüber wartest du? Ich warte darauf.",
            "reason": "Soru ve cevap aynı fiilin istediği edatı korumalıdır; warten auf çizgisi bozulmaz.",
        }
    }
)
_get_lesson(5)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Ich warte auf meinen Lehrer. Ich warte auf ihn.",
            "wrong": "Ich warte auf meinen Lehrer. Ich warte darauf.",
            "reason": "İnsanlara geri dönerken çoğu zaman da- değil, preposition + pronoun yapısı gerekir.",
        },
        "annotated_examples": [
            {
                "text": "Ich spreche mit meiner Schwester. Ich spreche oft mit ihr.",
                "note": "Kişi referansında mit ihr doğaldır; damit denmez.",
            },
            {
                "text": "Wir denken an den Plan. Wir denken oft daran.",
                "note": "Burada konu/şey referansı olduğu için daran kullanımı doğal hale gelir.",
            },
        ],
        "examples": [
            {
                "text": "Ich spreche mit meiner Schwester. Ich spreche oft mit ihr.",
                "note": "Kişi referansında mit ihr doğaldır; damit denmez.",
            },
            {
                "text": "Wir denken an den Plan. Wir denken oft daran.",
                "note": "Burada konu/şey referansı olduğu için daran kullanımı doğal hale gelir.",
            },
        ],
        "watch_out": "Şeylere geri dönerken da- yapısı, kişilere geri dönerken çoğu zaman preposition + pronoun kullanırsın. Bu ayrım akıcılık kadar doğruluk için de kritiktir.",
    }
)
_get_lesson(5).setdefault("common_mistakes", []).append(
    {
        "wrong": "Ich spreche mit meinem Bruder. Ich spreche damit.",
        "right": "Ich spreche mit meinem Bruder. Ich spreche mit ihm.",
        "why": "Kişiye geri dönüşte da- yapısı değil, edat + zamir kullanılır.",
    }
)
_extend_phrase_bank(
    5,
    [
        ("Ich warte auf die Nachricht. Ich warte schon lange darauf.", "Mesajı bekliyorum. Onu uzun süredir bekliyorum.", "Şey/konu referansında da- yapısının doğal kullanımını gösterir."),
        ("Ich spreche mit meiner Lehrerin. Ich spreche später mit ihr.", "Öğretmenimle konuşuyorum. Sonra onunla konuşacağım.", "Kişi referansında preposition + pronoun tekrar edilir."),
        ("Worüber redet ihr gerade?", "Şu anda ne hakkında konuşuyorsunuz?", "Soru-cevap zincirini doğal hale getirir."),
        ("Darüber möchte ich heute nicht sprechen.", "Bugün bunun hakkında konuşmak istemiyorum.", "A1 isteme/istememe kalıpları A2 referans yapısına bağlanır."),
    ],
)
_get_lesson(5).setdefault("exercises", []).append(
    _module(
        "a2-l5-person-vs-thing",
        "Kişi mi Şey mi?",
        "da- yapısı ile edat + zamir ayrımını bilinçli kur.",
        [
            _q("`Öğretmenimi bekliyorum. Onu bekliyorum.` için doğru ikinci cümle hangisi?", ["Ich warte darauf.", "Ich warte auf ihn.", "Ich warte daran."], 1, "Kişiye geri döndüğümüz için auf ihn gerekir."),
            _q("`Planı düşünüyorum. Onu düşünüyorum.` için doğru ikinci cümle hangisi?", ["Ich denke an ihn.", "Ich denke daran.", "Ich denke mit ihm."], 1, "Burada plan bir konu/şey olduğu için daran kullanılır."),
            _q("`Ne hakkında konuşuyorsunuz?` sorusu hangisi?", ["Worüber sprecht ihr?", "Worauf sprecht ihr?", "Mit wem sprecht ihr darüber?"], 0, "sprechen über -> worüber olur."),
            _q("Hangi cümle doğrudur?", ["Ich spreche mit meiner Schwester. Ich spreche damit.", "Ich spreche mit meiner Schwester. Ich spreche mit ihr.", "Ich spreche mit meiner Schwester. Ich spreche daran."], 1, "Kişi referansı yine mit ihr ile kurulur."),
        ],
    )
)

# A2 lesson 6 refinement: make modal tone and question usage more explicit.
_get_lesson(6)["lesson_blocks"].append(
    {
        "title": "Aynı geçmiş olay, farklı modal ile bambaşka duyulur",
        "body": "Bu dersin asıl noktası sadece konnte, wollte, musste görmek değil. Aynı olayın zorunluluk, izin, niyet ve tavsiye olarak nasıl farklı duyulduğunu fark etmek gerekir; Goethe A2 konuşmada bu ton farkı çok iş görür.",
    }
)
_get_lesson(6)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Ich musste gestern lange arbeiten.",
            "wrong": "Ich musste gestern lange gearbeitet.",
            "reason": "Modal geçmişte yalnız modal çekilir; asıl fiil yalın halde sonda kalır.",
        }
    }
)
_get_lesson(6)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich durfte gestern nicht ausgehen.",
            "wrong": "Ich musste gestern nicht ausgehen.",
            "reason": "İzin verilmediğini söylemek ile zorunlu olmadığını söylemek aynı şey değildir; ton farkı anlamı değiştirir.",
        }
    }
)
_get_lesson(6)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Du solltest früher schlafen.",
            "wrong": "Du musstest früher schlafen.",
            "reason": "Bir tavsiye verirken sollte, gerçek zorunluluk anlatırken musste daha uygundur.",
        },
        "annotated_examples": [
            {
                "text": "Ich musste um sechs Uhr aufstehen.",
                "note": "Burada dış koşulların zorunlu kıldığı bir durum var; konuşan bunu tercih olarak sunmuyor.",
            },
            {
                "text": "Du solltest heute früher nach Hause gehen.",
                "note": "Burada tavsiye ve beklenti tonu var; bu yüzden cümle daha yumuşak duyuluyor.",
            },
        ],
        "examples": [
            {
                "text": "Ich musste um sechs Uhr aufstehen.",
                "note": "Burada dış koşulların zorunlu kıldığı bir durum var; konuşan bunu tercih olarak sunmuyor.",
            },
            {
                "text": "Du solltest heute früher nach Hause gehen.",
                "note": "Burada tavsiye ve beklenti tonu var; bu yüzden cümle daha yumuşak duyuluyor.",
            },
        ],
    }
)
_get_lesson(6)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Ich wollte früher gehen.",
            "wrong": "Ich habe früher gehen wollen.",
            "reason": "Bu ikinci yapı teorik olarak mümkün olsa da günlük kısa anlatımda A2 için önce Präteritum modal refleksi daha doğal ve kullanışlıdır.",
        }
    }
)
_get_lesson(6).setdefault("common_mistakes", []).append(
    {
        "wrong": "Konntest du gestern kommen? Nein, ich musste nicht kommen.",
        "right": "Konntest du gestern kommen? Nein, ich durfte nicht kommen.",
        "why": "Gelmene izin verilmediyse durfte nicht gerekir; musste nicht zorunlu değildi anlamına kayar.",
    }
)
_extend_phrase_bank(
    6,
    [
        ("Konntest du gestern kommen?", "Dün gelebildin mi?", "Soru biçiminde modal geçmiş kullanımını güçlendirir."),
        ("Nein, ich durfte das Büro nicht früher verlassen.", "Hayır, ofisten daha erken çıkmama izin verilmedi.", "İzin ekseni ile zorunluluk eksenini ayırır."),
        ("Ich wollte eigentlich zu Hause bleiben.", "Aslında evde kalmak istiyordum.", "Niyet ve gerçek durum farkını kurar."),
        ("Du solltest heute früher schlafen.", "Bugün daha erken uyumalısın.", "Geçmiş dersleri tavsiye diliyle bağlar."),
    ],
)
_get_lesson(6).setdefault("exercises", []).append(
    _module(
        "a2-l6-modal-tone-and-questions",
        "Modal Tonu ve Soru Kalıpları",
        "Zorunluluk, izin, niyet ve tavsiye farkını soru-cevap içinde ayır.",
        [
            _q("`Dün gelebildin mi?` sorusu hangisi?", ["Konntest du gestern kommen?", "Könntest du gestern gekommen?", "Hast du gestern kommen gekonnt?"], 0, "A2 kullanımında kısa soru için bu form en doğaldır."),
            _q("`Erken çıkmama izin verilmedi` cümlesi hangisi?", ["Ich musste nicht früher gehen.", "Ich durfte nicht früher gehen.", "Ich wollte nicht früher gehen."], 1, "Burada izin yokluğu anlatılıyor."),
            _q("`Daha erken uyumalısın` cümlesi hangi tonla daha uygundur?", ["musstest", "solltest", "durftest"], 1, "Tavsiye tonu için sollte gerekir."),
            _q("Hangi cümle 'aslında istedim ama olmadı' tonuna daha yakındır?", ["Ich wollte früher nach Hause gehen.", "Ich durfte früher nach Hause gehen.", "Ich musste früher nach Hause gehen."], 0, "wollte niyet ve istek tonunu taşır."),
        ],
    )
)

# A2 lesson 7 refinement: make evaluation language and adjective patterns more concrete.
_get_lesson(7)["lesson_blocks"].append(
    {
        "title": "Bu derste amaç sadece kıyafet adı değil, satın alma kararı vermek",
        "body": "Goethe A2 düzeyinde alışveriş senaryosunda ürünü sadece adlandırman yetmez. Renk, beden, fiyat, rahatlık ve sana uyup uymadığı üzerinden kısa ama mantıklı bir tercih gerekçesi kurabilmen beklenir.",
    }
)
_get_lesson(7)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Ich suche eine schwarze Jacke.",
            "wrong": "Ich suche Jacke schwarze.",
            "reason": "Sıfat ismin önünde ve aynı blok içinde gelir; Türkçe dizilişi kopyalanmaz.",
        }
    }
)
_get_lesson(7)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich brauche einen warmen Mantel.",
            "wrong": "Ich brauche einen warme Mantel.",
            "reason": "Maskulin Akkusativ isimde sıfat sonu burada -en olur; bu kalıp alışverişte çok sık döner.",
        },
        "annotated_examples": [
            {
                "text": "Ich suche einen bequemen Pullover.",
                "note": "Maskulin üründe Akkusativ sonu bu yüzden -en olarak duyulur.",
            },
            {
                "text": "Sie kauft eine schwarze Hose.",
                "note": "Dişil isimle daha tanıdık olan -e sonu devam eder.",
            },
        ],
        "examples": [
            {
                "text": "Ich suche einen bequemen Pullover.",
                "note": "Maskulin üründe Akkusativ sonu bu yüzden -en olarak duyulur.",
            },
            {
                "text": "Sie kauft eine schwarze Hose.",
                "note": "Dişil isimle daha tanıdık olan -e sonu devam eder.",
            },
        ],
    }
)
_get_lesson(7)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Die Jacke gefällt mir, aber sie passt mir nicht.",
            "wrong": "Die Jacke gefällt mich, aber sie passt ich nicht.",
            "reason": "Her iki yapıda da mir gerekir; ayrıca gefallen beğeniyi, passen ise bedensel uyumu anlatır.",
        }
    }
)
_get_lesson(7)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Die Schuhe sind zu teuer, aber die Tasche ist sehr schön.",
            "wrong": "Die Schuhe sind sehr teuer zu, aber die Tasche ist zu schön.",
            "reason": "zu fazlalık/sorun hissi verir; sehr yalnızca yoğunluğu artırır. Yerleri ve anlamları değiştirilemez.",
        }
    }
)
_get_lesson(7).setdefault("common_mistakes", []).append(
    {
        "wrong": "Die Jacke gefällt mir, also passt sie mir.",
        "right": "Die Jacke gefällt mir, aber sie passt mir nicht.",
        "why": "Beğenmek ve bedene uymak aynı şey değildir; alışverişte bu ayrımı açık tutmak gerekir.",
    }
)
_extend_phrase_bank(
    7,
    [
        ("Die Farbe gefällt mir, aber die Größe passt mir nicht.", "Rengi hoşuma gidiyor ama bedeni olmuyor.", "Beğeni ve uyum farkını tek cümlede kurar."),
        ("Ich brauche einen wärmeren Mantel für den Winter.", "Kış için daha sıcak bir paltoya ihtiyacım var.", "Sıfat + isim bloğunu işlevsel bağlama taşır."),
        ("Die Hose ist schön, aber sie ist mir zu eng.", "Pantolon güzel ama bana fazla dar.", "Fiyat dışında beden sorunu anlatmayı öğretir."),
        ("Ich nehme lieber das günstigere Modell.", "Daha uygun fiyatlı modeli tercih ediyorum.", "Karar verme dilini güçlendirir."),
    ],
)
_get_lesson(7).setdefault("exercises", []).append(
    _module(
        "a2-l7-buying-decision",
        "Satın Alma Kararı",
        "Renk, beden, fiyat ve rahatlık üzerinden gerçek seçim dili kur.",
        [
            _q("`Rengi hoşuma gidiyor ama bedeni olmuyor` cümlesi hangisi?", ["Die Farbe gefällt mir, aber die Größe passt mir nicht.", "Die Farbe passt mir, aber die Größe gefällt mir nicht.", "Die Farbe gefällt mich, aber die Größe passt nicht mir."], 0, "gefallen ve passen farklı işlev taşır."),
            _q("`Daha sıcak bir palto arıyorum` için doğru seçenek hangisi?", ["Ich suche einen wärmeren Mantel.", "Ich suche eine wärmere Mantel.", "Ich suche Mantel wärmer."], 0, "Maskulin isimle komparativ sıfat burada doğru çekimlenir."),
            _q("`Bana fazla dar` anlamına en yakın seçenek hangisi?", ["sie ist mir sehr eng", "sie ist mir zu eng", "sie passt mich eng"], 1, "zu eng sorun/fazlalık hissi verir."),
            _q("Hangi cümle gerçek satın alma kararına daha yakındır?", ["Ich nehme lieber das günstigere Modell.", "Das Modell ist Modell.", "Ich bin das Modell lieber."], 0, "Karar verme dili net ve doğaldır."),
        ],
    )
)

# A2 lesson 8 refinement: sharpen connector logic and fix unnatural dialogue line.
_replace_dialogue(
    8,
    "Gerekçe ve karşıtlıkla konuşma",
    [
        ("A", "Kommst du heute Abend auch zum Kurs?", "Bu akşam kursa sen de geliyor musun?"),
        ("B", "Eigentlich bin ich sehr müde. Trotzdem komme ich, weil morgen die Prüfung ist.", "Aslında çok yorgunum. Yine de geliyorum çünkü yarın sınav var."),
        ("A", "Ich habe heute viel Arbeit. Deshalb komme ich vielleicht zehn Minuten später.", "Bugün çok işim var. Bu yüzden belki on dakika geç geleceğim."),
        ("B", "Kein Problem. Wenn du später kommst, reserviere ich dir einen Platz.", "Sorun değil. Geç gelirsen sana bir yer ayırırım."),
        ("A", "Super. Der Bus hat oft Verspätung, trotzdem möchte ich pünktlich sein.", "Harika. Otobüs sık sık gecikiyor, yine de zamanında olmak istiyorum."),
        ("B", "Dann schreib mir kurz. Dann warte ich am Eingang auf dich.", "O zaman bana kısaca yaz. O zaman girişte seni beklerim."),
    ],
)
_get_lesson(8)["lesson_blocks"].append(
    {
        "title": "Aynı olayı deshalb ve trotzdem ile ters yönlerde kurabilmelisin",
        "body": "Bu derste esas hedef iki kelimeyi ezberlemek değil, düşünce yönünü duymaktır. deshalb bir nedeni sonuca bağlar; trotzdem ise o nedenin beklenen sonucunu kırar ve yine de olanı söyler.",
    }
)
_get_lesson(8)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich bin müde. Trotzdem komme ich zum Kurs.",
            "wrong": "Ich bin müde. Trotzdem bleibe ich deshalb zu Hause.",
            "reason": "trotzdem engeli aşıp gerçekleşen eylemi söyler; cümlede yönü karıştırırsan mantık bozulur.",
        }
    }
)
_get_lesson(8)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Der Bus ist spät. Deshalb komme ich später.",
            "wrong": "Der Bus ist spät. Deshalb ich komme später.",
            "reason": "deshalb sonrasında fiil ikinci pozisyonda kalır; bu yapı yan cümle değildir.",
        }
    }
)
_get_lesson(8)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Ich bin krank. Trotzdem muss ich arbeiten.",
            "wrong": "Ich bin krank. Trotzdem ich muss arbeiten.",
            "reason": "Modal fiil de çekimli unsur olarak ikinci yerde gelir; infinitiv sona gider.",
        }
    }
)
_get_lesson(8).setdefault("common_mistakes", []).append(
    {
        "wrong": "Ich bin müde. Deshalb komme ich trotzdem nicht.",
        "right": "Ich bin müde. Trotzdem komme ich.",
        "why": "İki bağlacın yönünü aynı cümlede bulanıklaştırmak yerine tek mantığı temiz kurmak gerekir.",
    }
)
_extend_phrase_bank(
    8,
    [
        ("Ich bin krank. Trotzdem komme ich zur Arbeit.", "Hastayım. Yine de işe geliyorum.", "Engel bilgisi ile gerçekleşen eylemi karşıtlıkla bağlar."),
        ("Der Zug ist ausgefallen. Deshalb fahren wir mit dem Bus.", "Tren iptal oldu. Bu yüzden otobüsle gidiyoruz.", "Sebep-sonuç yönünü çok açık kurar."),
        ("Ich habe wenig Zeit. Trotzdem antworte ich dir heute.", "Az vaktim var. Yine de sana bugün cevap veriyorum.", "A1 mesaj ve zaman dili bu derste tekrar eder."),
        ("Es regnet stark. Deshalb bleiben wir am Abend zu Hause.", "Çok yağmur yağıyor. Bu yüzden akşam evde kalıyoruz.", "A1 hava durumu ve ev kalıpları bağlaçlarla büyür."),
    ],
)
_get_lesson(8).setdefault("exercises", []).append(
    _module(
        "a2-l8-direction-of-logic",
        "Bağlacın Mantık Yönü",
        "Sebep-sonuç ile karşıt-sonuç yönünü karıştırmadan kur.",
        [
            _q("`Yorgunum. Yine de geliyorum.` cümlesine en yakın seçenek hangisi?", ["Ich bin müde. Deshalb komme ich.", "Ich bin müde. Trotzdem komme ich.", "Ich bin müde. Trotzdem ich komme."], 1, "Engel olsa da gerçekleşen eylem var; bu yüzden trotzdem gerekir."),
            _q("`Otobüs geç. Bu yüzden geç geliyorum.` için doğru seçenek hangisi?", ["Der Bus ist spät. Deshalb komme ich später.", "Der Bus ist spät. Trotzdem komme ich später.", "Der Bus ist spät. Deshalb ich komme später."], 0, "Burada düz sonuç ilişkisi kuruluyor."),
            _q("Hangi cümlede modal fiil doğru yerde?", ["Ich bin krank. Trotzdem ich muss arbeiten.", "Ich bin krank. Trotzdem muss ich arbeiten.", "Ich bin krank. Trotzdem arbeiten ich muss."], 1, "Modal fiil ikinci pozisyonda kalır."),
            _q("Hangi kullanım mantık olarak daha temizdir?", ["Ich bin müde. Trotzdem komme ich.", "Ich bin müde. Deshalb trotzdem komme ich.", "Ich bin müde. Trotzdem deshalb komme ich nicht."], 0, "Tek bağlaçla tek yön kurmak daha doğrudur."),
        ],
    )
)

# A2 lesson 9 refinement: make comparison language more decision-oriented and replace generic contrasts.
_get_lesson(9)["lesson_blocks"].append(
    {
        "title": "Bu derste amaç sadece kıyas yapmak değil, seçimi gerekçelendirmek",
        "body": "Komparativ ve superlativ A2'de yalnız dil bilgisi değildir. Otel, ulaşım, ürün, şehir veya plan arasında karar verirken neden bir şeyi seçtiğini birkaç ölçüte dayanarak söyleyebilmen gerekir.",
    }
)
_get_lesson(9)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Dieses Fahrrad ist leichter als das andere.",
            "wrong": "Dieses Fahrrad ist mehr leicht als das andere.",
            "reason": "Çoğu sıfat komparativde doğrudan -er alır; mehr + temel sıfat her yerde kullanılmaz.",
        }
    }
)
_get_lesson(9)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Dieses Zimmer ist am ruhigsten.",
            "wrong": "Dieses Zimmer ist mehr ruhig.",
            "reason": "Bir grup içindeki en yüksek dereceyi anlatırken superlativ gerekir; komparativ tek başına yetmez.",
        }
    }
)
_get_lesson(9)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Der Weg zur Arbeit ist kürzer als früher.",
            "wrong": "Der Weg zur Arbeit ist kürzer wie früher.",
            "reason": "Standart karşılaştırma çizgisinde als kullanılır; wie burada aynı ölçü ilişkisi için beklenmez.",
        }
    }
)
_get_lesson(9)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Mit dem Zug fahre ich lieber als mit dem Auto.",
            "wrong": "Mit dem Zug fahre ich gerner als mit dem Auto.",
            "reason": "gern düzensiz olarak lieber olur; gerner biçimi kullanılmaz.",
        }
    }
)
_get_lesson(9).setdefault("common_mistakes", []).append(
    {
        "wrong": "Dieses Hotel ist am besser.",
        "right": "Dieses Hotel ist am besten.",
        "why": "gut düzensizdir; superlativte besten biçimi gelir.",
    }
)
_extend_phrase_bank(
    9,
    [
        ("Dieses Hotel ist ruhiger als das andere.", "Bu otel diğerinden daha sakin.", "Otel seçimi gibi gerçek karşılaştırma görevlerini güçlendirir."),
        ("Der frühere Zug ist für mich am praktischsten.", "Daha erken tren benim için en kullanışlı olan.", "A1 saat ve ulaşım dili komparativ/superlativ ile birleşiyor."),
        ("Ich lerne lieber am Morgen als am Abend.", "Akşamdan ziyade sabah çalışmayı tercih ederim.", "Düzensiz lieber kalıbını günlük planla bağlar."),
        ("Das zweite Modell ist nicht das billigste, aber es ist besser.", "İkinci model en ucuz değil ama daha iyi.", "Karar gerekçesinde fiyat ve kaliteyi birlikte kullanır."),
    ],
)
_get_lesson(9).setdefault("exercises", []).append(
    _module(
        "a2-l9-choice-justification",
        "Seçimi Gerekçelendirme",
        "Komparativ ve superlativ kullanarak neden bir seçeneği seçtiğini açıkla.",
        [
            _q("`Bu otel diğerinden daha sakin` cümlesi hangisi?", ["Dieses Hotel ist ruhiger als das andere.", "Dieses Hotel ist ruhiger wie das andere.", "Dieses Hotel ist am ruhiger."], 0, "Açık karşılaştırmada als kullanılır."),
            _q("`En kullanışlı seçenek` fikri için doğru yapı hangisi?", ["mehr praktisch", "am praktischsten", "praktischer als"], 1, "Grup içindeki en yüksek dereceyi superlativ verir."),
            _q("`Trenle gitmeyi daha çok tercih ediyorum` için doğru düzensiz biçim hangisi?", ["ich fahre mehr gern", "ich fahre lieber", "ich fahre gerner"], 1, "gern -> lieber düzensiz kalıptır."),
            _q("Hangi cümle seçim gerekçesi bakımından daha güçlüdür?", ["Das zweite Modell ist gut.", "Das zweite Modell ist leichter, bequemer und deshalb praktischer.", "Ich nehme Modell."], 1, "A2'de tercih dilini birkaç ölçütle gerekçelendirmek gerekir."),
        ],
    )
)

# A2 lesson 10 refinement: keep passive limited but more functional for notices and short process language.
_get_lesson(10)["lesson_blocks"].append(
    {
        "title": "A2'de pasifin hedefi her şeyi üretmek değil, kısa duyuruyu anlamak",
        "body": "Bu derste pasif tüm ayrıntılarıyla yüklenmiyor. Asıl hedef, duyuru, ofis süreci, bilgilendirme ve hazırlık cümlelerinde pasifi tanıyabilmek ve birkaç kısa kalıbı kontrollü biçimde kurabilmek.",
    }
)
_get_lesson(10)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Die Unterlagen werden heute vorbereitet.",
            "wrong": "Die Unterlagen sind heute vorbereitet.",
            "reason": "Burada hazırlık süreci anlatılıyor; sonuç durumu değil, işlem ön planda olduğu için werden gerekir.",
        }
    }
)
_get_lesson(10)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Die Tür ist geöffnet.",
            "wrong": "Die Tür wird geöffnet. (mevcut durumu anlatmak isterken)",
            "reason": "Kapının şu an açık olma durumunu anlatıyorsan sein kullanırsın; işlem anını değil sonucu vurgularsın.",
        }
    }
)
_get_lesson(10)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Die Rechnung wird gedruckt. / Die Rechnung ist gedruckt.",
            "wrong": "Die Rechnung wird gedruckt. / Die Rechnung wird gedruckt. (iki anlama aynı kalıpla gitmek)",
            "reason": "Yardımcı fiil değişince bakış açısı değişir; aynı formülle hem işlem hem sonuç anlatılamaz.",
        }
    }
)
_get_lesson(10)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Der Raum wird vorbereitet.",
            "wrong": "Der Raum wird vorbereiten.",
            "reason": "Pasifte mastar değil Partizip II gerekir; kısa örneklerde bile bu omurga korunur.",
        }
    }
)
_get_lesson(10).setdefault("common_mistakes", []).append(
    {
        "wrong": "Die Gäste sind informiert. (işlemin şu an yapıldığını anlatmak isterken)",
        "right": "Die Gäste werden informiert.",
        "why": "Bilgilendirme süreci sürüyorsa werden gerekir; sonuç oluşmuşsa erst dann sein düşünülür.",
    }
)
_extend_phrase_bank(
    10,
    [
        ("Die Unterlagen werden jetzt vorbereitet.", "Belgeler şimdi hazırlanıyor.", "Süreç odaklı pasifi ofis diliyle birleştirir."),
        ("Der Raum ist schon geöffnet.", "Oda çoktan açılmış durumda.", "Sonuç durumunu kısa ve temiz verir."),
        ("Die Gäste werden informiert und später begrüßt.", "Misafirler bilgilendiriliyor ve sonra karşılanıyor.", "Duyuru tonunda iki kısa pasif cümleyi bağlar."),
        ("Die Liste ist schon gedruckt, aber der Vertrag wird noch unterschrieben.", "Liste çoktan basılmış durumda ama sözleşme hâlâ imzalanıyor.", "Süreç ve sonuç farkını aynı bağlamda karşılaştırır."),
    ],
)
_get_lesson(10).setdefault("exercises", []).append(
    _module(
        "a2-l10-notice-and-status",
        "Duyuru ve Durum Ayrımı",
        "Kısa pasif cümlelerde işlem mi sonuç mu anlatıldığını ayır.",
        [
            _q("`Belgeler hazırlanıyor` cümlesi hangisi?", ["Die Unterlagen sind vorbereitet.", "Die Unterlagen werden vorbereitet.", "Die Unterlagen werden vorbereiten."], 1, "Süreç anlatıldığı için werden gerekir."),
            _q("`Kapı açık durumda` cümlesi hangisi?", ["Die Tür wird geöffnet.", "Die Tür ist geöffnet.", "Die Tür ist öffnen."], 1, "Mevcut durum anlatıldığı için sein gerekir."),
            _q("Hangi cümle süreç ile sonucu birlikte doğru ayırıyor?", ["Die Liste ist gedruckt, aber der Vertrag wird noch unterschrieben.", "Die Liste wird gedruckt, aber der Vertrag wird noch unterschrieben. (ikisi de sonuçken)", "Die Liste ist gedruckt, aber der Vertrag ist unterschrieben. (işlem sürerken)"], 0, "İlk cümle sonuç ve süreci bilinçli ayırıyor."),
            _q("A2 için bu derste en doğru hedef hangisi?", ["Pasifin tüm zamanlarını ezberlemek", "Duyurularda ve kısa ofis cümlelerinde pasifi tanımak", "Sadece uzun hukuk metni kurmak"], 1, "Bu ders bilerek sınırlı ve işlevsel tutuluyor."),
        ],
    )
)

# A2 lesson 11 refinement: turn hotel language into a real travel-service flow and replace generic contrasts.
_get_lesson(11)["lesson_blocks"].append(
    {
        "title": "Bu dersin omurgası check-in'den check-out'a kadar akışı kurmak",
        "body": "Otel dili yalnız tek tek kelimelerden oluşmaz. A2 düzeyinde rezervasyon sorma, oda tercihi belirtme, kahvaltı ve ulaşım bilgisi alma, küçük hizmet ricasi yapma ve çıkış sürecini kısaca yönetebilmen gerekir.",
    }
)
_get_lesson(11)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Wir bleiben im Hotel am Bahnhof.",
            "wrong": "Wir bleiben in dem Hotel an dem Bahnhof.",
            "reason": "A2'de bu tür sık birleşen yapılar ayrı ayrı çözülebilir ama gündelik kullanımda kısalmış biçimler daha doğal ve daha hızlı tanınır.",
        }
    }
)
_get_lesson(11)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Wann ist das Frühstück?",
            "wrong": "Wann das Frühstück ist?",
            "reason": "Ana soru cümlesinde çekimli fiil ikinci konuma gelir; resepsiyon dilinde bu tür kısa soruların akıcı çıkması gerekir.",
        }
    }
)
_get_lesson(11)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Ich komme aus dem Hotel, aber meine Freunde kommen vom Bahnhof.",
            "wrong": "Ich komme vom Hotel, aber meine Freunde kommen aus dem Bahnhof.",
            "reason": "aus daha iç mekân/kapalı alan çıkışını, vom ise bir nokta ya da hizmet yerinden geliş hissini daha doğal taşır; bağlamı ters kurmak kulağa yabancı gelir.",
        }
    }
)
_get_lesson(11)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Könnten Sie mir bitte ein ruhigeres Zimmer geben?",
            "wrong": "Ich will ein ruhigeres Zimmer.",
            "reason": "İstek mümkündür ama otel hizmet dilinde yumuşak rica kalıbı sosyal olarak daha doğru ve daha başarılıdır.",
        }
    }
)
_get_lesson(11).setdefault("common_mistakes", []).append(
    {
        "wrong": "Könnten Sie mir bitte den Schlüssel geben und wo ist Frühstück?",
        "right": "Könnten Sie mir bitte den Schlüssel geben? Und wo ist das Frühstück?",
        "why": "Hizmet dilinde iki işi tek bozuk cümlede sıkıştırmak yerine kısa ve net iki soru kurmak daha doğaldır; ayrıca Frühstück önünde artikel eksik kalmamalıdır.",
    }
)
_extend_phrase_bank(
    11,
    [
        ("Ich habe auf Ihren Namen eine Reservierung.", "Sizin adınıza bir rezervasyonum var.", "Check-in sırasında sahiplik ve rezervasyon bilgisi daha net kurulur."),
        ("Könnten Sie mir bitte ein Zimmer zum Innenhof geben?", "Bana mümkünse avluya bakan bir oda verebilir misiniz?", "A1 sıfat ve yön bilgisi artık daha somut hizmet ricasına bağlanıyor."),
        ("Ist das Frühstück im Preis inbegriffen?", "Kahvaltı fiyata dahil mi?", "Otel dili ödeme ve hizmet bilgisini birlikte taşır."),
        ("Könnte ich morgen etwas später auschecken?", "Yarın biraz daha geç çıkış yapabilir miyim?", "A2'de hizmet isteme yalnız check-in değil, check-out tarafını da kapsar."),
    ],
)
_get_lesson(11).setdefault("exercises", []).append(
    _module(
        "a2-l11-stay-flow",
        "Konaklama Akışı",
        "Rezervasyon, oda tercihi, kahvaltı ve çıkış sürecini tek akış olarak düşün.",
        [
            _q("`Kahvaltı fiyata dahil mi?` cümlesine en yakın seçenek hangisi?", ["Ist das Frühstück im Preis inbegriffen?", "Ist das Frühstück vom Preis?", "Frühstück ist Preis inklusive?"], 0, "inbegriffen kalıbı otel ve hizmet dilinde çok doğaldır."),
            _q("Daha nazik oda değişikliği talebi hangisi?", ["Ich will ein anderes Zimmer.", "Könnten Sie mir bitte ein anderes Zimmer geben?", "Geben Sie anderes Zimmer."], 1, "Hizmet dilinde yumuşak rica daha doğru çalışır."),
            _q("`Otel istasyonun yanında` cümlesinde en doğal yapı hangisi?", ["Das Hotel ist am Bahnhof.", "Das Hotel ist an dem Bahnhof.", "Das Hotel ist im Bahnhof."], 0, "am kısalmış ve doğal biçimdir."),
            _q("`Biraz daha geç çıkış yapabilir miyim?` için doğru seçenek hangisi?", ["Könnte ich etwas später auschecken?", "Ich kann später Auschecken?", "Können später ich auschecken?"], 0, "Nazik hizmet isteğinde könnte ich ... yapısı güvenli ve doğaldır."),
        ],
    )
)

# A2 lesson 12 refinement: make target-type selection explicit and remove weak tooltip choices.
_get_lesson(12)["lesson_blocks"].append(
    {
        "title": "Önce hedefin türünü tanı, sonra edatı seç",
        "body": "Bu derste asıl beceri yalnız yön sormak değil, hedefin ne olduğunu birkaç saniyede sınıflandırmaktır. Şehir ve ülke, kişi ve kurum, kapalı mekân, açık alan ve ev kalıpları ayrıştığında nach, zu, in ve auf daha güvenli yerleşir.",
    }
)
_get_lesson(12)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Wohin gehst du jetzt?",
            "wrong": "Wo gehst du jetzt?",
            "reason": "Bir hedefe doğru hareket soruluyorsa Wohin gerekir; Wo ancak mevcut konumu sorar.",
        }
    }
)
_get_lesson(12)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich fahre nach Köln, dann gehe ich zur Bank und später in die Apotheke.",
            "wrong": "Ich fahre zu Köln, dann gehe ich nach der Bank und später zur Apotheke hinein.",
            "reason": "Şehirlerde çoğu zaman nach, kişi/kurum yöneliminde zu, kapalı mekâna girişte in kullanılır; hedef türünü karıştırınca cümle doğal akmaz.",
        }
    }
)
_get_lesson(12)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Am Abend gehe ich nach Hause, aber jetzt bin ich noch zu Hause.",
            "wrong": "Am Abend gehe ich zu Hause, aber jetzt bin ich nach Hause.",
            "reason": "nach Hause hareket yönünü, zu Hause ise sabit konumu anlatır; bu ikiliyi ters çevirmek A2'de çok görünür bir hatadır.",
        }
    }
)
_get_lesson(12)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Gehen Sie zuerst geradeaus und biegen Sie dann links ab.",
            "wrong": "Gehen Sie zuerst geradeaus und dann Sie links abbiegen.",
            "reason": "Yön tarifinde ikinci fiilli bozuk yapı yerine kısa ve temiz komut cümleleri gerekir.",
        }
    }
)
_get_lesson(12).setdefault("common_mistakes", []).append(
    {
        "wrong": "Ich gehe nach der Apotheke und später zu Hause.",
        "right": "Ich gehe zur Apotheke und später nach Hause.",
        "why": "Kurum yöneliminde zu, eve dönüşte nach Hause gerekir; iki hedef türü aynı yapıyla kurulmaz.",
    }
)
_replace_reading(
    12,
    "Merkeze nasıl gidilir?",
    "14 kelime / kalıp",
    [
        "Yeni bir şehre gelen biri önce [[zum Bahnhof::istasyona]], sonra [[ins Zentrum::merkezin içine]] ve daha sonra başka bir kuruma nasıl gidileceğini ayırt etmek zorunda kalır. Bu yüzden hedefin şehir mi, kurum mu, yoksa kapalı bir mekân mı olduğunu fark etmek çok önemlidir.",
        "Bazen kişi önce [[zur Apotheke::eczane yönüne]] gider, sonra birkaç dakika [[geradeaus::dümdüz]] yürür ve büyük bir [[Kreuzung::kavşak]] yakınında sola döner. Eğer hava kötüyse, [[mit der U-Bahn::metro ile]] gitmek daha rahat olabilir; ama kısa yollarda yürümek yön ifadelerini daha iyi yerleştirir.",
        "Akşam olunca pek çok kişi [[nach Hause::eve]] döner; ertesi sabah ise yeniden [[zu Hause::evde]] hazırlanır ve işe ya da kursa gider. Aynı kelime alanı tekrar eder, ama bu kez hareket ve konum ayrımı daha bilinçli kullanılır.",
    ],
)
_extend_phrase_bank(
    12,
    [
        ("Ich fahre heute nach Köln und danach zur Universität.", "Bugün Köln'e gidiyorum, sonra üniversiteye geçiyorum.", "Şehir ve kurum hedefi aynı akışta ayrılıyor."),
        ("Am Abend gehen wir auf den Markt und später nach Hause.", "Akşam pazara gidiyoruz, sonra eve dönüyoruz.", "Açık alan ve ev kalıbı birlikte tekrar ediyor."),
        ("Nach dem Kurs gehe ich zur Apotheke und dann ins Zentrum.", "Dersten sonra eczaneye gidiyorum ve sonra merkeze geçiyorum.", "A1 rutin sırası hareket edatlarıyla büyüyor."),
        ("Gehen Sie an der Kreuzung rechts und dann geradeaus weiter.", "Kavşakta sağa dönün ve sonra dümdüz devam edin.", "Yön komutları artık daha gerçek rota zinciri kuruyor."),
    ],
)
_get_lesson(12).setdefault("exercises", []).append(
    _module(
        "a2-l12-target-type-selection",
        "Hedef Türünü Seç",
        "Şehir, kurum, kapalı mekân, açık alan ve ev için doğru hareket yapısını seç.",
        [
            _q("`Yarın Ankara'ya gidiyorum` cümlesine en yakın doğru yapı hangisi?", ["Ich gehe zur Ankara.", "Ich fahre nach Ankara.", "Ich fahre in Ankara."], 1, "Şehir yöneliminde çoğu zaman nach kullanılır."),
            _q("`Bankaya gidiyorum` cümlesinde en doğal seçenek hangisi?", ["Ich gehe zur Bank.", "Ich gehe nach der Bank.", "Ich gehe in Bank."], 0, "Kurum yöneliminde zu çok daha doğaldır."),
            _q("`Eczanenin içine gidiyor` cümlesi hangisi?", ["Sie geht zur Apotheke hinein.", "Sie geht in die Apotheke.", "Sie geht nach Apotheke."], 1, "Kapalı mekâna girişte in + Akkusativ beklenir."),
            _q("`Şimdi evdeyim ama birazdan eve gideceğim` cümlesinin doğru omurgası hangisi?", ["Ich bin nach Hause, aber später gehe ich zu Hause.", "Ich bin zu Hause, aber später gehe ich nach Hause.", "Ich bin im Hause, aber später gehe ich zu Hause."], 1, "Konum ve hareket için iki farklı kalıp gerekir."),
        ],
    )
)

# A2 lesson 13 refinement: sharpen conjunction meaning and verb-final reflex, remove weak tooltip choices.
_get_lesson(13)["lesson_blocks"].append(
    {
        "title": "Bağlaç seçmek yalnız anlamı değil, bütün cümle ritmini değiştirir",
        "body": "Bu derste hedef sadece weil, dass, wenn kelimelerini tanımak değil. Hangi bağlacın hangi ilişkiyi kurduğunu ve çekimli fiilin yan cümlede sistemli biçimde sona kaydığını otomatikleştirmen gerekiyor.",
    }
)
_get_lesson(13)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Ich lerne heute länger, weil ich morgen eine Prüfung habe.",
            "wrong": "Ich lerne heute länger, weil ich habe morgen eine Prüfung.",
            "reason": "weil sonrası artık ana cümle düzeniyle devam etmez; çekimli fiil yan cümlenin sonuna gider.",
        }
    }
)
_get_lesson(13)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Ich denke, dass der Plan gut ist.",
            "wrong": "Ich denke, dass ist der Plan gut.",
            "reason": "dass içerik cümlesi açar; yan cümle içinde özne ve diğer ögeler fiilden önce gelir, çekimli fiil sona kayar.",
        }
    }
)
_get_lesson(13)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Wenn ich Zeit habe, rufe ich meine Mutter an.",
            "wrong": "Wenn ich Zeit habe, ich rufe meine Mutter an.",
            "reason": "Yan cümle öne geldiğinde ana cümlenin çekimli fiili hemen gelir; iki parçayı peş peşe özneyle başlatamazsın.",
        }
    }
)
_get_lesson(13)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "..., weil der Bus spät kommt.",
            "wrong": "..., weil kommt der Bus spät.",
            "reason": "Yan cümlede bağlaçtan sonra Almanca fiili sona gönderir; bu dersin en görünür yapısal hedefi budur.",
        }
    }
)
_get_lesson(13).setdefault("common_mistakes", []).append(
    {
        "wrong": "Ich weiß, dass morgen kommt er später.",
        "right": "Ich weiß, dass er morgen später kommt.",
        "why": "dass yan cümlesinde de çekimli fiil sona gider; yarın gibi zaman ifadesi fiilden önce rahatça yer alabilir.",
    }
)
_replace_reading(
    13,
    "Neden böyle oldu?",
    "14 kelime / kalıp",
    [
        "Birçok kursiyer bir süre sonra fark eder, [[dass::...ki / ...dığını]] daha uzun cümleler kurabilmek için bağlaçlara gerçekten ihtiyaç vardır. Kısa cevaplar iletişimi başlatır; ama neden, düşünce ve şart anlatımı olmadan A2 konuşması sınırlı kalır.",
        "Örneğin biri bugün daha uzun çalışır, [[weil::çünkü]] yarın önemli bir görüşmesi vardır. Akşam eve dönünce bir arkadaşına yazar ve söyler, [[dass::...dığını]] biraz heyecanlı olduğunu ama yine de hazırlanabildiğini düşünüyor.",
        "Eğer akşam vakti kalırsa, yani [[wenn::eğer / ne zaman]] zamanı olursa, birkaç örnek daha tekrar eder ve eski A1 konularını da kullanır: aile, kurs, saat, yolculuk ve günlük planlar. Böylece yeni yapı eski kelime alanlarını da birlikte taşır.",
    ],
)
_extend_phrase_bank(
    13,
    [
        ("Ich sage dir Bescheid, wenn ich später komme.", "Daha geç gelirsem sana haber veririm.", "A1 mesaj ve zaman dili koşul cümlesine taşınıyor."),
        ("Ich hoffe, dass wir den Zug noch erreichen.", "Treni hâlâ yetiştireceğimizi umuyorum.", "A1 ulaşım alanı artık düşünce aktarımıyla birleşiyor."),
        ("Wir bleiben heute zu Hause, weil meine Schwester krank ist.", "Bugün evde kalıyoruz çünkü kız kardeşim hasta.", "A1 aile ve ev alanı neden cümlesine bağlanıyor."),
        ("Wenn der Kurs früher endet, trinken wir noch einen Kaffee.", "Kurs daha erken biterse bir kahve daha içeriz.", "A1 kurs ve içecek alanı yeni yapıyla tekrar ediyor."),
    ],
)
_get_lesson(13).setdefault("exercises", []).append(
    _module(
        "a2-l13-conjunction-and-verb-final",
        "Bağlaç ve Fiil Sonu",
        "weil, dass ve wenn ile anlamı seç ve fiili doğru yere gönder.",
        [
            _q("`Bugün daha uzun çalışıyorum çünkü yarın sınavım var` cümlesi hangisi?", ["Ich lerne heute länger, weil ich morgen eine Prüfung habe.", "Ich lerne heute länger, weil ich habe morgen eine Prüfung.", "Ich lerne heute länger, dass ich morgen eine Prüfung habe."], 0, "Sebep verildiği için weil gerekir ve fiil sona gider."),
            _q("`Planın iyi olduğunu düşünüyorum` cümlesi hangisi?", ["Ich denke, weil der Plan gut ist.", "Ich denke, dass der Plan gut ist.", "Ich denke, wenn der Plan gut ist."], 1, "Fikir içeriği aktarmada dass kullanılır."),
            _q("`Vaktim olursa seni ararım` cümlesine en yakın doğru seçenek hangisi?", ["Wenn ich Zeit habe, ich rufe dich an.", "Wenn ich Zeit habe, rufe ich dich an.", "Weil ich Zeit habe, rufe ich dich an."], 1, "Yan cümle öndeyse ana cümlenin fiili hemen gelir."),
            _q("Bu derste en temel yapısal refleks hangisi?", ["Bağlaçtan sonra fiili erkene almak", "Yan cümlede çekimli fiili sona göndermek", "Her cümleyi nur ile kurmak"], 1, "A2 yan cümle mantığının omurgası budur."),
        ],
    )
)

# A2 lesson 14 refinement: replace placeholder contrasts and turn the closing lesson into an exam-facing action plan.
_get_lesson(14)["lesson_blocks"].append(
    {
        "title": "Kapanış dersi geleceği anlatmaktan fazlasını yapmalı",
        "body": "A2 sonunda hedef yalnızca 'yapacağım' demek değil. Çalışma planını, sınav niyetini, tekrar düzenini ve gerekçeni bir arada anlatabiliyorsan bu ders gerçekten kapanış işlevi görür.",
    }
)
_get_lesson(14)["grammar_sections"][0].update(
    {
        "contrast": {
            "correct": "Ich werde morgen früher lernen.",
            "wrong": "Ich werde morgen früher lerne.",
            "reason": "werden ile gelecek kurarken asıl fiil çekilmez; yalın halde cümlenin sonunda kalır.",
        }
    }
)
_get_lesson(14)["grammar_sections"][1].update(
    {
        "contrast": {
            "correct": "Am Freitag werde ich zum Arzt gehen, aber es wird am Wochenende regnen.",
            "wrong": "Am Freitag wird ich zum Arzt gehen, aber es wird am Wochenende geregnet.",
            "reason": "İlk cümle takvimlenmiş plan, ikinci cümle tahmindir; ayrıca hava olayında gelecek tahmini için mastar kullanılır, pasif gibi kurulmaz.",
        }
    }
)
_get_lesson(14)["grammar_sections"][2].update(
    {
        "contrast": {
            "correct": "Nächste Woche werde ich zum Goethe-Zentrum fahren.",
            "wrong": "Nächste Woche werde ich fahren zum Goethe-Zentrum.",
            "reason": "Zaman ve hedef bilgisi ortaya gelebilir ama infinitiv genellikle sona kalır; Alman cümle ritmi burada korunmalıdır.",
        }
    }
)
_get_lesson(14)["grammar_sections"][3].update(
    {
        "contrast": {
            "correct": "Wenn ich genug übe, werde ich ruhiger sprechen.",
            "wrong": "Wenn ich genug übe, ich werde ruhiger sprechen.",
            "reason": "Yan cümle öne geldiğinde ana cümlenin çekimli unsuru hemen gelir; eski A2 yapıları burada yeniden devreye girer.",
        }
    }
)
_get_lesson(14).setdefault("common_mistakes", []).append(
    {
        "wrong": "Ich werde bin am Wochenende zu Hause.",
        "right": "Ich werde am Wochenende zu Hause sein.",
        "why": "werden gelecek hissini taşır; sein ise yalın infinitiv olarak sona gider. İki çekimli fiili üst üste kuramazsın.",
    }
)
_extend_phrase_bank(
    14,
    [
        ("Ich werde mich im Mai für die Prüfung anmelden.", "Mayısta sınav için kayıt yaptıracağım.", "Gelecek planı artık sınav hedefiyle somutlaşıyor."),
        ("Wenn ich konsequent wiederhole, werde ich sicherer sprechen.", "Düzenli tekrar edersem daha güvenli konuşacağım.", "A2 kapanışında yan cümle ve gelecek birleşiyor."),
        ("Ich glaube, dass ich bis zum Sommer längere Texte besser verstehen werde.", "Yaza kadar daha uzun metinleri daha iyi anlayacağımı düşünüyorum.", "dass yapısı ve gelecek birlikte sınav hedefi kuruyor."),
        ("Nächste Woche werde ich zuerst lesen und danach Schreiben üben.", "Gelecek hafta önce okuma sonra yazma çalışacağım.", "A1 sıra zarfları A2 kapanış planına taşınıyor."),
    ],
)
_get_lesson(14).setdefault("exercises", []).append(
    _module(
        "a2-l14-exam-facing-future",
        "Gelecek Planı ve Sınav Hedefi",
        "werden yapısını plan, tahmin ve çalışma stratejisiyle birlikte kur.",
        [
            _q("`Mayısta sınava kayıt yaptıracağım` cümlesine en yakın doğru seçenek hangisi?", ["Ich werde mich im Mai für die Prüfung anmelden.", "Ich werde mich im Mai für die Prüfung angemeldet.", "Ich mich werde im Mai für die Prüfung anmelden."], 0, "werden çekimli gelir, asıl fiil sonda yalın kalır."),
            _q("`Düzenli tekrar edersem daha güvenli konuşacağım` cümlesi hangisi?", ["Wenn ich konsequent wiederhole, ich werde sicherer sprechen.", "Wenn ich konsequent wiederhole, werde ich sicherer sprechen.", "Weil ich konsequent wiederhole, werde ich sicherer sprechen."], 1, "Yan cümle öndeyse ana cümlenin fiili hemen gelir."),
            _q("Hangisi tahmin tonu taşır?", ["Ich werde morgen um acht zum Kurs gehen.", "Es wird am Abend regnen.", "Ich werde mich anmelden."], 1, "Hava olaylarıyla kurulan bu cümle daha çok öngörü tonundadır."),
            _q("Kapanış dersinin en doğru hedefi hangisi?", ["Sadece werden formunu ezberlemek", "Gelecek planını eski A1-A2 yapılarıyla birlikte anlatabilmek", "Yalnızca şehir isimlerini tekrarlamak"], 1, "Bu ders bilinçli olarak toparlama ve üretim becerisi hedefler."),
        ],
    )
)
