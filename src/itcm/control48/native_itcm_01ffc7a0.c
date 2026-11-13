typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef int s32;
extern u8 *ov000_context_02246600_02223c54(void);
extern u32 native_fn_020642dc(void);
extern void native_fn_020620e8(u32, u32);
extern u32 native_fn_01ffa8d8(void);
extern void native_fn_02089804(void);
extern u8 native_data_ov000_02246720[];

void native_itcm_01ffc7a0(void) {
    u8 *record = ov000_context_02246600_02223c54();
    *(u32 *)(native_data_ov000_02246720 + 0x14) = 1;
    switch (native_fn_020642dc()) {
    case 1:
        if (*(s32 *)(native_data_ov000_02246720 + 8) >= 0) {
            native_fn_020620e8(20, 1);
        } else {
            native_fn_020620e8(27, 1);
        }
        return;
    case 2:
        if (native_fn_01ffa8d8() == 4) {
            native_fn_020620e8(23, 1);
        } else {
            native_fn_020620e8(24, 1);
        }
        return;
    case 8:
    case 9:
    case 10:
    case 11:
    case 12:
    case 13:
    case 14:
    case 15:
        native_fn_02089804();
        return;
    default:
        if (*(s8 *)(record + 0x58) == 0) {
            native_fn_020620e8(18, 1);
        } else {
            native_fn_020620e8(22, 1);
        }
        return;
    }
}
