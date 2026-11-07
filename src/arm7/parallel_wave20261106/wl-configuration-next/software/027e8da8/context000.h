typedef unsigned short int u16;

typedef unsigned long u32;

extern const u16 (*ctrdgi_fl_maxtime);

typedef struct {
    u32 Prev;
    u32 Next;
    u16 Flag;
    u16 BufID;
} HEAPBUF_HEADER, *LPHEAPBUF_HEADER;

typedef struct {
    LPHEAPBUF_HEADER Head;
    LPHEAPBUF_HEADER Tail;
    u16 Count;
    u16 Flag;
} HEAPBUF_MAN, *LPHEAPBUF_MAN;

u32 native_host_arm7_arm_037f8908(LPHEAPBUF_MAN pBufMan, void *pBuf);

void *GetHeapBufNextAdrs(void *pBuf);

void native_host_arm7_main_027e8da8(LPHEAPBUF_MAN pHeapBufMan);

u32 native_host_arm7_arm_037f8908(LPHEAPBUF_MAN pBufMan, void *pBuf);

void *GetHeapBufNextAdrs(void *pBuf)
{
    LPHEAPBUF_HEADER pHeader = (LPHEAPBUF_HEADER)pBuf;
    return (void *)(pHeader->Next);
}
