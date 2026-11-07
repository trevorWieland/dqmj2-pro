typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef int BOOL;

typedef u32 OSIntrMode;

extern OSIntrMode native_host_arm7_arm_037fdd00(void);

extern OSIntrMode native_host_arm7_arm_037fdd14(OSIntrMode state);

typedef enum SPIDeviceType {
	SPI_DEVICE_TYPE_TP = 0,
	SPI_DEVICE_TYPE_NVRAM,
	SPI_DEVICE_TYPE_MIC,
	SPI_DEVICE_TYPE_PM,
	SPI_DEVICE_TYPE_ARM7,
	SPI_DEVICE_TYPE_MAX
} SPIDeviceType;

typedef struct SPIEntry {
    SPIDeviceType type;
    u32 process;
    u32 arg[4 ];
} SPIEntry;

void native_host_arm7_arm_03803a48(u16 command, u16 result);

BOOL native_host_arm7_arm_03803b0c(SPIDeviceType type);

void native_host_arm7_arm_03803b28(SPIDeviceType type);

void native_host_arm7_arm_03803b40(SPIDeviceType type);

extern const u16 (*ctrdgi_fl_maxtime);

void native_host_arm7_arm_027f55c4(u32 address, u32 size, u8 *pData);

void native_host_arm7_main_027f5188(SPIEntry *entry);

void native_host_arm7_arm_027f54b0(void);

void native_host_arm7_arm_027f5514(void);

void native_host_arm7_arm_027f5554(u8 *buf);

void native_host_arm7_arm_027f56ec(u32 address, u32 size, u8 *buf);

void native_host_arm7_arm_027f580c(u32 address, u16 size, const u8 *buf);

void native_host_arm7_arm_027f5918(u32 address, u16 size, const u8 *buf);

void native_host_arm7_arm_027f5a24(u32 address);

void native_host_arm7_arm_027f5aac(u32 address);

void native_host_arm7_arm_027f5b34(void);

void native_host_arm7_arm_027f5b74(void);

void native_host_arm7_arm_027f5bb4(void);

void native_host_arm7_arm_027f5bf4(u8 *buf);

void native_host_arm7_arm_027f5c90(void);

extern BOOL native_host_arm7_arm_027f545c(void);

extern BOOL native_host_arm7_arm_027f5480(void);
