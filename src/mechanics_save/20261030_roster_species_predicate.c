typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Slot {
    u8 prefix[10];
    s16 species;
    u8 tail[12];
} Slot;
extern Slot native_data_021c4bf8[];
u32 native_main_0206db00(s32 sprite) {
    switch (native_data_021c4bf8[sprite].species) {
    case 139:
    case 176:
    case 188:
    case 254:
    case 350:
    case 425:
    case 426:
        return 1;
    default:
        return 0;
    }
}
