#include "vm_context.h"
void native_main_0204c510(NativeVm *vm)
{
    vm->threads[vm->thread].pending = 0;
    if (vm->threads[vm->thread].depth) {
        u32 pc = vm->threads[vm->thread].return_pc[vm->threads[vm->thread].depth - 1];
        vm->threads[vm->thread].depth--;
        vm->threads[vm->thread].pc = pc;
        return;
    }
    vm->threads[vm->thread].active = 0;
    if (!vm->thread)
        vm->running = 2;
    vm->threads[vm->thread].pending = 1;
}
