typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    s8 side;
    s8 slot;
    u8 unknown2;
    u8 unknown3;
} Position;
extern Position native_data_ov001_02238d40[6];
u32 native_ov001_021e8178(u32 index, s8 *side, s8 *slot) {
    if (side != 0) {
        *side = native_data_ov001_02238d40[index].side;
    }
    if (slot != 0) {
        *slot = native_data_ov001_02238d40[index].slot;
    }
    return (u16)((u8)native_data_ov001_02238d40[index].side | ((u8)native_data_ov001_02238d40[index].slot << 8));
}
