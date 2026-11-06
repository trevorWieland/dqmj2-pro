typedef unsigned char u8;
typedef unsigned short int u16;
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
typedef struct {
	void * lo[OS_ARENA_MAX];
	void * hi[OS_ARENA_MAX];
	u16 initialized;
	u8 padding[2];
} OSArenaInfo;
void native_main_020076ec(OSArenaId id, void * newHi);
extern const u16 (*ctrdgi_fl_maxtime);
