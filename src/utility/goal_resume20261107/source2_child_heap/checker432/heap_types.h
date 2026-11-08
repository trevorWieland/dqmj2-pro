typedef unsigned int u32;
typedef signed int s32;
typedef unsigned char u8;

typedef struct HeapSelection {
    s32 currentHeap;
} HeapSelection;

typedef struct HeapCell HeapCell;
struct HeapCell {
    HeapCell *previous;
    HeapCell *next;
    u32 size;
    u8 opaque[20];
};

typedef struct HeapDescriptor {
    s32 totalBytes;
    HeapCell *freeHead;
    HeapCell *allocatedHead;
} HeapDescriptor;

typedef struct HeapArena {
    HeapSelection selection;
    s32 heapCount;
    u8 *arenaStart;
    u8 *arenaEnd;
    HeapDescriptor *descriptors;
} HeapArena;
