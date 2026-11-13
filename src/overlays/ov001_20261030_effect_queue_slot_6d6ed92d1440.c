typedef unsigned char u8;
typedef signed int s32;
typedef unsigned int u32;
extern s32 native_data_ov001_02238dec[10];
extern s32 ov001_effect_resource_create_021eec7c(u32, u8 *, s32);
u32 native_ov001_021e9cd8(u32 id, u8 *actor, s32 kind) {
    s32 index;
    index = 0;
    do {
        if (native_data_ov001_02238dec[index] == -1) {
            native_data_ov001_02238dec[index] = ov001_effect_resource_create_021eec7c(id, actor, kind);
            return 1;
        }
        index++;
    } while (index < 10);
    return 0;
}
