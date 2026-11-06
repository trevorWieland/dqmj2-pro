#include "../../src/runtime/20261101_fifo_requests352/state.h"
typedef unsigned long DWORD;
typedef void *HANDLE;
__declspec(dllimport) HANDLE __stdcall GetStdHandle(int);
__declspec(dllimport) int __stdcall ReadFile(HANDLE, void *, DWORD, DWORD *, void *);
__declspec(dllimport) int __stdcall WriteFile(HANDLE, const void *, DWORD, DWORD *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, DWORD, DWORD);
__declspec(dllimport) void __stdcall ExitProcess(u32);
RequestState native_data_020e5438;
__declspec(align(4)) u8 native_data_020e53d0[60];
extern u32 native_main_0200ddf4(void);
extern u32 native_main_0200dfd8(void);
extern u32 native_main_0200f370(u32, u32, u32);
extern u32 native_main_0200f418(u32, u32, u32);
extern u32 native_main_0200f4c4(u32, u32, u32, u32);
extern s32 native_main_0200a440(u32, u32, u32);
static u32 callback_adapter(u32 first, u32 second, u32 third) {
    return (u32)native_main_0200a440(first, second, third);
}
__declspec(align(4)) u8 native_data_020ec360[12];
extern u32 native_main_020181b8(u32, u32);
extern u32 native_main_02018148(u32, u32, s32);
u32 native_fn_02018148(u32 first, u32 second, u32 third) {
    return native_main_02018148(first, second, (s32)third);
}
static u32 control;
static u32 irq_count;
static u32 irq_log[16];
static void record_irq(u32 address, u32 argument) {
    if (irq_count >= 8) {
        ExitProcess(9);
    }
    irq_log[irq_count * 2] = address;
    irq_log[irq_count * 2 + 1] = argument;
    ++irq_count;
}
u32 native_fn_02007ff4(void) {
    u32 previous = control & 0x80;
    control |= 0x80;
    record_irq(0x02007FF4, 0);
    return previous;
}
u32 native_fn_02008008(u32 value) {
    u32 previous = control & 0x80;
    control = (control & ~0x80U) | (value & 0x80);
    record_irq(0x02008008, value);
    return previous;
}
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
    u8 *mmio = VirtualAlloc((void *)0x04000000, 4096, 0x3000, 4);
    u32 header[3];
    u32 index;
    if (sizeof(void *) != 4 || sizeof(RequestState) != 40 || data != (u8 *)0x02380000 || mmio != (u8 *)0x04000000) {
        ExitProcess(2);
    }
    if (!read_all(input, header, sizeof(header)) || header[0] != 0x4A324649 || header[1] != 1 || !write_all(output, header, sizeof(header))) {
        ExitProcess(3);
    }
    for (index = 0; index < header[2]; ++index) {
        u32 words[7];
        u32 result[5];
        u32 slot;
        if (!read_all(input, words, sizeof(words)) || !read_all(input, data, 4096) || !read_all(input, mmio, 4096)) {
            ExitProcess(4);
        }
        control = words[6] & 0xFF;
        irq_count = 0;
        for (slot = 0; slot < 16; ++slot) {
            irq_log[slot] = 0;
        }
        copy((u8 *)&native_data_020e5438, data + 0x438, 40);
        copy(native_data_020e53d0, data + 0x3D0, 60);
        copy(native_data_020ec360, mmio + 0x360, 12);
        if (words[0] == 0x0200DDF4 || words[0] == 0x0200DFD8) {
            u32 callback = *(u32 *)(native_data_020e53d0 + 4);
            if (callback != 0 && callback != 0x0200A440) {
                ExitProcess(7);
            }
            if (callback) {
                *(u32 *)(native_data_020e53d0 + 4) = (u32)callback_adapter;
            }
        }
        result[0] = words[0];
        result[1] = words[1];
        if (words[0] == 0x0200F370) {
            result[2] = native_main_0200f370(words[2], words[3], words[4]);
        } else if (words[0] == 0x0200F418) {
            result[2] = native_main_0200f418(words[2], words[3], words[4]);
        } else if (words[0] == 0x0200F4C4) {
            result[2] = native_main_0200f4c4(words[2], words[3], words[4], words[5]);
        } else if (words[0] == 0x0200A440) {
            result[2] = (u32)native_main_0200a440(words[2], words[3], words[4]);
        } else if (words[0] == 0x0200DDF4) {
            result[2] = native_main_0200ddf4();
        } else if (words[0] == 0x0200DFD8) {
            result[2] = native_main_0200dfd8();
        } else if (words[0] == 0x020181B8) {
            result[2] = native_main_020181b8(words[2], words[3]);
        } else {
            ExitProcess(5);
        }
        if (words[0] == 0x020181B8) {
            copy(mmio + 0x360, native_data_020ec360, 12);
        } else if (words[0] == 0x0200DDF4 || words[0] == 0x0200DFD8) {
            u32 callback = *(u32 *)(native_data_020e53d0 + 4);
            if (callback == (u32)callback_adapter) {
                *(u32 *)(native_data_020e53d0 + 4) = 0x0200A440;
            } else if (callback != 0) {
                ExitProcess(8);
            }
            if (result[2] == (u32)native_data_020e53d0) {
                result[2] = 0x020E53D0;
            }
            copy(data + 0x3D0, native_data_020e53d0, 60);
        } else if (words[0] != 0x0200A440 && words[0] != 0x020181B8) {
            copy(data + 0x438, (const u8 *)&native_data_020e5438, 40);
        }
        result[3] = control;
        result[4] = irq_count;
        if (!write_all(output, result, sizeof(result)) || !write_all(output, irq_log, sizeof(irq_log)) || !write_all(output, data, 4096) || !write_all(output, mmio, 4096)) {
            ExitProcess(6);
        }
    }
    ExitProcess(0);
}
