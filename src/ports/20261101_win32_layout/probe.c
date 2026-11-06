typedef unsigned int u32;
typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Object {
    int frame, ratio;
    void *resource, *function;
    struct Object *next;
    const void *texture;
    u8 priority, count;
    u16 map[1];
} Object;
__declspec(dllimport) void *__stdcall GetStdHandle(u32 handle);
__declspec(dllimport) int __stdcall WriteFile(void *handle, const void *data, u32 size, u32 *written, void *overlapped);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32 code);
static const u32 layout[] = {sizeof(void *), sizeof(u32), sizeof(Object),
    (u32)&((Object *)0)->priority, (u32)&((Object *)0)->count, (u32)&((Object *)0)->map};
void entry(void) {
    u32 written = 0;
    int ok = WriteFile(GetStdHandle((u32)-11), layout, sizeof(layout), &written, 0);
    ExitProcess(!ok || written != sizeof(layout));
}
