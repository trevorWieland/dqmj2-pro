#include "vm_context.h"
extern void native_fn_0204bf1c(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204bf54(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204bf7c(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204bfd4(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c02c(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c094(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c1b8(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c280(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c3ac(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c418(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c464(NativeVm *vm, const NativeInstruction *instruction);
extern void native_fn_0204c510(NativeVm *vm);
int native_main_0204c5a0(NativeVm *vm)
{
    int result = 1;
    u32 pc = vm->threads[vm->thread].pc;
    const u8 *code = vm->code;
    switch (*(const u32 *)(code + pc)) {
    case 1024:
        native_fn_0204bf1c(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1036:
        native_fn_0204bf54(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1037:
        native_fn_0204bf7c(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1038:
        native_fn_0204bfd4(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1045:
        native_fn_0204c02c(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1046:
    case 1047:
    case 1048:
    case 1049:
    case 1050:
        native_fn_0204c094(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1051:
    case 1052:
    case 1053:
        native_fn_0204c1b8(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1039:
    case 1040:
    case 1041:
    case 1042:
    case 1043:
    case 1044:
        native_fn_0204c280(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1033:
        native_fn_0204c3ac(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1034:
        native_fn_0204c418(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1035:
        native_fn_0204c464(vm, (const NativeInstruction *)(code + pc));
        break;
    case 1026:
        native_fn_0204c510(vm);
        break;
    default:
        result = 0;
        break;
    }
    return result;
}
