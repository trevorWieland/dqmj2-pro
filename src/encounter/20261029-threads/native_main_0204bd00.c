#include "vm_context.h"
extern void *native_fn_02008d78(void *destination, int value, u32 bytes);
int native_main_0204bd00(NativeVm *vm, u32 entry)
{
    int result = 0;
    if (vm->active) {
        const s32 *data = (const s32 *)vm->source + entry;
        s32 pc = data[1];
        if (pc >= 0) {
            vm->entry = entry;
            vm->running = 1;
            native_fn_02008d78(vm->threads, 0, sizeof(vm->threads));
            native_fn_02008d78(vm->arguments, 0, sizeof(vm->arguments));
            vm->threads[0].pc = pc;
            vm->threads[0].active = 1;
            result = 1;
        }
    }
    return result;
}
