typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
struct NativeSoundRegister { u32 control, source; u16 timer, loopStart; u32 loopLength; };
typedef char RegisterSize[(sizeof(struct NativeSoundRegister) == 16) ? 1 : -1];
extern s32 native_host_arm7_data_038075c8;
extern u32 native_host_arm7_data_03807980;
extern u8 native_host_arm7_data_03807984[16];
extern u8 native_host_arm7_data_03807994[16];
extern u32 native_host_arm7_arm_037fec40(u32, s32);
#define NativeRegister(channel) ((volatile struct NativeSoundRegister *)(0x04000400u + (u32)(channel) * 16u))
