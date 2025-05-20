import os
import json
import re

OUTPUT_DIR = "raw_content_date"
MERGED_FILENAME = "merged_posts.json"

BATCH_PATTERN = re.compile(r"batch_(\d+)_posts\.json")

def merge_json_files(output_dir, merged_filename):
    batch_files = []
    for filename in os.listdir(output_dir):
        match = BATCH_PATTERN.match(filename)
        if match:
            batch_num = int(match.group(1))
            batch_files.append((batch_num, filename))
    batch_files.sort()
    all_posts = []
    for _, filename in batch_files:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                posts = json.load(f)
                if isinstance(posts, list):
                    all_posts.extend(posts)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    merged_path = os.path.join(output_dir, merged_filename)
    with open(merged_path, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)
    print(f"Merged {len(all_posts)} posts into {merged_path}")

if __name__ == "__main__":
    merge_json_files(OUTPUT_DIR, MERGED_FILENAME)