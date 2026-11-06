#include "vm_context.h"
void native_main_0204c3ac(NativeVm *vm, const NativeInstruction *instruction)
{
    u32 next = vm->threads[vm->thread].pc;
    next += instruction->bytes;
    vm->threads[vm->thread].return_pc[vm->threads[vm->thread].depth] = next;
    vm->threads[vm->thread].depth++;
    vm->threads[vm->thread].pc = instruction->left_type;
    vm->threads[vm->thread].pending = 0;
}
