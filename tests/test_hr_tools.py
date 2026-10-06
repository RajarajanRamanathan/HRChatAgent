from tools.hr_tools import (
    get_employee_profile,
    get_leave_balance,
    get_leave_history,
    get_holidays,
    get_employee_summary
)


# ============================================================
# Test Employee Profile
# ============================================================

print("\n")
print("=" * 60)
print("EMPLOYEE PROFILE")
print("=" * 60)

result = get_employee_profile(
    "EMP1001"
)

print(result)


# ============================================================
# Test Leave Balance
# ============================================================

print("\n")
print("=" * 60)
print("LEAVE BALANCE")
print("=" * 60)

result = get_leave_balance(
    "EMP1001"
)

print(result)


# ============================================================
# Test Specific Leave Type
# ============================================================

print("\n")
print("=" * 60)
print("CASUAL LEAVE")
print("=" * 60)

result = get_leave_balance(
    "EMP1001",
    "Casual Leave"
)

print(result)


# ============================================================
# Test Leave History
# ============================================================

print("\n")
print("=" * 60)
print("LEAVE HISTORY")
print("=" * 60)

result = get_leave_history(
    "EMP1001"
)

print(result)


# ============================================================
# Test Holidays
# ============================================================

print("\n")
print("=" * 60)
print("HOLIDAYS")
print("=" * 60)

result = get_holidays(
    2026
)

print(result)


# ============================================================
# Test Employee Summary
# ============================================================

print("\n")
print("=" * 60)
print("EMPLOYEE SUMMARY")
print("=" * 60)

result = get_employee_summary(
    "EMP1001"
)

print(result)