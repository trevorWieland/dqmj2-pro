# Code and progress policy (2026-11-10)

This document records the owner's current directives. Where a directive conflicts with earlier
practice, this document wins: it supersedes the "authored code has no comments" rule and the
practice of committing evidence artifacts, per-packet receipts and progress claims.

## 1. The public repository contains the complete decompilation

Everything that has been decompiled is published. No decompiled code is held back in a private
repository, a private branch, a private archive or an unpublished local tree. A public checkout
supplied with private inputs must be able to build the measured image.

## 2. ROMs and saves are private only

Original ROMs, saves and extracted original payloads are never committed, uploaded or reshared.
Contributors supply their own measured inputs. Private inputs are read-only build inputs, not
publication material.

## 3. CI reports progress from a real build and comparison

Progress is produced by the workflow at `.github/workflows/bytematch.yml`, which builds the
checked-out source and runs the genuine comparison. The generated report is the only progress
figure; percentages are never committed by hand.

## 4. Code that compiles and compares is the only evidence

Evidence artifacts provide zero value. A document, manifest, receipt, checksum list or screenshot
does not prove a match. The only valid evidence is code in the tree that compiles and compares
against the measured original. A claim that cannot be reproduced by building the tree is not a
claim.

## 5. Understandable code, documented in place

Code must be understandable. Functions, parameters and locals use meaningful names, and concise
comments in the code explain mechanism and intent. Documentation belongs in those comments, and
in `docs/` only when it describes cross-cutting design. Separate stale documents that restate the
code are not documentation; per-packet evidence write-ups are discontinued.

## Superseded practice

- "Authored code has no comments": reversed. Concise explanatory comments are expected.
- Committed progress percentages and manifests of accepted functions: removed as sources of truth.
- Per-packet evidence documents, acceptance receipts and committed progress snapshots: no longer
  created, and not part of review.

## Enforcement

Policy compliance is checked in review, and `public_tools/check_contribution.py` enforces the
mechanical rules on changed authored files. Dated records that describe the superseded practice
remain historical context only; they do not state current policy.
