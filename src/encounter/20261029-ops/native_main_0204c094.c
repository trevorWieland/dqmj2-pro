#include "vm_context.h"
extern NativeValue *native_fn_0204be40(NativeVm *vm, u32 type, f32 index);
extern f32 native_fn_0204bde0(NativeVm *vm, u32 type, f32 value);
void native_main_0204c094(NativeVm *vm, const NativeInstruction *instruction)
{
    f32 right;
    f32 left;
    NativeValue *destination = native_fn_0204be40(vm, instruction->destination_type, instruction->destination_value);
    if (!destination)
        return;
    left = native_fn_0204bde0(vm, instruction->left_type, instruction->left_value);
    right = native_fn_0204bde0(vm, instruction->right_type, instruction->right_value);
    switch (instruction->opcode) {
    case 1046:
        destination->number = left + right;
        break;
    case 1047:
        destination->number = left - right;
        break;
    case 1048:
        destination->number = left * right;
        break;
    case 1049:
        destination->number = left / right;
        break;
    case 1050:
        destination->number = (f32)((s32)left % (s32)right);
        break;
    }
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
