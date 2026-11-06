typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef volatile u8 REGType8v;
typedef int BOOL;
enum SNDLoop { SND_CAP_LOOP = 0, SND_CAP_ONESHOT = 1 };
#define reg_SNDCAPxCNT(x) (*(REGType8v *)(0x4000508 + ((int)(x))))
#define reg_SOUNDCNT_MIX (*(REGType8v *)0x4000501)
