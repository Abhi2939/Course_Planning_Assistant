from src.pipeline.rag_pipeline import ask
from evaluation.test_queries import test_queries

total = len(test_queries)
citation_count = 0
abstain_correct = 0
prereq_correct = 0

results = []

for q in test_queries:
    print("\n==============================")
    print("Query:", q["query"])

    response = ask(q["query"])
    print("Response:", response)

    # ✅ Check citation presence
    if "CS" in response or "Citations" in response:
        citation_count += 1

    # ✅ Check abstention
    if q["type"] == "unknown":
        if "don't have that information" in response.lower():
            abstain_correct += 1

    # ✅ Check prerequisite correctness (simple heuristic)
    if q["type"] == "prereq":
        if "prerequisite" in response.lower() or "required" in response.lower():
            prereq_correct += 1

    results.append({
        "query": q["query"],
        "response": response
    })


print("\n\n========== EVALUATION ==========")

print(f"Total Queries: {total}")
print(f"Citation Coverage: {citation_count/total:.2f}")
print(f"Abstention Accuracy: {abstain_correct/5:.2f}")
print(f"Prerequisite Accuracy: {prereq_correct/10:.2f}")