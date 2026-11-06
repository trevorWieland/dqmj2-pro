#include "context.h"
u32 native_main_02039b20(void *output, s32 index, s32 subindex)
{
    u32 *info = native_fn_02038dec(index);
    void *archive;
    ResourceRecord *record;
    if (!info) return 0;
    archive = native_fn_0203917c(*info);
    if (!archive) return 0;
    record = native_fn_020389f4(archive, subindex);
    if (!record) return 0;
    return native_fn_02039c9c(output, record->field9, record->field4, record->field8, record, archive, index, subindex);
}
