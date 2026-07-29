# from-j-to-q — local-first verification (CI calls these same targets)

J       ?= jconsole
Q       ?= q
LESSONS := $(wildcard lessons/*)

.PHONY: verify verify-j verify-q verify-showcase verify-eval verify-eval-run verify-prose

verify: verify-j verify-q verify-showcase verify-eval verify-eval-run verify-prose

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
		$(Q) $$f -q < /dev/null > /tmp/eval-actual.txt 2> /tmp/eval-err.txt || { cat /tmp/eval-err.txt; exit 1; }; \
		if [ -s /tmp/eval-err.txt ]; then echo "   q wrote to stderr (error masked by exit 0):"; cat /tmp/eval-err.txt; exit 1; fi; \
		diff -u $$exp /tmp/eval-actual.txt || exit 1; \
	done
	@echo "eval refs: OK"

# The M2 run's published numbers, re-derived from committed artifacts. Without
# this, results.csv and runs/traces.md are just prose that happened to be true
# on the day — the exact failure mode docs/COMPOUND.md keeps recording.
verify-eval-run:
	@echo "== eval run: results.csv correctness column vs. the committed answers =="
	@Q=$(Q) eval/harness/correctness.sh > /tmp/eval-run.txt 2>&1 \
		|| { cat /tmp/eval-run.txt; exit 1; }
	@tail -1 /tmp/eval-run.txt
	@echo "== eval run: runs/traces.md vs. the committed session logs =="
	@python3 eval/harness/mktraces.py eval/runs/logs --check eval/runs/traces.md

# The other verify- targets prove the lesson SOURCES run. None of them look at
# the outputs pasted into each lesson's narrative, which is exactly where the
# "captured from the real tools, never hand-typed" claim lives — and where a
# violation already shipped once (lesson 02's invented `q)` prompts).
# Two checks, because lessons state outputs in two different ways. Unlabelled
# fenced BLOCKS must appear in a fresh capture, in execution order. Trailing
# `/ 2f` comments inside ```q blocks are re-EVALUATED against the lesson's own
# q source and must equal what they claim — membership in the capture is not
# enough, since a wrong claim can collide with a real value elsewhere in the
# same lesson. Lesson 01 is written almost entirely in the comment style, so
# without the second check it would be nearly uncovered.
verify-prose:
	@echo "== lesson READMEs: pasted outputs vs. a fresh capture =="
	@Q=$(Q) J=$(J) python3 tools/check-lesson-outputs.py
