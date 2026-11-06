#include "roster_actions.h"
extern u32 native_fn_0202a634();
extern u32 native_fn_02048034();
extern u32 native_fn_0205dc70();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02062a10(u32);
extern u32 native_fn_02067748();
extern u32 native_fn_02068f60();
extern u32 native_fn_0206940c();
extern u32 native_fn_020698f4();
extern u32 native_fn_0206a04c();
extern u32 native_fn_0206a05c();
extern u32 native_fn_0206a06c();
extern u32 native_fn_0206be2c();
extern u32 native_fn_0206dcd0(void *);
extern u32 native_fn_020c1708(s32 *);
extern u32 native_fn_020c485c();
extern u32 native_fn_020cc75c();
extern u32 native_fn_020cd4e8();
extern u32 native_fn_020cd958();
extern u32 native_fn_020cd9ac();
extern u32 native_fn_020cdd78();
extern u8 native_data_021d6964[];
extern s32 native_counter_021d6964;
void native_main_020cda54(void) {
    u16 temp_r0_2;
    u16 temp_r0_3;
    u32 temp_r0;
    u32 temp_r0_4;
    u32 temp_r0_5;
    u8 *temp_r4;
    s32 var_r5;

    temp_r4 = (u8 *)native_fn_0202a634();
    native_fn_0206940c();
    temp_r0_3 = M2C_FIELD(temp_r4, u16 *, 2);
    if (temp_r0_3 & 1) {
        temp_r0_4 = native_fn_020698f4(0);
        switch (temp_r0_4) {
        case 1:
            native_fn_020cd958();
            native_fn_0205e7a8(-1, 0x52);
            break;
        case 2:
            native_fn_020cd9ac();
            native_fn_0205e7a8(-1, 0x53);
            break;
        default:
            if (native_fn_0206a04c() == 2) {
                native_fn_020cd4e8(0xE, -1);
                native_fn_020c485c();
                native_fn_02068f60(0);
                M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 2;
            }
            if (native_fn_020cc75c() == 2) {
                var_r5 = 0;
                temp_r0_5 = native_fn_0206a05c();
                if (temp_r0_5 == 2) {
                    native_fn_02048034(native_fn_0205dc70(9, 8, (u16) (M2C_FIELD(native_fn_02067748(), u32 *, 4) + 0xEU)), 0);
                    native_fn_020cd4e8(0x12, -1);
                    var_r5 = 1;
                } else if (temp_r0_5 == 3) {
                    native_fn_020cd4e8(0x2E, -1);
                    var_r5 = 1;
                }
                if (var_r5 != 0) {
                    native_fn_020c485c();
                    native_fn_02068f60(0);
                    M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 2;
                }
            }
            break;
        }
    } else if (temp_r0_3 & 2) {
        native_fn_0206a06c(1);
    }
    temp_r0_2 = M2C_FIELD(temp_r4, u16 *, 2);
    if (!(temp_r0_2 & 4)) {
        return;
    }
    temp_r0 = native_fn_020c1708(&native_counter_021d6964);
    if (temp_r0 == 0) {
        return;
    }
    native_fn_020cdd78(M2C_FIELD(native_data_021d6964, s32 *, 0));
    native_fn_0206dcd0((void *)native_fn_02062a10(native_fn_0206be2c()));
    native_fn_02068f60(0);
    M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 2;
    return;
}
