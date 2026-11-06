typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 prefix[4]; u16 group:4; u16 remaining:12; u8 tail[94]; } NativeKind;
extern NativeKind *native_kind_record(int);
u8 saved_variant_group(int species, int variant) {
    u8 group = native_kind_record(species)->group;
    u8 value = group + variant * 3;
    if (variant > 0) value = ((int)value - 1) / 3 * 3 + 1;
    return value;
}
u8 saved_kind_byte0d(int species, int previous) {
    int value = ((u8 *)native_kind_record(species))[13];
    value += previous;
    value -= previous;
    return value;
}
