typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u16 Basic; u16 Support; } NativeRateSet;
typedef struct {
    u32 opaquePrefixWords[7];
    u16 FrameLifeTimePerBeacon;
    u8 opaqueSuffix[10];
} NativeConfigView;
typedef struct {
    u32 opaquePrefixWords[24];
    NativeRateSet RateSet;
    u8 opaqueBeforeBeacon[10];
    u16 BeaconPeriod;
    u8 opaqueBeforeDtim[4];
    u16 DTIMPeriod;
    u8 opaqueBeforeLifeTime[22];
    u16 FrameLifeTime;
} NativeWorkView;
typedef struct {
    u32 opaquePrefixWords[199];
    NativeConfigView Config;
    NativeWorkView Work;
} NativeWlView;
extern u32 native_host_arm7_runtime_word_0380fff4;
extern u32 native_host_arm7_arm_027e9e3c(u32);
extern u32 native_host_arm7_arm_027e9bd8(void);
extern u32 native_host_arm7_arm_027ea584(void);
extern u32 native_host_arm7_arm_027f4e1c(u32,u32,u32);
#define wlMan ((NativeWlView *)native_host_arm7_runtime_word_0380fff4)
