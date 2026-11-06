typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
#define M2C_FIELD(value,type,offset) (*(type)((s8 *)(value)+(offset)))
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern u32 native_fn_02018148(u32,u32,u32);
extern u8 native_data_020ec360[];
u32 native_main_020181b8(u32 arg0, u32 arg1) {
    u32 temp_r0;

    temp_r0 = native_fn_02007ff4();
    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), u8 *, 0x50D) != 0) {
        native_fn_02008008(temp_r0);
        return 0U;
    }
    if (native_fn_02018148(arg0, 8U, arg1) == 0) {
        native_fn_02008008(temp_r0);
        return 0U;
    }
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x10) = (s16) arg1;
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x500) = (s16) arg0;
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x502) = 8;
    native_fn_02008008(temp_r0);
    return 1U;
}
