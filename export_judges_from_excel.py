import pandas as pd

EXCEL_PATH = "/Users/xavier/Desktop/UWMSRPC/2026_Poster_Competition_Judge_List_for_SCORING.xlsx"
OUTPUT_CSV = "/Users/xavier/Desktop/UWMSRPC/judge_emails.csv"
EMAIL_COLUMN = "email"

df = pd.read_excel(EXCEL_PATH).fillna("")

if EMAIL_COLUMN not in df.columns:
    raise ValueError(f"Column '{EMAIL_COLUMN}' not found. Columns: {list(df.columns)}")

out = df[[EMAIL_COLUMN]].copy()
out[EMAIL_COLUMN] = out[EMAIL_COLUMN].astype(str).str.strip().str.lower()
out = out[out[EMAIL_COLUMN] != ""].drop_duplicates()

out.to_csv(OUTPUT_CSV, index=False)
print(f"Wrote {len(out)} emails to {OUTPUT_CSV}")