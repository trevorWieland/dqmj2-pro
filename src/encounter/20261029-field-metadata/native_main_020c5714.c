#include "field_metadata.h"
int native_main_020c5714(s32 id)
{
    int index;
    int found = 0;
    for (index = 0; index < 24; index++) {
        if (native_data_021d540c[index].id == id)
            found = 1;
    }
    return found;
}
