from django.core.management.base import BaseCommand
from accounts.models import Skill

class Command(BaseCommand):
    help = 'Adds predefined skills to the database'

    def handle(self, *args, **options):
        # Define skills to add
        skills_to_add = [
            "Python",
            "Django",
            "JavaScript",
            "React",
            "HTML/CSS",
            "Data Science",
            "Machine Learning",
            "UI/UX Design",
            "Mobile Development",
            "DevOps"
        ]

        # Add skills to the database
        for skill_name in skills_to_add:
            # Check if skill already exists
            if not Skill.objects.filter(name=skill_name).exists():
                Skill.objects.create(name=skill_name)
                self.stdout.write(self.style.SUCCESS(f"Added skill: {skill_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skill already exists: {skill_name}"))

        self.stdout.write(self.style.SUCCESS("Skills have been added to the database!"))
