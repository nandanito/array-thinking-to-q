#!/usr/bin/env python3
"""selftest.py: prove the harness's gates pass what they should and fail what they should.

Runs without q, without a model and without spending a session, so CI runs it
on every PR (`make verify-harness`). Each gate is exercised in both directions:
a check that has only ever been seen passing has not been shown to check
anything. Synthetic logs and tasks live in a temp dir that is removed at exit.
"""
import copy, json, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
EVAL = HERE.parent
failures = []


def run(*cmd, env=None):
    import os
    e = dict(os.environ, **(env or {}))
    p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, env=e)
    return p.returncode, p.stdout + p.stderr


def expect(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)
        if detail:
            print("     " + detail.strip().replace("\n", "\n     ")[:1500])


tmp = pathlib.Path(tempfile.mkdtemp(prefix="atq-selftest."))
try:
    # ---- audit.py on synthetic logs ------------------------------------
    def init(cond, n, **over):
        d = {"type": "system", "subtype": "init", "cwd": f"/tmp/atq-neutral.{n}",
             "tools": ["Glob", "Read", "Skill"], "mcp_servers": [],
             "model": "m", "permissionMode": "default", "claude_code_version": "1",
             "output_style": "default", "agents": ["general-purpose"],
             "skills": ["builtin"] + (["demo:x"] if cond == "B" else []),
             # A built-in plugin in every session is context, not treatment
             # (Claude Code 2.1.284 loads two); --plugin-dir's plugin is `@inline`.
             "plugins": ([{"name": "demo", "path": "/p", "source": "demo@inline"}]
                         if cond == "B" else [])
                        + [{"name": "telemetry", "path": "builtin", "source": "telemetry@builtin"}],
             "memory_paths": {"auto": f"/h/.claude/projects/-tmp-atq-neutral-{n}/memory/"}}
        d.update(over)
        return d

    def write_run(d, sessions, order):
        d.mkdir(parents=True)
        for i, (name, ini) in enumerate(sessions):
            ts = f"2026-01-01T00:00:{i:02d}Z"
            lines = [ini,
                     {"type": "assistant", "timestamp": ts, "message": {"content": [
                         {"type": "tool_use", "name": "Skill", "input": {"skill": "demo:x"}}]}},
                     {"type": "result", "result": "print(1)", "usage": {"output_tokens": 5},
                      "total_cost_usd": 0.01}]
            (d / name).write_text("\n".join(json.dumps(x) for x in lines) + "\n")
        (d / "order.tsv").write_text("# seed=1 conditions=AB prompts=p\n" + "".join(
            f"{i}\t{t}\t{c}\n" for i, (t, c) in enumerate(order, 1)))

    order = [("t1", "B"), ("t1", "A"), ("t2", "A"), ("t2", "B")]
    clean = [(f"{t}.{c}.jsonl", init(c, f"{t}{c}")) for t, c in order]

    def audit(sessions, order_=order, label="run"):
        d = tmp / label
        write_run(d, sessions, order_)
        return run(sys.executable, HERE / "audit.py", d, "--order", d / "order.tsv")

    rc, out = audit(clean, label="clean")
    expect("audit passes a clean interleaved run", rc == 0, out)

    leak = copy.deepcopy(clean)
    leak[3][1]["tools"] = leak[3][1]["tools"] + ["mcp__claude_ai_Google_Drive__search_files"]
    rc, out = audit(leak, label="leak")
    expect("audit fails a session with an extra tool", rc == 1 and "tools differs" in out, out)

    conn = copy.deepcopy(clean)
    for _, ini in conn:
        ini["mcp_servers"] = [{"name": "claude.ai Gmail", "status": "pending"}]
    rc, out = audit(conn, label="conn")
    expect("audit fails a connector even when every session has it",
           rc == 1 and "account connectors" in out, out)

    shared = copy.deepcopy(clean)
    for _, ini in shared:
        ini["cwd"] = "/tmp/one-dir"
    rc, out = audit(shared, label="shared")
    expect("audit fails a shared neutral directory", rc == 1 and "cwd shared" in out, out)

    rc, out = audit(clean, order_=[("t1", "A"), ("t1", "B"), ("t2", "A"), ("t2", "B")],
                    label="order")
    expect("audit fails a run that did not follow order.tsv",
           rc == 1 and "did not run in the order" in out, out)

    builtin_b = copy.deepcopy(clean)
    builtin_b[0][1]["plugins"].append({"name": "extra", "path": "builtin", "source": "extra@builtin"})
    rc, out = audit(builtin_b, label="builtin")
    expect("audit fails a built-in plugin present in one session only",
           rc == 1 and "other plugins differs" in out, out)

    contam = copy.deepcopy(clean)
    contam[1][1]["plugins"].append({"name": "demo", "path": "/p", "source": "demo@inline"})
    rc, out = audit(contam, label="contam")
    expect("audit fails a condition-A session that loaded the plugin",
           rc == 1 and "expected []" in out, out)

    # The committed M2 logs predate these gates and must fail them, naming the
    # three condition-B sessions the connector reached.
    rc, out = run(sys.executable, HERE / "audit.py", EVAL / "runs/logs/partB")
    expect("audit fails the M2 logs on the connector leak and the shared directory",
           rc == 1 and all(f"{t}.B.jsonl" in out.split("tools differs")[1].split("\n")[0]
                           for t in ("03-word-frequency", "04-square-evens", "06-mean-no-avg"))
           and "cwd shared" in out, out)

    # ---- schedule.py ------------------------------------------------------
    prompts = tmp / "prompts"
    rc, out = run(sys.executable, HERE / "mkprompts.py", EVAL / "tasks/q", prompts)
    rc2, _ = run("diff", "-r", EVAL / "runs/prompts/B", prompts)
    expect("mkprompts regenerates the committed M2 prompts byte for byte", rc == 0 and rc2 == 0, out)

    def sched(seed, out_dir):
        rc, out = run(sys.executable, HERE / "schedule.py", "--prompts", prompts,
                      "--out", out_dir, "--seed", seed, "--dry-run")
        rows = [ln.split("\t") for ln in (out_dir / "order.tsv").read_text().splitlines()
                if not ln.startswith("#")] if rc == 0 else []
        return rc, out, rows

    rc, out, rows = sched(7, tmp / "s1")
    _, _, again = sched(7, tmp / "s2")
    pairs = [(rows[i][1], rows[i + 1][1]) for i in range(0, len(rows), 2)]
    firsts = [rows[i][2] for i in range(0, len(rows), 2)]
    expect("schedule: each task once per condition, pairs adjacent, A-first in 7 or 8 of 15, seed-stable",
           rc == 0 and len(rows) == 30 and all(a == b for a, b in pairs)
           and sorted([firsts.count("A"), firsts.count("B")]) == [7, 8] and rows == again, out)
    rc, out = run(sys.executable, HERE / "schedule.py", "--prompts", prompts,
                  "--out", tmp / "s1", "--seed", "7", "--dry-run")
    expect("schedule refuses to overwrite an existing run", rc != 0, out)

    # ---- correctness.sh on a tiny Python task set ---------------------------
    tasks, answers = tmp / "tasks", tmp / "answers"
    tasks.mkdir(), answers.mkdir()
    (tasks / "t1.expected").write_text("1\n")
    (tasks / "t2.expected").write_text("2\n")
    (answers / "t1.A.py").write_text("print(1)\n")
    (answers / "t1.B.py").write_text("print(3)\n")                      # wrong output
    (answers / "t2.A.py").write_text("import sys\nprint(2)\nsys.stderr.write('warn')\n")
    (answers / "t2.B.py").write_text("open('left.txt','w').write('x')\nprint(2)\n")
    csv = tmp / "results.csv"

    def score(rows):
        csv.write_text("task,condition,correctness\n" + "".join(f"{r}\n" for r in rows))
        return run("bash", HERE / "correctness.sh", env={
            "TASKS": str(tasks), "ANSWERS": str(answers), "CSV": str(csv),
            "EXT": "py", "RUN": f"{sys.executable} {{}}"})

    def score_relative(rows):
        # Relative paths, as a user in their study directory would pass them.
        csv.write_text("task,condition,correctness\n" + "".join(f"{r}\n" for r in rows))
        return run("bash", "-c", f"cd {tmp} && TASKS=tasks ANSWERS=answers CSV=results.csv "
                   f"EXT=py RUN='{sys.executable} {{}}' bash {HERE / 'correctness.sh'}")

    truth = ["t1,A,1", "t1,B,0", "t2,A,0", "t2,B,1"]
    rc, out = score(truth)
    expect("scorer agrees with a correct results.csv (wrong output and stderr both score 0)",
           rc == 0 and "4 candidates scored; correctness = 0 on 2" in out, out)
    rc, out = score_relative(truth)
    expect("scorer gives the same scores from relative paths", rc == 0 and
           "4 candidates scored; correctness = 0 on 2" in out, out)
    rc, out = score(["t1,A,1", "t1,B,1", "t2,A,0", "t2,B,1"])
    expect("scorer fails a results.csv that claims a wrong answer passed",
           rc == 1 and "MISMATCH" in out, out)
    (answers / "t2.B.py").unlink()
    rc, out = score(truth)
    expect("scorer fails when a task with a golden has no answer",
           rc == 1 and "missing answer t2.B.py" in out, out)

    csv.unlink()
    rc, out = run("bash", HERE / "correctness.sh", env={
        "TASKS": str(tasks), "ANSWERS": str(answers), "CSV": str(csv), "INIT": "1",
        "EXT": "py", "RUN": f"{sys.executable} {{}}"})
    (answers / "t2.B.py").write_text("print(2)\n")
    rc2, out2 = run("bash", HERE / "correctness.sh", env={
        "TASKS": str(tasks), "ANSWERS": str(answers), "CSV": str(csv), "INIT": "1",
        "EXT": "py", "RUN": f"{sys.executable} {{}}"})
    expect("scorer INIT=1 records the missing answer as a failure and refuses to overwrite",
           rc == 1 and "t2,B" not in csv.read_text() and rc2 == 2, out + out2)

    # ---- extract.py ----------------------------------------------------------
    b = EVAL / "runs/logs/partB/01-sum-squares.B.jsonl"
    a = EVAL / "runs/logs/partB/01-sum-squares.A.jsonl"
    _, fb = run(sys.executable, HERE / "extract.py", b, "--field", "fired")
    _, fa = run(sys.executable, HERE / "extract.py", a, "--field", "fired", "--plugin", "q-knowledge")
    expect("extract --field fired reads activation off the log (M2 01: B y, A n)",
           fb.strip() == "y" and fa.strip() == "n", fb + fa)
finally:
    shutil.rmtree(tmp)

if failures:
    sys.exit(f"\n{len(failures)} self-test(s) failed")
print("\nharness self-test: all gates pass and fail as they should")
