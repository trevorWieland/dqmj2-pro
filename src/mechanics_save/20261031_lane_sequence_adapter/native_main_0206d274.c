typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
extern u32 native_fn_02048644(u32 object,u32 context,u32 index);
extern u32 native_data_021c4b74[];
extern u8 native_data_021c4bf9[];
extern u8 native_data_021c4c00[];
u32 native_main_0206d274(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_lr;

    temp_lr = arg1 * 0x18;
    if (*(s8 *)(native_data_021c4c00 + temp_lr) == -1) {
        return native_fn_02048644(native_data_021c4b74[arg1], arg0, (u8) ((arg2 + *(native_data_021c4bf9 + temp_lr)) - 1));
    }
    return native_fn_02048644(native_data_021c4b74[arg1], arg0, arg2);
}
