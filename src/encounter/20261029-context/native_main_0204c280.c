#include "vm_context.h"
extern f32 native_fn_0204bde0(NativeVm *vm, u32 type, f32 value);
void native_main_0204c280(NativeVm *vm, const NativeInstruction *instruction)
{
    f32 left = native_fn_0204bde0(vm, instruction->left_type, instruction->left_value);
    f32 right = native_fn_0204bde0(vm, instruction->right_type, instruction->right_value);
    switch (instruction->opcode) {
    case 1039:
        vm->condition = left == right;
        break;
    case 1040:
        vm->condition = left != right;
        break;
    case 1041:
        vm->condition = left > right;
        break;
    case 1042:
        vm->condition = left < right;
        break;
    case 1043:
        vm->condition = left >= right;
        break;
    case 1044:
        vm->condition = left <= right;
        break;
    default:
        vm->condition = 0;
        break;
    }
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
