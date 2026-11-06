#include "field_metadata.h"
extern void native_fn_0203cf9c(int mode, FieldFile *file);
int native_main_020c5678(void)
{
    if (native_data_021d5404.file == 0)
        return 0;
    native_fn_0203cf9c(1, native_data_021d5404.file);
    native_data_021d5404.file = 0;
    native_data_021d5404.records = 0;
    return 1;
}
