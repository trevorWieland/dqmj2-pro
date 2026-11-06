typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    void *previous;
    void *next;
} Link;
typedef struct {
    void *head;
    void *tail;
    u16 count;
    u16 offset;
} List;
typedef struct {
    u32 signature;
    Link link;
    List children;
    void *start;
    void *end;
    u32 attribute;
} Heap;
typedef struct Block Block;
struct Block {
    u16 signature;
    u16 attribute;
    u32 size;
    Block *previous;
    Block *next;
};
typedef struct {
    Block *freeHead;
    Block *freeTail;
    Block *usedHead;
    Block *usedTail;
    u16 group;
    u16 feature;
} ExpHeap;
typedef struct {
    void *start;
    void *end;
} Region;
typedef unsigned long DWORD;
typedef void *HANDLE;
__declspec(dllimport) HANDLE __stdcall GetStdHandle(int);
__declspec(dllimport) int __stdcall ReadFile(HANDLE, void *, DWORD, DWORD *, void *);
__declspec(dllimport) int __stdcall WriteFile(HANDLE, const void *, DWORD, DWORD *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, DWORD, DWORD);
__declspec(dllimport) void __stdcall ExitProcess(u32);
u32 native_data_020edf74;
List native_data_020edf78;
extern void native_main_0202b914(Heap *, u32, void *, void *, u16);
extern Heap *native_main_0202ae28(void *, void *, u16);
extern u32 native_main_0202bb88(void *, int);
void *native_fn_0202bb88(List *list, void *object) {
    return (void *)native_main_0202bb88(list, (int)object);
}
void native_fn_02008c14(u32 value, void *destination, u32 bytes) {
    u32 *cursor = destination;
    u32 *end = (u32 *)((u8 *)destination + bytes);
    while (cursor < end) {
        *cursor++ = value;
    }
}
static u8 global_page[4096];
static void copy(u8 *destination, const u8 *source, u32 bytes) {
    u32 index;
    for (index = 0; index < bytes; ++index) {
        destination[index] = source[index];
    }
}
static int read_all(HANDLE handle, void *buffer, u32 bytes) {
    u8 *cursor = buffer;
    while (bytes) {
        DWORD completed = 0;
        if (!ReadFile(handle, cursor, bytes, &completed, 0) || !completed) {
            return 0;
        }
        cursor += completed;
        bytes -= completed;
    }
    return 1;
}
static int write_all(HANDLE handle, const void *buffer, u32 bytes) {
    const u8 *cursor = buffer;
    while (bytes) {
        DWORD completed = 0;
        if (!WriteFile(handle, cursor, bytes, &completed, 0) || !completed) {
            return 0;
        }
        cursor += completed;
        bytes -= completed;
    }
    return 1;
}
void j2p_entry(void) {
    HANDLE input = GetStdHandle(-10);
    HANDLE output = GetStdHandle(-11);
    u8 *data = VirtualAlloc((void *)0x02380000, 4096, 0x3000, 4);
    u32 header[3];
    u32 index;
    if (sizeof(void *) != 4 || sizeof(Heap) != 36 || sizeof(List) != 12 || data != (u8 *)0x02380000) {
        ExitProcess(2);
    }
    if (!read_all(input, header, sizeof(header)) || header[0] != 0x4A324850 || header[1] != 1) {
        ExitProcess(3);
    }
    if (!write_all(output, header, sizeof(header))) {
        ExitProcess(4);
    }
    for (index = 0; index < header[2]; ++index) {
        u32 words[7];
        u32 result[3];
        if (!read_all(input, words, sizeof(words)) || !read_all(input, data, 4096) || !read_all(input, global_page, 4096)) {
            ExitProcess(5);
        }
        copy((u8 *)&native_data_020edf74, global_page + 0xF74, 4);
        copy((u8 *)&native_data_020edf78, global_page + 0xF78, 12);
        result[0] = words[0];
        result[1] = words[1];
        result[2] = 0;
        if (words[0] == 0x0202B914) {
            native_main_0202b914((Heap *)words[2], words[3], (void *)words[4], (void *)words[5], (u16)words[6]);
        } else if (words[0] == 0x0202AE28) {
            result[2] = (u32)native_main_0202ae28((void *)words[2], (void *)words[3], (u16)words[4]);
        } else {
            ExitProcess(6);
        }
        copy(global_page + 0xF74, (const u8 *)&native_data_020edf74, 4);
        copy(global_page + 0xF78, (const u8 *)&native_data_020edf78, 12);
        if (!write_all(output, result, sizeof(result)) || !write_all(output, data, 4096) || !write_all(output, global_page, 4096)) {
            ExitProcess(7);
        }
    }
    ExitProcess(0);
}
