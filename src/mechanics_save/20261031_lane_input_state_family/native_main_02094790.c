#include "family.h"
extern u32 native_fn_020946ec(s32);
extern u32 native_fn_0209477c(void);
void native_main_02094790(u32 value) {
    u8 *record=(u8 *)native_fn_020946ec(1);
    FIELD(record,u32,12)=value;
    record[10]=(u8)native_fn_0209477c();
}
