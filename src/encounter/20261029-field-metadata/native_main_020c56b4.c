#include "field_metadata.h"
extern int native_fn_020c5750(s16 id);
extern const FieldRecord *native_fn_020c5868(s16 id);
const FieldRecord *native_main_020c56b4(s32 id)
{
    if (native_data_021d5404.records != 0) {
        native_fn_020c5750((s16)id);
        return &native_data_021d5404.records[id];
    }
    return native_fn_020c5868((s16)id);
}
