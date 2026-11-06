typedef unsigned int u32;
typedef struct UtilityArm9ModuleParameters {
    u32 autoloadTableBegin;
    u32 autoloadTableEnd;
    u32 autoloadPayloadBegin;
    u32 staticBssBegin;
    u32 staticBssEnd;
    u32 compressedStaticEnd;
    u32 sdkVersion;
    u32 sdkMarker;
    u32 sdkMarkerReverse;
} UtilityArm9ModuleParameters;
UtilityArm9ModuleParameters native_utility_child_arm9_module_params_02000bb4 = {
    0x2022900,
    0x2022918,
    0x2022620,
    0x2022620,
    0x202cd00,
    0x201e4a0,
    0x3027531,
    0xdec00621,
    0x2106c0de,
};
