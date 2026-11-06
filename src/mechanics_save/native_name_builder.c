typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 bytes[2]; } NativeTextSeed;
extern NativeTextSeed native_text_seed;
extern u8 ***native_text_roots[];
extern u8 *native_text_copy(u8 *, const u8 *);
extern u8 *native_text_append(u8 *, const u8 *);
extern u32 native_variant_offset(int);
extern u8 *saved_native_text_pointer(int, int, int);
u8 *saved_native_name_build(u8 *output, int species, int variant) {
    u8 *result = output;
    int id = species;
    int form = variant;
    u8 seed[2] = {0xe3, 0x1b};
    switch (form) {
    case 0: native_text_copy(result, seed); break;
    default: break;
    }
    native_text_copy(result, saved_native_text_pointer(2, 0, id));
    if (form) native_text_append(result, saved_native_text_pointer(2, 1, form + native_variant_offset(id)));
    return result;
}
