#include "vm_context.h"
extern int native_fn_0204c5a0(NativeVm *vm);
extern int native_fn_0205a65c(NativeVm *vm);
extern void native_fn_0204bd68(NativeVmThread *thread);
int native_main_0204bd6c(NativeVm *vm)
{
    int index;
    NativeVmThread *thread = vm->threads;
    for (index = 0; index < 4; index++, thread++) {
        if (thread->active) {
            vm->thread = index;
            for (;;) {
                if (!native_fn_0204c5a0(vm))
                    native_fn_0205a65c(vm);
                if (thread->pending)
                    break;
                native_fn_0204bd68(thread);
            }
        }
    }
    return vm->running == 2;
}
