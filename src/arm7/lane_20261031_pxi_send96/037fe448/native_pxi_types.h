typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef u32 OSIntrMode;
#define NULL ((void *)0)
#define true 1
#define PXI_IPC_FIFO_CNT_SEND_FULL 2
#define PXI_IPC_FIFO_CNT_RECV_EMPTY 256
#define PXI_IPC_FIFO_CNT_ERROR 0x4000
#define PXI_IPC_FIFO_CNT_ERROR_ACK 0x4000
#define PXI_IPC_FIFO_CNT_ENABLE 0x8000
typedef union PXI_UnkStruct1 { struct { u32 unk_00_0:5,unk_00_5:1,unk_00_6:26; } fields; u32 word; } PXI_UnkStruct1;
typedef char WordSize[(sizeof(PXI_UnkStruct1)==4)?1:-1];
#define REG_IPC_FIFO_CNT (*(volatile u16 *)0x04000184)
#define REG_IPC_FIFO_SEND (*(volatile u32 *)0x04000188)
#define REG_04100000 (*(volatile PXI_UnkStruct1 *)0x04100000)
extern void (*native_host_arm7_data_038078d0[32])(u32,u32,u32);
#define sFifoRecvCallbacks native_host_arm7_data_038078d0
extern u32 native_host_arm7_arm_037fdd00(void);
extern u32 native_host_arm7_arm_037fdd14(u32);
#define OS_DisableInterrupts native_host_arm7_arm_037fdd00
#define OS_RestoreInterrupts native_host_arm7_arm_037fdd14
extern s32 native_host_arm7_arm_037fe448(u32);
#define PXIi_SendWord native_host_arm7_arm_037fe448
