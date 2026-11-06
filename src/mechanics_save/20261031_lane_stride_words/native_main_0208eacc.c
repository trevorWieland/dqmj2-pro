#include "stride_words.h"
extern const u32 *native_data_020de7cc;
extern u32 native_data_021cfd48;
extern u32 native_data_021cfd14;
extern u32 native_data_021cfd24;
typedef struct {
    u32 field_0;
    u32 field_4;
} WordPair;
extern WordPair native_data_021cfd58;
typedef struct {
    u32 unknown_0[2];
    u32 field_8;
} FlagWords;
extern FlagWords native_data_021d1540;

u32 native_main_0208eacc(void) {
    u32 value;
    native_data_021cfd48=native_data_020de7cc[1];
    native_data_021cfd14=native_data_020de7cc[2];
    native_data_021cfd24=native_data_020de7cc[3];
    native_data_021cfd58.field_0=native_data_020de7cc[4];
    native_data_021cfd58.field_4=native_data_020de7cc[5];
    value=2|native_data_021d1540.field_8;
    native_data_021d1540.field_8=value;
    return value;
}
