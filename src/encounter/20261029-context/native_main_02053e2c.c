#include "vm_context.h"
extern const s16 *native_fn_0205bd60(void);
void native_main_02053e2c(NativeVm *vm, const NativeInstruction *instruction)
{
    s16 values[3];
    int index;
    for (index = 0; index < 3; index++) {
        s16 value = native_fn_0205bd60()[index];
        values[index] = value;
    }
    for (index = 0; index < 3; index++)
        vm->arguments[index] = (f32)values[index];
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
}
