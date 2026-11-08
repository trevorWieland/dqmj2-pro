import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import stat

CANONICAL = 'evidence/verification/cohort-2026-10-29-176.json'
SNAPSHOT = 'provenance/cohort176-original-pending-plan-20261108.json'
PENDING_SHA = 'fb4454849a40683fce80cfff9a43e9d7aaafc9a2e87f2973537ec416101d26de'
QUALIFIER_SHA = '628d027d95d8509f0586a64da7878e3d12d4eee0998dc5330ba05cfa88587ad2'
BUILDER_SHA = '0c3fcd7eda933054b858c77fc73a8919d612be18c053bbba3c7c8b2034d3636d'
OUTPUTS = dict(proof='evidence/verification/cohort176-main-workspace-scope-20261108.json',
    driver='evidence/verification/cohort176-current-scope-driver-20261108.json',
    started='evidence/verification/cohort176-current-scope-finalizer-started-20261108.json',
    temporary=CANONICAL + '.current-scope-new-20261108')


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned_read(io, row):
    raw = io.read(row['path'])
    require(sha(raw) == row['sha256'] and len(raw) == row['bytes'], 'pinned input differs')
    return raw


def finalize(io, qualifier, builder, contract, contract_pin, clock):
    require(contract['jsonPins']['plan']['path'] == SNAPSHOT
            and contract['jsonPins']['plan']['sha256'] == PENDING_SHA, 'pending contract not redirected')
    raw_pending = pinned_read(io, contract['jsonPins']['plan'])
    require(io.read(CANONICAL) == raw_pending, 'canonical receipt is not original pending bytes')
    for path in OUTPUTS.values():
        require(not io.exists(path), 'owned output already exists; no retry')
    io.write_new(OUTPUTS['started'], builder.encode(dict(cohort=176, state='STARTED_SCOPE_FINALIZATION',
        contract=contract_pin, pendingSha256=PENDING_SHA, startedUtc=clock())))
    proof = qualifier()
    require(proof['MainMatchingWorkspaceScopePassed'] is True
            and proof['contractSha256'] == contract_pin['sha256'], 'fresh qualification not passed')
    require(io.read(CANONICAL) == raw_pending, 'pending changed during qualification')
    completed = clock()
    require('qualificationCompletedUtc' not in proof, 'completion timestamp already supplied')
    proof = {**proof, 'qualificationCompletedUtc': completed}
    manifest_pin = contract['jsonPins']['manifest']
    manifest = json.loads(pinned_read(io, manifest_pin))
    failed_pin = contract['jsonPins']['driver']
    failed = json.loads(pinned_read(io, failed_pin))
    pinned_read(io, contract['jsonPins']['workspace'])
    pinned_read(io, contract['jsonPins']['getters'])
    supplement = json.loads(pinned_read(io, contract['jsonPins']['supplement']))
    proof_raw = builder.encode(proof)
    require(len(proof_raw) <= 131072, 'proof size bound exceeded')
    proof_pin = builder.pin(OUTPUTS['proof'], proof_raw)
    references = dict(originalPendingPlan=contract['jsonPins']['plan'], originalFailedDriver=failed_pin,
        originalWorkspace=contract['jsonPins']['workspace'], contract=contract_pin, proof=proof_pin,
        manifest=manifest_pin, getters=contract['jsonPins']['getters'], exactRom=supplement['exactLayoutROM'],
        scopedDriver=dict(path=OUTPUTS['driver']), manifestFacts=dict(
            initializedModuleByteDenominator=sum(row['bytes'] for row in manifest['modules']),
            sourceMatchedFunctionBytes=manifest['sourceMatchedFunctionBytes'],
            sourceMatchedDataBytes=manifest['sourceMatchedDataBytes']))
    driver, current = builder.build_records(json.loads(raw_pending), proof, failed, references, completed)
    driver_raw, current_raw = builder.encode(driver), builder.encode(current)
    require(len(driver_raw) <= 131072 and len(current_raw) <= 262144, 'record size bound exceeded')
    require(current['scopedDriver'] == builder.pin(OUTPUTS['driver'], driver_raw), 'driver serialization differs')
    io.write_new(OUTPUTS['proof'], proof_raw)
    io.write_new(OUTPUTS['driver'], driver_raw)
    io.write_new(OUTPUTS['temporary'], current_raw)
    pinned_read(io, proof_pin)
    pinned_read(io, current['scopedDriver'])
    pinned_read(io, contract['jsonPins']['plan'])
    io.checked_replace(OUTPUTS['temporary'], CANONICAL, raw_pending)
    require(io.read(CANONICAL) == current_raw, 'published current receipt verification failed')
    return dict(cohort=176, status='CURRENT_MAIN_MATCHING_SCOPE_FINALIZED_CLOSURE_REQUIRED',
        currentReceipt=builder.pin(CANONICAL, current_raw), scopeProof=proof_pin, scopedDriver=current['scopedDriver'],
        originalPendingPlan=contract['jsonPins']['plan'], historicalOriginalGateExitCode=1,
        originalFailedDriverUnmodified=True, originalWorkspaceUnmodified=True,
        strictWholeWorkspaceIsolationPassed=False, fullToolDelivery=False, committedClosureRequired=True)


class Files:
    def __init__(self, root):
        self.root = root.resolve()

    def path(self, name):
        require(type(name) is str and not PurePosixPath(name).is_absolute() and '\\' not in name
                and '..' not in PurePosixPath(name).parts, 'unsafe owned path')
        path = self.root / name
        require(path.resolve().is_relative_to(self.root), 'path escaped Root')
        for parent in [path, *path.parents]:
            if parent.exists():
                require(not parent.is_symlink() and not bool(getattr(parent.lstat(), 'st_file_attributes', 0)
                        & stat.FILE_ATTRIBUTE_REPARSE_POINT), 'reparse path refused')
            if parent == self.root:
                break
        return path

    def read(self, name):
        return self.path(name).read_bytes()

    def exists(self, name):
        return self.path(name).exists()

    def write_new(self, name, raw):
        path = self.path(name)
        require(path.parent.is_dir(), 'output parent absent')
        with path.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def checked_replace(self, temporary, canonical, expected):
        require(self.read(canonical) == expected, 'canonical changed before transition')
        os.replace(self.path(temporary), self.path(canonical))


def module(io, row, expected, name):
    require(row['sha256'] == expected, 'unreviewed code selection')
    pinned_read(io, row)
    spec = importlib.util.spec_from_file_location(name, io.path(row['path']))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def check_activation(contract, bindings, binding_sha):
    activation = contract.get('supportActivation')
    require(type(activation) is dict and activation.get('reviewedBy') == 'Root'
            and activation.get('mappingSha256') == binding_sha
            and contract['extraSupportPins'] == bindings['extraSupportPins'], 'support activation differs')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--contract', required=True)
    parser.add_argument('--contract-sha256', required=True)
    parser.add_argument('--bindings', required=True)
    parser.add_argument('--bindings-sha256', required=True)
    args = parser.parse_args()
    io = Files(args.root)
    binding_raw, contract_raw = io.read(args.bindings), io.read(args.contract)
    require(sha(binding_raw) == args.bindings_sha256 and sha(contract_raw) == args.contract_sha256, 'binding/contract SHA differs')
    bindings, contract = json.loads(binding_raw), json.loads(contract_raw)
    check_activation(contract, bindings, args.bindings_sha256)
    require(io.path(bindings['finalizer']['path']).resolve() == Path(__file__).resolve(), 'finalizer path differs')
    pinned_read(io, bindings['finalizer'])
    require(bindings['outputs'] == OUTPUTS, 'output ownership differs')
    qualifier = module(io, bindings['qualifier'], QUALIFIER_SHA, '_cohort176_workspace_scope')
    builder = module(io, bindings['builder'], BUILDER_SHA, '_cohort176_scope_state')
    contract_pin = builder.pin(args.contract, contract_raw)
    result = finalize(io, lambda: qualifier.qualify(io.root, args.contract, args.contract_sha256),
                      builder, contract, contract_pin, lambda: datetime.now(timezone.utc).isoformat())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
