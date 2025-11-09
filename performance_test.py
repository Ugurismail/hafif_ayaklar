#!/usr/bin/env python
"""
Hafif Ayaklar - Performans Test Script
Bu script en riskli noktaları test eder ve database sorgu sayısını + süreyi ölçer.
"""

import os
import sys
import django
import time
from django.db import connection, reset_queries
from django.conf import settings

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hafifayaklar.settings')
django.setup()

# Import models and views after Django setup
from django.contrib.auth.models import User
from core.models import Message, Question, Answer, Vote, SavedItem, Reference
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware


class PerformanceTester:
    """Performans testlerini yürüten sınıf"""

    def __init__(self):
        self.factory = RequestFactory()
        self.test_user = None
        self.results = []

    def setup(self):
        """Test için gerekli verileri hazırla"""
        print("\n" + "="*80)
        print("PERFORMANS TEST SETİ BAŞLIYOR")
        print("="*80)

        # Test kullanıcısı bul veya oluştur
        self.test_user = User.objects.first()
        if not self.test_user:
            print("\n⚠️  UYARI: Database'de hiç kullanıcı yok! Test yapılamıyor.")
            sys.exit(1)

        print(f"\n✓ Test kullanıcısı: {self.test_user.username}")

        # Database istatistikleri
        print(f"\n📊 DATABASE İSTATİSTİKLERİ:")
        print(f"   Kullanıcılar: {User.objects.count()}")
        print(f"   Sorular: {Question.objects.count()}")
        print(f"   Yanıtlar: {Answer.objects.count()}")
        print(f"   Mesajlar: {Message.objects.count()}")
        print(f"   Oylar: {Vote.objects.count()}")
        print(f"   Kaydedilenler: {SavedItem.objects.count()}")

    def measure_queries(self, test_name, test_func):
        """Bir fonksiyonun sorgu sayısını ve süresini ölç"""
        # Django'nun query logging'ini aç
        settings.DEBUG = True
        reset_queries()

        start_time = time.time()
        result = test_func()
        end_time = time.time()

        query_count = len(connection.queries)
        duration = (end_time - start_time) * 1000  # milliseconds

        # Sonuçları kaydet
        test_result = {
            'name': test_name,
            'queries': query_count,
            'duration_ms': round(duration, 2),
            'result': result
        }
        self.results.append(test_result)

        # Anlık rapor
        status = "⚠️" if query_count > 20 else "✓"
        print(f"\n{status} {test_name}")
        print(f"   Sorgu sayısı: {query_count}")
        print(f"   Süre: {duration:.2f} ms")

        if query_count > 50:
            print(f"   🚨 KRİTİK: {query_count} sorgu çok fazla!")
        elif query_count > 20:
            print(f"   ⚠️  UYARI: {query_count} sorgu optimize edilebilir")

        return test_result

    def test_1_message_list(self):
        """TEST 1: Message List View - N+1 Query Problemi"""
        print("\n" + "-"*80)
        print("TEST 1: MESSAGE LIST VIEW (message_views.py:30-65)")
        print("-"*80)

        def run_test():
            # Mesaj sayısını kontrol et
            message_count = Message.objects.filter(
                sender=self.test_user
            ).count() + Message.objects.filter(
                recipient=self.test_user
            ).count()

            if message_count == 0:
                print("   ℹ️  Hiç mesaj yok - simüle edilemiyor")
                return {'simulated': True, 'message_count': 0}

            # message_list view'ını simüle et
            messages = Message.objects.filter(
                Q(sender=self.test_user) | Q(recipient=self.test_user)
            ).select_related('sender', 'recipient')

            user_ids = set(messages.values_list('sender', flat=True)) | set(messages.values_list('recipient', flat=True))
            user_ids.discard(self.test_user.id)
            other_users = User.objects.filter(id__in=user_ids)

            conversation_count = 0
            for other_user in other_users:
                messages_with_user = messages.filter(
                    Q(sender=other_user, recipient=self.test_user) |
                    Q(sender=self.test_user, recipient=other_user)
                ).order_by('-timestamp')

                unread_count = messages_with_user.filter(
                    sender=other_user,
                    recipient=self.test_user,
                    is_read=False
                ).count()

                conversation_count += 1

            return {
                'simulated': True,
                'message_count': message_count,
                'conversation_count': conversation_count
            }

        from django.db.models import Q
        return self.measure_queries("Message List View", run_test)

    def test_2_get_user_answers(self):
        """TEST 2: Get User Answers - Missing select_related"""
        print("\n" + "-"*80)
        print("TEST 2: GET USER ANSWERS (answer_views.py:35-49)")
        print("-"*80)

        def run_test():
            # Kullanıcının yanıtlarını çek (DÜZELTİLMİŞ VERSİYON)
            answers = Answer.objects.filter(user=self.test_user).select_related('question')

            answer_count = answers.count()
            if answer_count == 0:
                print("   ℹ️  Hiç yanıt yok - simüle edilemiyor")
                return {'answer_count': 0}

            # Her answer için question_text'e eriş (artık N+1 YOK!)
            data = []
            for answer in answers[:20]:  # İlk 20 yanıt
                question_text = answer.question.question_text  # Artık ek sorgu YOK!
                question_slug = answer.question.slug  # Slug da kullanılıyor
                data.append(question_text)

            return {
                'answer_count': answer_count,
                'tested_count': len(data)
            }

        return self.measure_queries("Get User Answers (N+1)", run_test)

    def test_3_vote_check(self):
        """TEST 3: Vote Status Check - Missing Index"""
        print("\n" + "-"*80)
        print("TEST 3: VOTE STATUS CHECK (Her sayfa yüklemesinde)")
        print("-"*80)

        def run_test():
            from django.contrib.contenttypes.models import ContentType

            # 10 answer için oy durumunu kontrol et (normal bir sayfa yüklemesi)
            answers = Answer.objects.all()[:10]
            answer_ids = [a.id for a in answers]

            if not answer_ids:
                print("   ℹ️  Hiç answer yok - simüle edilemiyor")
                return {'tested_count': 0}

            content_type_answer = ContentType.objects.get_for_model(Answer)

            # Kullanıcının oylarını çek
            user_votes = Vote.objects.filter(
                user=self.test_user,
                content_type=content_type_answer,
                object_id__in=answer_ids
            ).values('object_id', 'value')

            vote_dict = {vote['object_id']: vote['value'] for vote in user_votes}

            return {
                'tested_count': len(answer_ids),
                'vote_count': len(vote_dict)
            }

        return self.measure_queries("Vote Status Check", run_test)

    def test_4_saved_item_check(self):
        """TEST 4: Saved Item Check - Missing Index"""
        print("\n" + "-"*80)
        print("TEST 4: SAVED ITEM CHECK (Her sayfa yüklemesinde)")
        print("-"*80)

        def run_test():
            from django.contrib.contenttypes.models import ContentType

            # 10 answer için kaydetme durumunu kontrol et
            answers = Answer.objects.all()[:10]
            answer_ids = [a.id for a in answers]

            if not answer_ids:
                print("   ℹ️  Hiç answer yok - simüle edilemiyor")
                return {'tested_count': 0}

            content_type_answer = ContentType.objects.get_for_model(Answer)

            # Kullanıcının kaydetmelerini çek
            saved_answer_ids = SavedItem.objects.filter(
                user=self.test_user,
                content_type=content_type_answer,
                object_id__in=answer_ids
            ).values_list('object_id', flat=True)

            return {
                'tested_count': len(answer_ids),
                'saved_count': len(saved_answer_ids)
            }

        return self.measure_queries("Saved Item Check", run_test)

    def test_5_reference_usage_count(self):
        """TEST 5: Reference.get_usage_count() - FELAKET"""
        print("\n" + "-"*80)
        print("TEST 5: REFERENCE USAGE COUNT (models.py:338-355)")
        print("-"*80)

        def run_test():
            # İlk kaynağı al
            ref = Reference.objects.first()

            if not ref:
                print("   ℹ️  Hiç kaynak yok - simüle edilemiyor")
                return {'reference_exists': False}

            # UYARI: Bu ÇOK YAVAŞ olabilir!
            print(f"   ⚠️  Reference ID {ref.id} kullanım sayısı hesaplanıyor...")
            print(f"   (Database'de {Answer.objects.count()} answer var)")

            usage_count = ref.get_usage_count()

            return {
                'reference_exists': True,
                'reference_id': ref.id,
                'usage_count': usage_count
            }

        return self.measure_queries("Reference Usage Count", run_test)

    def print_final_report(self):
        """Final raporu yazdır"""
        print("\n" + "="*80)
        print("FINAL RAPOR - PERFORMANS TESTİ SONUÇLARI")
        print("="*80)

        # Sıralama: En çok sorgu yapandan en aza
        sorted_results = sorted(self.results, key=lambda x: x['queries'], reverse=True)

        print("\n📊 SONUÇLAR (En riskli → En az riskli):\n")

        for i, result in enumerate(sorted_results, 1):
            risk_level = "🚨 KRİTİK" if result['queries'] > 50 else \
                        "⚠️  UYARI" if result['queries'] > 20 else \
                        "✓ İYİ"

            print(f"{i}. {result['name']}")
            print(f"   Risk: {risk_level}")
            print(f"   Sorgu: {result['queries']} | Süre: {result['duration_ms']} ms")
            print()

        # Öncelik önerileri
        print("\n" + "="*80)
        print("ÖNCELİK ÖNERİLERİ")
        print("="*80)

        critical = [r for r in sorted_results if r['queries'] > 50]
        warning = [r for r in sorted_results if 20 < r['queries'] <= 50]

        if critical:
            print("\n🚨 KRİTİK ÖNCELİK (Hemen düzeltilmeli):")
            for r in critical:
                print(f"   - {r['name']} ({r['queries']} sorgu)")

        if warning:
            print("\n⚠️  ORTA ÖNCELİK (Yakında düzeltilmeli):")
            for r in warning:
                print(f"   - {r['name']} ({r['queries']} sorgu)")

        if not critical and not warning:
            print("\n✓ Harika! Hiçbir kritik performans sorunu tespit edilmedi.")

        print("\n" + "="*80)
        print("Test tamamlandı! Şimdi optimizasyonlara başlayabiliriz.")
        print("="*80 + "\n")


def main():
    """Ana test fonksiyonu"""
    tester = PerformanceTester()

    try:
        # Setup
        tester.setup()

        # Testleri çalıştır
        print("\n" + "="*80)
        print("TESTLER BAŞLIYOR")
        print("="*80)

        tester.test_1_message_list()
        tester.test_2_get_user_answers()
        tester.test_3_vote_check()
        tester.test_4_saved_item_check()
        tester.test_5_reference_usage_count()

        # Final rapor
        tester.print_final_report()

    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
