#include "vm_context.h"
extern const u32 *native_fn_0203cf40(u32 source, u32 member, int context);
extern int native_fn_0204bc08(NativeVm *vm, const u32 *script);
int native_main_0204bc78(NativeVm *vm, u32 source, u32 member)
{
    int result = 0;
    if (!vm->active) {
        const u32 *script = native_fn_0203cf40(source, member, -1);
        if (script)
            result = native_fn_0204bc08(vm, script);
    }
    return result;
}
