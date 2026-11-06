#define NULL ((void *)0)
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
extern u32 native_fn_02061944();
extern u32 native_fn_020624b0();
extern u32 native_fn_020624c0();
extern u32 native_fn_0206de44();
extern u32 native_fn_0206de64();
extern u32 native_fn_02070808();
extern u32 native_fn_02070d04();
extern u32 native_fn_02070f44();
extern u32 native_fn_02071410();
extern u32 native_fn_02072f48();
extern u8 native_data_021c4f60[];
u32 native_main_0206dcd0(void *arg0) {
    s8 temp_r0;
    u32 var_r0;
    u32 var_r0_2;
    u32 var_r0_3;
    u32 var_r0_4;
    u32 temp_r5;
    u32 temp_r5_2;
    u32 temp_r5_3;

    if (M2C_FIELD(native_data_021c4f60, void **, 0x20) == arg0) {
        return (u32) M2C_FIELD(native_data_021c4f60, void **, 0x20);
    }
    M2C_FIELD(native_data_021c4f60, void **, 0x24) = (void *) M2C_FIELD(native_data_021c4f60, void **, 0x20);
    M2C_FIELD(native_data_021c4f60, void **, 0x20) = arg0;
    M2C_FIELD(native_data_021c4f60, s32 *, 0x30) = 0;
    native_fn_0206de44(1);
    native_fn_0206de64(1);
    temp_r0 = M2C_FIELD(native_fn_02061944(), s8 *, 0x269);
    switch (temp_r0) {
    case 5:
        temp_r5 = native_fn_02071410();
        if ((s32) (temp_r5 - 1) < (s32) native_fn_020624c0(5)) {
            var_r0_2 = native_fn_02071410() - 1;
        } else {
            var_r0_2 = native_fn_020624c0(5);
        }
        native_fn_020624b0(5, (s8) var_r0_2);
        break;
    case 4:
        native_fn_02070d04();
        temp_r5_2 = native_fn_02070f44();
        if ((s32) (temp_r5_2 - 1) < (s32) native_fn_020624c0(4)) {
            var_r0_3 = native_fn_02070f44() - 1;
        } else {
            var_r0_3 = native_fn_020624c0(4);
        }
        native_fn_020624b0(4, (s8) var_r0_3);
        break;
    case 3:
        temp_r5_3 = native_fn_02070808();
        if ((s32) (temp_r5_3 - 1) < (s32) native_fn_020624c0(3)) {
            var_r0_4 = native_fn_02070808() - 1;
        } else {
            var_r0_4 = native_fn_020624c0(3);
        }
        native_fn_020624b0(3, (s8) var_r0_4);
        break;
    }
    if (arg0 == NULL) {
        var_r0 = 0;
    } else {
        var_r0 = native_fn_02072f48(M2C_FIELD(arg0, s16 *, 0x18));
    }
    M2C_FIELD(native_data_021c4f60, s8 *, 0x2F) = (s8) var_r0;
    return var_r0;
}
