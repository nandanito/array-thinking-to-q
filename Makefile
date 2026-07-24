# from-j-to-q — local-first verification (CI calls these same targets)

J       ?= jconsole
Q       ?= q
LESSONS := $(wildcard lessons/*)

.PHONY: verify verify-j verify-q verify-showcase verify-eval

verify: verify-j verify-q verify-showcase verify-eval

verify-j:
	@echo "== J examples =="
	@for f in $$(find lessons -name '*.ijs' | sort); do \
		echo "-- $$f"; $(J) < $$f || exit 1; \
	done

verify-q:
	@echo "== q examples (requires KDB-X CE license; see docs/toolchain.md) =="
	@for f in $$(find lessons -name '*.q' | sort); do \
		echo "-- $$f"; $(Q) $$f -q < /dev/null || exit 1; \
	done

verify-showcase:
	@echo "== showcase: as-of join golden file =="
	@$(Q) showcase/aj/aj.q -q < /dev/null > /tmp/aj-actual.txt || exit 1
	@diff -u showcase/aj/expected.txt /tmp/aj-actual.txt && echo "aj: OK"

# eval verify-harness: every task reference solution runs and matches its golden.
# This is the self-test that keeps the measurement instrument honest; the same
# golden diff scores a candidate solution during the eval (see eval/README.md).
verify-eval:
	@echo "== eval reference solutions (golden diff) =="
	@for f in $$(find eval/tasks/q -name '*.ref.q' | sort); do \
		exp=$${f%.ref.q}.expected; \
		echo "-- $$f"; \
		$(Q) $$f -q < /dev/null > /tmp/eval-actual.txt || exit 1; \
		diff -u $$exp /tmp/eval-actual.txt || exit 1; \
	done
	@echo "eval refs: OK"
