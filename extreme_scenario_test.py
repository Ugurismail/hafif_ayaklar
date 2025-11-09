#!/usr/bin/env python
"""
Extreme Scenario Tests
Tests the most demanding real-world scenarios:
1. Heavy message user (200 conversations)
2. Popular question (500 answers)
3. Heavy profile (1000 entries)
4. Search performance (thousands of entries)
5. Concurrent writes (10 users writing simultaneously)
"""

import os
import sys
import django
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta
from django.utils import timezone

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hafifayaklar.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction, connection, reset_queries
from django.test import Client
from core.models import Question, Answer, Message
from django.conf import settings


class ExtremeScenarioTester:
    """Extreme scenario testing"""

    def __init__(self):
        self.results = []
        self.test_users = []
        self.test_questions = []

    def setup(self):
        """Initial setup"""
        print("\n" + "="*80)
        print("EXTREME SCENARIO TESTS - SETUP")
        print("="*80)

        # Get existing users
        self.existing_users = list(User.objects.all()[:50])
        self.existing_questions = list(Question.objects.all()[:50])

        print(f"\n✓ {len(self.existing_users)} existing users available")
        print(f"✓ {len(self.existing_questions)} existing questions available")

    def measure_with_queries(self, test_name, test_func):
        """Measure execution time and query count"""
        settings.DEBUG = True
        reset_queries()

        start_time = time.time()
        result = test_func()
        duration = (time.time() - start_time) * 1000  # ms

        query_count = len(connection.queries)

        test_result = {
            'name': test_name,
            'queries': query_count,
            'duration_ms': round(duration, 2),
            'result': result
        }
        self.results.append(test_result)

        return test_result

    # ============================================================================
    # TEST 1: HEAVY MESSAGE USER (200 conversations)
    # ============================================================================
    def test_1_heavy_message_user(self):
        """TEST 1: User with 200 message conversations"""
        print("\n" + "="*80)
        print("TEST 1: HEAVY MESSAGE USER (200 Conversations)")
        print("="*80)

        # Create test user
        test_user = User.objects.create_user(
            username="heavy_message_user",
            email="heavy@test.com",
            password="test12345"
        )
        self.test_users.append(test_user)

        print(f"\n📝 Creating 200 conversations with 5 messages each...")

        # Create 200 different users to talk with
        conversation_users = []
        with transaction.atomic():
            for i in range(200):
                user = User.objects.create_user(
                    username=f"msguser_{i}",
                    email=f"msguser_{i}@test.com",
                    password="test12345"
                )
                conversation_users.append(user)

                # Create 5 messages per conversation (alternating sender/recipient)
                for j in range(5):
                    if j % 2 == 0:
                        sender, recipient = test_user, user
                    else:
                        sender, recipient = user, test_user

                    Message.objects.create(
                        sender=sender,
                        recipient=recipient,
                        body=f"Test message {j} in conversation {i}",
                        timestamp=timezone.now() - timedelta(hours=i),
                        is_read=random.choice([True, False])
                    )

                if (i + 1) % 50 == 0:
                    print(f"   {i + 1}/200 conversations created...")

        print(f"✓ 200 conversations created (1000 total messages)")

        # Now test message_list performance
        print(f"\n🔍 Testing message_list view with 200 conversations...")

        def run_test():
            client = Client()
            client.force_login(test_user)

            start = time.time()
            response = client.get('/messages/')
            duration = (time.time() - start) * 1000

            return {
                'status_code': response.status_code,
                'duration_ms': round(duration, 2),
                'conversation_count': 200
            }

        result = self.measure_with_queries("Heavy Message User (200 conversations)", run_test)

        print(f"\n📊 RESULTS:")
        print(f"   Status: {result['result']['status_code']}")
        print(f"   Duration: {result['duration_ms']} ms")
        print(f"   Queries: {result['queries']}")

        if result['duration_ms'] > 1000:
            print(f"   🔴 WARNING: Page took > 1 second!")
        elif result['duration_ms'] > 500:
            print(f"   ⚠️  CAUTION: Page took > 500ms")
        else:
            print(f"   ✅ EXCELLENT: Fast page load!")

        # Cleanup
        print(f"\n🧹 Cleaning up test data...")
        Message.objects.filter(sender=test_user).delete()
        Message.objects.filter(recipient=test_user).delete()
        for user in conversation_users:
            user.delete()
        test_user.delete()

        return result

    # ============================================================================
    # TEST 2: POPULAR QUESTION (500 answers)
    # ============================================================================
    def test_2_popular_question(self):
        """TEST 2: Question with 500 answers"""
        print("\n" + "="*80)
        print("TEST 2: POPULAR QUESTION (500 Answers)")
        print("="*80)

        # Create test question
        test_user = random.choice(self.existing_users)
        test_question = Question.objects.create(
            question_text="extreme test - popular question with 500 answers",
            user=test_user
        )
        self.test_questions.append(test_question)

        print(f"\n📝 Creating 500 answers...")

        # Create 500 answers
        with transaction.atomic():
            for i in range(500):
                user = random.choice(self.existing_users)
                Answer.objects.create(
                    question=test_question,
                    user=user,
                    answer_text=f"Test answer {i} - some detailed content here about the question",
                    created_at=timezone.now() - timedelta(hours=i),
                    upvotes=random.randint(0, 50),
                    downvotes=random.randint(0, 10)
                )

                if (i + 1) % 100 == 0:
                    print(f"   {i + 1}/500 answers created...")

        print(f"✓ 500 answers created for question: {test_question.slug}")

        # Test question_detail performance
        print(f"\n🔍 Testing question_detail view with 500 answers...")

        def run_test():
            client = Client()
            client.force_login(test_user)

            start = time.time()
            response = client.get(f'/{test_question.slug}/')
            duration = (time.time() - start) * 1000

            return {
                'status_code': response.status_code,
                'duration_ms': round(duration, 2),
                'answer_count': 500
            }

        result = self.measure_with_queries("Popular Question (500 answers)", run_test)

        print(f"\n📊 RESULTS:")
        print(f"   Status: {result['result']['status_code']}")
        print(f"   Duration: {result['duration_ms']} ms")
        print(f"   Queries: {result['queries']}")

        if result['duration_ms'] > 2000:
            print(f"   🔴 CRITICAL: Page took > 2 seconds!")
        elif result['duration_ms'] > 1000:
            print(f"   ⚠️  WARNING: Page took > 1 second")
        else:
            print(f"   ✅ GOOD: Acceptable load time")

        # Cleanup
        print(f"\n🧹 Cleaning up test data...")
        Answer.objects.filter(question=test_question).delete()
        test_question.delete()

        return result

    # ============================================================================
    # TEST 3: HEAVY PROFILE (1000 entries)
    # ============================================================================
    def test_3_heavy_profile(self):
        """TEST 3: User profile with 1000 entries"""
        print("\n" + "="*80)
        print("TEST 3: HEAVY PROFILE (1000 Entries)")
        print("="*80)

        # Create test user
        test_user = User.objects.create_user(
            username="heavy_profile_user",
            email="heavyprofile@test.com",
            password="test12345"
        )
        self.test_users.append(test_user)

        print(f"\n📝 Creating 1000 answers across multiple questions...")

        # Create 1000 answers across existing questions
        with transaction.atomic():
            for i in range(1000):
                question = random.choice(self.existing_questions)
                Answer.objects.create(
                    question=question,
                    user=test_user,
                    answer_text=f"Test entry {i} - detailed answer content here",
                    created_at=timezone.now() - timedelta(hours=i),
                    upvotes=random.randint(0, 20),
                    downvotes=random.randint(0, 5)
                )

                if (i + 1) % 250 == 0:
                    print(f"   {i + 1}/1000 answers created...")

        print(f"✓ 1000 answers created for user: {test_user.username}")

        # Test profile page performance
        print(f"\n🔍 Testing profile view with 1000 entries...")

        def run_test():
            client = Client()
            client.force_login(test_user)

            start = time.time()
            response = client.get(f'/profile/{test_user.username}/')
            duration = (time.time() - start) * 1000

            return {
                'status_code': response.status_code,
                'duration_ms': round(duration, 2),
                'entry_count': 1000
            }

        result = self.measure_with_queries("Heavy Profile (1000 entries)", run_test)

        print(f"\n📊 RESULTS:")
        print(f"   Status: {result['result']['status_code']}")
        print(f"   Duration: {result['duration_ms']} ms")
        print(f"   Queries: {result['queries']}")

        if result['duration_ms'] > 2000:
            print(f"   🔴 CRITICAL: Page took > 2 seconds!")
        elif result['duration_ms'] > 1000:
            print(f"   ⚠️  WARNING: Page took > 1 second")
        else:
            print(f"   ✅ GOOD: Acceptable load time")

        # Cleanup
        print(f"\n🧹 Cleaning up test data...")
        Answer.objects.filter(user=test_user).delete()
        test_user.delete()

        return result

    # ============================================================================
    # TEST 4: SEARCH PERFORMANCE
    # ============================================================================
    def test_4_search_performance(self):
        """TEST 4: Search through thousands of entries"""
        print("\n" + "="*80)
        print("TEST 4: SEARCH PERFORMANCE (Searching Through All Data)")
        print("="*80)

        test_user = random.choice(self.existing_users)

        # Count current data
        total_questions = Question.objects.count()
        total_answers = Answer.objects.count()

        print(f"\n📊 Current database size:")
        print(f"   Questions: {total_questions}")
        print(f"   Answers: {total_answers}")

        # Test different search scenarios
        search_tests = [
            ("felsefe", "Common word search"),
            ("modern", "Medium frequency search"),
            ("xyz123", "No results search"),
        ]

        search_results = []

        for search_term, description in search_tests:
            print(f"\n🔍 Testing: {description} ('{search_term}')...")

            def run_test():
                client = Client()
                client.force_login(test_user)

                start = time.time()
                response = client.get(f'/?q={search_term}')
                duration = (time.time() - start) * 1000

                return {
                    'status_code': response.status_code,
                    'duration_ms': round(duration, 2),
                    'search_term': search_term
                }

            result = self.measure_with_queries(f"Search: {description}", run_test)

            print(f"   Duration: {result['duration_ms']} ms")
            print(f"   Queries: {result['queries']}")

            if result['duration_ms'] > 1000:
                print(f"   🔴 SLOW: > 1 second")
            elif result['duration_ms'] > 500:
                print(f"   ⚠️  MODERATE: > 500ms")
            else:
                print(f"   ✅ FAST: < 500ms")

            search_results.append(result)

        return search_results

    # ============================================================================
    # TEST 5: CONCURRENT WRITES
    # ============================================================================
    def test_5_concurrent_writes(self):
        """TEST 5: 10 users writing simultaneously"""
        print("\n" + "="*80)
        print("TEST 5: CONCURRENT WRITES (10 Users Writing Simultaneously)")
        print("="*80)

        # Create 10 test users
        print(f"\n📝 Creating 10 test users...")
        concurrent_users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f"concurrent_user_{i}",
                email=f"concurrent_{i}@test.com",
                password="test12345"
            )
            concurrent_users.append(user)
        self.test_users.extend(concurrent_users)

        # Create test question
        test_question = random.choice(self.existing_questions)

        print(f"✓ 10 users created")
        print(f"✓ Target question: {test_question.question_text}")

        def write_answer(user, answer_num):
            """Single user writing an answer"""
            try:
                client = Client()
                client.force_login(user)

                start = time.time()
                response = client.post(f'/{test_question.slug}/add_answer/', {
                    'answer_text': f'Concurrent test answer {answer_num} from {user.username}'
                })
                duration = (time.time() - start) * 1000

                return {
                    'success': True,
                    'user': user.username,
                    'duration_ms': round(duration, 2),
                    'status_code': response.status_code
                }
            except Exception as e:
                return {
                    'success': False,
                    'user': user.username,
                    'error': str(e)
                }

        print(f"\n🔄 Testing 10 concurrent writes...")

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(write_answer, user, i)
                for i, user in enumerate(concurrent_users)
            ]

            results = []
            for future in as_completed(futures):
                results.append(future.result())

        total_time = (time.time() - start_time) * 1000

        # Analyze results
        print(f"\n📊 RESULTS:")
        print(f"   Total time: {total_time:.2f} ms")
        print(f"   Average per write: {total_time/10:.2f} ms")

        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        print(f"\n   Successful: {len(successful)}/10")
        print(f"   Failed: {len(failed)}/10")

        if failed:
            print(f"\n   ❌ FAILURES:")
            for fail in failed:
                print(f"      {fail['user']}: {fail['error']}")

        if len(successful) == 10 and total_time < 2000:
            print(f"\n   ✅ EXCELLENT: All writes succeeded, no database locking issues!")
        elif len(successful) == 10:
            print(f"\n   ⚠️  ALL SUCCEEDED: But took longer than expected")
        else:
            print(f"\n   🔴 PROBLEM: Some writes failed - possible database locking issues")

        # Cleanup
        print(f"\n🧹 Cleaning up test data...")
        Answer.objects.filter(question=test_question, user__in=concurrent_users).delete()
        for user in concurrent_users:
            user.delete()

        return {
            'total_time_ms': round(total_time, 2),
            'successful': len(successful),
            'failed': len(failed),
            'results': results
        }

    def print_final_report(self):
        """Print comprehensive final report"""
        print("\n" + "="*80)
        print("EXTREME SCENARIO TEST - FINAL REPORT")
        print("="*80)

        if not self.results:
            print("\nNo results to report!")
            return

        print("\n📊 ALL TEST RESULTS:\n")

        for result in self.results:
            print(f"• {result['name']}")
            print(f"  Duration: {result['duration_ms']} ms")
            print(f"  Queries: {result['queries']}")

            # Risk assessment
            if result['duration_ms'] > 2000:
                print(f"  Status: 🔴 CRITICAL - Needs optimization!")
            elif result['duration_ms'] > 1000:
                print(f"  Status: ⚠️  WARNING - Should be optimized")
            elif result['duration_ms'] > 500:
                print(f"  Status: 🟡 MODERATE - Acceptable but could improve")
            else:
                print(f"  Status: ✅ EXCELLENT - Great performance!")
            print()

        # Summary stats
        durations = [r['duration_ms'] for r in self.results]
        queries = [r['queries'] for r in self.results]

        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        print(f"\nResponse Times:")
        print(f"  Fastest: {min(durations):.2f} ms")
        print(f"  Slowest: {max(durations):.2f} ms")
        print(f"  Average: {sum(durations)/len(durations):.2f} ms")

        print(f"\nDatabase Queries:")
        print(f"  Min: {min(queries)}")
        print(f"  Max: {max(queries)}")
        print(f"  Average: {sum(queries)/len(queries):.1f}")

        # Final recommendation
        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)

        critical = [r for r in self.results if r['duration_ms'] > 2000]
        warning = [r for r in self.results if 1000 < r['duration_ms'] <= 2000]

        if critical:
            print("\n🔴 CRITICAL ISSUES (> 2 seconds):")
            for r in critical:
                print(f"   • {r['name']}: {r['duration_ms']} ms")

        if warning:
            print("\n⚠️  NEEDS OPTIMIZATION (> 1 second):")
            for r in warning:
                print(f"   • {r['name']}: {r['duration_ms']} ms")

        if not critical and not warning:
            print("\n✅ EXCELLENT! No critical performance issues detected!")
            print("   All scenarios performed within acceptable limits.")

        print("\n" + "="*80 + "\n")


def main():
    """Main test runner"""
    print("\n" + "="*80)
    print("EXTREME SCENARIO TESTS")
    print("="*80)
    print("\nThis will test 5 extreme scenarios:")
    print("  1. Heavy message user (200 conversations)")
    print("  2. Popular question (500 answers)")
    print("  3. Heavy profile (1000 entries)")
    print("  4. Search performance (across all data)")
    print("  5. Concurrent writes (10 simultaneous users)")
    print("\n⚠️  WARNING: This test will:")
    print("   - Create temporary test data")
    print("   - Take 5-10 minutes to complete")
    print("   - Clean up after itself")

    # Auto-proceed for automated testing
    print("\n[Auto-proceeding with tests...]")

    tester = ExtremeScenarioTester()

    try:
        tester.setup()

        print("\n" + "="*80)
        print("RUNNING EXTREME SCENARIO TESTS")
        print("="*80)

        # Run all 5 tests
        tester.test_1_heavy_message_user()
        tester.test_2_popular_question()
        tester.test_3_heavy_profile()
        tester.test_4_search_performance()
        tester.test_5_concurrent_writes()

        # Final report
        tester.print_final_report()

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
