#include "field_metadata.h"
extern const FieldRecord *native_fn_020c56b4(s32 id);
int native_main_020c57bc(void)
{
    int first;
    int second;
    s16 temporary;
    for (first = 0; first < 23; first++) {
        for (second = first + 1; second < 24; second++) {
            if (native_data_021d540c[first].id < native_data_021d540c[second].id) {
                temporary = native_data_021d540c[first].id;
                native_data_021d540c[first].id = native_data_021d540c[second].id;
                native_data_021d540c[second].id = temporary;
            }
        }
    }
    for (first = 0; first < 24; first++) {
        if (native_data_021d540c[first].id > 0)
            native_data_021d540c[first].record = *native_fn_020c56b4(native_data_021d540c[first].id);
    }
    return 0;
}
