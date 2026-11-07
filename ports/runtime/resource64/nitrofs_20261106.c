#include <stddef.h>
#include "nitrofs_20261106.h"
#include "nitrofs_types_20261106.h"

#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error Native FS metadata objects require a qualified little-endian target
#endif

#if defined(_WIN32)
__declspec(dllimport) void *__stdcall GetProcessHeap(void);
__declspec(dllimport) void *__stdcall HeapAlloc(void *, uint32_t, size_t);
__declspec(dllimport) int __stdcall HeapFree(void *, uint32_t, void *);
static void *fs_allocate(size_t n) { return HeapAlloc(GetProcessHeap(), 8, n); }
static void fs_free(void *p) { if (p) HeapFree(GetProcessHeap(), 0, p); }
#else
#include <stdlib.h>
static void *fs_allocate(size_t n) { return calloc(1, n); }
static void fs_free(void *p) { free(p); }
#endif

struct J2pNitroFS {
    J2pScope scope;
    J2pGuestSpace io;
    unsigned char backend[0x120], cache[0x220], header[512];
    unsigned char *tables;
    char path[1024];
    void *file;
    FSArchive archive;
    uint32_t image_bytes, directories, file_count, named_files, reads, padded_reads, lookups;
};

static J2pNitroFS *fs_active;
_Static_assert(sizeof(u32) == 4 && sizeof(s32) == 4 && sizeof(FSArchiveFNT) == 8, "Native FS wire widths");
_Static_assert(sizeof(FSArchiveFAT) == 8, "FAT row width");

static uint32_t half(const unsigned char *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const unsigned char *p) { return half(p) | (half(p + 2) << 16); }
static void store(unsigned char *p, uint32_t value) {
    uint32_t i;
    for (i = 0; i != 4; ++i) p[i] = (unsigned char)(value >> (8 * i));
}

static int identity(J2pNitroFS *fs, J2pScope scope) {
    return fs && scope.program == fs->scope.program && scope.processor == fs->scope.processor &&
        scope.module == fs->scope.module && scope.generation == fs->scope.generation;
}

int j2p_nitrofs_card_read_at(void *context, uint32_t offset, unsigned char *destination, uint32_t length) {
    J2pNitroFS *fs = context;
    uint32_t available, i;
    if (!fs || !destination || length != 512 || (offset & 511) ||
        offset >= ((fs->image_bytes + 511) & ~UINT32_C(511))) return 0;
    available = fs->image_bytes - offset;
    if (available > 512) available = 512;
    if (!j2p_readonly_read_at(fs->file, offset, destination, available)) return 0;
    for (i = available; i != 512; ++i) destination[i] = 0xff;
    ++fs->reads;
    if (available < 512) ++fs->padded_reads;
    return 1;
}

static int transfer(J2pNitroFS *fs, J2pGuestSpace *space, uint32_t offset, uint32_t destination, uint32_t length) {
    unsigned char *backend;
    if ((uint64_t)offset + length > fs->image_bytes) return 0;
    if (!length) return 1;
    backend = j2p_guest_resolve(space, fs->scope, 0x020e5500, 0x120, 1);
    if (!backend || !j2p_guest_resolve(space, fs->scope, destination, length, 1)) return 0;
    store(backend + 0x1c, offset);
    store(backend + 0x20, destination);
    store(backend + 0x24, length);
    return j2p_card_read_polling(space, fs->scope, fs->cache, j2p_nitrofs_card_read_at, fs, length / 512 + 3) == 0;
}

static int validate(J2pNitroFS *fs) {
    const unsigned char *fnt = fs->tables, *fat = fnt + fs->archive.fnt_size;
    uint32_t d, i;
    fs->directories = half(fnt + 6);
    if (!fs->directories || fs->directories > 4096 || fs->directories * 8 > fs->archive.fnt_size) return 0;
    for (i = 0; i != fs->file_count; ++i) {
        uint32_t start = word(fat + i * 8), end = word(fat + i * 8 + 4);
        if (start > end || end > fs->image_bytes) return 0;
    }
    for (d = 0; d != fs->directories; ++d) {
        uint32_t pos = word(fnt + d * 8), index = half(fnt + d * 8 + 4), parent = d, steps = 0;
        if (pos < fs->directories * 8 || pos >= fs->archive.fnt_size || index > fs->file_count) return 0;
        while (parent) {
            if (++steps >= fs->directories) return 0;
            parent = half(fnt + parent * 8 + 6) & 4095;
            if (parent >= fs->directories) return 0;
        }
        for (;;) {
            uint32_t control, length;
            if (pos >= fs->archive.fnt_size) return 0;
            control = fnt[pos++];
            if (!control) break;
            length = control & 127;
            if (!length || length > fs->archive.fnt_size - pos) return 0;
            for (i = 0; i != length; ++i)
                if (!fnt[pos + i] || fnt[pos + i] == '/' || fnt[pos + i] == '\\' || fnt[pos + i] == ':') return 0;
            pos += length;
            if (control & 128) {
                uint32_t child;
                if (fs->archive.fnt_size - pos < 2) return 0;
                child = half(fnt + pos);
                pos += 2;
                if ((child & 0xf000) != 0xf000 || !(child &= 4095) || child >= fs->directories ||
                    (half(fnt + child * 8 + 6) & 4095) != d) return 0;
            } else {
                if (index >= fs->file_count || index >= 65536) return 0;
                ++index;
                ++fs->named_files;
            }
        }
    }
    return 1;
}

J2pNitroFS *j2p_nitrofs_mount(const char *path, uint32_t image_bytes, J2pScope scope) {
    J2pNitroFS *fs;
    uint32_t i, fnt, fnt_bytes, fat, fat_bytes;
    unsigned char probe;
    if (!path || image_bytes < 512 || image_bytes > UINT32_MAX - 511 || scope.program ||
        scope.processor != 9 || scope.module != 1 || !scope.generation) return 0;
    fs = fs_allocate(sizeof(*fs));
    if (!fs) return 0;
    for (i = 0; i != sizeof(fs->path); ++i) { fs->path[i] = path[i]; if (!path[i]) break; }
    if (i == sizeof(fs->path)) { fs_free(fs); return 0; }
    fs->scope = scope;
    fs->image_bytes = image_bytes;
    fs->file = j2p_readonly_open(path);
    if (!fs->file || !j2p_readonly_read_at(fs->file, image_bytes - 1, &probe, 1) ||
        j2p_readonly_read_at(fs->file, image_bytes, &probe, 1)) goto fail;
    if (!j2p_guest_map(&fs->io, scope, 0x020e5500, fs->backend, sizeof(fs->backend)) ||
        !j2p_guest_map(&fs->io, scope, 0x02700000, fs->header, sizeof(fs->header)) ||
        !transfer(fs, &fs->io, 0, 0x02700000, 512)) goto fail;
    fnt = word(fs->header + 0x40); fnt_bytes = word(fs->header + 0x44);
    fat = word(fs->header + 0x48); fat_bytes = word(fs->header + 0x4c);
    if (fnt < 512 || fat < 512 || fnt_bytes < 8 || fnt_bytes > 4 * 1024 * 1024 ||
        !fat_bytes || (fat_bytes & 7) || fat_bytes > 65536 * 8 ||
        (uint64_t)fnt + fnt_bytes > image_bytes || (uint64_t)fat + fat_bytes > image_bytes ||
        !((uint64_t)fnt + fnt_bytes <= fat || (uint64_t)fat + fat_bytes <= fnt)) goto fail;
    fs->archive.fnt = fnt; fs->archive.fnt_size = fnt_bytes;
    fs->archive.fat = fat; fs->archive.fat_size = fat_bytes;
    fs->file_count = fat_bytes / 8;
    fs->tables = fs_allocate((size_t)fnt_bytes + fat_bytes);
    fs->io.count = 1;
    if (!fs->tables || !j2p_guest_map(&fs->io, scope, 0x02700000, fs->tables, fnt_bytes + fat_bytes) ||
        !transfer(fs, &fs->io, fnt, 0x02700000, fnt_bytes) ||
        !transfer(fs, &fs->io, fat, 0x02700000 + fnt_bytes, fat_bytes) || !validate(fs)) goto fail;
    return fs;
fail:
    j2p_nitrofs_unmount(fs);
    return 0;
}

void j2p_nitrofs_unmount(J2pNitroFS *fs) {
    if (fs && fs != fs_active) {
        if (fs->file) j2p_readonly_close(fs->file);
        fs_free(fs->tables);
        fs_free(fs);
    }
}

FSResult native_fn_0200a81c(FSiSyncReadParam *cursor, void *destination, u32 length) {
    const unsigned char *input;
    unsigned char *output = destination;
    uint32_t offset, i;
    if (!fs_active || cursor->arc != &fs_active->archive || !destination) return FS_RESULT_FAILURE;
    if (cursor->pos >= fs_active->archive.fnt && (uint64_t)cursor->pos + length <= (uint64_t)fs_active->archive.fnt + fs_active->archive.fnt_size)
        offset = cursor->pos - fs_active->archive.fnt;
    else if (cursor->pos >= fs_active->archive.fat && (uint64_t)cursor->pos + length <= (uint64_t)fs_active->archive.fat + fs_active->archive.fat_size)
        offset = fs_active->archive.fnt_size + cursor->pos - fs_active->archive.fat;
    else return FS_RESULT_FAILURE;
    input = fs_active->tables + offset;
    for (i = 0; i != length; ++i) output[i] = input[i];
    cursor->pos += length;
    return FS_RESULT_SUCCESS;
}

FSResult native_fn_0200a63c(FSFile *file, FSCommandType command) {
    if (!fs_active || file->arc != &fs_active->archive) return FS_RESULT_FAILURE;
    if (command == FS_COMMAND_SEEKDIR) {
        if (file->arg.seekdir.pos.own_id >= fs_active->directories) return FS_RESULT_FAILURE;
        return native_main_0200a968(file);
    }
    if (command == FS_COMMAND_READDIR) return native_main_0200aa00(file);
    if (command == FS_COMMAND_OPENFILEDIRECT) {
        file->prop.file.own_id = file->arg.openfiledirect.index;
        file->prop.file.top = file->arg.openfiledirect.top;
        file->prop.file.bottom = file->arg.openfiledirect.bottom;
        file->prop.file.pos = file->prop.file.top;
        return FS_RESULT_SUCCESS;
    }
    return FS_RESULT_UNSUPPORTED;
}

void native_fn_0200a8dc(FSFile *file, u32 id) {
    file->stat |= 4;
    file->arg.seekdir.pos.arc = file->arc;
    file->arg.seekdir.pos.own_id = (u16)id;
    file->arg.seekdir.pos.index = 0;
    file->arg.seekdir.pos.pos = 0;
    (void)native_fn_0200a63c(file, FS_COMMAND_SEEKDIR);
}

int native_fn_0200a7cc(const char *left, const char *right, u32 length) { return native_main_0200a7cc(left, right, length); }

int j2p_nitrofs_file_id(J2pNitroFS *fs, J2pScope scope, uint32_t id, J2pNitroEntry *entry) {
    FSFile file = {0};
    FSResult status;
    if (!identity(fs, scope) || !entry || fs_active) return -1;
    if (id >= fs->file_count) return 0;
    file.arc = &fs->archive;
    file.arg.openfilefast.id.arc = &fs->archive;
    file.arg.openfilefast.id.file_id = id;
    fs_active = fs;
    status = native_main_0200b0bc(&file);
    fs_active = 0;
    if (status != FS_RESULT_SUCCESS) return -1;
    entry->id = id; entry->start = file.prop.file.top; entry->bytes = file.prop.file.bottom - file.prop.file.top;
    return 1;
}

int j2p_nitrofs_lookup(J2pNitroFS *fs, J2pScope scope, const char *path, J2pNitroEntry *entry) {
    FSFile file = {0};
    FSFileID id = {0};
    FSResult status;
    uint32_t length;
    if (!identity(fs, scope) || !path || !entry || fs_active) return -1;
    for (length = 0; length != 256 && path[length]; ++length) { }
    if (!length || length == 256) return -1;
    if (length >= 4 && path[3] == ':') {
        if (native_main_0200a7cc(path, "rom", 3)) return 0;
        path += 4;
    }
    if (*path == '/' || *path == '\\') ++path;
    file.arc = &fs->archive;
    file.arg.findpath.path = path;
    file.arg.findpath.pos.arc = &fs->archive;
    file.arg.findpath.result.file = &id;
    fs_active = fs;
    status = native_main_0200ab2c(&file);
    fs_active = 0;
    ++fs->lookups;
    return status == FS_RESULT_SUCCESS ? j2p_nitrofs_file_id(fs, scope, id.file_id, entry) : 0;
}

int j2p_nitrofs_read(J2pNitroFS *fs, J2pScope scope, uint32_t id, uint32_t offset,
                    J2pGuestSpace *space, uint32_t destination, uint32_t length) {
    J2pNitroEntry entry;
    if (j2p_nitrofs_file_id(fs, scope, id, &entry) != 1 || offset > entry.bytes || length > entry.bytes - offset) return 0;
    return transfer(fs, space, entry.start + offset, destination, length);
}

const char *j2p_nitrofs_container(J2pNitroFS *fs, J2pScope scope) { return identity(fs, scope) ? fs->path : 0; }

uint32_t j2p_nitrofs_metric(J2pNitroFS *fs, uint32_t id) {
    if (!fs) return UINT32_MAX;
    switch (id) { case 0: return fs->directories; case 1: return fs->file_count; case 2: return fs->named_files;
        case 3: return fs->reads; case 4: return fs->padded_reads; case 5: return fs->lookups; default: return UINT32_MAX; }
}
