typedef unsigned char u8;
typedef unsigned int u32;
extern u8 *native_fn_0207d2c8(u32 key);
u32 native_main_0207d708(u32 key) {
    u8 *row = native_fn_0207d2c8(key);
    u32 kind;
    if (key == 0) return 0;
    kind = row[3];
    if (kind == 4) return 21;
    if (kind == 6) return 0;
    if (kind == 8) return 25;
    return 0;
}
