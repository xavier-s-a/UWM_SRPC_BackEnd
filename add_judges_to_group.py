import csv
from django.contrib.auth.models import Group
from signup.models import User

CSV_PATH = "/home/ubuntu/SRPC-2026/UWM_Event_Backend/judge_emails.csv"
EMAIL_COLUMN = "email"

judge_group, _ = Group.objects.get_or_create(name="Judge")

added = 0
missing = 0

with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = str(row.get(EMAIL_COLUMN, "")).strip().lower()
        if not email:
            continue
        try:
            user = User.objects.get(email__iexact=email)
            user.groups.add(judge_group)
            added += 1
            print(f"ADDED: {email}")
        except User.DoesNotExist:
            missing += 1
            print(f"MISSING: {email}")

print(f"Done. Added={added}, Missing={missing}")