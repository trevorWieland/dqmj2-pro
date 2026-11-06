#include "vm_context.h"
extern u32 native_ov000_fn_02210b70(u32 value);
void native_main_02054f30(NativeVm *vm, const NativeInstruction *instruction)
{
    vm->arguments[0].number = (f32)native_ov000_fn_02210b70((u8)(u32)vm->arguments[0].number);
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
