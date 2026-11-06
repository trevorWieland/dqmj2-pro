#include "context.h"
void *native_main_02038eb4(s32 index)
{
    ResourceManager *manager = native_data_020f4c44;
    u32 relative = manager->blob8c->table14;
    OffsetTable *table = !relative ? 0 : (OffsetTable *)((u8 *)manager->blob8c + relative);
    u32 offset;
    ResourceBlob *base;
    if (!table) return 0;
    if (index < 0) return 0;
    if ((u32)index >= table->count) return 0;
    offset = table->offsets[index];
    base = manager->blob8c;
    return !offset ? 0 : (void *)((u8 *)base + offset);
}
