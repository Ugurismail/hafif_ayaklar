"""Release-candidate content for Phase 3, Stage A of the logic course.

This module is intentionally not imported by the learner-facing course yet.
Keeping the candidate data isolated lets us review the full stage, preserve
existing progress records, and switch the curriculum only after the release
gates in ``docs/logic_phase3_stage_a_spec.md`` are satisfied.
"""


STAGE_A_SOURCE_REFERENCES = {
    "forallx-arguments": {
        "title": "forall x: Calgary - Arguments",
        "url": "https://forallx.openlogicproject.org/html/Ch1.html",
    },
    "forallx-validity": {
        "title": "forall x: Calgary - Validity",
        "url": "https://forallx.openlogicproject.org/html/Ch2.html",
    },
    "forallx-notions": {
        "title": "forall x: Calgary - Other logical notions",
        "url": "https://forallx.openlogicproject.org/html/Ch3.html",
    },
    "forallx-use-mention": {
        "title": "forall x: Calgary - Use and mention",
        "url": "https://forallx.openlogicproject.org/html/Ch8.html",
    },
    "openstax-conditionals": {
        "title": "OpenStax Introduction to Philosophy - Logical statements",
        "url": "https://openstax.org/books/introduction-philosophy/pages/5-2-logical-statements",
    },
    "sep-necessary-sufficient": {
        "title": "Stanford Encyclopedia of Philosophy - Necessary and sufficient conditions",
        "url": "https://plato.stanford.edu/entries/necessary-sufficient/",
    },
    "dowden-only-unless": {
        "title": "Logical Reasoning - The logic of only, only-if, and unless",
        "url": "https://human.libretexts.org/Bookshelves/Philosophy/Logic_and_Reasoning/Logical_Reasoning_(Dowden)/11%3A_Logical_Form_and_Sentential_Logic/11.03%3A_Logical_Forms_of_Statements_and_Arguments/11.3.05%3A_The_Logic_of_Only_Only-If_and_Unless",
    },
}


def _section(
    title,
    summary,
    when_to_use,
    formula,
    logic,
    watch_out,
    examples,
    contrast,
):
    return {
        "title": title,
        "summary": summary,
        "when_to_use": when_to_use,
        "formula": formula,
        "logic": logic,
        "watch_out": watch_out,
        "examples": [
            {"text": text, "note": note}
            for text, note in examples
        ],
        "contrast": {
            "correct": contrast[0],
            "wrong": contrast[1],
            "reason": contrast[2],
        },
    }


def _worked(text, reason, badge_label, badge_variant="good"):
    return {
        "text": text,
        "reason": reason,
        "badge_label": badge_label,
        "badge_variant": badge_variant,
    }


def _practice(items):
    return [
        {
            "prompt": prompt,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "difficulty_label": difficulty,
        }
        for prompt, choices, answer, explanation, difficulty in items
    ]


def _production_task(
    prompt,
    checkpoints,
    sample_focus,
    stimulus_label,
    stimulus_items,
    stimulus_note="",
):
    return {
        "prompt": prompt,
        "checkpoints": checkpoints,
        "sample_focus": sample_focus,
        "stimulus": {
            "label": stimulus_label,
            "items": stimulus_items,
            "note": stimulus_note,
        },
    }


def _lesson(
    curriculum_id,
    slug,
    title,
    summary,
    focus,
    estimated_minutes,
    prerequisites,
    competencies,
    goals,
    key_terms,
    sections,
    worked_examples,
    mistakes,
    practice_items,
    guided_practice,
    production_tasks,
    mastery_evidence,
    review_prompts,
    next_step,
    source_ids,
    academic_note,
    legacy_sources,
):
    return {
        "curriculum_id": curriculum_id,
        "release_status": "candidate",
        "order": int(curriculum_id[1:]),
        "slug": slug,
        "title": title,
        "summary": summary,
        "focus": focus,
        "duration": f"{estimated_minutes} dk",
        "estimated_minutes": estimated_minutes,
        "prerequisites": prerequisites,
        "competencies": competencies,
        "goals": goals,
        "key_terms": [
            {"term": term, "definition": definition}
            for term, definition in key_terms
        ],
        "sections": sections,
        "worked_examples": worked_examples,
        "mistakes": mistakes,
        "practice": practice_items,
        "guided_practice": guided_practice,
        "production_tasks": production_tasks,
        "mastery_evidence": mastery_evidence,
        "review_prompts": review_prompts,
        "next_step": next_step,
        "source_ids": source_ids,
        "reading_note": "",
        "rigor_note": academic_note,
        "symbol_set": [],
        "proof_tools": [],
        "legacy_sources": legacy_sources,
    }


STAGE_A_CANDIDATE_LESSONS = [
    _lesson(
        "A1",
        "ders-1-onerme-nedir",
        "İfade, Bağlam ve Önerme",
        "Bir dil parçasının görünüşüne değil, bağlam içinde doğru ya da yanlış olabilen bir bildirim taşıyıp taşımadığına bakar.",
        "Mantıksal okuryazarlık",
        25,
        [],
        ["claim.identify", "context.resolve", "proposition.distinguish"],
        [
            "Soru, emir, yalın ünlem ve bildirim işlevlerini ayırmak.",
            "Cümle ile cümlenin bağlam içinde ifade ettiği önerme arasındaki çalışma ayrımını kullanmak.",
            "Bağlama bağlı ifadeleri değerlendirilebilir açık bildirimlere dönüştürmek.",
        ],
        [
            ("İfade", "Belirli bir bağlamda kullanılan sözlü ya da yazılı dil parçası."),
            ("Bildirim", "Bir şeyin öyle olduğunu ileri süren dilsel kullanım."),
            ("Önerme", "Bağlam içinde bir bildirim cümlesinin doğru ya da yanlış olabilen içeriği."),
            ("Doğruluk değeri", "Bir önermenin doğru veya yanlış olması."),
            ("Bağlama bağlı ifade", "Kişi, yer, zaman veya gösterilen nesne bilinmeden içeriği tamamlanmayan ifade."),
        ],
        [
            _section(
                "Dilbilgisel biçim ile kullanım işlevi",
                "Noktalama ve cümle biçimi ilk ipucunu verir; mantıksal sınıflama ise ifadenin bağlamda ne yaptığını sorar.",
                "Bir metindeki parçaların bildirim mi, soru mu, emir mi olduğunu ayırırken.",
                "Önce şu soruyu sor: Bu kullanım bir şeyin öyle olduğunu ileri sürüyor mu?",
                "Doğruluk değerlendirmesi, ancak bir iddia ortaya konduğunda başlayabilir.",
                "Retorik sorular ve dolaylı emirler yüzey biçimleriyle yanıltabilir; yalın ünlemi, içinde bildirim de bulunan ünlemli kullanımdan ayır.",
                [
                    ("Kapıyı kapat.", "Bir davranış talep eder; doğru ya da yanlış bir bildirim sunmaz."),
                    ("Kapı kapalıdır.", "Kapının durumu hakkında doğru veya yanlış olabilecek bir bildirimdir."),
                    ("Kapı kapalı mı?", "Bilgi ister; tek başına bir doğruluk iddiası ileri sürmez."),
                    ("Eyvah!", "Yalın bir duygu dışavurumudur; tek başına doğru ya da yanlış bir bildirim sunmaz."),
                    ("Eyvah, anahtarı içeride unuttum!", "Duygu dışavurumunun yanında doğru ya da yanlış olabilen bir bildirim de taşır."),
                ],
                (
                    "İfadeyi, bağlamdaki işlevine bakarak sınıflandırmak.",
                    "Sonunda nokta bulunan her şeyi önerme saymak.",
                    "Noktalama işareti tek başına kullanım işlevini ve doğruluk değeri taşıyan içeriği belirlemez.",
                ),
            ),
            _section(
                "Cümle ile ifade edilen içerik",
                "Bu derste önerme, bir bildirim cümlesinin doğru ya da yanlış olabilen içeriği için kullanılan çalışma terimidir.",
                "Farklı sözcüklerle kurulan cümlelerin aynı iddiayı taşıyıp taşımadığını incelerken.",
                "Yanlış olmak ile doğru ya da yanlış olamamak farklıdır.",
                "Bir önerme yanlış olabilir; önemli olan doğruluk değerlendirmesine açık olmasıdır.",
                "Önermenin metafizik statüsü burada çözülmüş sayılmaz; çalışma tanımı ileride yeniden tartışılacaktır.",
                [
                    ("Dünya'nın iki uydusu vardır.", "Yanlıştır; fakat yine de doğruluk değeri taşıyan bir içerik ifade eder."),
                    ("Türkiye'nin başkenti Ankara'dır.", "Ankara Türkiye'nin başkentidir cümlesiyle aynı temel içeriği ifade eder."),
                ],
                (
                    "Yanlış bildirimi önerme olarak tanımaya devam etmek.",
                    "Yanlış olan her ifadeyi önerme dışı saymak.",
                    "Önerme olma, doğru olma değil doğru veya yanlış olabilme koşuludur.",
                ),
            ),
            _section(
                "Bağlam içeriği tamamlar",
                "Ben, burada, bugün ve o gibi ifadelerin gönderimi konuşana, yere, zamana veya gösterime göre değişir.",
                "Bir cümlenin değerlendirilmesi için eksik kişi, yer ve zaman bilgisini belirlerken.",
                "Bağlamı açıkla: kim, nerede, ne zaman, hangi nesne?",
                "Bağlama bağlı ifade anlamsız değildir; uygun bağlam verildiğinde belirli bir önerme ifade edebilir.",
                "Bağlam bilinmiyorsa hemen yanlış deme; önce hangi bilginin eksik olduğunu göster.",
                [
                    ("Ben buradayım.", "Konuşan kişi ile söylenme yeri bilinirse değerlendirilebilir."),
                    ("Bugün hava soğuk.", "Tarih, yer ve ölçüt belirginleştiğinde daha açık bir bildirim olur."),
                ],
                (
                    "Eksik bağlam bilgisini adlandırmak.",
                    "Bağlama bağlı her ifadeyi anlamsız saymak.",
                    "Sorun çoğu kez anlam yokluğu değil, değerlendirme için gerekli bağlamın verilmemesidir.",
                ),
            ),
        ],
        [
            _worked("Kapıyı kapat.", "Bir eylem talep eder; doğru ya da yanlış değildir.", "Emir", "bad"),
            _worked("Eyvah!", "Yalın bir duygu dışavurumudur; tek başına doğruluk değeri taşımaz.", "Ünlem", "bad"),
            _worked("Toplantı ne zaman başladı?", "Bilgi ister; tek başına bir doğruluk iddiası sunmaz.", "Soru", "bad"),
            _worked("Dünya'nın iki uydusu vardır.", "Yanlış olsa da doğruluk değerlendirmesine açıktır.", "Önerme"),
            _worked("Bugün hava soğuk.", "Uygun yer, tarih ve ölçüt verildiğinde belirli bir önerme ifade eder.", "Bağlam gerekli"),
            _worked("Türkiye'nin başkenti Ankara'dır.", "Belirli ve doğruluk değeri taşıyan bir bildirimdir.", "Önerme"),
        ],
        [
            "Yanlış bir bildirimi önerme olmayan ifadeyle karıştırmak.",
            "Noktalama işaretini tek karar ölçütü yapmak.",
            "Bağlama bağlı ifadeyi otomatik olarak anlamsız saymak.",
            "Aynı içeriğin farklı cümlelerle ifade edilemeyeceğini varsaymak.",
        ],
        _practice([
            ("'Lütfen pencereyi aç.' hangi işlevdedir?", ["Bildirim", "Emir/rica", "Soru", "Tanım"], "Emir/rica", "Bir davranış talep eder; doğruluk iddiası sunmaz.", "Temel"),
            ("'Mars'ın üç uydusu vardır.' yanlışsa neden yine de önerme ifade eder?", ["Bilimsel olduğu için", "Doğru ya da yanlış olabildiği için", "Noktayla bittiği için", "Uzun olduğu için"], "Doğru ya da yanlış olabildiği için", "Fiilen yanlış olmak, doğruluk değeri taşıma özelliğini ortadan kaldırmaz.", "Temel"),
            ("'Ben yarın geleceğim.' ifadesini değerlendirmek için en az hangi bilgi gerekir?", ["Yalnız konuşanın yaşı", "Konuşan ve söylenme zamanı", "Yalnız cümlenin uzunluğu", "Hiçbir ek bilgi"], "Konuşan ve söylenme zamanı", "Ben ve yarın ifadelerinin gönderimi bağlama bağlıdır.", "Orta"),
            ("Hangisi tek başına bir bildirim değildir?", ["Su deniz seviyesinde yaklaşık 100 derecede kaynar.", "Toplantı saat üçte başladı.", "Toplantı ne zaman başladı?", "Ankara Türkiye'dedir."], "Toplantı ne zaman başladı?", "Bu kullanım bilgi ister; bir şeyin öyle olduğunu ileri sürmez.", "Orta"),
            ("Hangi iki cümle aynı temel içeriği ifade eder?", ["Ankara Türkiye'nin başkentidir / Türkiye'nin başkenti Ankara'dır", "Kapıyı aç / Kapı açıktır", "Yağmur yağıyor mu / Yağmur yağıyor", "Ali geldi / Ali gelmedi"], "Ankara Türkiye'nin başkentidir / Türkiye'nin başkenti Ankara'dır", "Sözcük dizimi farklı olsa da iki cümle aynı başkentlik iddiasını taşır.", "Orta"),
            ("'Bu ağırdır.' cümlesiyle ilgili en dikkatli karar hangisidir?", ["Kesinlikle yanlıştır", "Kesinlikle anlamsızdır", "Gösterilen nesne ve ölçüt bilinmeden değerlendirme eksiktir", "Her bağlamda doğrudur"], "Gösterilen nesne ve ölçüt bilinmeden değerlendirme eksiktir", "Bu ve ağır ifadeleri bağlam bilgisi ister.", "İleri"),
            ("Önerme olmanın ölçütü hangisidir?", ["Fiilen doğru olmak", "Doğru ya da yanlış olabilen içerik taşımak", "Resmî dil kullanmak", "En az beş sözcük içermek"], "Doğru ya da yanlış olabilen içerik taşımak", "Doğruluk değeri taşıma ile fiilen doğru olma ayrılmalıdır.", "İleri"),
            ("'Eyvah!' ifadesi bu bağlamda neden önerme ifade etmez?", ["Tek sözcük olduğu için", "Yalın bir duygu dışavurumu olup doğruluk iddiası sunmadığı için", "Ünlem işareti her zaman yasak olduğu için", "Gündelik dilde kullanıldığı için"], "Yalın bir duygu dışavurumu olup doğruluk iddiası sunmadığı için", "Ölçüt sözcük sayısı veya noktalama değil, kullanımın doğruluk değerlendirmesine açık bir iddia sunup sunmamasıdır.", "Zor"),
        ]),
        {
            "prompt": "'Bugün herkes burada' ifadesini değerlendirilebilir hâle getir.",
            "starter": "Önce bugün, herkes ve burada sözcüklerinin hangi bilgiye bağlı olduğunu sırayla yaz.",
            "checks": ["Tarih belirlendi", "İlgili grup belirlendi", "Yer belirlendi"],
            "solution": "Örneğin: 11 Ağustos 2026 saat 10.00'da mantık sınıfına kayıtlı on iki öğrencinin tamamı B-204 salonundadır.",
        },
        [
            _production_task(
                "Sekiz farklı ifadeyi sınıflandır; bağlama bağlı iki ifadeyi açık bildirime dönüştür.",
                [
                    "En az bir soru, emir, yalın ünlem, yanlış bildirim ve bağlama bağlı bildirim kullan.",
                    "Her sınıflama için işlev veya doğruluk değeri üzerinden tek cümlelik gerekçe yaz.",
                    "Dönüştürülen ifadelerde kişi, yer ve zaman bilgisini gerektiği ölçüde açıkla.",
                ],
                "Yanlış ile önerme değil ayrımını ve bağlamı tamamlama işlemini açıkça göster.",
                "Sınıflandırılacak ifadeler",
                [
                    "Lütfen ışığı kapat.",
                    "Eyvah!",
                    "Toplantı başladı mı?",
                    "Mars'ın üç uydusu vardır.",
                    "Ben yarın burada olacağım.",
                    "Bu ağırdır.",
                    "Ankara Türkiye'nin başkentidir.",
                    "Eyvah, anahtarı içeride unuttum!",
                ],
                "Beşinci ve altıncı ifadeyi açık bir bağlam vererek yeniden yaz.",
            ),
        ],
        [
            "Soru, emir, yalın ünlem, yanlış bildirim ve bağlama bağlı bildirimleri gerekçeli ayırır.",
            "Bağlama bağlı bir ifadenin eksik parametrelerini doğru belirler.",
            "Bağlamı tamamlanan ifadeyi doğru veya yanlış değerlendirilebilir biçimde yeniden yazar.",
        ],
        [
            "Yanlış bir cümle neden yine de önerme ifade edebilir?",
            "'Ben buradayım' ifadesini değerlendirmek için hangi bilgiler gerekir?",
        ],
        "Sonraki derste bildirimlerin birbirine gerekçe sunduğu argüman yapısını kuracağız.",
        ["forallx-arguments"],
        "Önerme burada tartışmasız bir metafizik varlık gibi değil, öğretim için sınırlı bir çalışma tanımıyla kullanılır.",
        ["ders-1-onerme-nedir"],
    ),
    _lesson(
        "A2",
        "ders-2-arguman-oncul-ve-sonuc",
        "Argüman, Gerekçe ve Sonuç",
        "Bir metnin argüman olup olmadığını işaret sözcüklerinden değil, cümlelerin birbirine sunduğu destek işlevinden belirler.",
        "Argüman çözümleme",
        30,
        ["ders-1-onerme-nedir"],
        ["argument.identify", "argument.map", "reason.role"],
        [
            "Argümanı açıklama, betimleme ve salt iddia dizisinden ayırmak.",
            "Öncül, ara sonuç ve ana sonucu destek yönüne göre bulmak.",
            "İşaretleyici sözcükleri ipucu olarak kullanıp son kararı cümlenin işlevine göre vermek.",
        ],
        [
            ("Argüman", "Bir veya daha çok öncülün bir sonucu desteklemek üzere sunulduğu yapı."),
            ("Öncül", "Sonuç lehine gerekçe olarak sunulan önerme."),
            ("Sonuç", "Öncüllerin desteklemesi amaçlanan önerme."),
            ("Ara sonuç", "Önceki gerekçelerin sonucu olup daha sonraki sonuç için öncül görevi gören önerme."),
            ("Argüman göstergesi", "Çünkü, öyleyse ve dolayısıyla gibi yapısal rol için ipucu veren ifade."),
        ],
        [
            _section(
                "Argümanı başka metin işlevlerinden ayırmak",
                "Argüman bir sonucun kabulü için gerekçe verir; açıklama ise çoğu kez kabul edilmiş bir olgunun nedenini anlamaya çalışır. Ayrım cümle biçiminden çok bağlamda yanıtlanan soruya dayanır ve bazı metinler iki işlevi birlikte taşıyabilir.",
                "Bir paragrafı şemaya dökmeden önce gerçekten destek ilişkisi içerip içermediğini sınarken.",
                "Sor: Yazar hangi iddiayı kabul ettirmek için hangi gerekçeyi sunuyor?",
                "Cümle dizisi ancak aralarında destek iddiası varsa argüman oluşturur.",
                "Aynı çünkü sözcüğü hem gerekçe hem neden açıklaması kurabilir; hedef iddianın tartışmada olup olmadığına bak.",
                [
                    ("Yol buzlu; çünkü sıcaklık sıfırın altında ve gece yağış oldu.", "Yolun buzlu olup olmadığı tartışılıyorsa gerekçe, buzlanma zaten kabul ediliyorsa açıklama işlevi görebilir."),
                    ("Cam kırıldı çünkü top cama çarptı.", "Camın kırıldığı zaten kabul ediliyorsa olayın nedenini açıklıyor olabilir."),
                ],
                (
                    "Metnin hedefini ve destek yönünü sormak.",
                    "Çünkü geçen her cümleyi otomatik argüman saymak.",
                    "Aynı dilsel işaret farklı bağlamlarda farklı işlev görebilir.",
                ),
            ),
            _section(
                "Öncül, ara sonuç ve ana sonuç",
                "Bir cümlenin rolü sırasına değil, hangi cümleyi desteklediğine ve hangilerinden destek aldığına bağlıdır.",
                "Birden çok adımlı akıl yürütmede destek zincirini görünür kılarken.",
                "Gerekçeler ara sonucu; ara sonuç yeni gerekçeyle ana sonucu destekleyebilir.",
                "Ara sonuç iki rol taşır: önceki adımın sonucu, sonraki adımın öncülüdür.",
                "Paragrafın son cümlesi her zaman ana sonuç değildir; yazar sonucu başta da verebilir.",
                [
                    ("Otobüs gecikti. Bu yüzden aktarmayı kaçıracağız; o hâlde toplantıya zamanında varamayız.", "Aktarmayı kaçırma ara sonuç, toplantıya geç kalma ana sonuçtur."),
                    ("Toplantıya geç kalacağız; çünkü aktarmayı kaçıracağız, zira otobüs gecikti.", "Sonuç başta verilse de destek yönü değişmez."),
                ],
                (
                    "Cümleleri numaralayıp desteğin yönünü açıklamak.",
                    "Metindeki sırayı mantıksal rol sanmak.",
                    "Mantıksal yapı, sunuluş sırasından bağımsız olarak yeniden kurulabilir.",
                ),
            ),
            _section(
                "Örtük öncülleri ölçülü biçimde açmak",
                "Bazı argümanlar, yazarın ve okurun paylaştığını varsaydığı bir bağlantıyı söylemeden bırakır.",
                "Açık cümleler sonucu desteklemeye yetmediğinde eksik bağlantıyı en tutumlu biçimde ararken.",
                "Eklenen öncül metni güçlendirmeli; yazara gereksiz ve aşırı bir iddia yüklememeli.",
                "Örtük öncül bulmak, yazarın aklından geçen her şeyi tahmin etmek değildir.",
                "Argümanı geçerli yapmak için metnin amacıyla bağdaşmayan güçlü öncüller icat etme.",
                [
                    ("Bu sınav açık kitap; dolayısıyla notlarını getirmelisin.", "Örtük bağlantı, öğrencinin sınavda yararlı araçlardan faydalanması gerektiği ve notların böyle bir araç olduğu yönündedir."),
                    ("Ali Ankaralı; öyleyse matematikte iyidir.", "Şehir ile matematik başarısı arasında makul bir örtük bağlantı verilmemiştir."),
                ],
                (
                    "Metnin gerektirdiği en zayıf makul bağlantıyı önermek.",
                    "Sonucu garanti etmek için aşırı güçlü bir öncül icat etmek.",
                    "İyi yeniden kurma hem yardımsever hem metinsel kanıta sadık olmalıdır.",
                ),
            ),
        ],
        [
            _worked("Yollar ıslak; çünkü gece yağmur yağdı. Bu nedenle dikkatli sürmeliyiz.", "İlk cümle ara sonuç olabilir; dikkatli sürme ana sonuçtur.", "Gerekçe zinciri"),
            _worked("Elektrikler neden kesildi? Fırtına hattı devirdi.", "Bir kabul edilmiş olgunun nedenini bildirir; bağlama göre açıklamadır.", "Açıklama"),
            _worked("Öyleyse ile başlayan her cümle sonuçtur.", "Gösterge güçlü bir ipucudur ama alıntı, ironi veya kötü kullanım mümkündür.", "Aşırı kural", "bad"),
            _worked("Toplantıyı ertelemeliyiz: iki konuşmacı gelemiyor ve salon kapalı.", "Sonuç ilk cümlede, gerekçeler sonradadır.", "Sonuç başta"),
        ],
        [
            "Paragraftaki her cümleyi öncül saymak.",
            "Çünkü içeren her metni argüman saymak.",
            "Son cümleyi otomatik olarak ana sonuç kabul etmek.",
            "Örtük öncül adı altında yazara ilgisiz ve aşırı güçlü iddialar yüklemek.",
        ],
        _practice([
            ("Argümanı argüman yapan temel özellik nedir?", ["En az üç cümle içermesi", "Bir iddianın başka bir iddiaya destek olarak sunulması", "Çünkü sözcüğünü içermesi", "Sonucun doğru olması"], "Bir iddianın başka bir iddiaya destek olarak sunulması", "Argüman, cümle sayısıyla değil destek ilişkisiyle tanımlanır.", "Temel"),
            ("Ara sonuç hangi iki rolü üstlenir?", ["Soru ve emir", "Önceki adımın sonucu ve sonraki adımın öncülü", "Tanım ve örnek", "Yalnız ana sonuç"], "Önceki adımın sonucu ve sonraki adımın öncülü", "Ara sonuç destek zincirinin iki yönüne bağlanır.", "Temel"),
            ("'Cam, top çarptığı için kırıldı' ne zaman açıklamadır?", ["Camın kırıldığı zaten kabul edilip nedeni soruluyorsa", "Her zaman", "Hiçbir zaman", "Sonuç yanlışsa"], "Camın kırıldığı zaten kabul edilip nedeni soruluyorsa", "Açıklama, kabul edilen olgunun nedenini vermeyi hedefler.", "Orta"),
            ("Sonuç göstergesi bulunmayan bir metinde ne yapılmalıdır?", ["Argüman olmadığına karar verilmeli", "En uzun cümle sonuç seçilmeli", "Cümlelerin destek işlevi incelenmeli", "Son cümle silinmeli"], "Cümlelerin destek işlevi incelenmeli", "Göstergeler zorunlu değil, yardımcı ipuçlarıdır.", "Orta"),
            ("Hangisi örtük öncül eklerken iyi ilkedir?", ["Mümkün olan en güçlü iddiayı eklemek", "Metinle uyumlu ve gerekenden güçlü olmayan bağlantıyı önermek", "Yazarın psikolojisini tahmin etmek", "Sonucu öncül olarak tekrar etmek"], "Metinle uyumlu ve gerekenden güçlü olmayan bağlantıyı önermek", "Tutumlu yeniden kurma metne gereksiz yük bindirmez.", "İleri"),
            ("'Toplantıya geç kalacağız; çünkü aktarmayı kaçıracağız, zira otobüs gecikti.' ana sonucu hangisidir?", ["Otobüs gecikti", "Aktarmayı kaçıracağız", "Toplantıya geç kalacağız", "Hiçbiri"], "Toplantıya geç kalacağız", "Sunuluş sırası değişse de destek zinciri bu sonuca yönelir.", "İleri"),
            ("Bir örnek hangi durumda ana sonuç sayılmaz?", ["Metinde son sıradaysa", "Yalnız bir genel iddiayı somutlaştırıyor ama destek hedefi değilse", "Kısa ise", "Doğru ise"], "Yalnız bir genel iddiayı somutlaştırıyor ama destek hedefi değilse", "Örnek ile sonuç farklı işlevlerdir.", "Zor"),
            ("İşaretleyici sözcükler hakkında en doğru karar hangisidir?", ["Mantıksal rolü kesin belirler", "Tamamen değersizdir", "İpucu verir; son karar işlev ve bağlamla verilir", "Yalnız akademik metinde kullanılır"], "İpucu verir; son karar işlev ve bağlamla verilir", "Yüzey göstergesi ile mantıksal işlev ayrılmalıdır.", "Zor"),
        ]),
        {
            "prompt": "Otobüs gecikti. Aktarmayı kaçıracağız. Bu nedenle toplantıya zamanında varamayız.",
            "starter": "Cümleleri 1, 2 ve 3 diye numarala; önce 1'in hangi cümleyi desteklediğini bul.",
            "checks": ["Ara sonuç belirlendi", "Ana sonuç belirlendi", "Destek yönü açıklandı"],
            "solution": "1, 2'yi; 2 de 3'ü destekler. 2 ara sonuç, 3 ana sonuçtur.",
        },
        [
            _production_task(
                "Verilen paragrafı numaralı yalın önermelere ayır ve argüman haritasını yazıyla kur.",
                [
                    "Metnin argüman mı, açıklama mı, betimleme mi olduğunu gerekçelendir.",
                    "Varsa öncül, ara sonuç ve ana sonucu ayrı adlandır.",
                    "Örtük öncül öneriyorsan metinle bağını ve neden daha güçlü bir iddia seçmediğini açıkla.",
                ],
                "Destek yönünü sunuluş sırasından bağımsız kur ve ara sonucun çift rolünü görünür yap.",
                "Çözümlenecek paragraf",
                [
                    "Kütüphane sınav haftasında gece 23.00'e kadar açık kalmalıdır. Çalışma salonları akşamları doluyor; geçen sınav döneminde 120 öğrenci yer bulamadı. Üstelik kampüs servisleri 23.15'e kadar çalıştığı için öğrencilerin güvenli dönüş olanağı vardır.",
                ],
                "Paragrafta açıkça yazılmamış normatif bağlantıyı yalnız gerektiği ölçüde belirt.",
            ),
        ],
        [
            "İşaretleyici bulunmayan bir metni işlev üzerinden doğru sınıflandırır.",
            "Ara sonucu hem desteklenen hem destek veren önerme olarak gösterir.",
            "Örtük öncülü metne sadık ve tutumlu biçimde gerekçelendirir.",
        ],
        [
            "Bir cümle aynı argümanda nasıl hem sonuç hem öncül olabilir?",
            "Açıklama ile argümanı ayırmak için hangi soru sorulur?",
        ],
        "Sonraki derste bir argümanın sonucunun doğruluğu ile çıkarımının geçerliliğini ayıracağız.",
        ["forallx-arguments"],
        "Yazarın psikolojik niyeti erişilebilir olmayabilir; çözümleme metinde savunulabilen destek yapısına dayanır.",
        ["ders-2-arguman-oncul-ve-sonuc", "ders-7-metin-icinde-arguman-ayiklama"],
    ),
    _lesson(
        "A3",
        "ders-3-gecerlilik-ve-dogruluk",
        "Doğruluk, Geçerlilik ve Sağlamlık",
        "Bir önermenin fiilen doğru olmasını, bir sonucun öncüllerden zorunlu olarak çıkmasından ayırır; geçerli ve sağlam argümanları doğru terimlerle değerlendirir.",
        "Tümdengelimsel değerlendirme",
        30,
        ["ders-2-arguman-oncul-ve-sonuc"],
        ["validity.evaluate", "soundness.evaluate", "consequence.explain"],
        [
            "Doğruluğun önerme içeriğine, geçerliliğin argümana yüklenen farklı özellikler olduğunu açıklamak.",
            "Geçerli, sağlam ve sağlam olmayan tümdengelimsel argümanları ayırmak.",
            "Mantıksal sonucu, öncüller doğruyken sonucun yanlış olamaması üzerinden ifade etmek.",
        ],
        [
            ("Doğruluk", "Bir önermenin öne sürdüğü şeyin gerçekten öyle olması; bu derste cümle içeriğine yüklenen özellik."),
            ("Geçerlilik", "Öncüllerin doğru, sonucun yanlış olmasının mümkün olmadığı tümdengelimsel yapı."),
            ("Sağlamlık", "Geçerli olup bütün öncülleri de doğru olan argümanın özelliği."),
            ("Mantıksal sonuç", "Sonucun, öncüllerin doğru olduğu her durumda doğru olmak zorunda olması."),
            ("Tümdengelim", "Öncüller doğruysa sonucun zorunlu olarak doğru olduğu iddiasını taşıyan akıl yürütme."),
        ],
        [
            _section(
                "Doğruluk ile geçerlilik farklı türden özelliklerdir",
                "Doğru veya yanlış olan önermelerdir; geçerli veya geçersiz olan ise öncüller ile sonuç arasındaki tümdengelimsel ilişkidir.",
                "Doğru bir sonucun kötü bir çıkarımla elde edilip edilmediğini sınarken.",
                "Sonuca değil şu olasılığa bak: Bütün öncüller doğruyken sonuç yanlış kalabilir mi?",
                "Geçerlilik, yalnız gerçek dünyadaki fiilî başarıya değil, öncüllerin doğru olduğu kabul edilebilir durumların tamamında sonucun da doğru kalmasına bakar.",
                "Sonuç zaten doğru diye argümana geçerli deme; destek ilişkisini ayrıca sınamak gerekir.",
                [
                    ("Ay Dünya'nın uydusudur; Ankara Türkiye'nin başkentidir; öyleyse Amazon Nehri Güney Amerika'dadır.", "Cümlelerin tümü fiilen doğru olsa da öncüller sonucu zorunlu kılmaz."),
                    ("Bütün balinalar böcektir; bütün böcekler sürüngendir; öyleyse bütün balinalar sürüngendir.", "İçerik yanlış olsa da tümdengelimsel biçim geçerlidir."),
                ],
                (
                    "Doğruluk kararını cümlelere, geçerlilik kararını argümanın ilişkisine vermek.",
                    "Doğru sonuç gördüğünde argümanı geçerli saymak.",
                    "Doğru sonuca ilgisiz veya yetersiz gerekçelerle de ulaşılabilir.",
                ),
            ),
            _section(
                "Sağlamlık iki koşulu birlikte ister",
                "Sağlam bir argüman hem geçerlidir hem de bütün öncülleri doğrudur.",
                "Bir tümdengelimsel argümanın yalnız biçimini değil gerçek öncül temelini de değerlendirirken.",
                "Önce geçerliliği sınama, sonra her öncülün doğruluğunu inceleme.",
                "Geçersiz bir argüman, bütün cümleleri doğru olsa bile sağlam olamaz.",
                "Sonucun doğruluğunu üçüncü bağımsız koşul gibi ekleme; geçerlilik ve doğru öncüller zaten sonucu güvenceye alır.",
                [
                    ("Bütün memeliler sıcakkanlıdır; yunus memelidir; öyleyse yunus sıcakkanlıdır.", "Geçerli biçim ve doğru öncüller birlikte sağlamlık verir."),
                    ("Bütün balinalar böcektir; bütün böcekler sürüngendir; öyleyse bütün balinalar sürüngendir.", "Geçerli ama yanlış öncüllü olduğu için sağlam değildir."),
                ],
                (
                    "Sağlamlık kararını geçerlilik ve öncül doğruluğu olarak iki adımda gerekçelendirmek.",
                    "Bütün cümleleri doğru olan her argümanı sağlam saymak.",
                    "Doğru cümleler arasında mantıksal destek bulunmayabilir; önce geçerlilik gerekir.",
                ),
            ),
            _section(
                "Geçerlilik tümdengelimsel bir standarttır",
                "Bazı argümanlar sonuçlarını zorunlu değil olası kılmayı amaçlar; bunlar güçlü veya zayıf diye ayrıca değerlendirilir.",
                "İstatistik, örneklem veya en iyi açıklamaya dayalı akıl yürütmeyi tümdengelim sanmamak için.",
                "Önce argümanın iddiasını belirle: zorunlu sonuç mu, olasılıksal destek mi?",
                "İyi bir tümevarımsal argümanın öncülleri doğru, sonucu yanlış olabilir; bu tek başına onun amaçladığı desteği bozmaz.",
                "Bu derste tümevarım ayrıntılı puanlanmaz; yalnız geçerlilik standardının kapsamı sınırlandırılır.",
                [
                    ("İncelenen bin örneğin çoğu özelliğe sahip; yeni örneğin de sahip olması beklenir.", "Sonuç olasıdır, zorunlu değildir."),
                    ("Bütün örnekler özelliğe sahip; bu nesne de örneklerden biridir; öyleyse o da özelliğe sahiptir.", "Bu yapı zorunlu sonuç iddiası taşır."),
                ],
                (
                    "Argümanın hedeflediği destek türünü belirlemek.",
                    "Zorunlu olmayan her çıkarımı mantıksal hata saymak.",
                    "Tümevarımsal başarı, tümdengelimsel geçerlilikten farklı ölçütlerle değerlendirilir.",
                ),
            ),
        ],
        [
            _worked("Bütün memeliler sıcakkanlıdır; kedi memelidir; öyleyse kedi sıcakkanlıdır.", "Biçim geçerli, öncüller doğru; argüman sağlamdır.", "Sağlam"),
            _worked("Bütün balinalar böcektir; bütün böcekler sürüngendir; öyleyse bütün balinalar sürüngendir.", "Biçim geçerli fakat öncüller yanlış; argüman sağlam değildir.", "Geçerli"),
            _worked("Ankara Türkiye'dedir; öyleyse iki artı iki dörttür.", "Öncül ve sonuç doğru olsa da öncül sonucu zorunlu kılmaz.", "Geçersiz", "bad"),
            _worked("Gözlenen kuğuların çoğu beyazdı; sıradaki kuğunun beyaz olması beklenir.", "Zorunlu sonuç değil, olasılıksal destek amaçlanır.", "Tümevarım"),
        ],
        [
            "Doğru sonucu görünce geçerlilik kararı vermek.",
            "Yanlış bir öncül görünce argümanı doğrudan geçersiz saymak.",
            "Bütün cümlelerin doğru olmasını sağlamlık için yeterli sanmak.",
            "Olasılıksal desteği tümdengelimsel geçerlilikle puanlamak.",
        ],
        _practice([
            ("Doğru veya yanlış olma özelliği öncelikle neye yüklenir?", ["Argümana", "Önerme içeriğine", "Paragraf uzunluğuna", "Konuşmacıya"], "Önerme içeriğine", "Doğruluk, cümlenin ifade ettiği içerikle ilgilidir.", "Temel"),
            ("Geçerlilik hangi soruyla sınanır?", ["Sonuç fiilen doğru mu?", "Öncüller ikna edici mi?", "Öncüller doğruyken sonuç yanlış olabilir mi?", "Metin kısa mı?"], "Öncüller doğruyken sonuç yanlış olabilir mi?", "Böyle bir durum mümkünse tümdengelimsel argüman geçersizdir.", "Temel"),
            ("Geçerli fakat sağlam olmayan argüman mümkün müdür?", ["Hayır", "Evet, öncüllerden en az biri yanlışsa", "Yalnız sonuç doğruysa", "Yalnız iki öncülü varsa"], "Evet, öncüllerden en az biri yanlışsa", "Geçerlilik korunurken öncül doğruluğu başarısız olabilir.", "Orta"),
            ("Bütün cümleleri doğru olan bir argüman neden yine de sağlam olmayabilir?", ["Çünkü çok kısa olabilir", "Çünkü öncüller sonucu zorunlu kılmayabilir", "Çünkü sonuç doğru olamaz", "Çünkü sağlamlık yalnız yanlış cümle ister"], "Çünkü öncüller sonucu zorunlu kılmayabilir", "Sağlamlık için doğru öncüllere ek olarak geçerlilik gerekir.", "Orta"),
            ("Yanlış öncüllü bir argüman hakkında hangi karar doğrudur?", ["Kesinlikle geçersizdir", "Geçerli olabilir ama sağlam olamaz", "Kesinlikle sağlamdır", "Sonucu mutlaka yanlıştır"], "Geçerli olabilir ama sağlam olamaz", "Geçerlilik biçimsel ilişkiyi, sağlamlık ayrıca öncül doğruluğunu içerir.", "İleri"),
            ("Mantıksal sonuç neyi ifade eder?", ["Sonucun popüler olmasını", "Öncüllerin doğru olduğu her durumda sonucun da doğru olmasını", "Sonucun metinde sonda olmasını", "Öncüllerin uzun olmasını"], "Öncüllerin doğru olduğu her durumda sonucun da doğru olmasını", "Mantıksal sonuç zorunlu koruma ilişkisidir.", "İleri"),
            ("Bir örneklemden yeni örneğe ilişkin beklenti hangi desteği amaçlar?", ["Her zaman tümdengelimsel geçerlilik", "Olasılıksal destek", "Hiçbir destek", "Tanım"], "Olasılıksal destek", "Örnekleme dayalı genelleme çoğu kez zorunluluk değil olasılık sağlar.", "Zor"),
            ("Argümanın sonucu zaten doğruysa ne söylenebilir?", ["Argüman zorunlu olarak geçerlidir", "Argüman zorunlu olarak sağlamdır", "Geçerlilik için yine öncül-sonuç ilişkisi sınanmalıdır", "Öncüller önemsizdir"], "Geçerlilik için yine öncül-sonuç ilişkisi sınanmalıdır", "Sonucun fiilî doğruluğu çıkarım ilişkisini tek başına belirlemez.", "Zor"),
        ]),
        {
            "prompt": "Bütün balinalar böcektir. Bütün böcekler sürüngendir. Öyleyse bütün balinalar sürüngendir.",
            "starter": "Önce yalnız yapıya bak; sonra öncüllerin dünyadaki doğruluğunu ayrı değerlendir.",
            "checks": ["Geçerlilik kararı verildi", "Öncül doğruluğu incelendi", "Sağlamlık kararı gerekçelendirildi"],
            "solution": "Yapı geçerlidir: iki sınıf içerme öncülü sonucu zorunlu kılar. Ancak öncüller yanlış olduğundan argüman sağlam değildir.",
        },
        [
            _production_task(
                "Dört akıl yürütmede önce amaçlanan destek türünü belirle; tümdengelimsel olanları geçerlilik ve sağlamlık bakımından iki ayrı aşamada değerlendir.",
                [
                    "Her örnekte önce zorunlu sonuç mu, olasılıksal destek mi hedeflendiğini yaz.",
                    "Tümdengelimsel örneklerde öncüller doğru kabul edildiğinde sonucun yanlış kalıp kalamayacağını sınayarak geçerlilik kararı ver.",
                    "Geçerli örneklerde her öncülün fiilî doğruluğunu ayrıca değerlendirerek sağlamlık kararı ver.",
                    "En az bir geçerli fakat sağlam olmayan ve bir doğru sonuçlu fakat geçersiz örneği gerekçelendir.",
                ],
                "Destek türünü başta ayır; geçerlilik kararını sonuç doğruluğundan bağımsız, sağlamlık kararını ise yalnız geçerlilikten sonra ver.",
                "Değerlendirilecek argümanlar",
                [
                    "Bütün memeliler sıcakkanlıdır. Bütün balinalar memelidir. Öyleyse bütün balinalar sıcakkanlıdır.",
                    "Bütün gezegenler yıldızdır. Dünya bir gezegendir. Öyleyse Dünya bir yıldızdır.",
                    "Ay Dünya'nın uydusudur. Ankara Türkiye'nin başkentidir. Öyleyse Amazon Nehri Güney Amerika'dadır.",
                    "Son beş sabah otobüs gecikti. Öyleyse yarın sabahki otobüsün de gecikmesi beklenir.",
                ],
                "Dördüncü örnek olasılıksal destek amaçlar; ona tümdengelimsel sağlamlık etiketi vermek yerine bu ayrımı açıkla.",
            ),
        ],
        [
            "Geçerli fakat sağlam olmayan bir argümanı doğru gerekçeyle tanır.",
            "Doğru sonuçlu fakat geçersiz bir argümanın kusurunu ilişki üzerinden açıklar.",
            "Tümdengelimsel zorunluluk ile olasılıksal desteği aynı ölçütle değerlendirmez.",
        ],
        [
            "Yanlış öncüllü bir argüman nasıl geçerli olabilir?",
            "Sonucun doğru olması neden tek başına geçerlilik kanıtı değildir?",
        ],
        "Sonraki derste geçersizliği göstermek için hedefe uygun karşı örnek ve karşı durum üreteceğiz.",
        ["forallx-validity"],
        "Argümanın sağlamlığı için 'sağlamlık', ileride kanıt sisteminin soundness özelliği için 'güvenirlik' terimi kullanılacaktır.",
        ["ders-3-gecerlilik-ve-dogruluk"],
    ),
    _lesson(
        "A4",
        "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
        "Biçim, Karşı Örnek ve Karşı Durum",
        "Bir iddiayı veya argümanı eleştirirken hedefe uygun tanık üretir; evrensel iddiaya karşı örnek ile geçersiz argümana karşı durumu ayırır.",
        "Çürütme ve biçim",
        30,
        ["ders-3-gecerlilik-ve-dogruluk"],
        ["form.abstract", "counterexample.construct", "countercase.construct"],
        [
            "Birden fazla argümanın paylaştığı biçimi içerikten ayırmak.",
            "Evrensel iddiaya karşı örnek ile tümdengelimsel argümana karşı durum arasındaki farkı kullanmak.",
            "Geçersizliği, bütün öncüllerin doğru ve sonucun yanlış olduğu tek bir tutarlı durumla göstermek.",
        ],
        [
            ("Biçim", "Belirli içerikler değişse de akıl yürütmeler arasında korunabilen yapısal düzen."),
            ("Şema", "İçerik yerlerine değişken öğeler koyarak ortak biçimi gösteren kalıp."),
            ("Karşı örnek", "Evrensel bir iddianın kapsamına girip iddianın yüklediği özelliği taşımayan örnek."),
            ("Karşı durum", "Bir argümanın bütün öncüllerini doğru, sonucunu yanlış yapan tutarlı olasılık."),
            ("Çürütme hedefi", "İtirazın evrensel iddiaya mı, çıkarım ilişkisine mi, yoksa bir öncüle mi yöneldiği."),
        ],
        [
            _section(
                "İçerikten ortak biçime geçmek",
                "Farklı konular hakkındaki argümanlar aynı destek düzenini paylaşabilir.",
                "Bir akıl yürütmenin başarısının konu bilgisinden mi yapısından mı geldiğini ayırırken.",
                "İçerik sözcüklerini yer tutucularla değiştir; tekrar eden yapıyı koru.",
                "Bir şema biçimsel olarak geçerliyse onun uygun bütün örneklemeleri geçerlidir; fakat tek bir başarılı örnek, şemanın kendisinin geçerli olduğunu göstermez.",
                "Doğal dilde sözcük anlamları bir örneği ayrıca geçerli kılabilir; yalnız yüzey benzerliğini tam mantıksal biçim sanma.",
                [
                    ("Bütün kediler memelidir; Mırmır kedidir; Mırmır memelidir.", "Bütün [A]lar [B]dir; x [A]dır; x [B]dir biçimini taşır."),
                    ("Bütün güller bitkidir; bu nesne güldür; bu nesne bitkidir.", "Konu değişse de aynı biçim korunur."),
                    ("Deniz göz doktorudur; öyleyse Deniz doktordur.", "İçerik bakımından sonuç çıkar; ancak '[x] A'dır, öyleyse [x] B'dir' yüzey şeması tek başına geçerli değildir."),
                ],
                (
                    "Yer tutucuları tutarlı kullanıp şemayı yeni içeriklerle sınamak.",
                    "Tek bir başarılı örnekten şemanın biçimsel olarak geçerli olduğu sonucunu çıkarmak.",
                    "Sözcük anlamı tek örneği kurtarabilir; biçimsel geçerlilik uygun bütün örneklemelerde korunmalıdır.",
                ),
            ),
            _section(
                "Evrensel iddiayı karşı örnekle sınamak",
                "Bütün veya hiçbir gibi evrensel iddiaları çürütmek için kapsam içindeki tek bir gerçek istisna yeterlidir.",
                "Bir sınıfın bütün üyeleri hakkında kurulan iddiayı sınarken.",
                "Örnek hedef sınıfa girmeli ve iddianın yüklediği özelliği taşımamalı.",
                "Karşı örnek iddiayla ilgili olmalı; yalnız şaşırtıcı veya olumsuz bir örnek olması yetmez.",
                "Çoğu, genellikle veya büyük olasılıkla diyen iddialar tek istisnayla otomatik çürümez.",
                [
                    ("Bütün kuşlar uçar.", "Penguen hedef sınıfa girer ve uçmaz; uygun karşı örnektir."),
                    ("Çoğu şehir kalabalıktır.", "Tek sakin şehir bu olasılıksal genellemeyi tek başına çürütmez."),
                ],
                (
                    "İddianın niceleme gücüne uygun örnek üretmek.",
                    "Hedef sınıfa girmeyen bir nesneyi karşı örnek göstermek.",
                    "Kapsam dışında kalan nesne, evrensel iddianın söylediği şeyi sınamaz.",
                ),
            ),
            _section(
                "Geçersizliği karşı durumla göstermek",
                "Bir tümdengelimsel argümanı çürütmek için öncüllerin hepsinin doğru, sonucun yanlış olduğu tek bir tutarlı durum yeterlidir.",
                "Argümanın geçersizliğini öncüllerden birini reddetmeden göstermek istediğinde.",
                "Bütün öncüller doğru; sonuç yanlış; betimlenen durum birlikte mümkün.",
                "Karşı durum gerçek dünyada gerçekleşmek zorunda değildir; tutarlı ve ilgili olması yeterlidir.",
                "Bir öncülün fiilen yanlış olduğunu göstermek argümanın sağlamlığını etkiler, fakat tek başına geçersizliğini göstermez.",
                [
                    ("Alarm kuruluysa kırmızı ışık yanar; kırmızı ışık yanıyor; öyleyse alarm kuruludur.", "Test modu ışığı yakarken alarm kapalı olabilir; öncüller doğru, sonuç yanlış kalır."),
                    ("Yağmur yağarsa yol ıslanır; yağmur yağıyor; öyleyse yol ıslaktır.", "Öncülleri doğru ve sonucu yanlış tutan tutarlı bir durum, olağan anlamlar altında kurulamaz."),
                ],
                (
                    "Öncülleri koruyup sonucu yanlış yapan ortak bir durum üretmek.",
                    "Bir öncülü yanlışlayıp buna geçersizlik demek.",
                    "Geçerlilik, öncüller doğru kabul edildiğinde sonucun korunup korunmadığıyla ilgilidir.",
                ),
            ),
        ],
        [
            _worked("Bütün kuşlar uçar; penguen kuştur ama uçmaz.", "Penguen evrensel iddianın kapsamına giren gerçek bir istisnadır.", "Karşı örnek"),
            _worked("Bütün kuşlar uçar; yarasa uçar.", "Yarasa kuş değildir; bu yüzden hedef evrensel iddiaya karşı örnek olmaz.", "İlgisiz örnek", "bad"),
            _worked("Alarm örneğinde test modu", "Öncülleri doğru tutarken sonucu yanlış yaptığı için karşı durumdur.", "Karşı durum"),
            _worked("Argümanın ilk öncülü gerçekte yanlış.", "Bu sağlamlık eleştirisidir; tek başına geçersizlik kanıtı değildir.", "Hedef karışıklığı", "bad"),
        ],
        [
            "Her itirazı karşı örnek diye adlandırmak.",
            "Hedef sınıfa girmeyen ilgisiz bir istisna üretmek.",
            "Bir öncülü yanlışlamayı argümanın geçersizliğini göstermek sanmak.",
            "Olasılıksal bir genellemeyi tek istisnayla otomatik çürütmek.",
        ],
        _practice([
            ("'Bütün kuşlar uçar' iddiasına uygun karşı örnek hangisidir?", ["Uçan yarasa", "Uçamayan penguen", "Yüzen balık", "Koşan insan"], "Uçamayan penguen", "Penguen kuştur ve yüklenen uçma özelliğini taşımaz.", "Temel"),
            ("Karşı durum hangi doğruluk düzenini ister?", ["Bir öncül yanlış, sonuç doğru", "Bütün öncüller doğru, sonuç yanlış", "Bütün cümleler yanlış", "Yalnız sonuç doğru"], "Bütün öncüller doğru, sonuç yanlış", "Bu düzen, öncüllerin sonucu zorunlu kılmadığını gösterir.", "Temel"),
            ("Bir öncülün fiilen yanlış olduğunu göstermek öncelikle neyi etkiler?", ["Argümanın sağlamlığını", "Her zaman geçerliliğini", "Cümle sayısını", "Biçimin varlığını"], "Argümanın sağlamlığını", "Geçerlilik öncülleri doğru varsayarak ilişkiyi sınar.", "Orta"),
            ("'Çoğu öğrenci erken geldi' iddiası tek geç kalan öğrenciyle neden otomatik çürümez?", ["Öğrenci sayılmadığı için", "Çoğu ifadesi evrensel olmadığı için", "Geç kalmak imkânsız olduğu için", "İddia her zaman doğru olduğu için"], "Çoğu ifadesi evrensel olmadığı için", "Olasılıksal/niceliksel çoğunluk iddiası istisnaya izin verir.", "Orta"),
            ("İki argümanın aynı biçimi taşıması için ne korunmalıdır?", ["Aynı konu hakkında olmaları", "Terimlerin yapısal tekrar ve rol düzeni", "Aynı uzunlukta olmaları", "Aynı sonucu yazmaları"], "Terimlerin yapısal tekrar ve rol düzeni", "Biçim, içerik değişirken yapısal bağlantıları korur.", "İleri"),
            ("Tek bir argüman örneğinin geçerli olması, çıkarılan yüzey şemasının da biçimsel olarak geçerli olduğunu kanıtlar mı?", ["Evet, tek örnek yeterlidir", "Hayır, örnek sözcük anlamları nedeniyle başarılı olabilir; şema yeni içeriklerle sınanmalıdır", "Yalnız sonuç uzunsa", "Yalnız öncül doğruysa"], "Hayır, örnek sözcük anlamları nedeniyle başarılı olabilir; şema yeni içeriklerle sınanmalıdır", "Biçimsel geçerlilik tek örneğin değil, uygun bütün örneklemelerin korunmasını ister.", "İleri"),
            ("Alarm örneğinde test modu neyi gösterir?", ["İlk öncülün anlamsızlığını", "Öncüller doğruyken sonucun yanlış kalabildiğini", "Sonucun her zaman doğru olduğunu", "Argümanın sağlam olduğunu"], "Öncüller doğruyken sonucun yanlış kalabildiğini", "Bu, geçersizliğin karşı durumudur.", "İleri"),
            ("Karşı durumun gerçek dünyada gerçekleşmiş olması gerekir mi?", ["Evet, mutlaka tarihsel kayıt gerekir", "Hayır, tutarlı ve ilgili bir olasılık olması yeterlidir", "Yalnız bilimsel argümanda", "Yalnız sonucu doğruysa"], "Hayır, tutarlı ve ilgili bir olasılık olması yeterlidir", "Geçerlilik mümkün durumlar üzerindeki koruma ilişkisini sınar.", "Zor"),
            ("Hangi eleştiri geçersizliği tek başına göstermez?", ["Bütün öncüller doğruyken sonucu yanlış yapan durum", "Aynı biçimde açık başarısız örnek", "Öncüllerden birinin gerçekte yanlış olması", "Sonucu zorunlu kılmayan tutarlı senaryo"], "Öncüllerden birinin gerçekte yanlış olması", "Yanlış öncül sağlamlığı bozar; geçerlilik için ilişki ayrıca sınanır.", "Zor"),
        ]),
        {
            "prompt": "Alarm kuruluysa kırmızı ışık yanar. Kırmızı ışık yanıyor. Öyleyse alarm kuruludur.",
            "starter": "İlk iki cümleyi doğru tutup alarmın kurulu olmadığı bir mekanizma düşün.",
            "checks": ["İki öncül de doğru tutuldu", "Sonuç yanlış tutuldu", "Senaryo birlikte tutarlı"],
            "solution": "Kırmızı ışık test modu nedeniyle yanıyor olabilir. Bu durumda koşul doğru, ışık yanıyor ve alarm kurulu değil; argüman geçersizdir.",
        },
        [
            _production_task(
                "Bir evrensel iddia için karşı örnek üret; verilen argümanın biçimini çıkarıp aynı biçime karşı durum kur ve neden farklı araçlar kullandığını açıkla.",
                [
                    "Karşı örneğin hedef sınıfa gerçekten girdiğini ve özelliği taşımadığını göster.",
                    "Argümanı yer tutucularla şemalaştırırken tekrar eden terimlerin rolünü koru.",
                    "Karşı durumda bütün öncülleri doğru, sonucu yanlış tut.",
                    "Eleştirinin iddiaya mı, çıkarım ilişkisine mi, yoksa öncül doğruluğuna mı yöneldiğini adlandır.",
                ],
                "Karşı örnek ile karşı durumu hedeflerine göre ayır; yalnız şaşırtıcı bir örnek vermekle yetinme.",
                "İki ayrı hedef",
                [
                    "Evrensel iddia: Bütün kuşlar uçar.",
                    "Argüman: Bir kişi avukatsa üniversite mezunudur. Deniz üniversite mezunudur. Öyleyse Deniz avukattır.",
                ],
                "İlk hedef bir iddia, ikinci hedef ise öncül-sonuç ilişkisidir; aynı eleştiri aracını kullanma.",
            ),
        ],
        [
            "Karşı örneği evrensel iddianın gerçek kapsamından seçer.",
            "Argümanın biçimini terim tekrarlarını ve destek rollerini koruyan yer tutucularla gösterir.",
            "Karşı durumda bütün öncülleri doğru ve sonucu yanlış tutar.",
            "Öncül doğruluğu eleştirisi ile geçerlilik eleştirisini ayrı gerekçelendirir.",
        ],
        [
            "Geçersizliği gösteren karşı durumda hangi cümleler doğru, hangisi yanlış olmalıdır?",
            "Olasılıksal bir genellemeyi tek istisna her zaman çürütür mü?",
        ],
        "Sonraki derste koşul ifadelerinin yönünü gerekli ve yeterli olma üzerinden kuracağız.",
        ["forallx-validity"],
        "Biçimsel yorum ve model semantiği henüz kurulmadığı için bu aşamada 'karşı durum' denir; 'karşı model' terimi yüklem mantığı semantiğine bırakılır.",
        ["ders-9-karsi-ornek-sema-ve-curutme-teknikleri", "ders-6-gecerli-kaliplar-ve-yon-hatalari"],
    ),
    _lesson(
        "A5",
        "ders-5-zorunlu-ve-yeterli-kosul",
        "Zorunlu ve Yeterli Koşullar",
        "Koşul ifadelerini standart çıkarımsal okumada sözcük sırasına göre değil, hangi durumun hangisini garanti ettiği veya gerektirdiğine göre yönlendirir.",
        "Koşul yönü",
        35,
        [
            "ders-3-gecerlilik-ve-dogruluk",
            "ders-9-karsi-ornek-sema-ve-curutme-teknikleri",
        ],
        ["condition.necessary", "condition.sufficient", "condition.direction"],
        [
            "Yeterli koşulu sonucu garanti eden, zorunlu koşulu sonuç için bulunması gereken taraf olarak okumak.",
            "Koşul kuran ise, yalnızca, ancak ve -medikçe yapılarında yönü gerekçelendirmek; aynı sözcüklerin koşul kurmayan kullanımlarını ayırmak.",
            "Tek yönlü koşulu çift yönlü tanım gibi kullanmamak ve tersini karşı durumla sınamak.",
        ],
        [
            ("Yeterli koşul", "Gerçekleşmesi, belirtilen sonucu garanti etmeye yeten koşul."),
            ("Zorunlu koşul", "Belirtilen sonucun gerçekleşmesi için bulunması gereken koşul."),
            ("Ters koşul", "Asıl koşulda garanti edilen tarafı başlangıç koşulu yaparak yönü değiştiren iddia."),
            ("Çift yönlü koşul", "İki tarafın da diğeri için hem zorunlu hem yeterli olduğu ilişki."),
            ("Garanti testi", "Bir koşul gerçekleştiğinde sonucun zorunlu olup olmadığını sınayan soru."),
            ("Standart çıkarımsal okuma", "Bir koşul cümlesini, başlangıç tarafının doğru olduğu her durumda sonuç tarafının da doğru olmasını gerektiren kural olarak ele alan okuma."),
        ],
        [
            _section(
                "Yeterli koşul garanti eder, zorunlu koşul gerekir",
                "Standart çıkarımsal okumada A'nın gerçekleşmesi B'yi garanti ediyorsa A, B için yeterlidir; B de A'nın gerçekleşmesi için zorunludur.",
                "Doğal dilde iki durum arasındaki tek yönlü koşulu çözümlemeye başlarken.",
                "Garanti eden taraftan, garanti edilen tarafa doğru oku.",
                "Aynı koşul ilişkisi bir taraftan yeterlilik, öteki taraftan zorunluluk olarak ifade edilir.",
                "Yeterli koşulu tek mümkün neden, zorunlu koşulu da tek başına sonucu üreten neden sanma.",
                [
                    ("Kare olmak dörtgen olmak için yeterlidir.", "Her kare dörtgendir; dörtgen olmak kare için zorunludur."),
                    ("Dört ile tam bölünebilmek için çift olmak zorunludur.", "Dörde bölünen sayı çifttir; fakat her çift sayı dörde bölünmez."),
                ],
                (
                    "Garanti ile gereklilik rollerini aynı ilişki üzerinde ayrı adlandırmak.",
                    "Zorunlu koşulu otomatik olarak yeterli saymak.",
                    "Bir koşulun bulunması gerekebilir ama tek başına sonucu garanti etmeyebilir.",
                ),
            ),
            _section(
                "Türkçe koşul yapılarında yönü bulmak",
                "Standart koşullu kullanımda 'A ise B' A'yı B için yeterli; 'A yalnızca B ise', 'A ancak B ise' ve 'B olmadıkça A olmaz' ise B'yi A için zorunlu olarak sunar.",
                "Sözcük sırası ile mantıksal yönün kolayca karıştığı doğal dil cümlelerinde.",
                "Önce yapının gerçekten koşul kurup kurmadığını sor; sonra 'Bir taraf gerçekleşip öteki gerçekleşmezse kural hangi durumda bozulur?' diye sına.",
                "Yalnızca ve koşul kuran ancak gerekli tarafı işaretler. '-medikçe' yapısı da standart okumada yokluğu sonucu dışlayan bir gereklilik bildirir; gerekli tarafın tek başına yeterli olduğunu söylemez.",
                "'Ancak' karşıtlık anlamında, 'ise' konu veya karşılaştırma işlevinde de kullanılabilir. İşaretleyiciye bakıp otomatik koşul şeması çıkarma.",
                [
                    ("Yalnızca bileti olanlar salona girebilir.", "Salona girmek, bilet sahibi olmayı gerektirir; bilet zorunlu koşuldur."),
                    ("Dosya ancak ödeme yapılırsa işleme alınır.", "İşleme alınmak ödemeyi gerektirir; ödeme yapılması tek başına işlemi garanti etmez."),
                    ("Şifreyi girmedikçe hesaba erişemezsin.", "Standart kural okumasında erişim, şifrenin girilmesini gerektirir; başka gereklilikler de bulunabilir."),
                    ("Rapor uzundu; ancak anlaşılırdı.", "Buradaki ancak karşıtlık bildirir; zorunlu veya yeterli koşul kurmaz."),
                ],
                (
                    "Önce koşul kullanımı olup olmadığını belirlemek, sonra garanti ve gereklilik sorularıyla yönü açıklamak.",
                    "Ancak veya ise görülen her cümleyi koşul saymak.",
                    "Aynı sözcükler Türkçede karşıtlık, konu değiştirme veya karşılaştırma işlevi de görebilir.",
                ),
            ),
            _section(
                "Ters koşul ve çift yönlü ilişki",
                "Tek yönlü bir koşul, ters yöndeki garantiyi kendiliğinden vermez; iki yön birlikte ancak ayrıca kurulursa çift yönlü ilişki oluşur.",
                "Bir koşuldan fazla sonuç çıkarılıp çıkarılmadığını sınarken.",
                "Asıl yön için ayrı, ters yön için ayrı karşı durum ara.",
                "Asıl koşulu koruyan bir örnek, ters koşulun da doğru olduğunu göstermez.",
                "Nedensel, zamansal veya tanımsal bağlantıları tek bir koşul türü sanma; biçimsel koşulun kesin semantiği sonraki aşamada kurulacaktır.",
                [
                    ("Kedi olmak memeli olmak için yeterlidir.", "Memeli olmak kedi olmak için yeterli değildir; köpek karşı durumdur."),
                    ("Bir tam sayı çiftse ikiye tam bölünür ve ikiye tam bölünüyorsa çifttir.", "Standart tanım altında iki yön birlikte kurulabilir."),
                ],
                (
                    "Ters yönü bağımsız bir iddia olarak sınamak.",
                    "Asıl koşul doğruysa tersinin de doğru olduğunu varsaymak.",
                    "Tek yönlü garanti, dönüş yolunu kendiliğinden lisanslamaz.",
                ),
            ),
        ],
        [
            _worked("Kare olmak dörtgen olmak için yeterlidir.", "Kare olan her şey dörtgendir; karelik garanti eden taraftır.", "Yeterli"),
            _worked("Dörtgen olmak kare olmak için yeterlidir.", "Dikdörtgen olup kare olmayan şekiller bu ters yönü bozar.", "Ters yön", "bad"),
            _worked("Yalnızca kimliği olanlar binaya girebilir.", "Binaya girmek kimlik sahibi olmayı gerektirir.", "Zorunlu"),
            _worked("Kimliği olan herkes binaya girer.", "Bu, önceki cümlenin söylemediği ters yönü ekler.", "Fazla okuma", "bad"),
            _worked("Şifreyi girmedikçe hesaba erişemezsin.", "Erişim için şifre gereklidir; şifre tek başına erişimi garanti etmez.", "Gerekli"),
            _worked("Toplantı uzundu; ancak verimli geçti.", "Ancak burada karşıtlık kurar, koşul yönü kurmaz.", "Koşul değil"),
        ],
        [
            "Sözcük sırasını doğrudan mantıksal yön sanmak.",
            "Ancak veya ise geçen her cümleyi koşul cümlesi saymak.",
            "Koşulun tersini otomatik olarak doğru kabul etmek.",
            "Zorunlu koşulu tek başına yeterli saymak.",
            "Gündelik nedensellik ile biçimsel koşul ilişkisini şimdiden özdeş saymak.",
        ],
        _practice([
            ("A'nın gerçekleşmesi B'yi garanti ediyorsa A, B için nedir?", ["Zorunlu koşul", "Yeterli koşul", "Karşı örnek", "Sonuç göstergesi"], "Yeterli koşul", "Garanti eden taraf yeterli koşuldur.", "Temel"),
            ("B olmadan A gerçekleşemiyorsa B, A için nedir?", ["Yeterli koşul", "Zorunlu koşul", "Ters koşul", "Örnek"], "Zorunlu koşul", "A'nın gerçekleşmesi B'nin bulunmasını gerektirir.", "Temel"),
            ("'Yalnızca bileti olanlar salona girer' cümlesinde zorunlu koşul hangisidir?", ["Salona girmek", "Bilet sahibi olmak", "Dışarı çıkmak", "Cümlenin söylenmesi"], "Bilet sahibi olmak", "Giriş gerçekleşirse bilet mutlaka bulunmalıdır.", "Orta"),
            ("Kare olmak dörtgen olmak için yeterliyse hangisi doğrudur?", ["Her dörtgen karedir", "Kare olan her şey dörtgendir", "Kare ile dörtgen ilgisizdir", "Hiçbir kare dörtgen değildir"], "Kare olan her şey dörtgendir", "Yeterli koşul, sonucu garanti eder.", "Orta"),
            ("'Dört ile bölünebilmek için çift olmak zorunludur' cümlesi ne söylemez?", ["Dörde bölünen her sayı çifttir", "Her çift sayı dörde bölünür", "Çiftlik gereklidir", "Tek sayılar dörde bölünmez"], "Her çift sayı dörde bölünür", "Bu, asıl cümlenin ters yönüdür ve örneğin altı sayısında başarısız olur.", "İleri"),
            ("'Bilet göstermedikçe içeri giremezsin' standart okumada ne kurar?", ["Bilet göstermek giriş için gereklidir", "Giriş bilet için gereklidir", "Bilet göstermek girişi imkânsız yapar", "Koşul içermez"], "Bilet göstermek giriş için gereklidir", "İçeri girmenin gerçekleşmesi bilet göstermeyi gerektirir.", "İleri"),
            ("'Dosya ancak ödeme yapılırsa işleme alınır' cümlesi hangisini söyler?", ["Ödeme, işleme alınmak için zorunludur", "Ödeme her durumda işlemi garanti eder", "İşleme alınmak ödeme için zorunludur", "Cümle koşul içermez"], "Ödeme, işleme alınmak için zorunludur", "Koşul kuran ancak, ödeme tarafını gerekli koşul yapar; başka koşullar bulunabilir.", "İleri"),
            ("'Rapor uzundu; ancak anlaşılırdı' cümlesindeki ancak ne yapar?", ["Zorunlu koşul kurar", "Yeterli koşul kurar", "Karşıtlık bildirir", "Çift yönlü koşul kurar"], "Karşıtlık bildirir", "Burada ancak, iki niteliği beklenmedik bir karşıtlıkla bağlar; koşul kurmaz.", "Orta"),
            ("Tek yönlü koşulun tersini sınamanın iyi yolu nedir?", ["Asıl örneği tekrar etmek", "Ters yönün başlangıcını doğru, sonucunu yanlış yapan karşı durum aramak", "Sözcükleri alfabetik dizmek", "Sonucu silmek"], "Ters yönün başlangıcını doğru, sonucunu yanlış yapan karşı durum aramak", "Ters koşul bağımsız bir iddiadır ve kendi karşı durumuyla sınanır.", "Zor"),
            ("Bir koşulun çift yönlü olması ne gerektirir?", ["Yalnız asıl yönün doğru olmasını", "Her iki tarafın da diğeri için hem zorunlu hem yeterli olmasını", "Cümlenin iki kez yazılmasını", "Bir tarafın yanlış olmasını"], "Her iki tarafın da diğeri için hem zorunlu hem yeterli olmasını", "Çift yönlü ilişki iki tek yönlü garantiyi birlikte taşır.", "Zor"),
        ]),
        {
            "prompt": "Şu üç cümleyi karşılaştır: 'Yalnızca kayıtlı öğrenciler sınava girebilir.' 'Öğrenci sınava ancak kayıtlıysa girebilir.' 'Öğrenci kaydolmadıkça sınava giremez.'",
            "starter": "Her cümlede gerçekleşen sonucu bul: sınava girmek. Sonra bu sonuç için mutlaka bulunması gereken koşulu ve söylenmeyen ters yönü yaz.",
            "checks": ["Üç yapıda da sonuç tarafı belirlendi", "Ortak zorunlu koşul belirlendi", "Kayıtlı olmanın tek başına yeterli sayılmadığı açıklandı"],
            "solution": "Standart koşul okumalarında üç cümle de sınava girmenin kayıtlı olmayı gerektirdiğini söyler. Kayıtlı olmak zorunludur; hiçbir cümle her kayıtlı öğrencinin mutlaka sınava gireceğini söylemez.",
        },
        [
            _production_task(
                "Altı doğal dil cümlesinde önce koşul kurulup kurulmadığını belirle. Koşul kuranları garanti ve gereklilik diliyle yeniden yaz; birinin tersini karşı durumla çürüt.",
                [
                    "Koşul kurmayan karşıtlık kullanımını gerekçesiyle ayır.",
                    "Koşul kuran her cümlede yeterli ve zorunlu tarafı ayrı adlandır.",
                    "Ters koşul için başlangıcı doğru, sonucu yanlış yapan ilgili bir karşı durum üret.",
                ],
                "Sözcük sırasına değil hangi tarafın hangisini garanti ettiğine dayan; tek yönü çift yöne genişletme.",
                "Çözümlenecek cümleler",
                [
                    "Bir sayı dörtle bölünüyorsa çifttir.",
                    "Yalnızca bileti olanlar salona girebilir.",
                    "Dosya ancak ödeme yapılırsa işleme alınır.",
                    "Alarm devredeyse kırmızı ışık yanar.",
                    "Şifreyi girmedikçe hesaba erişemezsin.",
                    "Toplantı uzundu; ancak verimli geçti.",
                ],
                "Her cümleyi önce gündelik anlamıyla oku. Bu aşamada yalnız standart çıkarımsal yön çözümlenecek; maddi koşul semantiği henüz kullanılmayacak.",
            ),
        ],
        [
            "Yalnızca, ancak ve -medikçe içeren koşullarda yönü doğru gerekçelendirir.",
            "Ancak ve ise sözcüklerinin koşul kurmayan kullanımlarını otomatik şemalaştırmaz.",
            "Yeterli ve zorunlu koşulu aynı ilişki üzerinde ters roller olarak açıklar.",
            "Tek yönlü koşulun tersini ilgili bir karşı durumla bağımsız olarak sınar.",
        ],
        [
            "'A yalnızca B ise' ifadesinde hangi taraf gerekli koşuldur?",
            "Bir cümledeki ancak sözcüğünün koşul mu, karşıtlık mı kurduğunu nasıl anlarsın?",
            "Bir koşulun tersi neden asıl koşuldan kendiliğinden çıkmaz?",
        ],
        "Sonraki derste nesneler hakkında konuşmak ile onları gösteren ifadeler hakkında konuşmayı ayıracağız.",
        ["openstax-conditionals", "dowden-only-unless", "sep-necessary-sufficient"],
        "Bu ders, gerekli ve yeterli koşulları standart çıkarımsal okumayla öğretir. Gündelik koşullar ayrıca nedensel, zamansal, açıklayıcı veya pragmatik anlamlar taşıyabilir; aynı sözcükler koşul dışı işlevlerde de kullanılabilir. Koşul işareti B aşamasında, doğruluk işlevsel maddi koşulun kesin semantiği ise C aşamasında ayrıca kurulacaktır.",
        ["ders-5-zorunlu-ve-yeterli-kosul", "ders-6-gecerli-kaliplar-ve-yon-hatalari"],
    ),
    _lesson(
        "A6",
        "ders-kullanim-anma-ve-dil-duzeyleri",
        "Kullanım, Anma ve Dil Düzeyleri",
        "Bir nesne veya içerik hakkında konuşmak ile onu gösteren ifadeden söz etmeyi; incelenen dil ile o dili açıklayan üst dili ayırır.",
        "Mantık dili hakkında konuşma",
        30,
        ["ders-1-onerme-nedir", "ders-3-gecerlilik-ve-dogruluk"],
        ["language.use_mention", "language.object_meta", "syntax_semantics.distinguish"],
        [
            "Bir ifadeyi kullanmak ile ifadeden söz etmek arasındaki farkı tırnaklarla göstermek.",
            "İncelenen nesne dili ile onu açıklamak için kullanılan üst dili ayırmak.",
            "Bir ifadenin biçimsel özellikleri hakkındaki iddia ile anlamı veya doğruluğu hakkındaki iddiayı karıştırmamak.",
        ],
        [
            ("Kullanım", "Bir ifadeyi, onun aracılığıyla bir nesneye gönderimde bulunmak veya bir içerik ileri sürmek için işletmek."),
            ("Anma", "Bir ifadeyi dilsel nesne hâline getirip ifadenin kendisi hakkında konuşmak; bu derste sınırı tırnakla gösterilir."),
            ("Nesne dili", "Belirli bir çözümlemede ifadeleri ve kuralları doğrudan incelenen dil."),
            ("Üst dil", "Nesne dilinin ifadelerini adlandırmak, sınıflandırmak veya açıklamak için kullanılan dil."),
            ("Sözdizimsel özellik", "Bir ifadenin işaretleri, sırası veya iyi kurulmuşluğu gibi biçimsel özelliği."),
            ("Anlamsal özellik", "Bir ifadenin anlamı, doğruluğu veya gönderimiyle ilgili semantik özellik."),
        ],
        [
            _section(
                "İfadeyi kullanmak ve ifadeyi anmak",
                "Bir ifadeyi kullanınca onun aracılığıyla nesne veya içerikten, ifadeyi tırnak içinde anınca dilsel ifadenin kendisinden söz ederiz.",
                "Sözcüklerin ve bütün cümlelerin harf sayısı, yazımı, anlamı veya doğruluğu hakkında kurulan cümleleri ayırırken.",
                "Nesne veya içerikten söz ederken ifadeyi kullan; dilsel ifadenin kendisinden söz ederken bu derste tırnakla sınırlandır.",
                "Kullanım ve anma, aynı yazı dizisinin cümlede farklı mantıksal roller üstlenmesini açıklar; tırnak içindeki ifade nesnesinin adı gibi çalışır.",
                "Tırnak her bağlamda teknik anma işareti değildir; doğrudan aktarım, ironi ve alıntı işlevleri ayrıca bulunur. Bu derste tırnağın hangi ifadeyi konu yaptığına bak.",
                [
                    ("Ankara Türkiye'nin başkentidir.", "Ankara adı bir şehre gönderimde bulunmak için kullanılır."),
                    ("'Ankara' altı harften oluşur.", "Şehir değil, Ankara sözcüğü anılır."),
                    ("'Kar beyazdır' iki sözcükten oluşur.", "Karın kendisi değil, bütün bir cümle anılır."),
                ],
                (
                    "Dilsel ifadeyi konu yaptığında tırnakla sınırlandırmak.",
                    "Ankara altı harften oluşur demek.",
                    "Harflerden oluşan şehir değil, şehri gösteren sözcüktür.",
                ),
            ),
            _section(
                "Nesne dili ve üst dil",
                "Bir dili incelerken o dilin ifadelerini başka bir dilde adlandırır, sınıflandırır ve onlar hakkında kurallar söyleriz.",
                "Mantıksal dilin işaretleri ve iyi kurulmuş ifadeleri hakkında konuşurken düzey karışıklığını önlemek için.",
                "Oyuncak nesne dili yalnız 'A' ve 'B' işaretlerini içersin; Türkçe bu işaretler hakkında konuşan üst dil olsun.",
                "Üst dil, nesne dilinin ifadelerini konu edinir; daha doğru veya daha değerli olduğu için 'üst' değildir.",
                "Nesne dili ve üst dil her zaman farklı doğal diller olmak zorunda değildir. Tek bir cümlenin bütünü üst dildeyken tırnak içindeki parçası nesne dilinden anılmış olabilir.",
                [
                    ("A", "Tek başına L dilinin bir satırında gösterildiğinde A, nesne dili cümlesi olarak kullanılır."),
                    ("'A' oyuncak dilin bir cümle harfidir.", "Türkçe üst dilde, nesne dilindeki bir işaretten söz edilir."),
                    ("'B', 'A'dan farklı bir işarettir.", "İki nesne dili ifadesinin biçimsel ilişkisi üst dilde belirtilir."),
                ],
                (
                    "Hangi ifadenin incelendiğini ve hangi dilde açıklama yaptığını belirtmek.",
                    "Üst dili daha üstün veya daha doğru bir dil sanmak.",
                    "Üst sözcüğü değer sırası değil, hakkında konuşma düzeyini gösterir.",
                ),
            ),
            _section(
                "Sözdizimi ve semantik hakkında konuşmak",
                "Bir ifadenin kaç işaret içerdiği ile ne anlama geldiği ya da doğru olup olmadığı farklı soru türleridir.",
                "Biçimsel dilde yapı kuralları ile yorum ve doğruluk kurallarını ayırmaya hazırlanırken.",
                "Sözdizimi sorusu: Hangi işaretlerden, hangi kuralla kurulmuş? Anlam sorusu: Ne anlama geliyor veya hangi durumda doğru?",
                "Aynı ifade hem sözdizimsel hem anlamsal incelemeye konu olabilir. İyi kurulmuş bir cümle yanlış olabilir; iyi kurulmamış bir işaret dizisi ise sırf bu nedenle yanlış bir cümle sayılmaz.",
                "Bir cümlenin kısa veya kurallı olmasından doğru olduğu; doğru olmasından da incelenen dilde iyi kurulduğu sonucu çıkmaz.",
                [
                    ("'Kar beyazdır' iki sözcükten oluşur.", "İfadenin biçimi hakkında sözdizimsel bir iddiadır."),
                    ("'Kar beyazdır' olağan koşullarda doğrudur.", "İfadenin doğruluğu hakkında anlamsal bir iddiadır."),
                    ("'A' oyuncak dilde izin verilen bir işarettir.", "Dilin alfabesi ve iyi kurulmuşluğu hakkında üst dil iddiasıdır."),
                    ("'Ankara İzmir'in ilçesidir' iyi kurulmuş fakat yanlış bir Türkçe cümledir.", "Sözdizimsel kabul ile doğruluk değeri farklı ölçütlerle değerlendirilir."),
                ],
                (
                    "Biçim ve anlam sorularını ayrı gerekçelerle cevaplamak.",
                    "İyi kurulmamış bir işaret dizisine yalnız 'yanlış cümle' demek.",
                    "Önce dizinin dilin cümlesi olup olmadığı, sonra böyle bir cümlenin doğruluğu sorulur.",
                ),
            ),
        ],
        [
            _worked("Ankara Türkiye'nin başkentidir.", "Ankara adı şehre gönderimde bulunmak için kullanılır.", "Kullanım"),
            _worked("'Ankara' altı harften oluşur.", "Şehrin değil, sözcüğün bir özelliği bildirilir.", "Anma"),
            _worked("Ankara altı harften oluşur.", "Tırnaksız okunduğunda harflerden oluşan şey şehir gibi görünür; düzey karışır.", "Düzey hatası", "bad"),
            _worked("'A' oyuncak dilin bir işaretidir.", "Türkçe üst dil nesne dilindeki A işaretini konu edinir.", "Üst dil"),
            _worked("'Ankara İzmir'in ilçesidir' iyi kurulmuş ama yanlıştır.", "Biçimsel kabul, doğruluğu garanti etmez.", "İki ayrı ölçüt"),
        ],
        [
            "Bir nesnenin özelliği ile onu gösteren sözcüğün özelliğini karıştırmak.",
            "Tırnak işaretini yalnız vurgu amacıyla kullanmak.",
            "Üst dili daha yüksek veya daha doğru bir doğal dil sanmak.",
            "Sözdizimsel özellikten doğrudan doğruluk sonucu çıkarmak.",
            "İyi kurulmamış bir diziyi, doğru veya yanlış olabilen sıradan bir cümle gibi sınıflandırmak.",
        ],
        _practice([
            ("Hangi cümle Ankara sözcüğünü anar?", ["Ankara kalabalıktır.", "Ankara Türkiye'dedir.", "'Ankara' altı harften oluşur.", "Ankara'ya gittim."], "'Ankara' altı harften oluşur.", "Tırnak içindeki ifade dilsel nesne olarak konu edilir.", "Temel"),
            ("'Kedi dört ayaklıdır' cümlesinde kedi sözcüğü ne yapar?", ["Anılır", "Kedilere gönderimde bulunmak için kullanılır", "Üst dil olur", "Harf sayar"], "Kedilere gönderimde bulunmak için kullanılır", "Cümle sözcüğün kendisinden değil kedilerden söz eder.", "Temel"),
            ("Nesne dili nedir?", ["Her zaman Türkçe", "İfadeleri doğrudan incelenen dil", "Daha doğru dil", "Yalnız bilgisayar kodu"], "İfadeleri doğrudan incelenen dil", "Nesne dili rolü, incelemenin hedefi olmasıyla belirlenir.", "Orta"),
            ("Üst dil neden 'üst' diye adlandırılır?", ["Daha değerli olduğu için", "Nesne dilinin ifadeleri hakkında konuştuğu için", "Daha uzun olduğu için", "Yalnız uzmanlar kullandığı için"], "Nesne dilinin ifadeleri hakkında konuştuğu için", "Adlandırma bir değer sırası değil, hakkında konuşma ilişkisi belirtir.", "Orta"),
            ("'Kar beyazdır' iki sözcükten oluşur cümlesi hangi tür özelliği bildirir?", ["Sözdizimsel", "Yalnız ahlaki", "Nedensel", "Coğrafi"], "Sözdizimsel", "Sözcük sayısı ifadenin biçimsel yapısıyla ilgilidir.", "İleri"),
            ("'Kar beyazdır' doğrudur cümlesi hangi tür soruya cevap verir?", ["İfade kaç harfli?", "İfadenin doğruluk koşulu karşılanıyor mu?", "İfade nerede yazıldı?", "Tırnak hangi renkte?"], "İfadenin doğruluk koşulu karşılanıyor mu?", "Doğruluk semantik değerlendirmedir.", "İleri"),
            ("Türkçe hem nesne dili hem üst dil olabilir mi?", ["Hayır, hiçbir zaman", "Evet, belirli bağlamda hangi ifadelerin incelendiğine göre", "Yalnız sözlükte", "Yalnız yanlış cümlelerde"], "Evet, belirli bağlamda hangi ifadelerin incelendiğine göre", "Ayrım dil adlarından çok işlevsel rollere dayanır.", "Zor"),
            ("Kullanım/anma ayrımında tırnağın temel görevi nedir?", ["Cümleyi süslemek", "Anılan dilsel ifadenin sınırını göstermek", "İfadeyi doğru yapmak", "Her sözcüğü vurgulamak"], "Anılan dilsel ifadenin sınırını göstermek", "Tırnak, ifadenin kendisini konu edinir.", "Zor"),
            ("L yalnız A ve B'yi cümle kabul ediyorsa, 'AB' için önce hangi soru sorulur?", ["Doğru mu?", "Yanlış mı?", "L'de iyi kurulmuş bir cümle mi?", "İkna edici mi?"], "L'de iyi kurulmuş bir cümle mi?", "Bir işaret dizisinin doğruluğunu değerlendirmeden önce incelenen dilde cümle olup olmadığı belirlenir.", "İleri"),
            ("'A, L'nin bir cümlesidir' Türkçe cümlesinde hangi parça nesne dilinden anılır?", ["Bütün Türkçe cümle", "Yalnız 'A'", "Yalnız 'L'nin'", "Hiçbiri"], "Yalnız 'A'", "Cümlenin bütünü Türkçe üst dildedir; tırnak içindeki A, L dilinden anılan ifadedir.", "Zor"),
        ]),
        {
            "prompt": "Ankara altı harften oluşur; Ankara Türkiye'nin başkentidir.",
            "starter": "İlk cümlede özellik şehre mi, sözcüğe mi ait? Yalnız gerekli olan ifadeyi tırnak içine al.",
            "checks": ["Anılan ifade tırnakla sınırlandı", "Kullanılan ad tırnaksız bırakıldı", "İki cümlenin farklı düzeyleri açıklandı"],
            "solution": "'Ankara' altı harften oluşur; Ankara Türkiye'nin başkentidir. İlk cümle sözcükten, ikincisi şehirden söz eder.",
        },
        [
            _production_task(
                "Altı kullanım/anma örneğini değerlendir; hatalı olanları düzelt, doğru kontrol örneklerini gerekçesiyle koru. Ardından yalnız A ve B işaretlerinden oluşan küçük bir nesne dili hakkında Türkçe üst dil cümleleri kur.",
                [
                    "Nesne ile onu gösteren sözcüğün özelliklerini doğru ayır.",
                    "L hakkında en az iki sözdizimsel ve iki anlamsal üst dil cümlesi üret.",
                    "Tek başına bir A satırı ile A'dan Türkçe üst dilde söz eden cümleyi ayrı göster.",
                    "Tırnakları vurgu için değil, anılan ifadenin sınırını göstermek için kullan.",
                ],
                "Hangi dilin incelendiğini ve hangi dilde açıklama yaptığını görünür tut; iyi kurulmuşluk ile doğruluğu ayrı kararlar olarak ver.",
                "Değerlendirilecek kullanım/anma örnekleri",
                [
                    "Ankara altı harften oluşur.",
                    "'Ankara' Türkiye'nin başkentidir.",
                    "'Kedi' dört harflidir.",
                    "'Kedi' dört ayaklıdır.",
                    "Kar beyazdır iki sözcükten oluşur.",
                    "'Kar beyazdır' olağan koşullarda doğrudur.",
                ],
                "Oyuncak dil L'de yalnız 'A' ve 'B' iyi kurulmuş cümlelerdir. 'A' cümlesi lamba yanıyorsa ve yalnız o durumda; 'B' cümlesi kapı açıksa ve yalnız o durumda doğrudur. Düzeltmelerden sonra L'nin işaretleri ve bu doğruluk koşulları hakkında istenen Türkçe üst dil cümlelerini kur.",
            ),
        ],
        [
            "Sözcük ile gönderimde bulunduğu nesneyi tırnak kullanımıyla doğru ayırır.",
            "Nesne dili ifadesi hakkında üst dilde doğru bir cümle kurar.",
            "Sözdizimsel bir özellik ile anlamsal bir özelliği farklı gerekçelerle açıklar.",
            "İyi kurulmuş fakat yanlış cümle ile iyi kurulmamış işaret dizisini ayırır.",
        ],
        [
            "'Kar beyazdır.' ile \"'Kar beyazdır' iki sözcükten oluşur.\" cümlelerinde aynı söz dizisi nasıl farklı rol oynar?",
            "Bir ifadenin nasıl kurulduğunu sormak ile ne anlama geldiğini sormak neden farklıdır?",
        ],
        "Bu aşamadan sonra önermeler mantığının nesne dilini kurmaya ve biçimsel ifadeleri üst dilde çözümlemeye hazırız.",
        ["forallx-use-mention"],
        "Kullanım/anma ayrımı burada doğal dil ve iki işaretli oyuncak dille kurulur; biçimsel formüller öğretilmeden öğrenci tanımadığı sembollerle sınanmaz. Kaynak bölümündeki üst değişkenler ve biçimsel alıntı kuralları B aşamasında, öğrenci önermeler mantığının nesne dilini öğrendikten sonra ele alınacaktır.",
        [],
    ),
]


STAGE_A_CANDIDATE_MAP = {
    lesson["slug"]: lesson
    for lesson in STAGE_A_CANDIDATE_LESSONS
}
