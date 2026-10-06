from langchain_core.messages import HumanMessage

from agent.hr_agent import build_hr_agent


agent = build_hr_agent()


# ============================================================
# Test 1 - Leave Balance
# ============================================================

print("\n")
print("=" * 70)
print("TEST 1 - LEAVE BALANCE")
print("=" * 70)

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "How many casual leaves do I have?"
                )
            )
        ],
        "employee_id": "EMP1001"
    }
)

print(
    result["messages"][-1].content
)


# ============================================================
# Test 2 - Employee Profile
# ============================================================

print("\n")
print("=" * 70)
print("TEST 2 - EMPLOYEE PROFILE")
print("=" * 70)

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "What is my designation?"
                )
            )
        ],
        "employee_id": "EMP1001"
    }
)

print(
    result["messages"][-1].content
)


# ============================================================
# Test 3 - Policy
# ============================================================

print("\n")
print("=" * 70)
print("TEST 3 - HR POLICY")
print("=" * 70)

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "How many casual leaves are employees "
                    "eligible for?"
                )
            )
        ],
        "employee_id": "EMP1001"
    }
)

print(
    result["messages"][-1].content
)


# ============================================================
# Test 4 - Leave Eligibility
# ============================================================

print("\n")
print("=" * 70)
print("TEST 4 - LEAVE ELIGIBILITY")
print("=" * 70)

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Can I take 5 days of casual leave "
                    "from October 5 to October 9?"
                )
            )
        ],
        "employee_id": "EMP1001"
    }
)

print(
    result["messages"][-1].content
)