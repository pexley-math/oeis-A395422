# Pre-Submission Checklist -- OEIS A395422

**Subject sequence:** A395422
**Project directory:** C:\Users\obnox\Documents\Other-Projects\research-outputs\paper-project\oeis-a395422
**Generated:** 2026-04-13T03:22:39Z

---

## Purpose

This checklist is the last gate before a submission goes to the OEIS
editors. Every claim in the paper, the OEIS draft, and the README has
been machine-checked by `verify_claims` (C1-C9); this step covers the
class of errors only a human can catch: wrong-sequence identification,
stale OEIS data, and misattribution.

You are signing a cryptographic commitment to the pinned files. Any
edit to a pinned file after you sign invalidates the signature and
`/publish` will refuse to run.

## Referenced A-numbers (auto-filled from research/prior-art-facts.md)

_(no prior-art-facts.md present; this project has no external A-number references to confirm)_

For each referenced A-number, tick the box AFTER you have actually
opened the OEIS page in your browser and confirmed that every claim
the paper makes about that sequence matches the live record.

The signer (`python -m tools.checklist.sign`) will open each URL and
enforce a short delay before accepting your confirmation. This is
deliberate. Do not sign without reading.

## Hygiene

- [ ] I verified the Name, Data, and Offset fields in `research/prior-art-facts.md` match what oeis.org currently shows.
- [ ] I read `submission/oeis-draft.txt` top to bottom, line by line.
- [ ] I confirmed the sequence of terms in `submission/oeis-draft.txt` exactly matches `research/solver-results.json`.
- [ ] I confirmed the EXAMPLE section ASCII art matches the proved solutions (not hand-written).
- [ ] I read the Phase 6 `tools.precommit.check_ai_tells` output for this project (run via `git ls-files --full-name $PROJECT | python -m tools.precommit.check_ai_tells --scope public-repo --files-from-stdin --repo-root $(git rev-parse --show-toplevel)`) and saw zero matches against the deny-list of model-vendor names.
- [ ] I confirmed no absolute Windows paths (`C:\Users\...`) leaked into any public file.
- [ ] I confirmed the LINKS field is sorted alphabetically by author surname.
- [ ] I have authority to submit this under my own name.
- [ ] I accept responsibility for every claim in every file being published.

## Sign

After ticking every box above, run:

```
python -m tools.checklist.sign C:\Users\obnox\Documents\Other-Projects\research-outputs\paper-project\oeis-a395422
```

This will:
1. Re-parse the checklist and refuse to sign if any box is still unticked.
2. Open each referenced OEIS page and pause for 10 seconds per page.
3. Prompt for your initials and the literal string `I confirm`.
4. Compute SHA-256 of every pinned file and write `submission/human-verified-by.txt`.

After signing, do NOT edit any pinned file. If you need to edit, you
must re-verify and re-sign. `/publish` calls `verify_signature.py`
and will block any stale signature.
