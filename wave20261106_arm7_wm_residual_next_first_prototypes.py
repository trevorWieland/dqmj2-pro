import os
import re
import subprocess
from project import ROOT,sha256
from elftools.elf.elffile import ELFFile
from wave20261106_arm7_wm_residual_next_first_build import SOURCE,WORK,COMPILER


def sections(path):
    with path.open('rb')as stream:return[(s.name,s.data().hex())for s in ELFFile(stream).iter_sections()if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wm-residual-next/first' or WORK!=ROOT/'work/w6wr/first':raise ValueError('Exact new request prototype scope differs')
    own=[];providers=[]
    for row in rows:
        tag=format(int(row['address'],0),'08x');directory=WORK/'prototypes'/tag;directory.mkdir(parents=True,exist_ok=True);flags=[*row['compilerFlags'],'-requireprotos','-w','error'];obj=directory/'explicit.o';positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Actual required C99 prototypes failed or changed executable bytes',positive.stdout,positive.stderr))
        headers={p.name:p.read_text()for p in(SOURCE/tag).glob('*.h')}
        for name,text in headers.items():(directory/name).write_text(text)
        call=directory/'callsite.c';call.write_text('\n'.join('#include "'+name+'"'for name in sorted(headers))+'\nextern void diagnostic(void);\nvoid diagnostic(void){'+row['name']+'((OSMessage)0);}\n');p=compile_source(call,directory/'callsite.o',flags)
        if p.returncode:raise ValueError(('Actual typed ARM7 entry callsite rejected',p.stdout,p.stderr))
        pattern=re.compile(r'\b'+re.escape(row['name'])+r'\s*\(');found=[name for name,text in headers.items()if pattern.search(text)]
        if len(found)!=1:raise ValueError('Actual caller declaration mutation ambiguous')
        name=found[0];(directory/name).write_text(pattern.sub('missing_actual_entry(',headers[name],count=1));bad=directory/'missing.o';bad.unlink(missing_ok=True);p=compile_source(call,bad,flags)
        if p.returncode==0 or bad.exists()or'no prototype'not in p.stdout:raise ValueError(('Missing actual ARM7 entry prototype admitted',p.stdout,p.stderr))
        own.append(dict(caller=row['address'],actualTypedCallsitePassed=True,executableSectionsUnchanged=True,negativeExitCode=p.returncode,negativeStdout=p.stdout,explicitObjectSha256=sha256(obj)))
        for provider,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function' or any(r['provider']==provider for r in providers):continue
            target=directory/provider;target.mkdir(exist_ok=True)
            for name,text in headers.items():(target/name).write_text(text)
            source=target/'main.c';source.write_text((ROOT/row['source']).read_text());pattern=re.compile(r'(?m)^([ \t]*(?:[A-Za-z_]\w*[ \t*]+)+)'+re.escape(provider)+r'([ \t]*\([^;{}]*\)[ \t]*;)');found=[name for name,text in headers.items()if pattern.search(text)]
            if len(found)!=1:raise ValueError('Actual original provider declaration mutation ambiguous')
            name=found[0];(target/name).write_text(pattern.sub(lambda m:m[1]+'missing_original_provider'+m[2],headers[name],count=1));bad=target/'missing.o';bad.unlink(missing_ok=True);p=compile_source(source,bad,flags)
            if p.returncode==0 or bad.exists()or'no prototype'not in p.stdout:raise ValueError(('Missing actual ARM7 provider prototype admitted',provider,p.stdout,p.stderr))
            providers.append(dict(caller=row['address'],provider=provider,negativeExitCode=p.returncode,negativeStdout=p.stdout))
    return dict(status='passed',sourceCredit=0,actualEntries=own,originalProviders=providers,flags=['-requireprotos','-w','error'],diagnosticCallerProviderOrStorageCredit=0)
