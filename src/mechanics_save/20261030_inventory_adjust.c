typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_02065d88(s32 item);
extern s32 native_fn_02063810(s32 item);
extern u8 native_data_021bd558[];

s32 native_main_020630e4(s32 item, s32 delta)
{
    u8 *descriptor;
    u8 capacity;
    if (item >= 255) {
        return 0;
    }
    descriptor = native_fn_02065d88(item);
    native_data_021bd558[item] = (u8)((u32)(s32)(s8)native_data_021bd558[item] + (u32)delta);
    capacity = descriptor[0x27];
    if ((s32)(s8)native_data_021bd558[item] > capacity) {
        native_data_021bd558[item] = capacity;
    }
    if ((s8)native_data_021bd558[item] < 0) {
        native_data_021bd558[item] = 0;
    }
    native_fn_02063810(item);
    return (s8)native_data_021bd558[item];
}
