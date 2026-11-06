typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef struct CPContext {
	u64 div_numer;
	u64 div_denom;
	u64 sqrt;
	u16 div_mode;
	u16 sqrt_mode;
} CPContext;
typedef struct OSContext {
	u32 cpsr;
	u32 r[13];
	u32 sp;
	u32 lr;
	u32 pc_plus4;
	u32 sp_svc;
	CPContext cp_context;
} OSContext;
typedef void (*OSExceptionHandler) (u32, void *);
void native_main_02007864(void);
typedef struct {
    OSContext context;
    u32 cp15;
    u32 spsr;
    u32 exinfo;
    u32 debug[4];
} OSiExContext;
typedef struct {
void * field_0000;
void * field_0004;
OSExceptionHandler field_0008;
u32 field_000c[8];
OSiExContext field_002c;
} NativeStorage_020e3644;
extern NativeStorage_020e3644 native_data_main_020e3644;
