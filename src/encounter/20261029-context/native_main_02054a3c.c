#include "vm_context.h"
extern int native_fn_02063c00(int index, int value);
void native_main_02054a3c(NativeVm *vm, const NativeInstruction *instruction)
{
    int index = (int)vm->arguments[0];
    int value = (int)vm->arguments[1];
    native_fn_02063c00(index, value);
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
