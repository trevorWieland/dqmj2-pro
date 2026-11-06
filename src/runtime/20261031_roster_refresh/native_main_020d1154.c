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
#define NULL ((void *)0)
extern u8 native_fn_02044cdc(u32);
extern u32 native_fn_02049f4c(void **);
extern void native_fn_02049ffc(void *);
extern u32 native_fn_020602ec(u32, s32, u32, u32, u32, u32);
extern u32 native_fn_02061dcc(s32);
extern u32 native_fn_02062a10(u32);
extern u32 native_fn_020cf29c(s32);
extern u8 native_data_021d6bb4[];
extern u32 native_data_021d6bc0[];
void native_main_020d1154(void) {
    s8 temp_r0_4;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    s8 var_r4;
    s8 var_r4_2;
    u8 temp_r5;
    u8 temp_r6;
    s8 var_r8_2;
    u8 var_r8;
    u32 temp_r9;
    s32 var_r10;

    temp_r9 = native_fn_020cf29c((s32) *native_data_021d6bb4);
    var_r4 = 0;
    do {
        native_fn_02049f4c((void **) native_fn_02061dcc((s32) (s8) (var_r4 + 6)));
        var_r4 += 1;
    } while ((s32) var_r4 < 6);
    var_r4_2 = 0;
    do {
        native_fn_02049ffc(M2C_FIELD(*(void **) native_fn_02061dcc((s32) (s8) (var_r4_2 + 6)), void **, 4));
        var_r4_2 += 1;
    } while ((s32) var_r4_2 < 6);
    var_r8 = 0;
    var_r10 = 0;
    do {
        temp_r0_2 = native_fn_02062a10(native_data_021d6bc0[var_r10]);
        if (temp_r0_2 != 0) {
            temp_r5 = native_fn_02044cdc((u32) M2C_FIELD(temp_r0_2, s16 *, 0x18));
            native_fn_020602ec(*(s32 *) native_fn_02061dcc((s32) (s8) (var_r8 + 6)), M2C_FIELD(temp_r0_2, s16 *, 0x18), temp_r0_2, 0, 0, 1);
            var_r8 += temp_r5 + 1;
        }
        var_r10 = (s8)(var_r10 + 1);
    } while ((s32) var_r10 < 3);
    var_r10 = 0;
    var_r8_2 = 0;
    do {
        temp_r0_3 = native_fn_02062a10(M2C_FIELD((temp_r9 + (var_r8_2 * 4)), u32 *, 0x18));
        if (temp_r0_3 != 0) {
            temp_r6 = native_fn_02044cdc((u32) M2C_FIELD(temp_r0_3, s16 *, 0x18));
            native_fn_020602ec(*(s32 *) native_fn_02061dcc((s32) (s8) (var_r10 + 9)), M2C_FIELD(temp_r0_3, s16 *, 0x18), temp_r0_3, 0, 0, 1);
            var_r10 = (u8)(var_r10 + (temp_r6 + 1));
        }
        temp_r0_4 = var_r8_2 + 1;
        temp_r0 = temp_r0_4 << 0x18;
        var_r8_2 = temp_r0_4;
    } while ((s32) var_r8_2 < 3);

}
