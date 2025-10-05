import json

results_dir = [
    # "C:/Users/Hp/Downloads/dihan_submit_5/submission.json",
    # "C:/Users/Hp/Downloads/dihan_submit_7/submission.json",
    # "C:/Users/Hp/Downloads/dihan_submit_4/submission.json",
    # "C:/Users/Hp/Downloads/dihan_submit_3/submission.json",
    # "C:/Users/Hp/Downloads/submission(6).json",
    # "C:/Users/Hp/Downloads/dihan_submit_8/submission.json",
    "submission/submission_2.json",
        "submission/submission_3.json",
    # "C:/Users/Hp/Downloads/testsubmit_3/submission_1_113.json",
    # "C:/Users/Hp/Downloads/testsubmit_3/submission_381_500.json"
]

data = []

for dir in results_dir:
    with open(dir, "r", encoding="utf-8") as f:
        data.append(json.load(f))

correct = 0
total = 0
tscore = 0

count = 1

submission = []
for i in range(1, 501):
    
    score = 0.0
    best_idx = -1
    best_solution = ""
    for j in range(len(results_dir)):
        for item in data[j]:
            if item["id"] == i:
                if item["score"] == 1.0:
                    if best_idx == -1:
                        best_idx = j
                        best_solution = item["response"]
                    elif len(item["response"]) > len(best_solution):
                        best_idx = j
                        best_solution = item["response"]
                score = max(score, item["score"])
                
        if score == 1.0:
            correct += 1
            break
        

    total += 1
    count += 1
    tscore += score

    submission.append({
        "id": i,
        "response": best_solution,
        "score": score,
    })

print(f"Accuracy: {correct}/{total} = {correct/total:.2%}")
print(f"Average Score: {tscore/total:.2%}")

with open("submission.json", "w", encoding="utf-8") as f:
    json.dump(submission, f, ensure_ascii=False, indent=4)

# zip the submission.json to submission.zip
import zipfile
with zipfile.ZipFile("submission.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("submission.json")

