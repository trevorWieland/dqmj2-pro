typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 bytes[2]; } NativeTextSeed;
extern NativeTextSeed native_text_seed;
extern u8 ***native_text_roots[];
extern u8 *native_text_copy(u8 *, const u8 *);
extern u8 *native_text_append(u8 *, const u8 *);
extern u32 native_variant_offset(int);
u8 *saved_native_text_pointer(int group, int table, int index) {
    return native_text_roots[group][table][index];
}
int saved_native_text_continues(const u8 *text) {
    if (!text) return 0;
    if (!text[0]) return 0;
    if (text[0] == 0xe3 && text[1] == 0x1b) return 0;
    return 1;
}
