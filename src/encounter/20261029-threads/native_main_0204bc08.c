#include "vm_context.h"
extern void *native_fn_02008d78(void *destination, int value, u32 bytes);
int native_main_0204bc08(NativeVm *vm, const u32 *script)
{
    int result = 0;
    vm->source = script;
    if (script[0] == 0x00524353) {
        vm->code = script + 1025;
        vm->active = 1;
        native_fn_02008d78(vm->threads, 0, sizeof(vm->threads));
        native_fn_02008d78(vm->arguments, 0, sizeof(vm->arguments));
        native_fn_02008d78(vm->variables, 0, sizeof(vm->variables));
        result = 1;
    }
    return result;
}
