# 2026-10-31: read-only unsigned 64-bit runtime entry characterization

Original measured ARM9 main image SHA-256 `ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f` contains the configured ARM parent `020260DC`/72 and interior ARM label `020260E8`. Both entries independently push R4–R7, FP, IP and LR. The first sets R4 to zero and branches to `020260F0`; the second sets R4 to one and falls into the same join. This is direct byte/prologue evidence, without any symbol, boundary or compiler-alias acceptance.

With unsigned numerator in R0:R1 and denominator in R2:R3, original `020260DC` returns the quotient in R0:R1 and `020260E8` returns the remainder in R0:R1 for the measured nonzero-divisor corpus. All 112 executions return to the actual sentinel and preserve R4–R12, SP, LR and control mode. Inputs cover zero/one numerators, 32-bit boundaries, high 64-bit values, maximum unsigned values, divisor ten and divisors through maximum unsigned64.

Thirty of those executions take the actual nested scalar entry `02026358`, inside configured parent `02026350`/484. Its observed input/output pairs agree with independent unsigned32 quotient/remainder arithmetic, and the hook observes actual returns to `02026110`. Other paths enter shared core `02025FA0`, within configured parent `02025F1C`/448. The evidence records visited code, saved frames, stack writes, raw registers and configured-main direct branch/call references. It changes none of these existing boundaries.

Six separate zero-divisor executions return the unchanged input numerator at both entries. They characterize original bytes only and receive zero supported-C-error-path credit. C division and modulus by zero are not given a defined-language claim.

`python characterize_main_u64_unsigned_entries_arm7_20261031.py` reproduces the report from the lane and an unrelated working directory. It uses fresh ARM946 Unicorn machines, a 100,000-instruction bound and a one-second execution timeout, with no providers or original-code modifications. Direct references are scanned only through configured main ARM/Thumb scopes; embedded pools can produce false-positive static references, and other-module/opaque indirect completeness is not claimed.

This is ABI research with zero source, function, assembly-provenance, boundary or compiler-helper alias credit. The integrator owns any address-qualified source calls and alternate-entry qualification. Compiler archive runtime library bodies were not found in the lane inventory, so this report supplies no original-written-assembly provenance.
