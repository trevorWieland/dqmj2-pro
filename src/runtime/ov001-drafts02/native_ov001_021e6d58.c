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
extern u32 native_fn_0203d294();
extern u32 ov001_side_slot_record_021db438();
void native_ov001_021e6d58(u32 arg0) {
    void *temp_r0;
    u8 temp_r0_2;

    temp_r0 = (void *) ov001_side_slot_record_021db438(1, arg0);
    temp_r0_2 = M2C_FIELD(M2C_FIELD(temp_r0, void **, 0x1E8), u8 *, 0xAA);
    switch (temp_r0_2) {
    case 4:
        M2C_FIELD(temp_r0, s8 *, 0x35B) = (s8) native_fn_0203d294(6);
        return;
    case 7:
        M2C_FIELD(temp_r0, s8 *, 0x35B) = (s8) native_fn_0203d294(2);
        return;
    default:
        M2C_FIELD(temp_r0, s8 *, 0x35B) = 0;
        return;
    }
}
