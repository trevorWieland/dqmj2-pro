#include "record_lookup_abi.h"
extern u32 native_fn_02069068(s32 species, u32 form, u32 field1d, u32 id, s32 arg1, s32 arg2, s32 arg3, u32 arg4, u32 arg5, u32 arg6, u32 zero);
u32 native_main_020692b0(u32 id, s32 arg1, s32 arg2, s32 arg3, u8 arg4, u8 arg5, u8 arg6) {
    SavedRecord *first;
    SavedRecord *second;
    first = native_fn_02062a10(id);
    second = native_fn_02062a10(id);
    return native_fn_02069068(*(s16 *)((u8 *)first + 0x18), *((u8 *)second + 0x1A), *((u8 *)native_fn_02062a10(id) + 0x1D), id, arg1, arg2, arg3, arg4, arg5, arg6, 0);
}
