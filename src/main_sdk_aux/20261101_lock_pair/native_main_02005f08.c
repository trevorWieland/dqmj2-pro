#include "native_lock_types.h"
u32 native_main_02005f08(s32 identity,LockWord *record,LockCallback callback,s32 both) {
    u32 previous;
    if (identity != record->owner) {
        return 0xFFFFFFFEU;
    }
    if (both != 0) {
        previous = native_fn_02008020();
    } else {
        previous = native_fn_02007ff4();
    }
    record->owner = 0;
    if (callback != 0) {
        callback();
    }
    record->flag = 0;
    if (both != 0) {
        native_fn_02008034(previous);
    } else {
        native_fn_02008008(previous);
    }
    return 0;
}
