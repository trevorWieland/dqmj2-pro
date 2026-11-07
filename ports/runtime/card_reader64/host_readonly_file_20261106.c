#include <stddef.h>
#include "card_reader_20261106.h"

#if defined(_WIN32)
__declspec(dllimport) void *__stdcall GetProcessHeap(void);
__declspec(dllimport) void *__stdcall HeapAlloc(void *, uint32_t, size_t);
__declspec(dllimport) int __stdcall HeapFree(void *, uint32_t, void *);
__declspec(dllimport) int __stdcall MultiByteToWideChar(uint32_t, uint32_t, const char *, int, uint16_t *, int);
__declspec(dllimport) void *__stdcall CreateFileW(const uint16_t *, uint32_t, uint32_t, void *, uint32_t, uint32_t, void *);
__declspec(dllimport) int __stdcall SetFilePointerEx(void *, int64_t, int64_t *, uint32_t);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, uint32_t, uint32_t *, void *);
__declspec(dllimport) int __stdcall CloseHandle(void *);
typedef struct { void *handle; } HostFile;

void *j2p_readonly_open(const char *path) {
    HostFile *file;
    uint16_t *wide;
    void *handle;
    int length;
    if (!path) return 0;
    length = MultiByteToWideChar(65001, 8, path, -1, 0, 0);
    if (length <= 0 || length > 32768) return 0;
    wide = HeapAlloc(GetProcessHeap(), 0, (size_t)length * 2);
    if (!wide) return 0;
    if (!MultiByteToWideChar(65001, 8, path, -1, wide, length)) {
        HeapFree(GetProcessHeap(), 0, wide);
        return 0;
    }
    handle = CreateFileW(wide, UINT32_C(0x80000000), 1, 0, 3, 0x80, 0);
    HeapFree(GetProcessHeap(), 0, wide);
    if ((intptr_t)handle == -1) return 0;
    file = HeapAlloc(GetProcessHeap(), 0, sizeof(*file));
    if (!file) {
        CloseHandle(handle);
        return 0;
    }
    file->handle = handle;
    return file;
}

int j2p_readonly_read_at(void *context, uint32_t offset, unsigned char *destination, uint32_t length) {
    HostFile *file = context;
    uint32_t total = 0;
    if (!file || (length && !destination) || !SetFilePointerEx(file->handle, offset, 0, 0)) return 0;
    while (total < length) {
        uint32_t received = 0;
        if (!ReadFile(file->handle, destination + total, length - total, &received, 0) || !received) return 0;
        total += received;
    }
    return 1;
}

int j2p_readonly_close(void *context) {
    HostFile *file = context;
    int status;
    if (!file) return 0;
    status = CloseHandle(file->handle);
    HeapFree(GetProcessHeap(), 0, file);
    return status != 0;
}
#else
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
typedef struct { int descriptor; } HostFile;

void *j2p_readonly_open(const char *path) {
    HostFile *file;
    int descriptor;
    if (!path) return 0;
    descriptor = open(path, O_RDONLY);
    if (descriptor < 0) return 0;
    file = malloc(sizeof(*file));
    if (!file) {
        close(descriptor);
        return 0;
    }
    file->descriptor = descriptor;
    return file;
}

int j2p_readonly_read_at(void *context, uint32_t offset, unsigned char *destination, uint32_t length) {
    HostFile *file = context;
    uint32_t total = 0;
    if (!file || (length && !destination)) return 0;
    while (total < length) {
        ssize_t received = pread(file->descriptor, destination + total, length - total, (off_t)offset + total);
        if (received < 0 && errno == EINTR) continue;
        if (received <= 0) return 0;
        total += (uint32_t)received;
    }
    return 1;
}

int j2p_readonly_close(void *context) {
    HostFile *file = context;
    int status;
    if (!file) return 0;
    status = close(file->descriptor);
    free(file);
    return status == 0;
}
#endif
