/* Four-way dispatch on a small selector, defaulting to 0x02008430.
   Unknowns: what the four branches produce and the selector domain. */
#include "context.h"
void native_fn_02008430(void);
void native_fn_02004e58(const void *, u32, u32);
void native_fn_02004f18(const void *, u32, u32);
void native_fn_02004fd8(const void *, u32, u32);
void native_fn_02005098(const void *, u32, u32);
void native_fn_02004eb8(const void *, u32, u32);
void native_fn_02004f78(const void *, u32, u32);
void native_fn_02005038(const void *, u32, u32);
void native_fn_020050f8(const void *, u32, u32);
void *native_fn_020040ec(void);
void *native_fn_02004140(void);
void *native_fn_02004194(void);
void *native_fn_02004224(void);
void *native_fn_02004120(void);
void *native_fn_02004174(void);
void *native_fn_020041e4(void);
void *native_fn_0200427c(void);
void native_fn_02004b58(const void *, u32, u32);
void native_fn_02004c18(const void *, u32, u32);
void native_fn_02004cd8(const void *, u32, u32);
void native_fn_02004d98(const void *, u32, u32);
void native_fn_02004bb8(const void *, u32, u32);
void native_fn_02004c78(const void *, u32, u32);
void native_fn_02004d38(const void *, u32, u32);
void native_fn_02004df8(const void *, u32, u32);
void native_fn_02007308(const void *, u32);

void *native_main_02045b4c(u32 arg0) {
    switch (arg0) {
    case 0:
        return native_fn_02003e88();
    case 1:
        return native_fn_02003edc();
    case 2:
        return native_fn_02003f80();
    case 3:
        return native_fn_02004078();
    default:
        native_fn_02008430();
        return 0U;
    }
}