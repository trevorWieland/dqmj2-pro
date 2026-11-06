#include "root_initializer.h"
extern u32 native_fn_02041538();
extern void native_fn_02048e74(void *,s32);
extern u32 native_fn_02048fcc(s32);
extern u32 native_fn_020cc730();
extern u32 native_fn_020cc740();
extern u32 native_fn_020ce048();
extern u8 native_data_021d69a0[];
typedef struct {s32 field_0; s32 field_4; s32 field_8; s32 field_c;} InitRoot;
extern InitRoot native_initializer_021d69a0;
u32 native_main_020cde78(void) {
    void *temp_r0;

    native_fn_02048e74(&native_initializer_021d69a0, 1);
    native_fn_02048fcc((s32)native_fn_020cc740());
    native_fn_020ce048();
    if (native_fn_020cc730() != 0) {
        native_fn_02041538(0, 2, 0xA);
    }
    M2C_FIELD(native_data_021d69a0, s32 *, 4) = 0;
    *(s32 *) native_fn_020cc740() = 0;
    temp_r0 = (void *) native_fn_020cc740();
    M2C_FIELD(temp_r0, s8 *, 0x10) = 1;
    return (u32) temp_r0;
}
