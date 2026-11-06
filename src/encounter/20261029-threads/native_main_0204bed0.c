#include "vm_context.h"
extern int native_fn_0204bea0(NativeVm *vm);
extern void *native_fn_02008d78(void *destination, int value, u32 bytes);
int native_main_0204bed0(NativeVm *vm, u32 pc, u32 unused)
{
    int index = native_fn_0204bea0(vm);
    if (index > 0) {
        NativeVmThread *thread = &vm->threads[index];
        native_fn_02008d78(thread, 0, sizeof(*thread));
        thread->active = 1;
        thread->pc = pc;
    }
    return index;
}
