import json

results_dir = [
    # "submission/submission_1.json", # First one will get priority if multiple have score 1.0
    "submission/submission_2.json",
    "submission/submission_3.json",
]

data = []

for dir in results_dir:
    with open(dir, "r", encoding="utf-8") as f:
        data.append(json.load(f))

correct = 0
total = 0
score = 0

count = 1

submission = []
for i in range(len(data[0])):
    
    for j in range(len(results_dir)):
        if data[j][i]["score"] == 1.0:
            correct += 1
            break

    score += max(data[j][i]["score"] for j in range(len(results_dir)))
    total += 1
    count += 1
    # Find all indices with score 1.0
    ones = [j for j in range(len(results_dir)) if data[j][i]["score"] == 1.0]
    if ones:
        # Pick the one with the largest response (string comparison)
        best_idx = max(ones, key=lambda j: data[j][i]["response"])
    else:
        # Fall back to the highest score
        best_idx = max(range(len(results_dir)), key=lambda j: data[j][i]["score"])
    submission.append({
        "id": data[0][i]["id"],
        "response": data[best_idx][i]["response"],
        "score": data[best_idx][i]["score"],
    })

print(f"Accuracy: {correct}/{total} = {correct/total:.2%}")
print(f"Average Score: {score/total:.2%}")

with open("submission.json", "w", encoding="utf-8") as f:
    json.dump(submission, f, ensure_ascii=False, indent=4)

# zip the submission.json to submission.zip
import zipfile
with zipfile.ZipFile("submission.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("submission.json")

