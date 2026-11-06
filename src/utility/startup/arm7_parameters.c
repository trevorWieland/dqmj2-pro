typedef unsigned int u32;
typedef struct UtilityArm7ModuleParameters {
    u32 autoloadTableBegin;
    u32 autoloadTableEnd;
    u32 autoloadPayloadBegin;
    u32 staticBssBegin;
    u32 staticBssEnd;
    u32 unknown14;
} UtilityArm7ModuleParameters;
UtilityArm7ModuleParameters native_utility_child_arm7_boot_params_02380198 = {
    0x23a5fe4,
    0x23a5ffc,
    0x23801b0,
    0x23801b0,
    0x23801b0,
    0x0,
};
