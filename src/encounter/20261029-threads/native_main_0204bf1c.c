#include "vm_context.h"
void native_main_0204bf1c(NativeVm *vm, const NativeInstruction *instruction)
{
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
