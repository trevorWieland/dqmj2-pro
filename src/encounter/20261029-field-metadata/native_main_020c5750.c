#include "field_metadata.h"
extern int native_fn_020c5714(s32 id);
int native_main_020c5750(s16 id)
{
    int index;
    int inserted = 0;
    for (index = 0; index < 24; index++) {
        if (id >= 0 && !native_fn_020c5714(id) && native_data_021d540c[index].id <= 0) {
            native_data_021d540c[index].id = id;
            inserted = 1;
            break;
        }
    }
    return inserted;
}
