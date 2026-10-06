from services.policy_service import search_hr_policies


question = "How many casual leaves can an employee take?"

results = search_hr_policies(
    question,
    top_k=3
)

print("\nPolicy Search Results")
print("=" * 60)

for index, result in enumerate(
    results,
    start=1
):

    print(f"\nResult {index}")

    print(
        f"Policy: {result['policy_name']}"
    )

    print(
        f"Type: {result['policy_type']}"
    )

    print(
        f"Page: {result['page_number']}"
    )

    print(
        f"Distance: {result['distance']}"
    )

    print(
        f"Content:\n{result['content']}"
    )