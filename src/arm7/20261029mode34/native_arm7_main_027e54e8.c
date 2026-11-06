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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fe12c(u32, u32, u32);
extern u32 native_arm7_fn_037fe070(u32, u32, u32);
extern u32 native_arm7_fn_027e2458(u32, u32);
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_038073a4(u32);
extern u8 native_arm7_data_027f8884;
u32 native_arm7_main_027e54e8(void *arg0) {
    u16 temp_r0_2;
    void *temp_r0;
    void *temp_r0_3;
    u16 temp_r4_2;
    void *temp_r4;
    u8 sp0[512];

    temp_r4 = M2C_FIELD((u32) &native_arm7_data_027f8884, void **, 0x550);
    M2C_FIELD(temp_r4, u16 *, 0x196) = (u16) M2C_FIELD(arg0, s32 *, 4);
    temp_r0_2 = M2C_FIELD(temp_r4, u16 *, 0x196);
    switch (temp_r0_2) {
    case 0:
        M2C_FIELD(temp_r4, s32 *, 0x198) = 0;
        break;
    case 1:
    case 2:
    case 3:
        M2C_FIELD(temp_r4, s32 *, 0x198) = 1;
        break;
    default:
        M2C_FIELD(temp_r4, s32 *, 0x198) = 0;
        break;
    }
    if (M2C_FIELD(temp_r4, s32 *, 0x198) == 1) {
        native_arm7_fn_037fe12c(M2C_FIELD(arg0, u32 *, 8), (u32) (temp_r4 + 0x19C), 0x50U);
    } else {
        native_arm7_fn_037fe070((u32) (temp_r4 + 0x19C), 0U, 0x50U);
    }
    M2C_FIELD(temp_r4, u16 *, 0xC4) = (u16) M2C_FIELD(arg0, s32 *, 0xC);
    temp_r4_2 = M2C_FIELD((void *) native_arm7_fn_027e2458((u32) &sp0, (u32) M2C_FIELD(temp_r4, u16 *, 0xC4)), u16 *, 4);
    if (temp_r4_2 != 0) {
        temp_r0_3 = (void *) native_arm7_fn_038073f0();
        M2C_FIELD(temp_r0_3, s16 *, 0) = 0x14;
        M2C_FIELD(temp_r0_3, s16 *, 2) = 1;
        M2C_FIELD(temp_r0_3, s16 *, 4) = 0x207;
        M2C_FIELD(temp_r0_3, u16 *, 6) = temp_r4_2;
        native_arm7_fn_038073a4((u32) temp_r0_3);
    }
    temp_r0 = (void *) native_arm7_fn_038073f0();
    M2C_FIELD(temp_r0, s16 *, 0) = 0x27;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_arm7_fn_038073a4((u32) temp_r0);
}
