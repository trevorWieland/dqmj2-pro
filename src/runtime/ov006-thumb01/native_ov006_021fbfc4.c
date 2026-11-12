typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_ov006_021f23f4();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f5740();
extern u32 native_fn_ov006_021f57b0();
extern u32 native_fn_ov006_021fbef0();
extern u32 native_fn_ov006_021fc054();
extern u32 native_fn_ov006_021ff6d4();
extern u32 native_fn_ov006_021ff718();
extern u32 native_fn_ov006_02200344();
extern u8 native_data_ov006_0221c0fc[];
u32 native_ov006_021fbfc4(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov006_021f5740();
    switch (temp_r0) {
    default:
        return temp_r0;
    case 3:
        *native_data_ov006_0221c0fc = 1;
        native_fn_ov006_021ff718();
        native_fn_ov006_021f57b0();
        return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fbef0);
    case 4:
        *native_data_ov006_0221c0fc = 0;
        native_fn_ov006_021ff718();
        native_fn_ov006_021ff6d4(9);
        native_fn_ov006_02200344(0xD, 1, 1, -1, 0);
        native_fn_ov006_021f23f4();
        return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fc054);
    case 5:
        *native_data_ov006_0221c0fc = 0;
        native_fn_ov006_021ff718();
        native_fn_ov006_021ff6d4(0x12);
        native_fn_ov006_02200344(0xE, 1, 1, -1, 0);
        native_fn_ov006_021f23f4();
        return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fc054);
    }
}
