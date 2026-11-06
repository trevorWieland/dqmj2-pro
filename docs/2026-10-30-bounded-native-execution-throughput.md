# Bounded native execution throughput experiment

The official [Unicorn2.1.4 implementation](https://github.com/unicorn-engine/unicorn/blob/2.1.4/uc.c) starts a timer thread for nonzero emulation timeouts and joins that thread before returning. The consulted upstream source SHA256 is `af8d8281594036b2d3e7d65940999b444761e4410d3b5801c998667f59331364`. The official [performance FAQ](https://github.com/unicorn-engine/unicorn/blob/master/docs/FAQ.md) also identifies fine-grained instruction/memory instrumentation costs. No library, dependency pin or frozen fixture was changed.

`python benchmark_unicorn_bounds_20261030.py` compares64 fresh checksum machines per mode. Both modes keep a20000-instruction per-call limit, actual return-sentinel/SP/callee-saved-register checks and an independent Python checksum model. The count-only experiment also runs inside a separately bounded child process. All general registers, CPSR, input RAM, stack and sentinel-page state agree across modes. Four count-limit/unmapped-input controls have zero returns; an independent hanging child is terminated by its external deadline and gains zero return credit.

Measured timer mode:0.991325s; count-only mode:0.271017s; ratio:3.658x on this run. Timings are observations for this checksum workload, not a VM or game speedup promise. This creates no reconstructed-source credit.

The method is not adopted for acceptance. Before a future version can use it, a separately scoped real-VM workload must match the existing execution contract for CPU state, all relevant RAM, ordered stores, termination and unsupported errors. Its instruction bounds, external deadline and isolated state must be recorded truthfully; old timeout-bearing metadata cannot be reused under an override. Existing frozen matchers continue with their original limits.

Evidence is `evidence/tools/unicorn-bounds-benchmark-20261030.json`. The downloaded unmodified upstream source is disposable research under `work/tool-research/`; reproduction does not require it. The experiment neither removes required instrumentation nor changes accepted game sources.
