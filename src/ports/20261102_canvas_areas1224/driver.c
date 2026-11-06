typedef unsigned int u32;
typedef unsigned char u8;
typedef struct NNSiG2dCharCanvasVTable NNSiG2dCharCanvasVTable;
typedef struct NNSG2dCharCanvas {
    u8 *charBase;
    int areaWidth;
    int areaHeight;
    u8 dstBpp;
    u8 reserved[3];
    unsigned long param;
    const NNSiG2dCharCanvasVTable *vtable;
} NNSG2dCharCanvas;
typedef char canvas_width[(sizeof(NNSG2dCharCanvas)==24)?1:-1];
typedef char pointer_width[(sizeof(void *) == 4) ? 1 : -1];
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
extern void native_main_02035650(void *,int,int,int,int,unsigned long,int);
extern void native_main_02035e40(const NNSG2dCharCanvas *,int,int,int,int,int);
extern void native_main_02035fdc(const NNSG2dCharCanvas *,int,int,int,int,int);
unsigned long native_fn_0203553c(unsigned long x,unsigned long y,unsigned long width,unsigned long height,unsigned long sw,unsigned long sh) {
    unsigned long ow=1UL<<sw,oh=1UL<<sh;
    (void)height;
    return ((y/oh)*(width/ow)+x/ow)*ow*oh+(y%oh)*ow+x%ow;
}
void native_fn_02008c58(unsigned long value,void *destination,unsigned long size) {
    unsigned long *words=destination;
    unsigned long index;
    for(index=0;index<size/4;++index)words[index]=value;
}

static void read_exact(void *handle, void *destination, u32 size) {
    u8 *out = destination;
    while (size) {
        u32 count = 0;
        if (!ReadFile(handle, out, size, &count, 0) || !count) ExitProcess(81);
        out += count;
        size -= count;
    }
}

static void write_exact(void *handle, const void *source, u32 size) {
    const u8 *data = source;
    while (size) {
        u32 count = 0;
        if (!WriteFile(handle, data, size, &count, 0) || !count) ExitProcess(82);
        data += count;
        size -= count;
    }
}

void entry(void) {
    void *input = GetStdHandle((u32)-10), *output = GetStdHandle((u32)-11);
    u8 *data = VirtualAlloc((void *)0x02400000, 32768, 0x3000, 4);
    u32 total, index;
    if (data != (void *)0x02400000 || sizeof(unsigned long) != 4) ExitProcess(83);
    read_exact(input, &total, 4);
    if (total > 8192) ExitProcess(84);
    for (index = 0; index < total; ++index) {
        u32 h[9];
        read_exact(input, h, sizeof(h));
        read_exact(input, data, 32768);
        if(h[0]==0x02035650)
            native_main_02035650((void *)h[1],h[2],h[3],h[4],h[5],h[6],h[7]);
        else if(h[0]==0x02035E40)
            native_main_02035e40((const NNSG2dCharCanvas *)h[1],h[2],h[3],h[4],h[5],h[6]);
        else if(h[0]==0x02035FDC)
            native_main_02035fdc((const NNSG2dCharCanvas *)h[1],h[2],h[3],h[4],h[5],h[6]);
        else ExitProcess(85);
        write_exact(output, &index, 4);
        write_exact(output, data, 32768);
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(86);
    ExitProcess(0);
}
