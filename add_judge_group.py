import pandas as pd
from django.contrib.auth.models import Group
from signup.models import User

EXCEL_PATH = "/Users/xavier/Desktop/UWMSRPC/SRPCjudges.xlsx"

df = pd.read_excel(EXCEL_PATH).fillna("")

if "email" not in df.columns:
    raise ValueError("Excel must contain an 'email' column.")

judge_group, _ = Group.objects.get_or_create(name="Judge")

added = 0
missing = 0

for _, row in df.iterrows():
    email = str(row.get("email", "")).strip().lower()
    if not email:
        continue

    try:
        user = User.objects.get(email__iexact=email)
        user.groups.add(judge_group)
        added += 1
        print(f"ADDED: {email} -> Judge")
    except User.DoesNotExist:
        missing += 1
        print(f"MISSING: {email} not found in User table")

print(f"\nDone. Added: {added}, Missing: {missing}")


#python manage.py shell < add_judge_group.py