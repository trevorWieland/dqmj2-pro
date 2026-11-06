typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef struct { u8 prefix[0x64]; u16 count; u16 reserved; u8 first[8]; u8 second[8]; } RawControls;
extern RawControls native_controls;
extern u8 native_section3[];
void saved_raw_controls_reset(void) {
    u8 *root = (u8 *)&native_controls;
    s8 index = 0;
    do {
        u8 *entry = root + index;
        entry[0x68] = 255;
        entry[0x70] = 255;
        index++;
    } while (index < 8);
    ((RawControls *)root)->count = 0;
}
RawControls *saved_raw_controls_pointer(void) { return &native_controls; }
u8 *saved_section3_base_pointer(void) { return native_section3; }
u8 *saved_identity_array_pointer(void) { return native_section3 + 0x40; }
u8 *saved_section3_word228c_pointer(void) { return native_section3 + 0x228c; }
u8 *saved_section3_word2290_pointer(void) { return native_section3 + 0x2290; }
u8 *saved_section3_buffer1994_pointer(void) { return native_section3 + 0x1994; }
u8 *saved_section3_buffer1a94_pointer(void) { return native_section3 + 0x1a94; }
u8 *saved_section3_pair2284_pointer(void) { return native_section3 + 0x2284; }
