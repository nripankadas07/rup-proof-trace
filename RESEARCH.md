# Research —19 October2026

User: SAT experiment authors debugging small unsatisfiability certificates.

Pain: A partial or rejected trace needs clause-level reasons; successful intermediate additions do not prove the complete certificate.

MVP: Explain small RUP additions with assumptions, unit reasons and an explicit final-empty-clause requirement.

Acceptance: Clause-reason traces, full/incomplete/rejected proof, contradictory assumptions, initial empty clause, duplicate multiset and unit deletions, final-empty enforcement, DIMACS bounds and visit-budget failure.

Demand is inferred from workflows and adjacent discussions, not verified requests. Discovery path: descriptive GitHub topics, runnable invented examples and chronological project index. No unsolicited outreach or artificial activity.

## Alternatives

Live GitHub search sorted Most stars: `DRAT proof; DRUP (unrelated Drupal matches excluded)`. Highest-star relevant comparable found: **marijnheule/drat-trim**. This is bounded search/reference-follow coverage, not an exhaustive global ranking. Broad/unrelated keyword matches were excluded.

| Repository | Stars observed | Last push UTC | API license |
| --- | ---: | --- | --- |
| [marijnheule/drat-trim](https://github.com/marijnheule/drat-trim) | 72 | 2024-11-25T15:20:29Z | MIT |
| [digama0/frat](https://github.com/digama0/frat) | 16 | 2023-04-08T06:55:38Z | UNCLASSIFIED |
| [krobelus/rate](https://github.com/krobelus/rate) | 10 | 2022-02-12T05:44:34Z | MIT |

DRAT-trim implements much broader DRAT checking and proof output; FRAT carries annotated proof evidence; rate addresses RAT elimination. Their historical research repositories remain useful comparisons even with older push dates. DRAT-trim LRAT issue42/PR43 is a different checker path, not evidence of a defect in RUP or demand for this tool. Existing algorithms are not claimed as new.

Current READMEs, selected relevant source and up to five issue/PR records were read; exact observations and source identities are in [provenance](RESEARCH_PROVENANCE.json). Our clean-install example establishes our behavior only. Established alternatives provide broader capability, docs, examples and communities. Competitor installability, time to first useful result, reliability, support response and performance were not measured. No feature-absence claim. Stars are discovery evidence, not quality/performance. Unclassified licenses are not permission to copy. No competitor code, prose, branding or fixtures are bundled.

Primary technical reference: https://www.cs.utexas.edu/~marijn/drat-trim/. NASA's current FITS4 PDF fetch timed out; the official standard landing page and NASA CFITSIO primer were readable. ELF reference is explicitly a draft generic ABI; processor-specific behavior remains outside scope. No technical performance benchmark was conducted.

Portfolio distinction: No owned CNF proof checker was found among198 repositories. Numeric and bit-vector tools do not validate clause-addition proofs.

Original capability is the bounded implementation/evidence workflow, not a claim to invent the file format or standard algorithm.
