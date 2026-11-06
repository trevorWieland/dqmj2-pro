from project import ROOT,sha256,write_json
import prove_ov003_config526_20261101 as R
import ov003_config525_machine_20261101 as M
import ov003_config525_models_20261101 as P


def run():
    R.WORK=ROOT/'work/ol525-rejected-model';row,link,body=R.compile_unit(R.SOURCE,'candidate');original=M.inputs();cases=[];returns=0;native=0;providers=0
    for profile in[p for p in P.profiles()if p['keys']==0x800]:
        for name,code in[('original',None),('linkedC',body)]:
            result=M.Machine(original,profile,code).run();rejection=None
            try:P.model(result,original)
            except ValueError as error:rejection=str(error)
            if rejection is None:raise ValueError('525 incorrect byte-table model unexpectedly passed')
            returns+=1;native+=len(result['nativeReturns']);providers+=len(result['providedEvents']);cases.append(dict(profile=profile['name'],image=name,actualTopReturn=True,rejection=rejection))
    report=dict(schemaVersion=1,evidenceClass='rejected-independent-model',romSha256=R.configuration()['romSha256'],processor='arm9',program='',module='ov003',address=hex(M.ENTRY),mode='arm',sourceCredit=0,exactBytes=0,actualTopReturns=returns,actualNativeDependencyReturns=native,providedCalls=providers,rejectedModels=len(cases),compilation=row,genuineLink=link,candidateSourceAlreadyUsesCorrectUnsigned16Table=True,cases=cases,generatorSha256=sha256(__file__),originalFixtureSha256=sha256(ROOT/'ov003_config525_machine_20261101.py'),rejectedModelSha256=sha256(ROOT/'ov003_config525_models_20261101.py'),limits=['Every original andlinked C run actuallyreturns; deliberately incorrect byte-table expectations are independently rejected','Diagnostic counts are separate from thepositive526 oracle andgivezero source credit','526 candidate source/context hashes equal525 preserved source/context; onlythe fixture/model changed'],reproductionCommand='python replay_ov003_config525_rejected_model_20261101.py')
    write_json(ROOT/'evidence/attempts/ov003-config525-rejected-replay-20261101.json',report);print(dict(actualTopReturns=returns,actualNativeDependencyReturns=native,providedCalls=providers,rejectedModels=len(cases)))

if __name__=='__main__':run()
