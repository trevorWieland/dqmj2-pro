import argparse
import json
import subprocess
from pathlib import Path
import utility_runtime
import utility_seeds
import utility_dtcm_audit

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/utility-ghidra"
GHIDRA = ROOT / "tools/ghidra/ghidra_12.2_PUBLIC"
JAVA = ROOT / "tools/jdk/jdk-25.0.5+8/bin/java.exe"
SEED = """import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.ArrayDataType;
import ghidra.program.model.data.ByteDataType;
import com.google.gson.JsonParser;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.ByteArrayInputStream;
import java.util.HashSet;
public class UtilitySeed extends GhidraScript {
    void seed(long raw, String id, HashSet<Long> seeded) throws Exception {
        if (!seeded.add(raw)) return;
        Address entry = toAddr(raw & ~1L);
        var register = currentProgram.getRegister("TMode");
        var mode = currentProgram.getProgramContext().getValue(register, entry, false);
        if (getInstructionAt(entry) == null || mode == null || mode.intValue() != (raw & 1L)) {
            if (getFunctionAt(entry) != null) currentProgram.getFunctionManager().removeFunction(entry);
            if (getInstructionAt(entry) != null) clearListing(entry, entry.add(3));
            currentProgram.getProgramContext().setValue(register, entry, entry, BigInteger.valueOf(raw & 1L));
        }
        currentProgram.getSymbolTable().addExternalEntryPoint(entry);
        disassemble(entry);
        if (getFunctionAt(entry) == null) createFunction(entry, "native_" + id.replace('-', '_') + "_" + entry.toString());
    }
    public void run() throws Exception {
        String[] args = getScriptArgs();
        var layout = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        var classification = JsonParser.parseString(Files.readString(Path.of(args[4]))).getAsJsonObject();
        var memory = currentProgram.getMemory();
        var initial = memory.getBlocks()[0];
        for (var item : layout.getAsJsonArray("modules")) {
            var module = item.getAsJsonObject();
            if (!module.get("processor").getAsString().equals(args[2])) continue;
            String id = module.get("id").getAsString();
            long base = Long.decode(module.get("base").getAsString());
            Address start = toAddr(base);
            byte[] bytes = Files.readAllBytes(Path.of(args[1]).resolve(module.get("binary").getAsString()));
            var block = memory.getBlock(start);
            if (block == initial) block.setName(id);
            else block = memory.createInitializedBlock(id, start, new ByteArrayInputStream(bytes), bytes.length, monitor, false);
            block.setRead(true);
            block.setWrite(true);
            boolean dataOnly = id.equals(classification.get("module").getAsString())
                && module.get("sha256").getAsString().equals(classification.get("inputModuleSha256").getAsString())
                && args[2].equals(classification.get("processor").getAsString())
                && classification.get("supportsNonExecutableAnalysisBlock").getAsBoolean();
            block.setExecute(!dataOnly);
            if (!block.isExecute()) {
                clearListing(block.getStart(), block.getEnd());
                createData(block.getStart(), new ArrayDataType(ByteDataType.dataType, bytes.length, 1));
            }
            int zeros = module.get("bssBytes").getAsInt();
            if (zeros > 0) {
                var bss = memory.createUninitializedBlock(id + "-bss", toAddr(Long.decode(module.get("bssStart").getAsString())), zeros, false);
                bss.setRead(true);
                bss.setWrite(true);
                bss.setExecute(false);
            }
        }
        var seeded = new HashSet<Long>();
        for (var item : layout.getAsJsonArray("modules")) {
            var module = item.getAsJsonObject();
            if (!module.get("processor").getAsString().equals(args[2])) continue;
            String id = module.get("id").getAsString();
            for (String key : new String[]{"runtimeEntry", "applicationEntry"}) {
                if (module.get(key).isJsonNull()) continue;
                long raw = Long.decode(module.get(key).getAsString());
                seed(raw, id, seeded);
            }
        }
        var extra = JsonParser.parseString(Files.readString(Path.of(args[3]))).getAsJsonObject();
        for (var item : extra.getAsJsonArray("entrySeeds")) {
            var entry = item.getAsJsonObject();
            if (!entry.get("processor").getAsString().equals(args[2])) continue;
            long raw = Long.decode(entry.get("address").getAsString());
            if (entry.get("mode").getAsString().equals("thumb")) raw |= 1L;
            seed(raw, entry.get("module").getAsString(), seeded);
        }
    }
}
"""
INVENTORY = """import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.program.model.address.AddressRange;
import com.google.gson.GsonBuilder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.HexFormat;
public class UtilityInventory extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        Path output = Path.of(args[0]);
        Path drafts = output.getParent().resolve("decompiled");
        Files.createDirectories(drafts);
        int remaining = Integer.parseInt(args[2]);
        var root = new LinkedHashMap<String,Object>();
        root.put("processor", args[1]);
        root.put("program", "dwc/utility.bin/move/child.srl");
        root.put("language", currentProgram.getLanguageID().toString());
        var memory = currentProgram.getMemory();
        var blocks = new ArrayList<Object>();
        for (var block : memory.getBlocks()) {
            var row = new LinkedHashMap<String,Object>();
            row.put("name", block.getName());
            row.put("address", "0x" + block.getStart().toString());
            row.put("bytes", block.getSize());
            row.put("execute", block.isExecute());
            row.put("initialized", block.isInitialized());
            if (block.isInitialized()) {
                byte[] bytes = new byte[(int)block.getSize()];
                memory.getBytes(block.getStart(), bytes);
                row.put("sha256", HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)));
            }
            blocks.add(row);
        }
        root.put("memoryBlocks", blocks);
        var functions = new ArrayList<Object>();
        var decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        var iterator = currentProgram.getFunctionManager().getFunctions(true);
        while (iterator.hasNext()) {
            var function = iterator.next();
            var entry = function.getEntryPoint();
            var block = memory.getBlock(entry);
            if (block == null || !block.isExecute() || !block.isInitialized()) continue;
            var row = new LinkedHashMap<String,Object>();
            row.put("module", block.getName());
            row.put("processor", args[1]);
            row.put("address", "0x" + entry.toString());
            row.put("name", function.getName());
            var mode = currentProgram.getProgramContext().getValue(currentProgram.getRegister("TMode"), entry, false);
            row.put("mode", mode != null && mode.intValue() == 1 ? "thumb" : "arm");
            row.put("bodyBytes", function.getBody().getNumAddresses());
            var ranges = new ArrayList<Object>();
            var body = function.getBody().getAddressRanges();
            while (body.hasNext()) {
                AddressRange range = body.next();
                ranges.add(new String[]{"0x" + range.getMinAddress().toString(), "0x" + range.getMaxAddress().add(1).toString()});
            }
            row.put("ranges", ranges);
            row.put("boundaryVerified", false);
            if (remaining-- > 0) {
                var result = decompiler.decompileFunction(function, 5, monitor);
                row.put("decompileCompleted", result.decompileCompleted());
                if (result.decompileCompleted()) {
                    Path file = drafts.resolve(entry.toString() + ".c");
                    Files.writeString(file, result.getDecompiledFunction().getC());
                    row.put("draft", file.toString());
                }
            }
            functions.add(row);
        }
        decompiler.dispose();
        root.put("functions", functions);
        root.put("sourceReconstructionComplete", false);
        Files.writeString(output, new GsonBuilder().setPrettyPrinting().create().toJson(root));
        println("UTILITY_INVENTORY " + args[1] + " " + functions.size());
    }
}
"""


def run(processor, decompile_limit):
    layout, materialized = utility_runtime.derive()
    proof = utility_dtcm_audit.derive()
    utility_dtcm_audit.OUTPUT.write_text(json.dumps(proof, indent=2) + "\n")
    utility_seeds.OUTPUT.write_text(json.dumps(utility_seeds.derive(), indent=2) + "\n")
    if json.loads(utility_runtime.OUTPUT.read_text()) != layout or any(path.read_bytes() != data for path, data in materialized.items()):
        raise ValueError("Utility runtime source inputs must be verified before analysis")
    if utility_runtime.sha(JAVA.read_bytes()) != "f961fb8db73c7c546821bc6d30fdaa8ce2458da460a5e75e2c39189cd107e6ba":
        raise ValueError("Utility Ghidra JVM identity changed")
    work = WORK / processor
    work.mkdir(parents=True, exist_ok=True)
    (work / "UtilitySeed.java").write_text(SEED)
    (work / "UtilityInventory.java").write_text(INVENTORY)
    vmargs = [line.split("=", 1)[1] for line in (GHIDRA / "support/launch.properties").read_text().splitlines()
              if line.startswith("VMARGS=") or line.startswith("VMARGS_WINDOWS=")]
    private = work / "profile"
    private.mkdir(exist_ok=True)
    vmargs.extend(["-Xmx2G", "-XX:ParallelGCThreads=2", "-XX:CICompilerCount=2", f"-Duser.home={private}"])
    for key in ("settingsdir", "cachedir", "tempdir"):
        path = private / key
        path.mkdir(exist_ok=True)
        vmargs.append(f"-Dapplication.{key}={path}")
    projects = work / "projects"
    projects.mkdir(exist_ok=True)
    implicit = "main" if processor == "arm9" else "boot"
    main_module = next(module for module in layout["modules"] if module["id"] == f"utility-child-{processor}-{implicit}")
    language = "ARM:LE:32:v5t" if processor == "arm9" else "ARM:LE:32:v4t"
    output = work / "inventory.json"
    command = [str(JAVA), *vmargs, "-cp", str(GHIDRA / "Ghidra/Framework/Utility/lib/Utility.jar"), "ghidra.Ghidra",
               "ghidra.app.util.headless.AnalyzeHeadless", str(projects), "utility-private", "-import", str(ROOT / main_module["binary"]),
               "-overwrite", "-loader", "BinaryLoader", "-loader-baseAddr", main_module["base"], "-processor", language, "-cspec", "default",
               "-scriptPath", str(work), "-preScript", "UtilitySeed.java", str(utility_runtime.OUTPUT), str(ROOT), processor, str(utility_seeds.OUTPUT), str(utility_dtcm_audit.OUTPUT),
               "-postScript", "UtilityInventory.java", str(output), processor, str(decompile_limit),
               "-analysisTimeoutPerFile", "120", "-max-cpu", "2", "-log", str(work / "analysis.log")]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors="replace", timeout=240)
    (work / "stdout.txt").write_text(result.stdout)
    (work / "stderr.txt").write_text(result.stderr)
    run_report = {"command": command, "exitCode": result.returncode, "javaSha256": utility_runtime.sha(JAVA.read_bytes()), "language": language}
    (work / "run.json").write_text(json.dumps(run_report, indent=2) + "\n")
    if result.returncode or not output.exists():
        raise ValueError("Utility Ghidra analysis did not produce an inventory")
    inventory = json.loads(output.read_text())
    blocks = {block["name"]: block for block in inventory["memoryBlocks"]}
    for module in layout["modules"]:
        if module["processor"] != processor:
            continue
        block = blocks[module["id"]]
        if block["sha256"] != module["sha256"] or int(block["address"], 0) != int(module["base"], 0):
            raise ValueError("Utility Ghidra analysis does not preserve the measured module mapping")
    out = ROOT / f"evidence/utility/ghidra-{processor}.json"
    out.write_text(json.dumps(inventory, indent=2) + "\n")
    return inventory


def publish():
    functions = []
    for processor in ("arm9", "arm7"):
        path = ROOT / f"evidence/utility/ghidra-{processor}.json"
        if not path.exists():
            continue
        inventory = json.loads(path.read_text())
        for entry in inventory["functions"]:
            functions.append({"program": utility_runtime.PROGRAM, "processor": processor, "module": entry["module"],
                              "address": entry["address"], "mode": entry["mode"],
                              "symbol": "func_" + entry["module"].replace("-", "_") + "_" + entry["address"][2:],
                              "size": None, "instructionBodyBytes": entry["bodyBytes"], "bodyRanges": entry["ranges"],
                              "boundaryVerified": False, "boundaryConfidence": "heuristic-ghidra-on-measured-embedded-runtime-map",
                              "evidence": path.relative_to(ROOT).as_posix()})
    report = {"schemaVersion": 1, "romSha256": utility_runtime.audit_regions.ROM_HASH, "program": utility_runtime.PROGRAM,
              "runtimeMappingCanonical": True, "functions": functions, "sourceReconstructionComplete": False,
              "limitations": ["Runtime map hashes are verified; all automatic functions, boundaries and inferred types remain candidates",
                              "Separate Ghidra projects retain both processor and embedded-program identity"]}
    (ROOT / "evidence/utility/runtime-functions.json").write_text(json.dumps(report, indent=2) + "\n")
    from reconcile_utility_inventory import main as reconcile
    report = reconcile()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processor", choices=["arm9", "arm7", "all"], default="all")
    parser.add_argument("--decompile-limit", type=int, default=40)
    args = parser.parse_args()
    for processor in (["arm9", "arm7"] if args.processor == "all" else [args.processor]):
        inventory = run(processor, args.decompile_limit)
        report = publish()
        print({"processor": processor, "candidates": len(inventory["functions"]), "combinedCandidates": len(report["functions"])}, flush=True)


if __name__ == "__main__":
    main()
