#include "context.h"
u32 native_ov001_0220fa6c(void *arg0) {
    u32 var_r4;

    var_r4 = 0;
    if (((s32) native_fn_0207b674(0x2A, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 2) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x40);
    }
    if (((s32) native_fn_0207b674(0x48, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 2) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x2000);
    }
    if (((s32) native_fn_0207b674(0x7B, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 5) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x8000);
    }
    if (((s32) native_fn_0207b674(0x7C, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 5) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x10000);
    }
    if (((s32) native_fn_0207b674(0x7D, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 5) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x20000);
    }
    if (((s32) native_fn_0207b674(0xBC, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 5) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x02000000);
    }
    if (((s32) native_fn_0207b674(0x7E, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 5) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x40000);
    }
    if (((s32) native_fn_0207b674(0x7F, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0x64, 0x19) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x100000);
    }
    if (((s32) native_fn_0207b674(0xEC, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0x64, 0x19) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x200000);
    }
    if (((s32) native_fn_0207b674(0xED, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0x64, 0x19) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x400000);
    }
    if (((s32) native_fn_0207b674(0xBE, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0x64, 0x19) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x04000000);
    }
    if (((s32) native_fn_0207b674(0xBD, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (native_fn_ov001_02210ad0(arg0, 0x64, 0x19) != 0)) {
        var_r4 |= 1;
        M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 0x08000000);
    }
    return var_r4;
}
