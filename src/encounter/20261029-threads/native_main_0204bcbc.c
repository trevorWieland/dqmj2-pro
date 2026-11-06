#include "vm_context.h"
extern void native_fn_0203cf9c(int context, const void *script);
int native_main_0204bcbc(NativeVm *vm)
{
    int result = 0;
    if (vm->active) {
        if (vm->source) {
            native_fn_0203cf9c(-1, vm->source);
            vm->source = 0;
        }
        vm->active = 0;
        result = 1;
    }
    return result;
}
