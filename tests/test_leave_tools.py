from tools.leave_tools import (
    calculate_working_days,
    calculate_leave_days,
    check_leave_balance,
    calculate_prorated_leave,
    get_leave_allocation,
    calculate_leave_eligibility
)


# ============================================================
# Working Days
# ============================================================

print("\n")
print("=" * 60)
print("WORKING DAYS")
print("=" * 60)

result = calculate_working_days(
    "2026-10-05",
    "2026-10-09"
)

print(result)


# ============================================================
# Leave Days
# ============================================================

print("\n")
print("=" * 60)
print("LEAVE DAYS")
print("=" * 60)

result = calculate_leave_days(
    "2026-10-05",
    "2026-10-09"
)

print(result)


# ============================================================
# Leave Balance
# ============================================================

print("\n")
print("=" * 60)
print("LEAVE BALANCE CHECK")
print("=" * 60)

result = check_leave_balance(
    "EMP1001",
    "Casual Leave",
    3
)

print(result)


# ============================================================
# Prorated Leave
# ============================================================

print("\n")
print("=" * 60)
print("PRORATED LEAVE")
print("=" * 60)

result = calculate_prorated_leave(
    "2026-07-10",
    24,
    2026
)

print(result)


# ============================================================
# Leave Allocation
# ============================================================

print("\n")
print("=" * 60)
print("LEAVE ALLOCATION")
print("=" * 60)

result = get_leave_allocation(
    "Earned Leave"
)

print(result)


# ============================================================
# Complete Eligibility
# ============================================================

print("\n")
print("=" * 60)
print("LEAVE ELIGIBILITY")
print("=" * 60)

result = calculate_leave_eligibility(
    employee_id="EMP1001",
    leave_type="Casual Leave",
    start_date="2026-10-05",
    end_date="2026-10-09"
)

print(result)