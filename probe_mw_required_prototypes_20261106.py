import os
import subprocess
from project import ROOT, configuration, native_dependencies, write_json, sha256


def main():
    config = configuration()
    native_dependencies(config)
    from elftools.elf.elffile import ELFFile
    root = ROOT / 'work/interface-declaration-preflight-20261106'
    root.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    positive = 'extern void supplied(void *);\nvoid entry(void *);\nvoid entry(void *p) { supplied(p); }\n'
    implicit = 'void entry(void *);\nvoid entry(void *p) { supplied(p); }\n'
    results = []
    for profile in ['base', 'sp1p5']:
        compiler = ROOT / f'tools/mwccarm/mwccarm/2.0/{profile}/mwccarm.exe'
        directory = root / profile
        directory.mkdir(exist_ok=True)
        outputs = {}
        for label, code, strict in [('explicit-baseline', positive, False), ('explicit-required', positive, True),
                                     ('implicit-baseline', implicit, False), ('implicit-required', implicit, True)]:
            source, obj = directory / (label + '.c'), directory / (label + '.o')
            source.write_text(code, encoding='utf-8')
            flags = ['-O2', '-proc', 'arm946e', '-sym', 'on', '-nolink', '-lang', 'c99', '-w', 'off']
            if strict:
                flags += ['-requireprotos', '-w', 'error']
            command = [str(compiler), *flags, '-c', str(source), '-o', str(obj)]
            run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
            diagnostic = (run.stdout + run.stderr).decode('utf-8', errors='replace')
            (directory / (label + '.txt')).write_text(diagnostic, encoding='utf-8')
            if label == 'implicit-required':
                assert run.returncode != 0 and not obj.exists(), diagnostic
            else:
                assert run.returncode == 0 and obj.is_file(), diagnostic
                with obj.open('rb') as stream:
                    elf = ELFFile(stream)
                    outputs[label] = [(s.name, s.data().hex()) for s in elf.iter_sections() if s['sh_flags'] & 4]
            results.append(dict(profile=profile, compilerSha256=sha256(compiler), label=label,
                                exitCode=run.returncode, command=command, diagnostic=diagnostic))
        assert outputs['explicit-baseline'] == outputs['explicit-required'] == outputs['implicit-baseline']
    write_json(ROOT / 'evidence/verification/mw-required-prototype-preflight-20261106.json',
        dict(passed=True, sourceCredit=0, profiles=results, explicitCallCodeBytesUnchanged=True,
             implicitDeclarationsRejectedByBothPinnedCompilers=True,
             generatorSha256=sha256(__file__), limits=[
                 'Presence-of-prototype diagnostic only; correctness of types still requires measured ABI evidence.',
                 'No frozen caller, primary compiler flags or accepted source has changed.',
                 'Fixture objects are private diagnostics and are not linked game implementations.']))
    print(dict(passed=True, profiles=2, implicitDeclarationRejections=2, sourceCredit=0))


if __name__ == '__main__':
    main()
