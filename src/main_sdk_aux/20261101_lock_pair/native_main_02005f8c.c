#include "native_lock_types.h"
u32 native_main_02005f8c(u32 identity,LockWord *record,LockCallback callback,s32 both) {
    u32 result;
    u32 previous;
    if (both != 0) {
        previous = native_fn_02008020();
    } else {
        previous = native_fn_02007ff4();
    }
    result = native_fn_02008f4c(identity,record);
    if (result == 0) {
        if (callback != 0) {
            callback();
        }
        record->owner = (u16)identity;
    }
    if (both != 0) {
        native_fn_02008034(previous);
    } else {
        native_fn_02008008(previous);
    }
    return result;
}
