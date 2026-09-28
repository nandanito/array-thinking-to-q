"""sessionlog.py: read one `claude -p --output-format stream-json` session log.

Shared by extract.py, mktraces.py, aggregates.py and audit.py so that every
number they report comes from one parser. Nothing here knows which plugin is
under test: the treatment is whatever plugin `--plugin-dir` loaded, which the
`system/init` line records with source `<name>@inline` (see `treatment`).
Other plugins can be present in every session: Claude Code 2.1.284 loads
`agents-md@builtin` and `telemetry@builtin` into both conditions (2.1.220, the
M2 build, loaded none). Those are context, and audit.py requires them to be
identical across sessions.
"""
import json, pathlib


class Session:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.init, self.result, self.first_ts = None, None, None
        self.inits = 0
        self.tool_uses = []          # (name, input) in emission order
        for line in self.path.open():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if self.first_ts is None and d.get("timestamp"):
                self.first_ts = d["timestamp"]
            kind = d.get("type")
            if kind == "system" and d.get("subtype") == "init":
                self.inits += 1
                self.init = self.init or d
            elif kind == "assistant":
                for b in d["message"].get("content", []):
                    if b.get("type") == "tool_use":
                        self.tool_uses.append((b["name"], b.get("input", {})))
            elif kind == "result":
                self.result = d

    # Log names are <task>.<condition>.jsonl for generation sessions.
    @property
    def task(self):
        return self.path.name.split(".")[0]

    @property
    def cond(self):
        return self.path.name.split(".")[1]

    @property
    def plugins(self):
        """Plugins loaded by --plugin-dir: the treatment, if any."""
        return [p.get("name") for p in (self.init or {}).get("plugins") or []
                if str(p.get("source", "")).endswith("@inline")]

    @property
    def other_plugins(self):
        """Every other plugin (built-ins): context, identical in both conditions."""
        return sorted(f"{p.get('name')}@{p.get('version', '')}" for p in
                      (self.init or {}).get("plugins") or []
                      if not str(p.get("source", "")).endswith("@inline"))

    @property
    def answer(self):
        return (self.result or {}).get("result") or ""

    @property
    def output_tokens(self):
        return ((self.result or {}).get("usage") or {}).get("output_tokens", "")

    def fired(self, plugin):
        """Mechanical activation: a Skill tool call naming one of the plugin's skills.

        Plugin skills are namespaced `<plugin>:<skill>`; M2 matched the bare prefix,
        and so does this, so a call to the plugin's own name also counts.
        """
        return bool(plugin) and any(
            n == "Skill" and str(i.get("skill", "")).startswith(plugin)
            for n, i in self.tool_uses)


def load(logs):
    return [Session(p) for p in sorted(pathlib.Path(logs).glob("*.jsonl"))]


def treatment(sessions):
    """The single plugin --plugin-dir loaded across the logs. Exactly one, or it is an error."""
    names = {n for s in sessions for n in s.plugins}
    if len(names) != 1:
        raise SystemExit(f"expected exactly one plugin across the logs, found {sorted(names)}")
    return names.pop()
