typedef unsigned int u32;
typedef enum { OS_ARENA_MAIN=0,OS_ARENA_MAIN_SUBPRIV=1,OS_ARENA_MAINEX=2,OS_ARENA_ITCM=3,OS_ARENA_DTCM=4,
    OS_ARENA_SHARED=5,OS_ARENA_WRAM_MAIN=6,OS_ARENA_WRAM_SUB=7,OS_ARENA_WRAM_SUBPRIV=8,OS_ARENA_MAX=9 } OSArenaId;
struct NativeArenaArrays { void *lo[9],*hi[9]; };
typedef char UsedArenaPrefixSize[(sizeof(struct NativeArenaArrays)==72)?1:-1];
#define OSi_GetArenaInfo() (*(struct NativeArenaArrays *)0x027ffda0)
extern void *native_host_arm7_arm_037fcabc(OSArenaId);
extern void *native_host_arm7_arm_037fcb38(OSArenaId);
