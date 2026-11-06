typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_02041f74();
extern u32 native_fn_02042c2c();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d7814();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021db9e0();
extern u32 native_fn_ov001_021dbaac();
extern u8 native_data_ov001_02239a14[];
void native_ov001_021f9ef0(u32 arg0) {
    u32 temp_r0;
    u32 temp_r4;

    if (arg0 == 0) {
        temp_r4 = native_fn_ov001_021db9e0(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34));
        if (native_fn_ov001_021dbaac(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34)) != 0) {
            if (M2C_FIELD(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), u8 *, 0x31E) == 1) {
                native_fn_ov001_021d75d4(8);
            } else {
                native_fn_ov001_021d75d4(9);
            }
        } else if (temp_r4 == 2) {
            native_fn_ov001_021d75d4(7);
        } else if (temp_r4 == 1) {
            native_fn_ov001_021d75d4(6);
        } else {
            native_fn_ov001_021d75d4(5);
        }
        native_fn_ov001_021d77b0(-1, native_fn_02042c2c(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34)));
        native_fn_ov001_021d7814(-1, native_fn_02041f74(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), 0));
        native_fn_ov001_021d94cc(1, 0);
        return;
    } else if (arg0 == 2) {
        native_fn_ov001_021d75d4(0xD);
        native_fn_ov001_021d94cc(1, 1);
        return;
    } else if (arg0 == 1) {
        temp_r0 = native_fn_ov001_021db9e0(M2C_FIELD(native_data_ov001_02239a14, void **, 0x40));
        if (temp_r0 == 2) {
            native_fn_ov001_021d75d4(0xC);
        } else if (temp_r0 == 1) {
            native_fn_ov001_021d75d4(0xB);
        } else {
            native_fn_ov001_021d75d4(0xA);
        }
        native_fn_ov001_021d77b0(-1, native_fn_02042c2c(M2C_FIELD(native_data_ov001_02239a14, void **, 0x40)));
        native_fn_ov001_021d7814(-1, native_fn_02041f74(M2C_FIELD(native_data_ov001_02239a14, void **, 0x40), 0));
        native_fn_ov001_021d94cc(1, 1);
        return;
    }
    return;
}
