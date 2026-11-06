import json
from pathlib import Path
import utility_dtcm_audit
import utility_runtime
import utility_entrypoints
from project import write_json

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT / "evidence/utility/runtime-functions.json"
    report = json.loads(path.read_text())
    proof = utility_dtcm_audit.derive()
    if not proof["dataOnlyAsLoaded"] or report["program"] != proof["program"] or report["romSha256"] != proof["romSha256"]:
        raise ValueError("Utility inventory data classification is unqualified or unresolved")
    before = utility_runtime.sha(json.dumps(report["functions"], sort_keys=True).encode())
    write_json(utility_dtcm_audit.OUTPUT, proof)
    classifications = [item for item in report.get("moduleClassifications", []) if item["module"] != proof["module"]]
    classifications.append({"program": proof["program"], "processor": proof["processor"], "module": proof["module"],
                            "inputModuleSha256": proof["inputModuleSha256"], "functionInventoryStatus": proof["functionInventoryStatus"],
                            "classification": proof["classification"], "initialModuleDataClassificationComplete": True,
                            "initializedCodeBytes": 0, "initializedDataBytes": 96, "bssDataBytes": 32, "functionCredit": 0,
                            "evidence": utility_dtcm_audit.OUTPUT.relative_to(ROOT).as_posix(),
                            "evidenceSha256": utility_runtime.sha(utility_dtcm_audit.OUTPUT.read_bytes()),
                            "scope": "The measured ARM9 DTCM loader image under its native startup configuration; distinct from ARM7 code at the same numeric address"})
    report["moduleClassifications"] = classifications
    report['entryPointAssociations'] = utility_entrypoints.publish()['entryPointAssociations']
    write_json(path, report)
    if before != utility_runtime.sha(json.dumps(json.loads(path.read_text())["functions"], sort_keys=True).encode()):
        raise ValueError("Data classification must not alter canonical function candidate rows")
    print({"classifiedDataModules": len(classifications), "functionRowsUnchanged": True, "dataBytes": 96, "bssDataBytes": 32})
    return report


if __name__ == "__main__":
    main()
