#include "vm_context.h"
extern int native_fn_0203d0cc(int index);
void native_main_02054980(NativeVm *vm, const NativeInstruction *instruction)
{
    vm->arguments[0] = (f32)native_fn_0203d0cc((int)vm->arguments[0]);
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
