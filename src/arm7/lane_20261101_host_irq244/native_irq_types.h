typedef unsigned int u32;
typedef unsigned short u16;
#define NATIVE_IME (*(volatile u16 *)0x04000208)
#define NATIVE_IE (*(volatile u32 *)0x04000210)
#define NATIVE_IF (*(volatile u32 *)0x04000214)
extern u32 native_host_arm7_arm_037fb8d8(void);
