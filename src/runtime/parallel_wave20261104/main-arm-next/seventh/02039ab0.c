#include "context.h"
u32 native_main_02039ab0(void *output, s32 field9, s32 field4, s32 field8, s32 index)
{
    ResourceRecord *record = native_fn_02038d88(index);
    if (!record) return 0;
    if (field8 < 0) field8 = record->field8;
    if (field4 < 0) field4 = record->field4;
    if (field9 < 0) field9 = record->field9;
    return native_fn_02039ba0(output, field9, field4, field8, record, index);
}
