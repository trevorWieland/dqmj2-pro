import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import arm7_runtime

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work/lowlevel-recovery/arm7-ghidra"
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
public class Arm7Seed extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        var layout = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        var memory = currentProgram.getMemory();
        var boot = memory.getBlocks()[0];
        memory.split(boot, toAddr(0x0238021cL));
        boot.setName("arm7-boot");
        boot.setExecute(true);
        var source = memory.getBlock(toAddr(0x0238021cL));
        source.setName("arm7-autoload-source");
        source.setExecute(false);
        clearListing(source.getStart(), source.getEnd());
        createData(source.getStart(), new ArrayDataType(ByteDataType.dataType, (int)source.getSize(), 1));
        for (var item : layout.getAsJsonArray("modules")) {
            var module = item.getAsJsonObject();
            String id = module.get("id").getAsString();
            Address start = toAddr(Long.decode(module.get("runtimeBase").getAsString()));
            if (!id.equals("arm7-boot")) {
                byte[] bytes = Files.readAllBytes(Path.of(args[1]).resolve(module.get("binary").getAsString()));
                var block = memory.createInitializedBlock(id, start, new ByteArrayInputStream(bytes), bytes.length, monitor, false);
                block.setRead(true);
                block.setWrite(true);
                block.setExecute(true);
                int bssBytes = module.get("bssBytes").getAsInt();
                if (bssBytes > 0) {
                    var bss = memory.createUninitializedBlock(id + "-bss", toAddr(Long.decode(module.get("bssStart").getAsString())), bssBytes, false);
                    bss.setRead(true);
                    bss.setWrite(true);
                    bss.setExecute(false);
                }
            }
            if (!module.get("runtimeEntry").isJsonNull()) {
                Address entry = toAddr(Long.decode(module.get("runtimeEntry").getAsString()));
                currentProgram.getProgramContext().setValue(currentProgram.getRegister("TMode"), entry, entry, BigInteger.ZERO);
                currentProgram.getSymbolTable().addExternalEntryPoint(entry);
                disassemble(entry);
                if (getFunctionAt(entry) == null) createFunction(entry, "native_" + id.replace('-', '_') + "_" + entry.toString());
            }
        }
    }
}
"""
INVENTORY = """import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import ghidra.program.model.address.AddressRange;
import ghidra.program.model.symbol.Reference;
import com.google.gson.GsonBuilder;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.HexFormat;
public class Arm7Inventory extends GhidraScript {
    public void run() throws Exception {
        String[] arguments = getScriptArgs();
        Path output = Path.of(arguments[0]);
        Path drafts = output.getParent().resolve("decompiled");
        Files.createDirectories(drafts);
        int remaining = Integer.parseInt(arguments[1]);
        var root = new LinkedHashMap<String,Object>();
        var memory = currentProgram.getMemory();
        byte[] binary = new byte[160048];
        memory.getBytes(toAddr(0x02380000L), binary);
        root.put("processor", "ARM7TDMI");
        root.put("language", currentProgram.getLanguageID().toString());
        root.put("baseAddress", "0x02380000");
        root.put("runtimeMappingCanonical", true);
        root.put("bytes", binary.length);
        root.put("sha256", HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(binary)));
        var blocks = new ArrayList<Object>();
        for (var block : memory.getBlocks()) {
            var row = new LinkedHashMap<String,Object>();
            row.put("name", block.getName());
            row.put("address", "0x" + Long.toHexString(block.getStart().getOffset()));
            row.put("bytes", block.getSize());
            row.put("initialized", block.isInitialized());
            row.put("executable", block.isExecute());
            if (block.isInitialized()) {
                byte[] body = new byte[(int)block.getSize()];
                memory.getBytes(block.getStart(), body);
                row.put("sha256", HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(body)));
            }
            blocks.add(row);
        }
        root.put("memoryBlocks", blocks);
        var rows = new ArrayList<Object>();
        var iterator = currentProgram.getFunctionManager().getFunctions(true);
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        while (iterator.hasNext()) {
            Function function = iterator.next();
            var row = new LinkedHashMap<String,Object>();
            var entry = function.getEntryPoint();
            String module = memory.getBlock(entry).getName();
            if (!module.equals("arm7-boot") && !module.equals("arm7-wram") && !module.equals("arm7-main")) continue;
            row.put("module", module);
            row.put("processor", "arm7");
            row.put("address", "0x" + Long.toHexString(entry.getOffset()));
            row.put("name", function.getName());
            BigInteger thumb = currentProgram.getProgramContext().getValue(currentProgram.getRegister("TMode"), entry, false);
            row.put("mode", thumb == null ? "unknown" : thumb.signum() == 0 ? "arm" : "thumb");
            row.put("bodyBytes", function.getBody().getNumAddresses());
            row.put("minimumAddress", "0x" + Long.toHexString(function.getBody().getMinAddress().getOffset()));
            row.put("maximumAddress", "0x" + Long.toHexString(function.getBody().getMaxAddress().getOffset()));
            var ranges = new ArrayList<Object>();
            for (AddressRange range : function.getBody().getAddressRanges()) {
                ranges.add(new String[]{"0x" + Long.toHexString(range.getMinAddress().getOffset()), "0x" + Long.toHexString(range.getMaxAddress().getOffset() + 1)});
            }
            row.put("ranges", ranges);
            var incoming = new ArrayList<Object>();
            for (Reference reference : getReferencesTo(entry)) {
                incoming.add(new String[]{reference.getFromAddress().toString(), reference.getReferenceType().toString()});
            }
            row.put("incomingReferences", incoming);
            row.put("boundaryVerified", false);
            if (remaining > 0) {
                DecompileResults result = decompiler.decompileFunction(function, 5, monitor);
                row.put("decompileCompleted", result.decompileCompleted());
                if (result.decompileCompleted()) {
                    Path draft = drafts.resolve(entry.toString() + ".c");
                    Files.writeString(draft, result.getDecompiledFunction().getC());
                    row.put("draft", draft.toString());
                } else row.put("decompileFailure", result.getErrorMessage());
                remaining--;
            }
            rows.add(row);
        }
        decompiler.dispose();
        root.put("functions", rows);
        root.put("functionCount", rows.size());
        root.put("sourceReconstruction", false);
        root.put("limitations", new String[]{"Automatic function boundaries and types remain heuristic", "Decompiler C is an unaccepted draft until compiler and native comparisons pass"});
        Files.writeString(output, new GsonBuilder().setPrettyPrinting().create().toJson(root));
        println("ARM7_INVENTORY " + rows.size());
    }
}
"""


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publish(inventory):
    layout = json.loads(arm7_runtime.MANIFEST.read_text())
    if not inventory.get("runtimeMappingCanonical") or inventory["sha256"] != layout["imageSha256"]:
        raise ValueError("Cannot publish a raw-file ARM7 inventory as runtime functions")
    blocks = {block["name"]: block for block in inventory["memoryBlocks"]}
    for module in layout["modules"]:
        block = blocks[module["id"]]
        if block["sha256"] != module["sha256"] or int(block["address"], 0) != int(module["runtimeBase"], 0):
            raise ValueError("Canonical ARM7 Ghidra memory mapping differs: " + module["id"])
    functions = []
    for function in inventory["functions"]:
        module = next(module for module in layout["modules"] if module["id"] == function["module"])
        address = int(function["address"], 0)
        if not int(module["runtimeBase"], 0) <= address < int(module["runtimeEnd"], 0):
            raise ValueError("Function entry lies outside its ARM7 runtime module")
        functions.append({"module": module["id"], "processor": "arm7", "address": hex(address),
                          "mode": function["mode"], "size": None,
                          "symbol": "func_" + module["id"].replace("-", "_") + f"_{address:08x}",
                          "instructionBodyBytes": function["bodyBytes"], "bodyRanges": function["ranges"],
                          "boundaryVerified": False, "boundaryConfidence": "heuristic-ghidra-armv4t-runtime-map",
                          "evidence": "evidence/arm7/ghidra-runtime-inventory.json",
                          "unknowns": ["complete function and literal-pool extent", "semantic types", "compiler configuration"]})
    report = {"schemaVersion": 1, "processor": "arm7", "imageSha256": layout["imageSha256"],
              "runtimeMappingCanonical": True, "functionCount": len(functions), "functions": functions,
              "limitations": ["Runtime module addresses are established by native loader tracing", "Function discovery, body boundaries and modes remain analysis candidates until independently validated"]}
    out = ROOT / "evidence/arm7"
    out.mkdir(parents=True, exist_ok=True)
    (out / "ghidra-runtime-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
    (out / "runtime-functions.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--decompile-limit", type=int, default=0)
    args = parser.parse_args()
    binary = ROOT / "extract/arm7/arm7.bin"
    if sha(binary) != "9f40087972ccb8b89d4cc4baf8288123e26a479bb43fa68b18a30a59650633a1":
        raise ValueError("ARM7 inventory input namespace differs")
    layout = arm7_runtime.derive(binary.read_bytes())
    if json.loads(arm7_runtime.MANIFEST.read_text()) != layout:
        raise ValueError("ARM7 runtime layout must be regenerated and verified first")
    for module in layout["modules"]:
        if sha(ROOT / module["binary"]) != module["sha256"]:
            raise ValueError("ARM7 split input differs")
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "Arm7Seed.java").write_text(SEED)
    (WORK / "Arm7Inventory.java").write_text(INVENTORY)
    vmargs = [line.split("=", 1)[1] for line in (GHIDRA / "support/launch.properties").read_text().splitlines()
              if line.startswith("VMARGS=") or line.startswith("VMARGS_WINDOWS=")]
    private = WORK / "profile"
    private.mkdir(exist_ok=True)
    vmargs.extend(["-Xmx2G", "-XX:ParallelGCThreads=2", "-XX:CICompilerCount=2", f"-Duser.home={private}"])
    for key in ("settingsdir", "cachedir", "tempdir"):
        path = private / key
        path.mkdir(exist_ok=True)
        vmargs.append(f"-Dapplication.{key}={path}")
    projects = WORK / "projects"
    projects.mkdir(exist_ok=True)
    output = WORK / "inventory.json"
    if output.exists() and not json.loads(output.read_text()).get("runtimeMappingCanonical"):
        archive = WORK / "raw-container-inventory.json"
        if not archive.exists():
            archive.write_bytes(output.read_bytes())
    command = [str(JAVA), *vmargs, "-cp", str(GHIDRA / "Ghidra/Framework/Utility/lib/Utility.jar"),
               "ghidra.Ghidra", "ghidra.app.util.headless.AnalyzeHeadless", str(projects), "arm7-private",
               "-import", str(binary), "-overwrite", "-loader", "BinaryLoader", "-loader-baseAddr", "0x02380000",
               "-processor", "ARM:LE:32:v4t", "-cspec", "default", "-scriptPath", str(WORK),
               "-preScript", "Arm7Seed.java", str(arm7_runtime.MANIFEST), str(ROOT),
               "-postScript", "Arm7Inventory.java", str(output), str(args.decompile_limit),
               "-analysisTimeoutPerFile", "120", "-max-cpu", "2", "-log", str(WORK / "analysis.log")]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors="replace", timeout=240)
    (WORK / "stdout.txt").write_text(result.stdout)
    (WORK / "stderr.txt").write_text(result.stderr)
    report = {"schemaVersion": 1, "command": command, "exitCode": result.returncode, "inputSha256": sha(binary),
              "javaSha256": sha(JAVA), "language": "ARM:LE:32:v4t", "outputProduced": output.exists()}
    if output.exists():
        inventory = json.loads(output.read_text())
        if inventory["sha256"] != sha(binary):
            raise ValueError("Ghidra ARM7 import bytes changed")
        report["functionCount"] = inventory["functionCount"]
        report["inventorySha256"] = sha(output)
        publish(inventory)
    (WORK / "run.json").write_text(json.dumps(report, indent=2) + "\n")
    print({key: value for key, value in report.items() if key != "command"})
    if result.returncode or not output.exists():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
