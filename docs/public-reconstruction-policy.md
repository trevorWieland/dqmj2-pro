# Public reconstruction policy

The owner authorized public reconstruction sources, tooling, configuration, documentation and progress reporting on 2026-11-06. The public repository must contain the actual work, following the general model of [pokebw2](https://github.com/fuddlesworth/pokebw2). A metadata-only mirror does not satisfy that instruction.

Publish readable authored C/C++, justified assembly, headers, compiler profiles, symbol/relocation configuration, build and verification scripts, source selection manifests, research conclusions and explicit limitations. Preserve stable CPU/program/overlay/mode identities. Source matching, bounded behavior, semantic understanding, interpreted-source recovery and native platform execution remain separate measurements.

Do not publish the original ROM or save, extracted original executable/data payloads, executable scaffolding, compiler binaries, credentials or private generated memory/instruction dumps. Public checks obtain original targets from the user's own measured input. An exact scaffold-assisted ROM remains an incomplete decompilation.

The private historical repository contains approximately 6.4 GiB of tracked files, principally generated evidence. Initial publication uses a clean source history with a hash-bound accepted manifest. It preserves authored source contents without exposing private historical evidence blobs. The original local Git history and immutable proof records remain intact. Do not attach the public remote to the private historical branch or push its ancestry.

Public CI checks source integrity and tooling without original inputs. Source compilation requires the pinned compiler. Full byte matching, real module links, original/source model comparisons and exact container verification run in a trusted local checkout with owned inputs. A public repository's general self-hosted Actions runner must not expose a machine containing those inputs to untrusted pull requests. See [GitHub's security guidance](https://docs.github.com/en/actions/reference/security/secure-use).

ByteMatch will track this same public source repository. Reports must come from real original target objects and freshly built source objects at a named public revision, with the full intended denominator. Never publish the existing instruction-rich objdiff self-test JSON, force completion flags, count original scaffold objects as reconstructed source, or present a small pilot's 100% as project progress. Standard report output is checked against an explicit public schema before upload. [Setup instructions](https://bytematch.dev/docs/setup-prompt) and [source linking](https://bytematch.dev/docs/source-linking) govern the integration.

Until the complete public checkout build and report path has been exercised, document that limitation directly. Published sources make the work inspectable; source hashes and historical acceptance receipts do not substitute for an independent rebuild.
