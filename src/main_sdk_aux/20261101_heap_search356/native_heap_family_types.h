typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef int BOOL;
#define NULL ((void *)0)
typedef struct Block Block;
struct Block { u16 marker,attributes; u32 bytes; Block *previous,*next; };
typedef struct { Block *head,*tail; } List;
typedef struct { List free,used; u16 group,feature; } ExpHeap;
typedef struct { u8 unknown[32]; u32 flags; ExpHeap exp; } Heap;
typedef struct { u32 begin,end; } Region;
typedef char Block_Size16[(sizeof(Block)==16)?1:-1];
typedef char ExpHeap_Size20[(sizeof(ExpHeap)==20)?1:-1];
extern u32 native_fn_0202ae9c(ExpHeap *,Block *,u32,u32,u16);
extern Block *native_fn_0202ada4(List *,Block *);
extern Block *native_fn_0202adcc(List *,Block *,Block *);
extern Block *native_fn_0202adfc(Region *,u32);
extern void native_fn_02008c14(u32,u32,u32);
extern u32 native_fn_0202b9cc(u32);
static inline u16 heap_mode(ExpHeap *exp) { return (u16)(exp->feature & 1); }
static inline u16 heap_options(List *list) { Heap *owner = (Heap *)((u8 *)list - 36); return (u16)(owner->flags & 255); }
