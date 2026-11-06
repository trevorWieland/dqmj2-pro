typedef unsigned char u8;
typedef unsigned int u32;
extern u8 *native_fn_02062a10(u32);
u8 *native_main_02062ecc(u32 id, int slot) {
    return (u8 *)((unsigned long)native_fn_02062a10(id) + 0x7A + (unsigned long)slot * 2);
}
