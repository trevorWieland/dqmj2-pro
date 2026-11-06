typedef unsigned char u8;
typedef signed int s32;
typedef unsigned int u32;

extern const u8 *data_ov001_02238d58;

s32 native_ov001_021e8e08(u32 curve, u32 level) {
    if (data_ov001_02238d58 == 0) {
        return -1;
    }
    return data_ov001_02238d58[curve * 100 + level - 1];
}
