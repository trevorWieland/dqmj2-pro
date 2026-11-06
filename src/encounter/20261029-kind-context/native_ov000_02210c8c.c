#include "kind_context.h"
extern const FieldRecord *native_fn_020c56b4(s32 id);
extern u32 native_fn_020c58c0(s32 id);
extern const KindRecord *native_fn_020449d4(u32 id);
extern s32 native_ov000_fn_021dfdc4(s32 key);
extern s32 native_ov000_fn_021e7b08(s32 key);
int native_ov000_02210c8c(s32 id)
{
    int count = 0;
    int key;
    key = native_fn_020c56b4(id)->byte6;
    if (key == 1)
        key = 150;
    else if (key == 2)
        key = 0;
    else if (key == 0)
        key = 151;
    else
        key = 0;
    if (key > 0 && native_ov000_fn_021e7b08(key))
        count++;
    key = native_fn_020449d4(native_fn_020c58c0((s16)id))->byte61;
    if (key > 0 && native_ov000_fn_021e7b08(native_ov000_fn_021dfdc4(key + 13)))
        count++;
    return count;
}
