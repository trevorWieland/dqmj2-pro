typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_data_ov001_02239d6c[];
u32 native_ov001_022023dc(s32 arg0) {
    u32 temp_r0;

    temp_r0 = *native_data_ov001_02239d6c & ~arg0;
    *native_data_ov001_02239d6c = temp_r0;
    return temp_r0;
}
