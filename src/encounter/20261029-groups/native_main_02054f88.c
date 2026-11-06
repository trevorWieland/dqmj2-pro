#include "vm_context.h"
extern u32 native_ov000_fn_02210b88(void);
void native_main_02054f88(NativeVm *vm, const NativeInstruction *instruction)
{
    vm->arguments[0].number = (f32)native_ov000_fn_02210b88();
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
