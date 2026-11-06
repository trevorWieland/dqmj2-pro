#include "vm_context.h"
typedef struct { u32 opcode; u32 bytes; u32 pc; u32 unused; } NativeForkInstruction;
extern int native_fn_0204bed0(NativeVm *vm, u32 pc, u32 unused);
void native_main_0204c418(NativeVm *vm, const NativeForkInstruction *instruction)
{
    native_fn_0204bed0(vm, instruction->pc, instruction->unused);
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
