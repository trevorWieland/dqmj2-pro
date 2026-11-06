#include "family.h"
typedef unsigned long long u64;
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern void native_fn_02007e10(void *);
extern void native_fn_02007da4(void *,u64,void (*)(void *),void *);
extern void native_fn_0208a660(void *);
void native_main_0208a5ac(u32 value) {
    u32 irq=native_fn_02007ff4();
    if (FIELD(native_data_021cfcb4,u32,0x2260)==9 && value!=9) {
        native_fn_02007e10(native_data_021cfcb4+0x22CC);
    }
    if (FIELD(native_data_021cfcb4,u32,0x2260)!=11) {
        FIELD(native_data_021cfcb4,u32,0x2260)=value;
    }
    if (value==9) {
        native_fn_02007da4(native_data_021cfcb4+0x22CC,0x022F5341ULL,native_fn_0208a660,0);
    }
    native_fn_02008008(irq);
}
