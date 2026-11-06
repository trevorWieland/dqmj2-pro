#include "vm_context.h"
extern f32 *native_fn_0204be40(NativeVm *vm, u32 type, f32 index);
extern f32 native_fn_0204bde0(NativeVm *vm, u32 type, f32 value);
void native_main_0204c02c(NativeVm *vm, const NativeInstruction *instruction)
{
    f32 *destination = native_fn_0204be40(vm, instruction->left_type, instruction->left_value);
    if (!destination)
        return;
    *destination = native_fn_0204bde0(vm, instruction->right_type, instruction->right_value);
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
