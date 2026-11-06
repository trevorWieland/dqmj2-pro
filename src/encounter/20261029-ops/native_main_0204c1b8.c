#include "vm_context.h"
extern NativeValue *native_fn_0204be40(NativeVm *vm, u32 type, f32 index);
extern f32 native_fn_0204bde0(NativeVm *vm, u32 type, f32 value);
void native_main_0204c1b8(NativeVm *vm, const NativeInstruction *instruction)
{
    u32 left;
    NativeValue *destination = native_fn_0204be40(vm, instruction->destination_type, instruction->destination_value);
    u32 right;
    if (!destination)
        return;
    left = (u32)native_fn_0204bde0(vm, instruction->left_type, instruction->left_value);
    right = (u32)native_fn_0204bde0(vm, instruction->right_type, instruction->right_value);
    switch (instruction->opcode) {
    case 1051:
        destination->bits = left & right;
        break;
    case 1052:
        destination->bits = left | right;
        break;
    case 1053:
        destination->bits = left ^ right;
        break;
    }
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
