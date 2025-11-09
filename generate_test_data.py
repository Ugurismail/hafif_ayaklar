#!/usr/bin/env python
"""
Test Verisi Oluşturma Script'i
10,000 kullanıcı senaryosu için gerçekçi test verisi oluşturur
"""

import os
import sys
import django
import random
from datetime import timedelta
from django.utils import timezone

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hafifayaklar.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from core.models import (
    Question, Answer, Message, Vote, SavedItem,
    UserProfile, Reference, Poll, PollOption
)
from django.contrib.contenttypes.models import ContentType


class TestDataGenerator:
    """Test verisi oluşturucu"""

    def __init__(self):
        self.users = []
        self.questions = []
        self.answers = []

        # Türkçe başlıklar için örnek kelimeler
        self.topic_words = [
            "felsefe", "edebiyat", "müzik", "sinema", "teknoloji",
            "bilim", "sanat", "tarih", "psikoloji", "sosyoloji",
            "ekonomi", "siyaset", "spor", "gastronomi", "seyahat",
            "doğa", "mimari", "fotograf", "dans", "tiyatro"
        ]

        self.adjectives = [
            "modern", "klasik", "çağdaş", "alternatif", "mainstream",
            "underground", "popüler", "niche", "indie", "experimental"
        ]

    def create_users(self, count=100):
        """Kullanıcıları oluştur"""
        print(f"\n📝 {count} kullanıcı oluşturuluyor...")

        created_count = 0
        with transaction.atomic():
            for i in range(count):
                username = f"testuser{i+1:04d}"

                # Kullanıcı zaten varsa atla
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    self.users.append(user)
                    continue

                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@test.com",
                    password="test12345"
                )

                # UserProfile oluştur
                UserProfile.objects.get_or_create(user=user)

                self.users.append(user)
                created_count += 1

                if (i + 1) % 25 == 0:
                    print(f"   {i + 1}/{count} kullanıcı oluşturuldu...")

        print(f"✓ {created_count} yeni kullanıcı oluşturuldu (toplam {len(self.users)} kullanıcı)")

    def create_questions(self, count=200):
        """Başlıkları oluştur"""
        print(f"\n📝 {count} başlık oluşturuluyor...")

        created_count = 0
        with transaction.atomic():
            for i in range(count):
                # Rastgele başlık oluştur
                topic = random.choice(self.topic_words)
                adj = random.choice(self.adjectives)

                question_text = f"{adj} {topic} üzerine"

                # Aynı başlık varsa atla
                if Question.objects.filter(question_text=question_text).exists():
                    continue

                user = random.choice(self.users)

                question = Question.objects.create(
                    question_text=question_text,
                    user=user,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 90))
                )

                question.users.add(user)
                self.questions.append(question)
                created_count += 1

                if (i + 1) % 50 == 0:
                    print(f"   {i + 1}/{count} başlık oluşturuldu...")

        print(f"✓ {created_count} yeni başlık oluşturuldu (toplam {len(self.questions)} başlık)")

    def create_answers(self, count=1000):
        """Yanıtları oluştur"""
        print(f"\n📝 {count} yanıt oluşturuluyor...")

        if not self.questions:
            print("⚠️  Önce başlık oluşturulmalı!")
            return

        created_count = 0
        with transaction.atomic():
            for i in range(count):
                question = random.choice(self.questions)
                user = random.choice(self.users)

                answer_text = f"Bu konuda düşüncelerim şöyle: {random.choice(self.adjectives)} bir yaklaşım benimsemek gerekir. {random.choice(self.topic_words)} ile de ilişkilendirilebilir."

                answer = Answer.objects.create(
                    question=question,
                    user=user,
                    answer_text=answer_text,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 60)),
                    upvotes=random.randint(0, 20),
                    downvotes=random.randint(0, 5)
                )

                self.answers.append(answer)
                created_count += 1

                if (i + 1) % 250 == 0:
                    print(f"   {i + 1}/{count} yanıt oluşturuldu...")

        print(f"✓ {created_count} yanıt oluşturuldu")

    def create_messages(self, count=500):
        """Mesajları oluştur"""
        print(f"\n📝 {count} mesaj oluşturuluyor...")

        created_count = 0
        with transaction.atomic():
            for i in range(count):
                sender = random.choice(self.users)
                recipient = random.choice([u for u in self.users if u != sender])

                body = f"Merhaba! {random.choice(self.topic_words)} hakkında ne düşünüyorsun?"

                Message.objects.create(
                    sender=sender,
                    recipient=recipient,
                    body=body,
                    timestamp=timezone.now() - timedelta(hours=random.randint(0, 720)),
                    is_read=random.choice([True, False])
                )

                created_count += 1

                if (i + 1) % 100 == 0:
                    print(f"   {i + 1}/{count} mesaj oluşturuldu...")

        print(f"✓ {created_count} mesaj oluşturuldu")

    def create_votes(self, count=500):
        """Oyları oluştur"""
        print(f"\n📝 {count} oy oluşturuluyor...")

        if not self.answers:
            print("⚠️  Önce yanıt oluşturulmalı!")
            return

        content_type = ContentType.objects.get_for_model(Answer)
        created_count = 0

        with transaction.atomic():
            for i in range(count):
                user = random.choice(self.users)
                answer = random.choice(self.answers)

                # Aynı kullanıcı aynı answer'a zaten oy verdiyse atla
                if Vote.objects.filter(user=user, content_type=content_type, object_id=answer.id).exists():
                    continue

                Vote.objects.create(
                    user=user,
                    content_type=content_type,
                    object_id=answer.id,
                    value=random.choice([-1, 1])
                )

                created_count += 1

                if (i + 1) % 100 == 0:
                    print(f"   {i + 1}/{count} oy oluşturuldu...")

        print(f"✓ {created_count} oy oluşturuldu")

    def create_saved_items(self, count=300):
        """Kaydedilen öğeleri oluştur"""
        print(f"\n📝 {count} kayıt oluşturuluyor...")

        if not self.answers:
            print("⚠️  Önce yanıt oluşturulmalı!")
            return

        content_type = ContentType.objects.get_for_model(Answer)
        created_count = 0

        with transaction.atomic():
            for i in range(count):
                user = random.choice(self.users)
                answer = random.choice(self.answers)

                # Aynı kullanıcı aynı answer'ı zaten kaydettiyse atla
                if SavedItem.objects.filter(user=user, content_type=content_type, object_id=answer.id).exists():
                    continue

                SavedItem.objects.create(
                    user=user,
                    content_type=content_type,
                    object_id=answer.id,
                    saved_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )

                created_count += 1

                if (i + 1) % 75 == 0:
                    print(f"   {i + 1}/{count} kayıt oluşturuldu...")

        print(f"✓ {created_count} kayıt oluşturuldu")

    def print_summary(self):
        """Özet raporu yazdır"""
        print("\n" + "="*80)
        print("TEST VERİSİ OLUŞTURMA TAMAMLANDI")
        print("="*80)
        print(f"\n📊 DATABASE İSTATİSTİKLERİ:")
        print(f"   Kullanıcılar: {User.objects.count()}")
        print(f"   Sorular: {Question.objects.count()}")
        print(f"   Yanıtlar: {Answer.objects.count()}")
        print(f"   Mesajlar: {Message.objects.count()}")
        print(f"   Oylar: {Vote.objects.count()}")
        print(f"   Kaydedilenler: {SavedItem.objects.count()}")
        print("\n✅ Şimdi performans testini çalıştırabilirsiniz: python performance_test.py")
        print("="*80 + "\n")


def main():
    """Ana fonksiyon"""
    print("\n" + "="*80)
    print("TEST VERİSİ OLUŞTURMA BAŞLIYOR")
    print("="*80)
    print("\nBu script şunları oluşturacak:")
    print("  - 100 kullanıcı")
    print("  - 500 başlık")
    print("  - 5000 yanıt (entry)")
    print("  - 1000 mesaj")
    print("  - 1000 oy")
    print("  - 500 kayıt")
    print("\n⚠️  UYARI: Bu işlem birkaç dakika sürebilir!")

    response = input("\nDevam etmek istiyor musunuz? (y/n): ")
    if response.lower() != 'y':
        print("İptal edildi.")
        return 1

    generator = TestDataGenerator()

    try:
        generator.create_users(100)
        generator.create_questions(500)
        generator.create_answers(5000)
        generator.create_messages(1000)
        generator.create_votes(1000)
        generator.create_saved_items(500)
        generator.print_summary()

        return 0

    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
