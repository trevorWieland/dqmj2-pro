typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 head,tail;u16 count,offset; } HeapList;
typedef struct { u32 signature,previous,next;HeapList children;u32 begin,end,options; } CommonHeap;
typedef struct { u32 head,tail,opaqueState; } Frame;
typedef struct { CommonHeap common;Frame frame; } Heap;
typedef char Common36[(sizeof(CommonHeap)==36)?1:-1];
typedef char Frame12[(sizeof(Frame)==12)?1:-1];
typedef char Heap48[(sizeof(Heap)==48)?1:-1];
extern void native_fn_0202b914(void *,u32,u32,u32,u32);
extern void native_fn_02008c14(u32,u32,u32);
extern u32 native_fn_0202b9cc(u32);
static inline u16 frame_options(Frame *frame) {
    Heap *owner=(Heap *)((u8 *)frame-36);
    return (u16)(owner->common.options&255);
}
