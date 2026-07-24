# from-j-to-q — local-first verification (CI calls these same targets)

J       ?= jconsole
Q       ?= q
LESSONS := $(wildcard lessons/*)

.PHONY: verify verify-j verify-q verify-showcase

verify: verify-j verify-q verify-showcase

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
