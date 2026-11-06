typedef unsigned long u32;
typedef int BOOL;
extern u32 native_data_main_027e0000[];
u32 native_fn_02006de4(void);
typedef enum {
	OS_ARENA_MAIN            = 0,
	OS_ARENA_MAIN_SUBPRIV    = 1,
	OS_ARENA_MAINEX          = 2,
	OS_ARENA_ITCM            = 3,
	OS_ARENA_DTCM            = 4,
	OS_ARENA_SHARED          = 5,
	OS_ARENA_WRAM_MAIN       = 6,
	OS_ARENA_WRAM_SUB        = 7,
	OS_ARENA_WRAM_SUBPRIV    = 8,
	OS_ARENA_MAX             = 9
} OSArenaId;
void * native_main_02007560(OSArenaId id);
extern void native_data_main_027e0080(void);
extern void native_data_main_00001000(void);
extern void native_data_main_00001000(void);
typedef struct {
BOOL field_0000;
BOOL field_0004;
} NativeStorage_020e363c;
extern NativeStorage_020e363c native_data_main_020e363c;
