import os

base_dir = os.path.dirname(__file__)

# Raw files (same folder)
file1 = os.path.join(base_dir, "courses.txt")
file2 = os.path.join(base_dir, "extra_docs.txt")

# Final dataset → ROOT folder
output_file = os.path.abspath(os.path.join(base_dir, "..", "..", "final_dataset.txt"))

with open(output_file, "w", encoding="utf-8") as outfile:
    for fname in [file1, file2]:
        if not os.path.exists(fname):
            print(f"❌ Missing: {fname}")
            continue

        print(f"📂 Adding: {fname}")

        with open(fname, "r", encoding="utf-8") as infile:
            content = infile.read().strip()

            if content:
                outfile.write(content)
                outfile.write("\n\n")
            else:
                print(f"⚠️ Empty file: {fname}")

print("✅ Final dataset created at:", output_file)