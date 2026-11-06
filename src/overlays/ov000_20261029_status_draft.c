typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u8 unknown_00[0x278];
    u8 field_278;
} State;

extern State data_ov000_022322d4;

u32 native_ov000_021e0f58(void) {
    if (data_ov000_022322d4.field_278 != 2 &&
        data_ov000_022322d4.field_278 != 3 &&
        data_ov000_022322d4.field_278 != 4) {
        return 0;
    }
    return 1;
}
