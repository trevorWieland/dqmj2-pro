#include "field_metadata.h"
extern const char native_data_020e2e40[];
extern FieldFile *native_fn_0203cc3c(const char *name, int mode);
int native_main_020c55dc(void)
{
    int index;
    FieldFile *file = native_fn_0203cc3c(native_data_020e2e40, 1);
    FieldRecord *record;
    CompactField *lookup;
    native_data_021d5404.file = file;
    if (file != 0) {
        record = file->records;
        native_data_021d5404.records = record;
        lookup = native_data_021d588c;
        index = 0;
        do {
            index++;
            lookup->id = record->word0;
            lookup->kind = record->byte4;
            lookup++;
            record++;
        } while (index < 1399);
        return 1;
    }
    return 0;
}
