typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef int BOOL;
typedef enum {
	MI_CTRDG_ROMCYCLE1_10 = 0,
	MI_CTRDG_ROMCYCLE1_8 = 1,
	MI_CTRDG_ROMCYCLE1_6 = 2,
	MI_CTRDG_ROMCYCLE1_18 = 3
} MICartridgeRomCycle1st;
typedef enum {
	MI_CTRDG_ROMCYCLE2_6 = 0,
	MI_CTRDG_ROMCYCLE2_4 = 1
} MICartridgeRomCycle2nd;
typedef u32 OSIntrMode;
typedef struct {
	u32 startAddress;
	u8 nintendoLogo[0x9c];
	char titleName[12];
	u32 gameCode;
	u16 makerCode;
	u8 isRomCode;
	u8 machineCode;
	u8 deviceType;
	u8 exLsiID[3];
	u8 reserved_A[4];
	u8 softVersion;
	u8 complement;
	u16 moduleID;
} CTRDGHeader;
typedef struct {
	union {
		struct {
			u8 bitID;
			u8 numberID :5;
			u8 :2;
			u8 disableExLsiID :1;
		};
		u16 raw;
	};
} CTRDGModuleID;
typedef struct {
	CTRDGModuleID moduleID;
	u8 exLsiID[3];
	u8 isAgbCartridge :1;
	u8 detectPullOut :1;
	u8 :0;
	u16 makerCode;
	u32 gameCode;
} CTRDGModuleInfo;
BOOL native_main_02019214(void);
typedef struct CTRDGRomCycle {
	MICartridgeRomCycle1st c1;
	MICartridgeRomCycle2nd c2;
} CTRDGRomCycle;
typedef struct CTRDGLockByProc {
	BOOL locked;
	OSIntrMode irq;
} CTRDGLockByProc;
void native_fn_0201939c(u16 lockID, CTRDGLockByProc * info);
void native_fn_020193f8(u16 lockID, CTRDGLockByProc * info);
void native_fn_02019320(CTRDGRomCycle * r);
void native_fn_02019368(CTRDGRomCycle * r);
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct CTRDGWork {
	vu16 subpInitialized;
	u16 lockID;
} CTRDGWork;
typedef struct {
BOOL field_0000;
CTRDGWork field_0004;
} NativeStorage_020ec3b8;
extern NativeStorage_020ec3b8 native_data_main_020ec3b8;
void native_fn_02019320 (CTRDGRomCycle *r);
void native_fn_02019368 (CTRDGRomCycle *r);
void native_fn_0201939c (u16 lockID, CTRDGLockByProc *info);
void native_fn_020193f8 (u16 lockID, CTRDGLockByProc *info);
