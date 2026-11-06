import json
import random
import struct
from pathlib import Path
import utility_runtime
import match_lowlevel
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "evidence/utility/dtcm-data-proof.json"
MODULE = "utility-child-arm9-dtcm"


def instruction(binary, base, address, mnemonic, operands):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoded = next(decoder.disasm(binary[address - base:address - base + 4], address))
    if decoded.mnemonic != mnemonic or decoded.op_str != operands:
        raise ValueError("Native DTCM classification configuration/consumer instruction changed")
    return {"address": hex(address), "instruction": decoded.mnemonic + " " + decoded.op_str, "sha256": utility_runtime.sha(decoded.bytes)}


def irq_case(modules, files, words, enabled, active):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address, size in [(0x01FF8000, 0x8000), (0x02000000, 0x800000), (0x03000000, 0x20000), (0x04000000, 0x2000), (0x05000000, 0x1000)]:
        engine.mem_map(address, size)
    for module in modules:
        if module["processor"] == "arm9":
            engine.mem_write(int(module["base"], 0), bytes(files[ROOT / module["binary"]]))
    engine.mem_write(0x04000208, struct.pack("<I", enabled))
    engine.mem_write(0x04000210, struct.pack("<II", active, active))
    engine.reg_write(UC_ARM_REG_CPSR, 0x12)
    rng = random.Random(20261027 + active + enabled)
    for register in match_lowlevel.REGISTERS:
        engine.reg_write(register, rng.getrandbits(32))
    engine.reg_write(UC_ARM_REG_SP, 0x0301FFF0)
    engine.reg_write(UC_ARM_REG_LR, 0x05000000)
    selected = (active & -active).bit_length() - 1 if active and enabled else None
    target = words[selected] if selected is not None else 0x05000000
    if target == 0:
        raise ValueError("IRQ table test must not invoke an uninstalled NULL handler")
    reads, writes, visited = [], [], []
    def read(uc, access, address, size, value, user):
        if 0x027E0000 <= address < 0x027E0080:
            reads.append({"address": hex(address), "bytes": size, "value": hex(int.from_bytes(uc.mem_read(address, size), "little"))})
    def code(uc, address, size, user):
        visited.append(address)
        if address == target & ~1:
            uc.emu_stop()
    engine.hook_add(UC_HOOK_MEM_READ, read)
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append({"address": hex(address), "bytes": size, "value": hex(value)}))
    engine.hook_add(UC_HOOK_CODE, code)
    engine.emu_start(0x01FF8000, 0x05000000, count=200)
    if engine.reg_read(UC_ARM_REG_PC) != target & ~1 or any(0x027E0000 <= address < 0x027E0080 for address in visited):
        raise ValueError("Native IRQ path entered the data image or failed to reach its installed handler")
    expected = [] if selected is None else [{"address": hex(0x027E0000 + selected * 4), "bytes": 4, "value": hex(target)}]
    if reads != expected or any(0x027E0000 <= int(write["address"], 0) < 0x027E0080 for write in writes):
        raise ValueError("Native IRQ consumer did not use the selected DTCM slot strictly as pointer data")
    if selected is not None and not engine.reg_read(UC_ARM_REG_CPSR) & 0x20:
        raise ValueError("Native IRQ handler pointer lost its measured Thumb interworking state")
    return {"ime": enabled, "pendingMask": hex(active), "selectedIndex": selected, "target": hex(target), "dtcmReads": reads,
            "visitedInstructionAddresses": [hex(address) for address in visited], "writes": writes, "handlerBodyExecuted": False}


def derive():
    layout, files = utility_runtime.derive()
    modules = {module["id"]: module for module in layout["modules"]}
    module = modules[MODULE]
    if module["processor"] != "arm9" or int(module["base"], 0) != 0x027E0000 or module["bytes"] != 96 or module["bssBytes"] != 32 or module["runtimeEntry"] is not None:
        raise ValueError("DTCM audit requires the measured ARM9 data-loader extent")
    binary = bytes(files[ROOT / module["binary"]])
    main = bytes(files[ROOT / modules["utility-child-arm9-main"]["binary"]])
    itcm = bytes(files[ROOT / modules["utility-child-arm9-itcm"]["binary"]])
    words = list(struct.unpack("<24I", binary))
    rows = []
    for index, value in enumerate(words):
        destination = next((item for item in layout["modules"] if item["processor"] == "arm9" and int(item["base"], 0) <= value & ~1 < int(item["runtimeEnd"], 0)), None) if value else None
        if value and (not value & 1 or destination is None or destination["id"] == MODULE):
            raise ValueError("Native initialized DTCM is not the measured external Thumb-handler pointer table")
        rows.append({"index": index, "address": hex(0x027E0000 + index * 4), "bytes": 4, "value": hex(value),
                     "kind": "Thumb-function-pointer" if value else "NULL-handler-slot", "targetModule": destination["id"] if destination else None,
                     "targetProcessor": "arm9" if destination else None, "targetProgram": utility_runtime.PROGRAM if destination else None})
    if len([value for value in words if value]) != 22 or words[-2:] != [0, 0]:
        raise ValueError("DTCM installed/NULL handler slot composition changed")
    base_word = struct.unpack_from("<I", main, 0xB94)[0]
    clear_mask, enable_mask = struct.unpack_from("<I", main, 0xB80)[0], struct.unpack_from("<I", main, 0xBAC)[0]
    region = base_word | 0xA
    size = 512 << ((region >> 1) & 31)
    if base_word != 0x027E0000 or size != 0x4000 or clear_mask & 0xF0000 != 0xF0000 or enable_mask & 0xF0000 != 0x50000:
        raise ValueError("Native DTCM base/size/enable/load configuration changed")
    configuration = [instruction(main, 0x02000000, address, mnemonic, operands) for address, mnemonic, operands in
                     [(0x02000B38, "ldr", "r0, [pc, #0x54]"), (0x02000B3C, "orr", "r0, r0, #0xa"), (0x02000B40, "mcr", "p15, #0, r0, c9, c1, #0"),
                      (0x02000B34, "mcr", "p15, #0, r0, c9, c1, #1"), (0x02000B78, "mcr", "p15, #0, r0, c1, c0, #0")]]
    consumers = [instruction(itcm, 0x01FF8000, address, mnemonic, operands) for address, mnemonic, operands in
                 [(0x01FF8040, "ldr", "r1, [pc, #8]"), (0x01FF8044, "ldr", "r0, [r1, r0, lsl #2]"), (0x01FF804C, "bx", "r0"),
                  (0x01FF8058, "ldr", "ip, [pc, #0x144]"), (0x01FF8060, "ldr", "ip, [ip]"), (0x01FF8094, "str", "r3, [ip]"),
                  (0x01FF8098, "str", "r3, [ip, #4]")]]
    if struct.unpack_from("<I", itcm, 0x50)[0] != 0x027E0000 or struct.unpack_from("<I", itcm, 0x1A4)[0] != 0x027E0060:
        raise ValueError("Native IRQ handler table or queue-state data literal changed")
    census_path = ROOT / "evidence/utility/runtime-functions.json"
    census = json.loads(census_path.read_text()) if census_path.exists() else {"program": layout["program"], "romSha256": layout["romSha256"], "functions": []}
    if census["program"] != layout["program"] or census["romSha256"] != layout["romSha256"]:
        raise ValueError("DTCM reference census has a different program namespace")
    entries, branches, literals, inspected = [], [], [], 0
    for function in census["functions"]:
        if function["processor"] != "arm9":
            continue
        if function["module"] == MODULE:
            entries.append(function)
        code_module = modules[function["module"]]
        payload, base = bytes(files[ROOT / code_module["binary"]]), int(code_module["base"], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if function["mode"] == "thumb" else CS_MODE_ARM)
        decoder.detail = True
        for begin, end in function["bodyRanges"]:
            for decoded in decoder.disasm(payload[int(begin, 0) - base:int(end, 0) - base], int(begin, 0)):
                inspected += 1
                if (decoded.group(CS_GRP_CALL) or decoded.group(CS_GRP_JUMP)) and decoded.operands and decoded.operands[0].type == 2 and 0x027E0000 <= decoded.operands[0].imm & ~1 < 0x027E0080:
                    branches.append({"module": function["module"], "address": hex(decoded.address), "target": hex(decoded.operands[0].imm)})
    for code_module in layout["modules"]:
        if code_module["processor"] != "arm9":
            continue
        payload = bytes(files[ROOT / code_module["binary"]])
        for offset in range(0, len(payload) - 3, 4):
            value = struct.unpack_from("<I", payload, offset)[0]
            if 0x027E0000 <= value & ~1 < 0x027E0080:
                literals.append({"module": code_module["id"], "address": hex(int(code_module["base"], 0) + offset), "value": hex(value),
                                 "kind": "stored-address-value-not-automatically-code-entry"})
    vectors = [(1, 1 << bit) for bit in range(22)] + [(1, mask) for mask in (3, 0x201, 0x210000, 0x3FFFFF)] + [(0, 1), (1, 0)]
    cases = [irq_case(layout["modules"], files, words, enabled, active) for enabled, active in vectors]
    supported = not entries and not branches
    return {"schemaVersion": 1, "romSha256": layout["romSha256"], "program": layout["program"], "processor": "arm9", "module": MODULE,
            "inputModuleSha256": module["sha256"], "dataOnlyAsLoaded": supported, "supportsNonExecutableAnalysisBlock": supported,
            "classification": "verified-IRQ-pointer-table-and-zeroed-queue-storage-as-loaded" if supported else "unresolved-control-entry-conflict",
            "functionInventoryStatus": "data-only-verified-as-loaded" if supported else "pending-qualified-analysis",
            "initializedDataBytes": 96, "bssDataBytes": 32, "initializedCodeBytes": 0 if supported else None,
            "functionSourceCredit": 0, "sourceReconstructionComplete": False,
            "loaderDescriptor": next(descriptor for processor in layout["processors"] if processor["processor"] == "arm9" for descriptor in processor["descriptors"] if int(descriptor["runtimeAddress"], 0) == 0x027E0000),
            "configuredDtcm": {"base": hex(base_word), "regionRegister": hex(region), "visibleBytes": size, "controlClearMask": hex(clear_mask), "controlEnableMask": hex(enable_mask),
                               "enabled": True, "loadMode": False, "itcmVisibleRange": ["0x00000000", "0x02000000"], "instructions": configuration},
            "positiveDataUses": consumers, "handlerSlots": rows, "installedHandlerWords": 22, "nullHandlerWords": 2, "distinctHandlers": len(set(words) - {0}),
            "queueBss": {"address": "0x027e0060", "bytes": 32, "loaderInitialValue": 0, "observedUses": "IRQ continuation reads queue head and clears head/tail words; remaining allocation is loader-zeroed storage"},
            "nativeConsumerOracle": {"vectors": len(cases), "cases": cases, "allInstalledSlotsReadAsData": True, "handlerBodiesExecuted": False,
                                     "physicalTcmAndInterruptDeliveryEmulated": False},
            "scopedReferences": {"inventory": census_path.relative_to(ROOT).as_posix(), "functionRowsSha256": utility_runtime.sha(json.dumps(census["functions"], sort_keys=True).encode()),
                                  "inventoryAvailable": census_path.exists(),
                                  "candidateInstructionsInspected": inspected, "candidateEntries": entries, "directBranchesIntoLoadedDataOrBss": branches, "storedAddressValues": literals,
                                  "absenceOfGhidraFunctionsAloneIsNotDataProof": True},
            "architectureReference": {"title": "ARM946E-S Technical Reference Manual", "document": "ARM DDI 0201D", "sections": ["2.3.2/control bits16-19", "2.3.12/TCM region registers", "5.2.1-5.2.8"],
                                      "url": "https://documentation-service.arm.com/static/5e8e3ee588295d1e18d3aa82", "pdfSha256": "fb45e13849688dcb8165cdf1c5ce0849492a64712ac5f094eecc23955a6d043f",
                                      "inference": "Measured native configuration enables the separate data TCM for data loads/stores; its loaded pointer table is separate from the ITCM instruction-fetch region"},
            "limitations": ["This classifies the128-byte ARM9 DTCM loader image under its measured startup configuration, not arbitrary future memory contents",
                            "A later CP15 remap, fabricated computed target or copying data elsewhere is not excluded by the scoped static reference scan",
                            "Instruction fetch through external memory at a numerically overlapping address is not equated with executing this private DTCM data image",
                            "ARM7 main at027e0000 is a different processor-qualified executable image and is never included in this ARM9 data classification",
                            "Ghidra’s previous nonexecute-by-module-suffix decision is treated as an analysis configuration, not evidence of data-only status"],
            "reproduce": ["python", "utility_dtcm_audit.py"]}


def main():
    report = derive()
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    if not report["dataOnlyAsLoaded"]:
        raise ValueError("DTCM data-only reconciliation found a qualified entry conflict")
    print({"initializedDataBytes": 96, "zeroedDataBytes": 32, "nativeConsumerVectors": report["nativeConsumerOracle"]["vectors"], "dataOnlyAsLoaded": True})


if __name__ == "__main__":
    main()
