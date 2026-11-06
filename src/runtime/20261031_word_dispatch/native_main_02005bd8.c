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
extern u8 native_data_020e335c[];
extern u8 native_data_027e0000[];
u32 native_main_02005bd8(u32 arg0) {
    s32 bit_index;
    u32 remaining;
    u8 *cursor;

    remaining = arg0;
    cursor = native_data_027e0000;
    bit_index = 0;
loop_1:
    if (!(remaining & 1)) {
        goto block_9;
    }
    if (bit_index < 8) {
        goto block_5;
    }
    if (bit_index > 0xB) {
        goto block_5;
    }
    return *(u32 *)(native_data_020e335c + ((bit_index - 8) * 0xC));
block_5:
    if (bit_index < 3) {
        goto block_8;
    }
    if (bit_index > 6) {
        goto block_8;
    }
    return *(u32 *)(native_data_020e335c + ((bit_index + 1) * 0xC));
block_8:
    return *(u32 *)cursor;
block_9:
    bit_index += 1;
    remaining = remaining >> 1;
    cursor += 4;
    if (bit_index < 0x16) {
        goto loop_1;
    }
    return 0U;
}
