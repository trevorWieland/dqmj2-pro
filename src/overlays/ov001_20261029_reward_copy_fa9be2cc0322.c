typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov001_02238d18[];
u32 native_ov001_021e6720(u8 *arg0) {
    u8 value;
    s32 index;
    u8 *destination;

    destination = native_data_ov001_02238d18;
    index = 0;
    do {
        value = *(arg0 + index);
        index += 1;
        *destination = value;
        destination += 1;
    } while (index < 3);
    return (u32)arg0;
}
