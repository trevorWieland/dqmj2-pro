typedef unsigned char u8;
typedef unsigned int u32;
#define M2C_FIELD(value,type,offset) (*(type)((u8 *)(value)+(offset)))
extern u32 func_ov004_021d82c8(void);
extern u32 func_ov004_021d8304(void);
extern u32 func_ov004_021d8890(void);
extern u32 func_ov004_021d88cc(void);
static inline u8 *adjust_address(u8 *pointer) {
    return pointer - 0x2000;
}

u32 native_ov004_021d7854(void) {
    u8 *temp_r0;

    temp_r0 = adjust_address((u8 *)(func_ov004_021d82c8 + 0x1000));
    if (M2C_FIELD(temp_r0, u8 *, 0x1000) != 0xF) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1001) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1002) != 0x8F) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1003) != 0xE1) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1004) != 0xC) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1005) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1006) != 0x1C) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1007) != 0xE0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1008) != 0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1009) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100A) != 0xA0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100B) != 3) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100C) != 0x1C) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100D) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100E) != 0x8C) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100F) != 0x12) {
        return 0xB177U;
    }
    return 0xAA65U;
}

u32 native_ov004_021d7970(void) {
    u8 *temp_r0;

    temp_r0 = adjust_address((u8 *)(func_ov004_021d8304 + 0x1000));
    if (M2C_FIELD(temp_r0, u8 *, 0x1000) != 0xF) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1001) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1002) != 0x8F) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1003) != 0xE1) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1004) != 0xC) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1005) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1006) != 0x1C) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1007) != 0xE0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1008) != 0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1009) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100A) != 0xA0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100B) != 3) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100C) != 0x1C) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100D) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100E) != 0x8C) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100F) != 0x12) {
        return 0xAA65U;
    }
    return 0xB177U;
}

u32 native_ov004_021d7a8c(void) {
    u8 *temp_r0;

    temp_r0 = adjust_address((u8 *)(func_ov004_021d8890 + 0x1000));
    if (M2C_FIELD(temp_r0, u8 *, 0x1000) != 0xF) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1001) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1002) != 0x8F) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1003) != 0xE1) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1004) != 0xC) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1005) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1006) != 0x1C) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1007) != 0xE0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1008) != 0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1009) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100A) != 0xA0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100B) != 3) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100C) != 0x1C) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100D) != 0xC0) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100E) != 0x8C) {
        return 0xB177U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100F) != 0x12) {
        return 0xB177U;
    }
    return 0xAA65U;
}

u32 native_ov004_021d7ba8(void) {
    u8 *temp_r0;

    temp_r0 = adjust_address((u8 *)(func_ov004_021d88cc + 0x1000));
    if (M2C_FIELD(temp_r0, u8 *, 0x1000) != 0xF) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1001) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1002) != 0x8F) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1003) != 0xE1) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1004) != 0xC) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1005) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1006) != 0x1C) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1007) != 0xE0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1008) != 0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x1009) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100A) != 0xA0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100B) != 3) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100C) != 0x1C) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100D) != 0xC0) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100E) != 0x8C) {
        return 0xAA65U;
    }
    if (M2C_FIELD(temp_r0, u8 *, 0x100F) != 0x12) {
        return 0xAA65U;
    }
    return 0xB177U;
}
