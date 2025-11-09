#!/usr/bin/env python
"""
Gerçek Dünya Yük Testi (Load Test)
Concurrent kullanıcıları simüle eder ve gerçek performansı ölçer
"""

import os
import sys
import django
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hafifayaklar.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection, reset_queries
from django.test import Client
from core.models import Question, Answer, Message


class LoadTester:
    """Gerçek dünya yük testi"""

    def __init__(self):
        self.results = []
        self.lock = Lock()
        self.users = list(User.objects.all()[:50])  # İlk 50 kullanıcı
        self.questions = list(Question.objects.all()[:100])  # İlk 100 soru

    def simulate_user_session(self, user_id, session_id):
        """Bir kullanıcının tipik session'ını simüle et"""
        client = Client()
        user = random.choice(self.users)

        # Login
        client.force_login(user)

        actions = []
        errors = []

        try:
            # 1. Ana sayfa yükle
            start = time.time()
            response = client.get('/')
            duration = (time.time() - start) * 1000
            actions.append({
                'action': 'Homepage',
                'duration': duration,
                'status': response.status_code
            })

            # 2. Rastgele bir başlığa git
            if self.questions:
                question = random.choice(self.questions)
                start = time.time()
                response = client.get(f'/{question.slug}/')
                duration = (time.time() - start) * 1000
                actions.append({
                    'action': 'Question Detail',
                    'duration': duration,
                    'status': response.status_code
                })

            # 3. Mesajları kontrol et
            start = time.time()
            response = client.get('/messages/')
            duration = (time.time() - start) * 1000
            actions.append({
                'action': 'Message List',
                'duration': duration,
                'status': response.status_code
            })

            # 4. Profil sayfası
            start = time.time()
            response = client.get(f'/profile/{user.username}/')
            duration = (time.time() - start) * 1000
            actions.append({
                'action': 'User Profile',
                'duration': duration,
                'status': response.status_code
            })

        except Exception as e:
            errors.append(str(e))

        with self.lock:
            self.results.append({
                'session_id': session_id,
                'user': user.username,
                'actions': actions,
                'errors': errors
            })

        return len(errors) == 0

    def run_concurrent_test(self, num_users=20):
        """Eş zamanlı kullanıcı testi"""
        print(f"\n{'='*80}")
        print(f"EŞ ZAMANLI KULLANICI TESTİ - {num_users} kullanıcı")
        print(f"{'='*80}")

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [
                executor.submit(self.simulate_user_session, i, f"session_{i}")
                for i in range(num_users)
            ]

            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 5 == 0:
                    print(f"   {completed}/{num_users} session tamamlandı...")

        total_time = time.time() - start_time

        print(f"\n✓ {num_users} kullanıcı testi {total_time:.2f} saniyede tamamlandı")
        print(f"   Ortalama: {(total_time/num_users)*1000:.2f} ms/kullanıcı")

        return total_time

    def analyze_results(self):
        """Sonuçları analiz et"""
        print(f"\n{'='*80}")
        print("DETAYLI ANALİZ")
        print(f"{'='*80}")

        if not self.results:
            print("Hiç sonuç yok!")
            return

        # Action bazlı analiz
        action_times = {}
        action_errors = {}

        for result in self.results:
            for action in result['actions']:
                action_name = action['action']

                if action_name not in action_times:
                    action_times[action_name] = []
                    action_errors[action_name] = 0

                action_times[action_name].append(action['duration'])

                if action['status'] != 200:
                    action_errors[action_name] += 1

        print(f"\n📊 SAYFA YÜKLEME SÜRELERİ:\n")
        print(f"{'Sayfa':<25} {'Min':<10} {'Max':<10} {'Ort':<10} {'Error':<10}")
        print("-" * 65)

        for action_name in sorted(action_times.keys()):
            times = action_times[action_name]
            min_time = min(times)
            max_time = max(times)
            avg_time = sum(times) / len(times)
            errors = action_errors[action_name]

            status = "🟢" if avg_time < 100 else "🟡" if avg_time < 500 else "🔴"

            print(f"{status} {action_name:<23} {min_time:>6.0f}ms {max_time:>8.0f}ms {avg_time:>8.0f}ms {errors:>8}")

        # Yavaş sayfalar
        print(f"\n⚠️  YAVAS SAYFALAR (>500ms):")
        slow_pages = []
        for action_name, times in action_times.items():
            avg = sum(times) / len(times)
            if avg > 500:
                slow_pages.append((action_name, avg, max(times)))

        if slow_pages:
            for page, avg, max_time in sorted(slow_pages, key=lambda x: x[1], reverse=True):
                print(f"   - {page}: {avg:.0f}ms ortalama, {max_time:.0f}ms maksimum")
        else:
            print("   Hiç yavaş sayfa yok! ✅")

        # Error analizi
        total_errors = sum(len(r['errors']) for r in self.results)
        if total_errors > 0:
            print(f"\n❌ TOPLAM ERROR: {total_errors}")
            for result in self.results:
                if result['errors']:
                    print(f"   Session {result['session_id']}: {result['errors']}")
        else:
            print(f"\n✅ HİÇ ERROR YOK!")

    def run_stress_test(self):
        """Stres testi - giderek artan yük"""
        print(f"\n{'='*80}")
        print("STRES TESTİ - GİDEREK ARTAN YÜK")
        print(f"{'='*80}")

        test_levels = [5, 10, 20, 50]

        results_summary = []

        for num_users in test_levels:
            print(f"\n🔄 {num_users} eş zamanlı kullanıcı testi başlıyor...")

            self.results = []  # Reset
            total_time = self.run_concurrent_test(num_users)

            # Ortalama response time hesapla
            all_times = []
            for result in self.results:
                for action in result['actions']:
                    all_times.append(action['duration'])

            if all_times:
                avg_response = sum(all_times) / len(all_times)
            else:
                avg_response = 0

            results_summary.append({
                'users': num_users,
                'total_time': total_time,
                'avg_response': avg_response
            })

            # Kısa analiz
            print(f"   Ortalama response time: {avg_response:.0f}ms")

            # Çok yavaşsa dur
            if avg_response > 2000:
                print(f"\n⚠️  UYARI: Response time 2 saniyeyi geçti! Test durduruluyor.")
                break

        # Stres testi özeti
        print(f"\n{'='*80}")
        print("STRES TESTİ ÖZETİ")
        print(f"{'='*80}\n")

        print(f"{'Kullanıcı':<15} {'Toplam Süre':<15} {'Ort Response':<15} {'Durum':<10}")
        print("-" * 55)

        for summary in results_summary:
            status = "✅ İyi" if summary['avg_response'] < 500 else \
                    "⚠️  Yavaş" if summary['avg_response'] < 1000 else \
                    "🔴 Kötü"

            print(f"{summary['users']:<15} {summary['total_time']:<14.2f}s {summary['avg_response']:<14.0f}ms {status:<10}")

    def check_database_performance(self):
        """Database performansını kontrol et"""
        print(f"\n{'='*80}")
        print("DATABASE PERFORMANS KONTROLÜ")
        print(f"{'='*80}")

        from django.db import connection

        # Toplam veri miktarı
        with connection.cursor() as cursor:
            # SQLite için table boyutlarını al
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table'
                ORDER BY name;
            """)
            tables = cursor.fetchall()

            print(f"\n📊 DATABASE İÇERİĞİ:\n")

            total_rows = 0
            for (table_name,) in tables:
                if table_name.startswith('django_') or table_name.startswith('sqlite_'):
                    continue

                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_rows += count

                if count > 0:
                    print(f"   {table_name:<30} {count:>8} row")

            print(f"\n   {'TOPLAM':<30} {total_rows:>8} row")

        # Yavaş sorguları simüle et
        print(f"\n🔍 YAVAS SORGU TESTİ:\n")

        # Test 1: Filtreli arama (index olmadan)
        start = time.time()
        messages = Message.objects.filter(
            recipient__username__icontains='test',
            is_read=False
        )[:100]
        list(messages)  # Force evaluation
        duration = (time.time() - start) * 1000

        status = "✅" if duration < 50 else "⚠️" if duration < 200 else "🔴"
        print(f"   {status} Filtreli mesaj araması: {duration:.2f}ms")

        # Test 2: JOIN heavy query
        start = time.time()
        answers = Answer.objects.select_related('question', 'user').filter(
            question__question_text__icontains='felsefe'
        )[:50]
        list(answers)
        duration = (time.time() - start) * 1000

        status = "✅" if duration < 50 else "⚠️" if duration < 200 else "🔴"
        print(f"   {status} JOIN'li yanıt araması: {duration:.2f}ms")

        # Test 3: Aggregate query
        start = time.time()
        from django.db.models import Count
        users_with_answers = User.objects.annotate(
            answer_count=Count('answers')
        ).filter(answer_count__gt=5)[:20]
        list(users_with_answers)
        duration = (time.time() - start) * 1000

        status = "✅" if duration < 100 else "⚠️" if duration < 300 else "🔴"
        print(f"   {status} Aggregate sorgusu: {duration:.2f}ms")


def main():
    """Ana test fonksiyonu"""
    print("\n" + "="*80)
    print("GERÇEK DÜNYA YÜK TESTİ")
    print("="*80)
    print("\nBu test şunları yapacak:")
    print("  1. Eş zamanlı kullanıcıları simüle et")
    print("  2. Gerçek sayfa yüklemelerini test et")
    print("  3. Stres testi (5, 10, 20, 50 kullanıcı)")
    print("  4. Database performansını kontrol et")
    print("\n⚠️  UYARI: Bu test 2-3 dakika sürebilir!")

    response = input("\nDevam etmek istiyor musunuz? (y/n): ")
    if response.lower() != 'y':
        print("İptal edildi.")
        return 1

    tester = LoadTester()

    try:
        # 1. Database kontrolü
        tester.check_database_performance()

        # 2. Stres testi
        tester.run_stress_test()

        # 3. Son test için detaylı analiz
        print(f"\n{'='*80}")
        print("SON TEST - DETAYLI ANALİZ İÇİN")
        print(f"{'='*80}")
        tester.results = []
        tester.run_concurrent_test(20)
        tester.analyze_results()

        # Final öneriler
        print(f"\n{'='*80}")
        print("SONUÇ VE ÖNERİLER")
        print(f"{'='*80}\n")

        print("Bu testler gerçek dünya koşullarını simüle etti.")
        print("Eğer:")
        print("  - Response time < 500ms  : ✅ Mükemmel")
        print("  - Response time < 1000ms : ⚠️  Kabul edilebilir, optimizasyon önerilir")
        print("  - Response time > 1000ms : 🔴 Optimizasyon şart!")
        print("\nBir sonraki adım: Index'leri eklemek ve tekrar test etmek.")

        return 0

    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
