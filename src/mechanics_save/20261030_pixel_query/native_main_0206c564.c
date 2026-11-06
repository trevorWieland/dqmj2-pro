typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern void * native_fn_02062a10(u32);
extern u32 native_fn_0206c1a8(s32);
extern u8 native_data_021c4a04[];
extern u8 native_data_021c491a[];
s32 native_main_0206c564(s32 x, s32 y) {
    s16 species;
    s32 horizontal;
    s32 index;
    u8 *row;
    u8 origin;
    void *layout;

    row = native_data_021c4a04;
    index = 0;
loop_1:
    if (M2C_FIELD(row, u8 *, 9) != 0) {
        species = M2C_FIELD(native_fn_02062a10(M2C_FIELD(row, u32 *, 0)), s16 *, 0x18);
        horizontal = M2C_FIELD(row, u8 *, 6) * 5;
        layout = native_data_021c491a + (M2C_FIELD(row, u8 *, 8) * 5);
        origin = M2C_FIELD(layout, u8 *, 1);
        if ((x >= (s32) ((origin + 1 + horizontal) * 8)) && (x < (s32) ((origin + 6 + horizontal) * 8)) && (y >= (s32) ((M2C_FIELD(layout, u8 *, 2) + 1 + (M2C_FIELD(row, u8 *, 7) * 5)) * 8)) && (y < (s32) ((M2C_FIELD((native_data_021c491a + (M2C_FIELD(row, u8 *, 8) * 5)), u8 *, 2) + 1 + (M2C_FIELD(row, u8 *, 7) * 5) + ((native_fn_0206c1a8((s32) species) + 1) * 5)) * 8))) {
            return index;
        }
    }
    index += 1;
    row += 0x10;
    if (index >= 0xF) {
        return -1;
    }
    goto loop_1;
}
