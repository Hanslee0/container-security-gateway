package deploy

default decision := {
  "result": "ALLOW",
  "reason": "No blocking vulnerabilities found"
}

decision := {
  "result": "BLOCK",
  "reason": sprintf("Critical vulnerabilities found: %d", [input.summary.CRITICAL])
} if {
  input.summary.CRITICAL > 0
}

decision := {
  "result": "HOLD",
  "reason": sprintf("High vulnerabilities are 3 or more: %d", [input.summary.HIGH])
} if {
  input.summary.CRITICAL == 0
  input.summary.HIGH >= 3
}
