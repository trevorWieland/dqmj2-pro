#include "kind_context.h"
extern const char native_data_020dda98[];
extern KindManager native_data_020f69ec;
extern KindFile *native_fn_0203cc2c(const char *name, s32 mode);
int native_main_02044998(s32 mode)
{
    KindFile *file = native_fn_0203cc2c(native_data_020dda98, mode);
    native_data_020f69ec.file = file;
    if (file != 0) {
        native_data_020f69ec.records = file->records;
        return 1;
    }
    return 0;
}
