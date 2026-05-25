package deploy

critical_count := object.get(input.summary, "CRITICAL", 0)
high_count := object.get(input.summary, "HIGH", 0)
unknown_count := object.get(input.summary, "UNKNOWN", 0)
environment := object.get(input, "environment", "dev")

decision := {
  "result": "BLOCK",
  "reason": sprintf("prod environment: CRITICAL vulnerabilities found: %d", [critical_count])
} if {
  environment == "prod"
  critical_count >= 1
} else := {
  "result": "HOLD",
  "reason": sprintf("prod environment: HIGH vulnerabilities are 3 or more: %d", [high_count])
} if {
  environment == "prod"
  high_count >= 3
} else := {
  "result": "HOLD",
  "reason": sprintf("prod environment: UNKNOWN vulnerabilities are 5 or more: %d", [unknown_count])
} if {
  environment == "prod"
  unknown_count >= 5
} else := {
  "result": "BLOCK",
  "reason": sprintf("staging environment: CRITICAL vulnerabilities are 3 or more: %d", [critical_count])
} if {
  environment == "staging"
  critical_count >= 3
} else := {
  "result": "HOLD",
  "reason": sprintf("staging environment: CRITICAL vulnerabilities found: %d", [critical_count])
} if {
  environment == "staging"
  critical_count >= 1
} else := {
  "result": "HOLD",
  "reason": sprintf("staging environment: HIGH vulnerabilities are 5 or more: %d", [high_count])
} if {
  environment == "staging"
  high_count >= 5
} else := {
  "result": "BLOCK",
  "reason": sprintf("dev environment: CRITICAL vulnerabilities are 5 or more: %d", [critical_count])
} if {
  environment == "dev"
  critical_count >= 5
} else := {
  "result": "HOLD",
  "reason": sprintf("dev environment: HIGH vulnerabilities are 10 or more: %d", [high_count])
} if {
  environment == "dev"
  high_count >= 10
} else := {
  "result": "ALLOW",
  "reason": sprintf("Allowed by %s policy", [environment])
}