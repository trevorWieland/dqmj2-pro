typedef unsigned int u32;
typedef struct NativeArm7BootParameters {
    u32 autoloadTableBegin;
    u32 autoloadTableEnd;
    u32 initializedSource;
    u32 zeroFillBegin;
    u32 zeroFillEnd;
    u32 unknown14;
} NativeArm7BootParameters;
const NativeArm7BootParameters native_arm7_boot_parameters_02380204 = {
    0x023a7118,
    0x023a7130,
    0x0238021c,
    0x0238021c,
    0x0238021c,
    0
};
