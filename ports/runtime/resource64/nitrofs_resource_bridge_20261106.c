#include <stddef.h>
#include "nitrofs_20261106.h"

#if defined(_WIN32)
__declspec(dllimport) void *__stdcall GetProcessHeap(void);
__declspec(dllimport) void *__stdcall HeapAlloc(void *, uint32_t, size_t);
__declspec(dllimport) int __stdcall HeapFree(void *, uint32_t, void *);
static void *allocate_context(size_t bytes) { return HeapAlloc(GetProcessHeap(), 8, bytes); }
static void free_context(void *pointer) { HeapFree(GetProcessHeap(), 0, pointer); }
#else
#include <stdlib.h>
static void *allocate_context(size_t bytes) { return calloc(1, bytes); }
static void free_context(void *pointer) { free(pointer); }
#endif

typedef struct { uint32_t offset, bytes, used; } Block;
typedef struct { uint32_t enabled, unknown4, unknown8, allocations, heap; } HeapSlot;

struct J2pResourceContext {
    J2pGuestSpace *space;
    J2pNitroFS *filesystem;
    J2pScope scope;
    char container[1024], entry_name[256];
    uint32_t entry_start, entry_bytes, heap_id, heap_base, heap_bytes;
    Block blocks[32];
    unsigned char cache[0x220];
    void *open_file;
    uint32_t fs_status, allocation_status, allocation_counter, last_read_status, read_calls;
};

static J2pResourceContext *active;
uint32_t native_data_020edec8;
signed char native_data_020dd580[1];
HeapSlot native_data_020edd64[16];
unsigned char native_data_020edd54[3];
extern uint32_t native_main_0203cb8c(uint32_t, uint32_t, uint32_t);
extern uint32_t native_main_0203cc2c(uint32_t, uint32_t);
extern uint32_t native_main_0202a8e0(uint32_t);
extern uint32_t native_main_0202a37c(uint32_t, uint32_t, int32_t);

static void store32(unsigned char *bytes, uint32_t value) {
    unsigned i;
    for (i = 0; i != 4; ++i) bytes[i] = (unsigned char)(value >> (8 * i));
}

static int copy_name(char *destination, size_t capacity, const char *source) {
    size_t i;
    if (!source) return 0;
    for (i = 0; i != capacity; ++i) {
        destination[i] = source[i];
        if (!source[i]) return 1;
    }
    return 0;
}

static int matches_path(uint32_t path) {
    uint32_t i;
    if (!active) return 0;
    if (active->filesystem) {
        char name[256];
        J2pNitroEntry entry;
        for (i = 0; i != sizeof(name); ++i) {
            const unsigned char *byte;
            if (i > UINT32_MAX - path) return 0;
            byte = j2p_guest_resolve(active->space, active->scope, path + i, 1, 1);
            if (!byte) return 0;
            name[i] = (char)*byte;
            if (!*byte) break;
        }
        if (i == sizeof(name) || j2p_nitrofs_lookup(active->filesystem, active->scope, name, &entry) != 1) return 0;
        active->entry_start = entry.start;
        active->entry_bytes = entry.bytes;
        return 1;
    }
    for (i = 0; i != sizeof(active->entry_name); ++i) {
        const unsigned char *byte;
        if (i > UINT32_MAX - path) return 0;
        byte = j2p_guest_resolve(active->space, active->scope, path + i, 1, 1);
        if (!byte || *byte != (unsigned char)active->entry_name[i]) return 0;
        if (!*byte) return 1;
    }
    return 0;
}

static int release_block(J2pResourceContext *context, uint32_t address) {
    uint32_t i;
    for (i = 0; i != 32; ++i) {
        Block *block = &context->blocks[i];
        if (block->used && context->heap_base + block->offset == address) {
            block->used = 0;
            return 1;
        }
    }
    return 0;
}

uint32_t native_fn_0202b334(uint32_t heap, uint32_t bytes, int32_t alignment) {
    uint32_t order[32], count = 0, free_slot = 32, i, gap, best = UINT32_MAX;
    if (!active || heap != active->heap_base || !bytes || bytes > active->heap_bytes ||
        (alignment != 4 && alignment != -4)) return 0;
    for (i = 0; i != 32; ++i) {
        if (active->blocks[i].used) {
            uint32_t position = count++;
            while (position && active->blocks[order[position - 1]].offset > active->blocks[i].offset) {
                order[position] = order[position - 1];
                --position;
            }
            order[position] = i;
        } else free_slot = i;
    }
    if (free_slot == 32) return 0;
    for (gap = 0; gap <= count; ++gap) {
        uint32_t begin = gap ? active->blocks[order[gap - 1]].offset + active->blocks[order[gap - 1]].bytes : 0;
        uint32_t end = gap < count ? active->blocks[order[gap]].offset : active->heap_bytes;
        if (end >= begin && end - begin >= bytes) {
            uint32_t candidate = alignment > 0 ? (begin + 3) & ~UINT32_C(3) : (end - bytes) & ~UINT32_C(3);
            if (candidate >= begin && candidate <= end - bytes) {
                best = candidate;
                if (alignment > 0) break;
            }
        }
    }
    if (best == UINT32_MAX) return 0;
    active->blocks[free_slot].offset = best;
    active->blocks[free_slot].bytes = bytes;
    active->blocks[free_slot].used = 1;
    return active->heap_base + best;
}

void native_fn_0200bd04(void *object) {
    unsigned char *bytes = object;
    unsigned i;
    for (i = 0; i != 72; ++i) bytes[i] = 0;
}

uint32_t native_fn_0200bfe4(void *object, uint32_t path) {
    unsigned char *bytes = object;
    if (!matches_path(path) || active->open_file) return 0;
    active->open_file = j2p_readonly_open(active->container);
    if (!active->open_file) return 0;
    store32(bytes + 36, active->entry_start);
    store32(bytes + 40, active->entry_start + active->entry_bytes);
    return 1;
}

void native_fn_0200c02c(void *object) {
    (void)object;
    if (active && active->open_file) {
        j2p_readonly_close(active->open_file);
        active->open_file = 0;
    }
}

uint32_t native_fn_0202a8e0(uint32_t path) { return native_main_0202a8e0(path); }
uint32_t native_fn_0203cb8c(uint32_t path, uint32_t heap, uint32_t selector) { return native_main_0203cb8c(path, heap, selector); }
uint32_t native_fn_0202a250(void) { return active ? (uint32_t)(int32_t)native_data_020dd580[0] : UINT32_MAX; }
uint32_t native_fn_0202a37c(uint32_t heap, uint32_t bytes, int32_t alignment) { return native_main_0202a37c(heap, bytes, alignment); }

uint32_t native_fn_0202a818(uint32_t path, uint32_t buffer, uint32_t bytes, uint32_t offset) {
    unsigned char *backend;
    void *file;
    int result;
    uint32_t i;
    if (!matches_path(path) || offset > active->entry_bytes || bytes > active->entry_bytes - offset) return 0;
    for (i = 0; i != 32; ++i) {
        Block *block = &active->blocks[i];
        if (block->used && active->heap_base + block->offset == buffer && bytes <= block->bytes) break;
    }
    if (i == 32) return 0;
    backend = j2p_guest_resolve(active->space, active->scope, 0x020e5500, 0x120, 1);
    if (!backend) return 0;
    file = j2p_readonly_open(active->container);
    if (!file) return 0;
    store32(backend + 0x1c, active->entry_start + offset);
    store32(backend + 0x20, buffer);
    store32(backend + 0x24, bytes);
    ++active->read_calls;
    result = j2p_card_read_polling(active->space, active->scope, active->cache,
                                 active->filesystem ? j2p_nitrofs_card_read_at : j2p_readonly_read_at,
                                 active->filesystem ? (void *)active->filesystem : file, active->entry_bytes / 512 + 3);
    active->last_read_status = (uint32_t)result;
    j2p_readonly_close(file);
    return result == 0;
}

uint32_t native_fn_0202a498(int32_t heap, uint32_t buffer) {
    return active && (uint32_t)heap == active->heap_id ? (uint32_t)release_block(active, buffer) : 0;
}

J2pResourceContext *j2p_resource_create(J2pGuestSpace *space, J2pScope scope, const char *container,
                                      const char *entry_name, uint32_t start, uint32_t bytes,
                                      uint32_t heap_id, uint32_t heap_base, uint32_t heap_bytes) {
    J2pResourceContext *context;
    if (scope.program || scope.processor != 9 || scope.module != 1 || !scope.generation || heap_id >= 16 ||
        !heap_base || (heap_base & 3) || !heap_bytes || (heap_bytes & 3) ||
        (uint64_t)start + bytes > UINT32_MAX || !j2p_guest_resolve(space, scope, heap_base, heap_bytes, 1) ||
        !j2p_guest_resolve(space, scope, 0x020e5500, 0x120, 1)) return 0;
    context = allocate_context(sizeof(*context));
    if (!context) return 0;
    if (!copy_name(context->container, sizeof(context->container), container) ||
        !copy_name(context->entry_name, sizeof(context->entry_name), entry_name)) {
        free_context(context);
        return 0;
    }
    context->space = space;
    context->scope = scope;
    context->entry_start = start;
    context->entry_bytes = bytes;
    context->heap_id = heap_id;
    context->heap_base = heap_base;
    context->heap_bytes = heap_bytes;
    store32(context->cache + 4, 0xa1000000);
    store32(context->cache + 8, UINT32_MAX);
    return context;
}

uint32_t j2p_resource_load(J2pResourceContext *context, uint32_t path, uint32_t heap, uint32_t selector) {
    uint32_t result;
    if (!context || active || (heap != context->heap_id && heap != UINT32_MAX)) return 0;
    active = context;
    native_data_020edec8 = context->fs_status;
    native_data_020edd54[2] = (unsigned char)context->allocation_status;
    native_data_020dd580[0] = (signed char)context->heap_id;
    native_data_020edd64[context->heap_id].enabled = 1;
    native_data_020edd64[context->heap_id].heap = context->heap_base;
    native_data_020edd64[context->heap_id].allocations = context->allocation_counter;
    result = selector == 0 ? native_main_0203cc2c(path, heap) : native_main_0203cb8c(path, heap, selector);
    context->fs_status = native_data_020edec8;
    context->allocation_status = native_data_020edd54[2];
    context->allocation_counter = native_data_020edd64[context->heap_id].allocations;
    active = 0;
    return result;
}

int j2p_resource_release(J2pResourceContext *context, uint32_t address) {
    return context && !active ? release_block(context, address) : 0;
}

uint32_t j2p_resource_metric(J2pResourceContext *context, uint32_t metric) {
    uint32_t count = 0, i;
    if (!context) return UINT32_MAX;
    if (metric == 0) return context->fs_status;
    if (metric == 1) return context->allocation_status;
    if (metric == 2) {
        for (i = 0; i != 32; ++i) count += context->blocks[i].used != 0;
        return count;
    }
    if (metric == 3) return context->allocation_counter;
    if (metric == 4) return context->last_read_status;
    if (metric == 5) return context->read_calls;
    return UINT32_MAX;
}

void j2p_resource_destroy(J2pResourceContext *context) {
    if (context && !active) {
        if (context->open_file) j2p_readonly_close(context->open_file);
        free_context(context);
    }
}

J2pResourceContext *j2p_nitrofs_resource_create(J2pNitroFS *filesystem, J2pGuestSpace *space, J2pScope scope,
                                              uint32_t heap_id, uint32_t heap_base, uint32_t heap_bytes) {
    const char *path = j2p_nitrofs_container(filesystem, scope);
    J2pResourceContext *context;
    if (!path) return 0;
    context = j2p_resource_create(space, scope, path, "", 0, 0, heap_id, heap_base, heap_bytes);
    if (context) context->filesystem = filesystem;
    return context;
}
