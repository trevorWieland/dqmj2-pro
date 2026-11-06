typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef int OSHeapHandle;
typedef u32 OSIntrMode;
typedef enum { OS_ARENA_MAIN=0,OS_ARENA_MAIN_SUBPRIV=1,OS_ARENA_MAINEX=2,OS_ARENA_ITCM=3,OS_ARENA_DTCM=4,
    OS_ARENA_SHARED=5,OS_ARENA_WRAM_MAIN=6,OS_ARENA_WRAM_SUB=7,OS_ARENA_WRAM_SUBPRIV=8,OS_ARENA_MAX=9 } OSArenaId;
typedef struct Cell Cell;
struct Cell { Cell *prev,*next; long size; };
typedef struct { long size; Cell *free,*allocated; } HeapDesc;
typedef struct { volatile OSHeapHandle currentHeap; int numHeaps; void *arenaStart,*arenaEnd; HeapDesc *heapArray; } OSHeapInfo;
typedef char CellSize[(sizeof(Cell)==12)?1:-1];
typedef char HeapSize[(sizeof(HeapDesc)==12)?1:-1];
typedef char InfoSize[(sizeof(OSHeapInfo)==20)?1:-1];
#define NULL ((void *)0)
#define OSi_ROUND(value,alignment) (((u32)(value)+((alignment)-1))&~((alignment)-1))
#define OSi_TRUNC(value,alignment) ((u32)(value)&~((alignment)-1))
#define OSi_OFFSET(value,alignment) ((u32)(value)&((alignment)-1))
#define OSi_InRange(value,start,end) ((u32)(start)<=(u32)(value)&&(u32)(value)<(u32)(end))
#define HEADERSIZE OSi_ROUND(sizeof(Cell),32)
#define MINOBJSIZE (HEADERSIZE+32)
#define OSi_CHECK(expression) do { if (!(expression)) { goto exit_OS_CheckHeap; } } while (0)
extern OSHeapInfo *native_host_arm7_data_03807870[9];
extern u32 native_host_arm7_arm_037fdd00(void);
extern u32 native_host_arm7_arm_037fdd14(u32);
extern Cell *native_host_arm7_arm_037fcba4(Cell *,Cell *);
extern Cell *native_host_arm7_arm_037fcbcc(Cell *,Cell *);
#define OSiHeapInfo native_host_arm7_data_03807870
#define OS_DisableInterrupts native_host_arm7_arm_037fdd00
#define OS_RestoreInterrupts native_host_arm7_arm_037fdd14
#define DLExtract native_host_arm7_arm_037fcba4
#define DLInsert native_host_arm7_arm_037fcbcc

static inline Cell* DLAddFront(Cell* list, Cell* cell)
{
    cell->next = list;
    cell->prev = NULL;

    if (list != NULL)
        list->prev = cell;
    return cell;
}
