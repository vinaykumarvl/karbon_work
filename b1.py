import os
import sys
import click
import importlib
import pandas as pd
import pdfplumber

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.option("--target", required=True, help="Bank name (e.g., icici, sbi)")
def run_agent(target: str):
    pdf_path = os.path.join(BASE_DIR, "data", target, f"{target}_sample.pdf")
    csv_path = os.path.join(BASE_DIR, "data", target, f"{target}_sample.csv")
    parser_path = os.path.join(BASE_DIR, "custom_parser", f"{target}_parser.py")

    if not os.path.exists(parser_path):
        generate_parser(target, parser_path)

    for attempt in range(3):
        print(f"\n[Agent] Attempt {attempt+1}/3 for {target} parser...")
        try:
            spec = importlib.util.spec_from_file_location(f"{target}_parser", parser_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"{target}_parser"] = module
            spec.loader.exec_module(module)

            df = module.parse(pdf_path)
            expected = pd.read_csv(csv_path)

            if df.equals(expected):
                print("[Agent] ✅ Parser successful and matches CSV.")
                return
            else:
                print("[Agent] ❌ Data mismatch with expected CSV.")
        except Exception as e:
            print(f"[Agent] Error: {e}")

        generate_parser(target, parser_path)

    print("[Agent] ❌ Failed after 3 attempts.")

def generate_parser(target: str, parser_path: str):
    template = '''import pandas as pd
import pdfplumber

def parse(pdf_path: str) -> pd.DataFrame:
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines[1:]:  # skip header
                    parts = line.split()
                    if len(parts) >= 4:
                        date, desc, amount, balance = parts[0], " ".join(parts[1:-2]), parts[-2], parts[-1]
                        data.append([date, desc, amount, balance])
    df = pd.DataFrame(data, columns=["Date", "Description", "Amount", "Balance"])
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    return df
'''
    os.makedirs(os.path.dirname(parser_path), exist_ok=True)
    with open(parser_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"[Agent] Generated parser at {parser_path}")

if __name__ == "__main__":
    run_agent()
