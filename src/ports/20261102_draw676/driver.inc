__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
typedef struct { u32 op, count, values[64]; } Command;
static Command commands[4];
static u32 command_count, texture_count, texture[11];
void native_fn_0202e434(u32 op, const u32 *values, u32 count) {
    Command *command;
    u32 i;
    if (command_count >= 4 || count > 64) ExitProcess(81);
    command = commands + command_count++;
    command->op = op;
    command->count = count;
    for (i = 0; i < count; ++i) command->values[i] = values[i];
}
u32 native_fn_0202e380(s32 *source, u32 bytes) {
    if (bytes < 4 || bytes > 256 || (bytes & 3)) ExitProcess(82);
    native_fn_0202e434((u32)source[0], (const u32 *)(source + 1), bytes / 4 - 1);
    return 0xC676C676U;
}
static void record_texture(u32 mode, const NNSG3dMatAnmResult *result) {
    u32 i;
    if (++texture_count != 1) ExitProcess(83);
    for (i = 0; i < 11; ++i) texture[i] = 0;
    texture[0] = mode;
    texture[1] = result->flag;
    if (!(result->flag & 1)) {
        texture[2] = result->scaleS;
        texture[3] = result->scaleT;
    }
    if (!(result->flag & 2)) texture[4] = (u16)result->sinR | ((u32)(u16)result->cosR << 16);
    if (!(result->flag & 4)) {
        texture[5] = result->transS;
        texture[6] = result->transT;
    }
    texture[7] = result->origWidth | ((u32)result->origHeight << 16);
    texture[8] = result->magW;
    texture[9] = result->magH;
}
static void texture0(const NNSG3dMatAnmResult *result) { record_texture(0, result); }
static void texture1(const NNSG3dMatAnmResult *result) { record_texture(1, result); }
static void texture2(const NNSG3dMatAnmResult *result) { record_texture(2, result); }
static void texture3(const NNSG3dMatAnmResult *result) { record_texture(3, result); }
NNSG3dSendTexSRT native_data_020dd680[4] = {texture0, texture1, texture2, texture3};
static void read_exact(void *handle, void *destination, u32 size) {
    u8 *out = destination;
    while (size) {
        u32 count = 0;
        if (!ReadFile(handle, out, size, &count, 0) || !count) ExitProcess(84);
        out += count;
        size -= count;
    }
}
static void write_exact(void *handle, const void *source, u32 size) {
    const u8 *data = source;
    while (size) {
        u32 count = 0;
        if (!WriteFile(handle, data, size, &count, 0) || !count) ExitProcess(85);
        data += count;
        size -= count;
    }
}
void entry(void) {
    void *input = GetStdHandle((u32)-10), *output = GetStdHandle((u32)-11);
    u8 *data = VirtualAlloc((void *)0x02400000, 65536, 0x3000, 4);
    u32 total, index;
    if (data != (void *)0x02400000 || sizeof(void *) != 4 || sizeof(NNSG3dMatAnmResult) != 56) ExitProcess(86);
    read_exact(input, &total, 4);
    if (total > 4096) ExitProcess(87);
    for (index = 0; index < total; ++index) {
        u32 args[4], header[3], i;
        read_exact(input, args, sizeof(args));
        read_exact(input, data, 65536);
        command_count = texture_count = 0;
        native_main_0202dafc((const NNSG3dResMdl *)args[0], args[1], args[2], (BOOL)args[3]);
        header[0] = index;
        header[1] = command_count;
        header[2] = texture_count;
        write_exact(output, header, sizeof(header));
        for (i = 0; i < command_count; ++i) write_exact(output, commands + i, (2 + commands[i].count) * 4);
        if (texture_count) write_exact(output, texture, sizeof(texture));
        write_exact(output, data, 65536);
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(88);
    ExitProcess(0);
}
