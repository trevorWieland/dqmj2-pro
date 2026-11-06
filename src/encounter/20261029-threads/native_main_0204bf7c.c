#include "vm_context.h"
void native_main_0204bf7c(NativeVm *vm, const NativeInstruction *instruction)
{
    if (vm->condition)
        vm->threads[vm->thread].pc = instruction->left_type;
    else
        vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
