typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 first[4]; u16 reserved4:8; u16 category:4; u16 remaining4:4; u16 flags; u16 alias; u8 remaining[90]; } NativeEktRecord;
extern struct { u32 count; NativeEktRecord *records; } native_ekt_state;
extern u32 native_library_obtained[3][16];
extern u32 native_library_seen[3][16];
extern u32 native_saved_bits_0ba4[];
extern u32 native_saved_nibbles_0bc4[];
extern u32 native_saved_bits_0b84[];
extern void native_secondary_bit_set(int, int);
extern NativeEktRecord *saved_native_ekt_record(int);
u32 saved_native_id_alias(int id, int variant) {
    u32 alias = saved_native_ekt_record(id)->alias;
    return alias | ((alias == 0 ? 0 : (u16)variant) << 16);
}
int saved_native_id_predicate(int id, int unused, int enabled) {
    switch (id) {
    case 139:
    case 176:
    case 188:
    case 350:
        if (enabled) return 1;
        break;
    case 353:
        return 1;
    }
    return 0;
}
u8 saved_native_category(int id) { return (int)native_ekt_state.records[id].category / 3; }
int saved_library_obtained_get(int id, int variant) {
    u32 alias = saved_native_id_alias(id, variant);
    if (alias) {
        id = (u16)alias;
        variant = (u16)(alias >> 16);
    }
    return (native_library_obtained[variant][id >> 5] & (1U << (id & 31))) != 0;
}
int saved_library_obtained_set(int id, int variant) {
    int previous;
    u32 alias = saved_native_id_alias(id, variant);
    if (alias) {
        id = (u16)alias;
        variant = (u16)(alias >> 16);
    }
    previous = saved_library_obtained_get(id, variant);
    native_library_obtained[variant][id >> 5] |= 1U << (id & 31);
    return previous;
}
int saved_library_seen_get(int id, int variant) {
    u32 alias = saved_native_id_alias(id, variant);
    if (alias) {
        id = (u16)alias;
        variant = (u16)(alias >> 16);
    }
    return (native_library_seen[variant][id >> 5] & (1U << (id & 31))) != 0;
}
int saved_library_seen_set(int id, int variant) {
    int previous;
    u32 alias;
    switch (id) {
    case 353:
    case 452:
    case 455:
        return 0;
    }
    if (id == 500) { id = 431; variant = 2; }
    else {
        alias = saved_native_id_alias(id, variant);
        if (alias) { id = (u16)alias; variant = (u16)(alias >> 16); }
    }
    previous = saved_library_seen_get(id, variant);
    native_library_seen[variant][id >> 5] |= 1U << (id & 31);
    if (saved_native_category(id) == 1) native_secondary_bit_set(17, 1);
    return previous;
}
int saved_raw_bits_0ba4_get(int id) { return (native_saved_bits_0ba4[id >> 5] & (1U << (id & 31))) != 0; }
int saved_raw_bits_0ba4_set(int id) {
    int previous = saved_raw_bits_0ba4_get(id);
    native_saved_bits_0ba4[id >> 5] |= 1U << (id & 31);
    return previous;
}
u32 saved_raw_nibbles_0bc4_get(int id) { return (native_saved_nibbles_0bc4[id >> 3] >> ((id & 7) * 4)) & 15; }
u32 saved_raw_nibbles_0bc4_set(int id, u32 value) {
    u32 previous = saved_raw_nibbles_0bc4_get(id);
    u32 shift = (id & 7) * 4;
    native_saved_nibbles_0bc4[id >> 3] &= ~(15U << shift);
    native_saved_nibbles_0bc4[id >> 3] |= value << shift;
    return previous;
}
int saved_raw_bits_0b84_get(int id) { return (native_saved_bits_0b84[id >> 5] & (1U << (id & 31))) != 0; }
int saved_raw_bits_0b84_set(int id) {
    int previous = saved_raw_bits_0b84_get(id);
    native_saved_bits_0b84[id >> 5] |= 1U << (id & 31);
    return previous;
}
