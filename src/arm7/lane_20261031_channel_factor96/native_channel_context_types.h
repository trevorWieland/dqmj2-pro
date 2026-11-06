typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef volatile u8 REGType8v;
typedef volatile u16 REGType16v;
typedef volatile u32 REGType32v;
extern s32 native_host_arm7_data_038075c8;
extern u32 native_host_arm7_data_03807980;
extern u8 native_host_arm7_data_03807984[16];
extern u8 native_host_arm7_data_03807994[16];
extern u32 native_host_arm7_arm_037fec40(u32,s32);
#define sMasterPan native_host_arm7_data_038075c8
#define sSurroundDecay ((s32)native_host_arm7_data_03807980)
#define sOrgPan native_host_arm7_data_03807984
#define sOrgVolume native_host_arm7_data_03807994
#define CalcSurroundDecay native_host_arm7_arm_037fec40
#define reg_SOUNDxCNT_VOL(x)  (*(REGType8v *)(0x4000400 + ((int)(x) * 0x10)))
#define reg_SOUNDxCNT_VOLS(x) (*(REGType16v *)(0x4000400 + ((int)(x) * 0x10)))
#define reg_SOUNDxCNT_PAN(x)  (*(REGType8v *)(0x4000402 + ((int)(x) * 0x10)))
#define reg_SOUNDoffCNT(off)  (*(REGType32v *)(0x4000400 + (int)(off)))
#define reg_SOUNDoffSAD(off)  (*(REGType32v *)(0x4000404 + (int)(off)))
#define reg_SOUNDoffTMR(off)  (*(REGType16v *)(0x4000408 + (int)(off)))
#define reg_SOUNDoffPNT(off)  (*(REGType16v *)(0x400040A + (int)(off)))
#define reg_SOUNDoffLEN(off)  (*(REGType32v *)(0x400040C + (int)(off)))
#define SND_CHANNEL_COUNT 16
