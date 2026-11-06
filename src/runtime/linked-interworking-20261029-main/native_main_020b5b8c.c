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
extern u32 native_fn_0201b208();
extern u32 native_fn_020a85dc();
extern u32 native_fn_020a8614();
extern u32 native_fn_020a89a4();
extern u32 native_fn_020a8ef8();
extern u32 native_fn_020a929c();
extern u32 native_fn_020b3b34();
extern u32 native_fn_020b59ac();
extern u32 native_fn_020b5b80();
u32 native_main_020b5b8c(void *arg0, u32 *arg1, s32 arg2, s16 arg3) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 sp0;

    sp0 = 0;
    if (native_fn_020b59ac(arg0, arg2, arg3) != 0) {
        return 5U;
    }
    temp_r0 = native_fn_020b5b80();
    sp0 = temp_r0;
    if (temp_r0 != 0) {
        native_fn_0201b208(temp_r0, 0, 0xA0);
        M2C_FIELD(sp0, s32 *, 0) = arg2;
        M2C_FIELD(sp0, s16 *, 4) = arg3;
        M2C_FIELD(sp0, void **, 8) = arg0;
        M2C_FIELD(sp0, u32 *, 0x1C) = native_fn_020a8ef8();
        M2C_FIELD(sp0, u32 *, 0x88) = (u32) M2C_FIELD(sp0, u32 *, 0x1C);
        M2C_FIELD(sp0, s16 *, 0x64) = 0;
        M2C_FIELD(sp0, s16 *, 0x66) = 0;
        if ((native_fn_020b3b34(sp0 + 0x44, M2C_FIELD(arg0, s32 *, 0x3C)) != 0) && (native_fn_020b3b34(sp0 + 0x50, M2C_FIELD(arg0, s32 *, 0x38)) != 0)) {
            M2C_FIELD(sp0, u32 *, 0x5C) = native_fn_020a85dc(0x10, 0x40, 0);
            if (M2C_FIELD(sp0, u32 *, 0x5C) != 0) {
                M2C_FIELD(sp0, u32 *, 0x60) = native_fn_020a85dc(0x10, 0x40, 0);
                if (M2C_FIELD(sp0, u32 *, 0x60) != 0) {
                    M2C_FIELD(sp0, u32 *, 0x98) = native_fn_020a85dc(4, 2, 0);
                    if (M2C_FIELD(sp0, u32 *, 0x98) != 0) {
                        M2C_FIELD(sp0, u32 *, 0x9C) = native_fn_020a85dc(4, 2, 0);
                        if (M2C_FIELD(sp0, u32 *, 0x9C) != 0) {
                            native_fn_020a89a4(M2C_FIELD(arg0, s32 *, 0xC), &sp0);
                            temp_r0_2 = native_fn_020b59ac(arg0, arg2, arg3);
                            *arg1 = temp_r0_2;
                            if (temp_r0_2 != 0) {
                                return 0U;
                            }
                        }
                    }
                }
            }
        }
    }
    if (sp0 != 0) {
        native_fn_020a929c(M2C_FIELD(sp0, u32 *, 0x44));
        native_fn_020a929c(M2C_FIELD(sp0, u32 *, 0x50));
        if (M2C_FIELD(sp0, u32 *, 0x5C) != 0) {
            native_fn_020a8614();
        }
        if (M2C_FIELD(sp0, u32 *, 0x60) != 0) {
            native_fn_020a8614();
        }
        if (M2C_FIELD(sp0, u32 *, 0x98) != 0) {
            native_fn_020a8614();
        }
        if (M2C_FIELD(sp0, u32 *, 0x9C) != 0) {
            native_fn_020a8614();
        }
        native_fn_020a929c(sp0);
    }
    return 1U;
}
