#include "vm_context.h"
extern f32 native_fn_0204bde0(NativeVm *vm, u32 type, f32 value);
void native_main_0204c464(NativeVm *vm, const NativeInstruction *instruction)
{
    NativeVmThread *thread = &vm->threads[vm->thread];
    if (!thread->wait_phase) {
        thread->wait_count = (s32)native_fn_0204bde0(vm, instruction->destination_type, instruction->destination_value);
        thread->wait_phase = 10;
    }
    if (thread->wait_phase != 10)
        return;
    thread->wait_count--;
    if (thread->wait_count >= 0) {
        vm->threads[vm->thread].pending = 1;
        return;
    }
    vm->threads[vm->thread].pc += instruction->bytes;
    vm->threads[vm->thread].pending = 0;
    thread->wait_phase = 0;
}
