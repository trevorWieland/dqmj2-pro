from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import match_main_material768_v2_20261101 as producer
from link_runtime_unit import measured_module


def main():
    producer.main()
    config=configuration();assert sha256(config["rom"])==config["romSha256"]
    metadata,image,unused=measured_module("main")
    report=read_json(producer.REPORT)
    for row in report["matches"]:
        row.update(exactBytes=row["bytes"],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage="C")
    report.update(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     romSha256=config["romSha256"],moduleSha256=metadata["sha256"],module="main",processor="arm9",program="",
     matchedFunctions=6,matchedBytes=768,reproductionCommand="python match_main_material768_namespace_v3_20261101.py",
     replayDependencies=report["nativeEvidence"],sourceOrigin=dict(referenceRevision="d636fb5d2b212e8736f09859fff447be2bd0ac85",
      historicalSdkRevisionProven=False,standaloneC=True,headerOrLibcPlaceholders=False))
    write_json(ROOT/"evidence/matches/main-material768-v3-20261101.json",report)
    print("Material768 namespace/schema preflight complete")


if __name__=="__main__":
    main()
