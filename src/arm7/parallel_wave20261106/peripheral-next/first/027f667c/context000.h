typedef unsigned short int u16;

typedef unsigned long u32;

typedef struct RTCRawStatus1 {
	u16 reset :1;
	u16 format :1;
	u16 dummy0 :2;
	u16 intr1 :1;
	u16 intr2 :1;
	u16 bld :1;
	u16 poc :1;
	u16 dummy1 :8;
} RTCRawStatus1;

typedef struct RTCRawAlarm {
	u32 week :3;
	u32 dummy0 :4;
	u32 we :1;
	u32 hour :6;
	u32 afternoon :1;
	u32 he :1;
	u32 minute :7;
	u32 me :1;
	u32 dummy2 :8;
} RTCRawAlarm;

void native_host_arm7_main_027f667c(u16 format);

void RTC_ReadStatus1(RTCRawStatus1 *stat);

void RTC_WriteStatus1(const RTCRawStatus1 *stat);

void native_host_arm7_arm_027f6f1c(void);

void native_host_arm7_arm_027f6f5c(void);

void native_host_arm7_arm_027f6f90(u16 command, u16 parameter);

void native_host_arm7_arm_027f7010(const void *pData, u32 size);

void RTCi_GpioReceiveData(void *pData, u32 size);

typedef enum {
	EXI_GPIOIF_SERIAL = 0x0000,
	EXI_GPIOIF_UNDEF  = 0x4000 ,
	EXI_GPIOIF_GPIO   = 0x8000 ,
	EXI_GPIOIF_JOY    = 0x8000 | 0x4000
} EXIGpioIF;

void native_host_arm7_arm_037fe5a8(EXIGpioIF type);

extern void native_host_arm7_arm_027f6ca0(RTCRawAlarm *alarm);

extern void native_host_arm7_arm_027f6db0(RTCRawAlarm *alarm);

void native_host_arm7_arm_027f6ec0(u16 inst, u16 param, void *buf, u32 size);
