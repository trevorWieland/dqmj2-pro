typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_02008e0c();
extern u32 native_fn_0203d294();
extern u32 native_fn_02044424();
extern u32 native_fn_02044dc4();
extern s32 native_fn_ov001_021e88a4(s32,s32,u32);
u32 native_ov001_021e88e4(void *destination, void *enemy) {
    u8 rate;
    void *drop;
    s32 dropSlot;

    if ((s32) M2C_FIELD(destination, s32 *, 0) >= 0) {
        M2C_FIELD(destination, s16 *, 0x11C) = (s16) M2C_FIELD(enemy, s16 *, 0x30);
        M2C_FIELD(destination, s16 *, 0x11E) = (s16) M2C_FIELD(enemy, s16 *, 0x32);
        M2C_FIELD(destination, s16 *, 0x124) = (s16) M2C_FIELD(enemy, s16 *, 0x34);
        M2C_FIELD(destination, s16 *, 0x126) = (s16) M2C_FIELD(enemy, s16 *, 0x36);
        M2C_FIELD(destination, s16 *, 0x128) = (s16) M2C_FIELD(enemy, s16 *, 0x38);
        M2C_FIELD(destination, s16 *, 0x12A) = (s16) M2C_FIELD(enemy, s16 *, 0x3A);
        M2C_FIELD(destination, u32 *, 8) = (u32) M2C_FIELD(enemy, u32 *, 0x28);
        M2C_FIELD(destination, s16 *, 0x2C) = (s16) M2C_FIELD(enemy, s32 *, 0x24);
        native_fn_02008e0c(enemy + 0x1C, destination + 0xCA, 8);
        native_fn_02008e0c(enemy + 0x5E, destination + 0xD2, 4);
        M2C_FIELD(destination, s16 *, 0x32) = (s16) M2C_FIELD(enemy, s16 *, 0x3C);
        M2C_FIELD(destination, u8 *, 0xAA) = (u8) M2C_FIELD(enemy, u8 *, 0x2F);
        M2C_FIELD(destination, u8 *, 0x12C) = (u8) M2C_FIELD(enemy, u8 *, 0x2C);
        M2C_FIELD(destination, s16 *, 0x36) = (s16) M2C_FIELD(enemy, s16 *, 0x40);
        M2C_FIELD(destination, s16 *, 0x38) = (s16) M2C_FIELD(enemy, s16 *, 0x42);
        M2C_FIELD(destination, s16 *, 0x3A) = (s16) M2C_FIELD(enemy, s16 *, 0x44);
        M2C_FIELD(destination, s16 *, 0x3C) = (s16) M2C_FIELD(enemy, s16 *, 0x46);
        M2C_FIELD(destination, s16 *, 0x3E) = (s16) M2C_FIELD(enemy, s16 *, 0x48);
        M2C_FIELD(destination, s16 *, 0x40) = (s16) M2C_FIELD(enemy, s16 *, 0x4A);
        M2C_FIELD(destination, u8 *, 0x44) = (u8) M2C_FIELD(enemy, u8 *, 0x58);
        M2C_FIELD(destination, u8 *, 0x45) = (u8) M2C_FIELD(enemy, u8 *, 0x59);
        M2C_FIELD(destination, u8 *, 0x46) = (u8) M2C_FIELD(enemy, u8 *, 0x5A);
        M2C_FIELD(destination, u8 *, 0x47) = (u8) M2C_FIELD(enemy, u8 *, 0x5B);
        if ((native_fn_02044424(8) != 0) && (M2C_FIELD(enemy, u8 *, 0x63) == 0)) {
            if ((native_fn_02044dc4(M2C_FIELD(destination, s16 *, 0x2E), M2C_FIELD(destination, u8 *, 0x30)) <= 3U) && (native_fn_0203d294(2) == 0)) {
                M2C_FIELD(destination, u8 *, 0x30) = (u8) (M2C_FIELD(destination, u8 *, 0x30) + 1);
            }
            if (M2C_FIELD(destination, u8 *, 0x30) == 0) {
                M2C_FIELD(destination, s16 *, 0x11C) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x11C), 0x1800, 2);
                M2C_FIELD(destination, s16 *, 0x11E) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x11E), 0x1800, 2);
                M2C_FIELD(destination, s16 *, 0x124) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x124), 0x1800, 2);
                M2C_FIELD(destination, s16 *, 0x126) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x126), 0x1800, 2);
                M2C_FIELD(destination, s16 *, 0x128) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x128), 0x1800, 2);
                M2C_FIELD(destination, s16 *, 0x12A) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x12A), 0x1800, 2);
                M2C_FIELD(destination, u8 *, 0x12C) = (u8) native_fn_ov001_021e88a4((s16) M2C_FIELD(destination, u8 *, 0x12C), 0x1800, 1);
                M2C_FIELD(destination, u32 *, 8) = native_fn_ov001_021e88a4(M2C_FIELD(destination, s32 *, 8), 0x1800, 4);
                M2C_FIELD(destination, s16 *, 0x2C) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x2C), 0x1800, 2);
                M2C_FIELD(destination, s16 *, 0x32) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x32), 0x800, 2);
                M2C_FIELD(destination, s16 *, 0x36) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x36), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x38) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x38), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x3A) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x3A), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x3C) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x3C), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x3E) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x3E), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x40) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x40), 0x1000, 2);
            } else {
                M2C_FIELD(destination, s16 *, 0x11C) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x11C), 0x2000, 2);
                M2C_FIELD(destination, s16 *, 0x11E) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x11E), 0x2000, 2);
                M2C_FIELD(destination, s16 *, 0x124) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x124), 0x2000, 2);
                M2C_FIELD(destination, s16 *, 0x126) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x126), 0x2000, 2);
                M2C_FIELD(destination, s16 *, 0x128) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x128), 0x2000, 2);
                M2C_FIELD(destination, s16 *, 0x12A) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x12A), 0x2000, 2);
                M2C_FIELD(destination, u8 *, 0x12C) = (u8) native_fn_ov001_021e88a4((s16) M2C_FIELD(destination, u8 *, 0x12C), 0x2000, 1);
                M2C_FIELD(destination, u32 *, 8) = native_fn_ov001_021e88a4(M2C_FIELD(destination, s32 *, 8), 0x2000, 4);
                M2C_FIELD(destination, s16 *, 0x2C) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x2C), 0x2000, 2);
                M2C_FIELD(destination, s16 *, 0x32) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x32), 0x800, 2);
                M2C_FIELD(destination, s16 *, 0x36) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x36), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x38) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x38), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x3A) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x3A), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x3C) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x3C), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x3E) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x3E), 0x1000, 2);
                M2C_FIELD(destination, s16 *, 0x40) = (s16) native_fn_ov001_021e88a4(M2C_FIELD(destination, s16 *, 0x40), 0x1000, 2);
            }
            dropSlot = 0;
            do {
                drop = destination + (dropSlot * 4);
                if (M2C_FIELD(drop, u16 *, 0xCA) != 0) {
                    rate = M2C_FIELD(drop, u8 *, 0xCC);
                    if ((u32) (u8) (rate - 2) <= 4U) {
                        M2C_FIELD(drop, u8 *, 0xCC) = (u8) (rate - 1);
                    }
                }
                dropSlot += 1;
            } while (dropSlot < 2);
        }
        M2C_FIELD(destination, s16 *, 0x120) = (s16) M2C_FIELD(destination, s16 *, 0x11C);
        M2C_FIELD(destination, s16 *, 0x122) = (s16) M2C_FIELD(destination, s16 *, 0x11E);
        return 1U;
    }
    return 0U;
}
