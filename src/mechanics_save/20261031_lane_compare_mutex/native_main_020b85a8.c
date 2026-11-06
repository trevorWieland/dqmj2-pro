#include "compare_mutex.h"
extern s32 native_fn_0201d800(const u8 *left,const u8 *right);
typedef struct {
    u8 unknown_0[0x7C];
    const u8 *field_7c;
} Prefix20E277C;
extern Prefix20E277C native_data_020e277c;
extern const u8 *native_data_020e27fc;

u32 native_main_020b85a8(const u8 *value) {
    if ((native_fn_0201d800(value,native_data_020e277c.field_7c)==0)||(native_fn_0201d800(value,native_data_020e27fc)==0)) return 1;
    return 0;
}
