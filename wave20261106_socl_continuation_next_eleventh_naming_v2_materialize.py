from project import ROOT

RENAMES={'signature_length':'pub_algorithm','certificate_flag':'date_ok','certificate_name':'issuer'}


def execute():
    source=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eleventh-naming-v2'
    evidence=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2'
    if source!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eleventh-naming-v2'or evidence!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2'or source.exists()or evidence.exists():raise ValueError('Exact fresh naming-only source/evidence paths required')
    source.mkdir();evidence.mkdir()
    for name in ['context.h','020911b0.c','02091c5c.c']:
        text=(source.parent/'eleventh'/name).read_text()
        for old,new in RENAMES.items():text=text.replace(old,new)
        (source/name).write_text(text)
    for kind in ['compiler','bindings','build','models','execution','controls','proof','package']:
        path=ROOT/('wave20261106_socl_continuation_next_eleventh_naming_v2_'+kind+'.py')
        if path.exists():raise ValueError('Fresh naming-only helper exists')
        text=(ROOT/('wave20261106_socl_continuation_next_eleventh_'+kind+'.py')).read_text().replace('_eleventh_','_eleventh_naming_v2_').replace('/eleventh','/eleventh-naming-v2').replace('-eleventh','-eleventh-naming-v2')
        for old,new in RENAMES.items():text=text.replace(old,new)
        text=text.replace('signature-sentinel','public-key-algorithm-sentinel').replace('signature sentinel','public-key-algorithm sentinel').replace('signature/pub-algorithm sentinel','public-key-algorithm sentinel')
        if kind=='models':
            text=text.replace('dict(flag=f,length=l,algorithm=a','dict(flag=f,pub_algorithm=l,algorithm=a');a=text.index('def certificate(');b=text.index('\n\ndef plaintext(',a);section=text[a:b].replace("f['length']","f['pub_algorithm']");text=text[:a]+section+text[b:]
        path.write_text(text)
    (evidence/'native-inputs.json').write_bytes((evidence.parent/'eleventh/native-inputs.json').read_bytes())


if __name__=='__main__':execute()
