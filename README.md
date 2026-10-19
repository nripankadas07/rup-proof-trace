# rup-proof-trace

Explain small RUP additions with assumptions, unit reasons and an explicit final-empty-clause requirement.

For SAT experiment authors debugging small unsatisfiability certificates. A partial or rejected trace needs clause-level reasons; successful intermediate additions do not prove the complete certificate.

## Quickstart

Python3.10+; zero runtime dependencies. Wheel builds require setuptools from the normal Python registry.

```sh
git clone https://github.com/nripankadas07/rup-proof-trace.git
cd rup-proof-trace
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/rup-proof-trace example.cnf example.drup
```

Exit0: addition1 has a unit conflict under assumption-1; the final empty clause is accepted after adding1.

Example generators create only an explicitly named new file and refuse overwrite. Reports never modify the input. Windows equivalents use `.venv\Scripts\python.exe` and the installed `.exe`; Windows/macOS have not been executed by this release's Linux CI.

## Contract

ASCII DIMACS p cnf header with exact clause count and0 termination;0..64 variables,0..256 initial clauses. Text proof has one addition or d-prefixed deletion per noncomment line. Canonical clauses retain duplicate-clause identities; deletion removes exactly one matching active clause, including units, and absent deletions fail. For each addition assume its negation and perform deterministic unit propagation; report assumptions, implied literals with clause IDs, and conflict. Only an accepted empty clause as the final noncomment step yields verified/exit0. Non-RUP additions and incomplete traces exit1, not a SAT counterexample.

JSON reports go to stdout. Exit0 means the documented successful result, exit1 a valid finding/incomplete/rejected result, exit2 invalid/unsupported input, I/O or budget failure with stderr and no partial report. Ranges are half-open.

## Limits

Combined inputs1 MiB,512 steps,2million literal visits. Existing variables only. No RAT, fresh variables, binary DRAT, FRAT or LRAT. Strict unit-deletion application differs from some DRAT-trim modes; no broad compatibility certification. Educational bounded checker, not formally verified or production assurance. Proof comments start with c on their own lines.

## Verify

```sh
python3 -m unittest -v test_behavior
python3 -m compileall -q .
python3 -m pip wheel --no-deps --wheel-dir dist .
python3 -m venv /tmp/rup-proof-trace-check
/tmp/rup-proof-trace-check/bin/python -m pip install --no-deps dist/*.whl
python3 verify_installed.py /tmp/rup-proof-trace-check/bin/python
```

[Validation](VALIDATION.md), [research](RESEARCH.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), [security](SECURITY.md), [MIT license](LICENSE).

Original implementation, prose and invented fixtures developed with AI assistance. No measured performance-superiority or verified production-adoption claim.
