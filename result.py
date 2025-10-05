import json


with open("C:/Users/Hp/Downloads/dihan_submit_6/submission.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
    
correct = 0
total = 0
score = 0

count = 1
for item in data:
    if item["score"] == 1.0:
        correct += 1
    # else:
    #     print(item["id"])
    score += item["score"]
    total += 1
    if not item["id"] == count:
        print(f"ID mismatch: expected {count}, got {item['id']}")
        break
    # if total == 341:
    #     break
    count += 1
    

print(f"Accuracy: {correct}/{total} = {correct/total:.2%}")
print(f"Average Score: {score/total:.2%}")