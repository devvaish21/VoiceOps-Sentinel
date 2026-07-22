from pii_redactor import redact_pii
# Performs a privacy audit by testing the redact_pii function containing PII test cases.
print("=== PRIVACY AUDIT - 10 PII TEST CASES ===\n")
# Define test cases
test_cases = [
    "Customer name is John Smith",
    "Phone number is 9876543210",
    "Email: customer@gmail.com",
    "Credit card: 4111 1111 1111 1111",
    "Address: 123 Main Street New York",
    "My name is Priya and I need help",
    "Call me at +1-800-555-0199",
    "Send invoice to sarah@outlook.com",
    "Card number 5500 0000 0000 0004",
    "Contact John at john@company.com or 9988776655"
]

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    redacted = redact_pii(test)
    
    # Check if any PII still exists
    is_redacted = (
        redacted != test and
        '<' in redacted
    )
    
    status = "✅ PASS" if is_redacted else "❌ FAIL"
    
    if is_redacted:
        passed += 1
    else:
        failed += 1
    
    print(f"Test {i}: {status}")
    print(f"  INPUT:    {test}")
    print(f"  REDACTED: {redacted}")
    print()

print("=" * 40)
print(f"TOTAL: {passed}/10 PASSED")
print(f"RESULT: {'✅ AUDIT PASSED!' if passed >= 8 else '❌ NEEDS IMPROVEMENT'}")