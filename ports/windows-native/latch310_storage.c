typedef unsigned char u8;
typedef unsigned int u32;
u8 native_data_021b9bd4[0x280];
void latch_reset(u32 previous) {
    u32 index;
    for (index = 0; index < 0x280; index++) native_data_021b9bd4[index] = 0xA5;
    native_data_021b9bd4[0x26E] = (u8)previous;
}
