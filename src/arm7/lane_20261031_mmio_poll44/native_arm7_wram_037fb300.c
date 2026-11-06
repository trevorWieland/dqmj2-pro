typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern volatile u16 native_host_arm7_data_0480819c[];
u32 native_arm7_wram_037fb300(void) {
    u32 status;
    s32 remaining = 4000;
    while (remaining != 0) {
        status = *native_host_arm7_data_0480819c;
        if (status & 128) return status;
        --remaining;
    }
    return status;
}
