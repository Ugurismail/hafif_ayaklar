import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Reference


class Command(BaseCommand):
    help = 'Import references from references.txt file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the references.txt file'
        )
        parser.add_argument(
            '--user',
            type=str,
            default=None,
            help='Username of the user to assign as creator (default: first superuser)'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        self.stdout.write(self.style.WARNING(f'📖 Reading references from {file_path}...'))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'❌ File not found: {file_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'✅ Found {len(lines)} lines'))

        created_count = 0
        skipped_count = 0
        error_count = 0

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                # Parse APA citation
                # Format: Author, A. I., & Author2, S. (Year). Title and rest...

                # Extract first author surname and initials
                author_match = re.match(r'^([^,]+),\s*([^,&(]+)', line)
                if not author_match:
                    self.stdout.write(self.style.WARNING(f'⚠️  Line {line_num}: Could not parse author'))
                    error_count += 1
                    continue

                author_surname = author_match.group(1).strip()
                author_name = author_match.group(2).strip().rstrip('.,')

                # Extract year
                year_match = re.search(r'\((\d{4}[a-z]?)\)', line)
                year = year_match.group(1) if year_match else None

                # Rest of the citation (everything after first parenthesis with year)
                if year_match:
                    rest = line[year_match.end():].strip().lstrip('.')
                else:
                    # If no year found, take everything after the first author
                    rest = line[author_match.end():].strip()

                # Generate abbreviation
                if year:
                    # Remove any letters from year for abbreviation
                    year_num = re.sub(r'[a-z]', '', year)
                    abbreviation = f"{author_surname.replace(' ', '')}{year_num}"
                else:
                    abbreviation = f"{author_surname.replace(' ', '')}"

                # Check if already exists
                if Reference.objects.filter(abbreviation=abbreviation).exists():
                    self.stdout.write(self.style.WARNING(f'⏭️  Line {line_num}: {abbreviation} already exists, skipping'))
                    skipped_count += 1
                    continue

                # Create reference
                Reference.objects.create(
                    author_surname=author_surname[:200],  # Limit to model max_length
                    author_name=author_name[:200] if author_name else None,
                    year=year[:50] if year else None,
                    rest=rest if rest else None,
                    abbreviation=abbreviation[:50]  # Limit to model max_length
                )

                created_count += 1
                if created_count % 100 == 0:
                    self.stdout.write(self.style.SUCCESS(f'✅ Created {created_count} references...'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Line {line_num}: Error - {str(e)}'))
                error_count += 1
                continue

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Import complete!'))
        self.stdout.write(self.style.SUCCESS(f'✅ Created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'⏭️  Skipped (already exists): {skipped_count}'))
        self.stdout.write(self.style.ERROR(f'❌ Errors: {error_count}'))
