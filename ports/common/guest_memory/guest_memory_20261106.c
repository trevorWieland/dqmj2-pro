#include "guest_memory_20261106.h"

static int same_scope(J2pScope left, J2pScope right) {
    return left.program == right.program && left.processor == right.processor &&
        left.module == right.module && left.generation == right.generation;
}

int j2p_guest_map(J2pGuestSpace *space, J2pScope scope, uint32_t base, void *bytes, uint32_t length) {
    uint32_t i;
    uint64_t end = (uint64_t)base + length;
    if (!space || !bytes || !length || space->count >= 16 || end > UINT64_C(0x100000000) ||
        (scope.processor != 7 && scope.processor != 9) || !scope.generation) return 0;
    for (i = 0; i != space->count; ++i) {
        J2pGuestRegion *region = &space->regions[i];
        uint64_t other_end = (uint64_t)region->base + region->length;
        if (same_scope(scope, region->scope) && base < other_end && region->base < end) return 0;
    }
    space->regions[space->count].scope = scope;
    space->regions[space->count].base = base;
    space->regions[space->count].length = length;
    space->regions[space->count].bytes = bytes;
    ++space->count;
    return 1;
}

void *j2p_guest_resolve(J2pGuestSpace *space, J2pScope scope, uint32_t address, uint32_t length, uint32_t alignment) {
    uint32_t i;
    uint64_t end = (uint64_t)address + length;
    if (!space || space->count > 16 || !alignment || alignment & (alignment - 1) ||
        address & (alignment - 1) || end > UINT64_C(0x100000000)) return 0;
    for (i = 0; i != space->count; ++i) {
        J2pGuestRegion *region = &space->regions[i];
        if (same_scope(scope, region->scope) && address >= region->base &&
            end <= (uint64_t)region->base + region->length) {
            uint8_t *pointer = region->bytes + (address - region->base);
            if ((uintptr_t)pointer & (alignment - 1)) return 0;
            return pointer;
        }
    }
    return 0;
}

int j2p_guest_copy(J2pGuestSpace *space, J2pScope scope, uint32_t address, const void *source, uint32_t length) {
    uint8_t *destination;
    const uint8_t *input = source;
    uintptr_t first, second;
    uint32_t i;
    if (!length) return 1;
    if (!source) return 0;
    destination = j2p_guest_resolve(space, scope, address, length, 1);
    if (!destination) return 0;
    first = (uintptr_t)input;
    second = (uintptr_t)destination;
    if (length > UINTPTR_MAX - first || length > UINTPTR_MAX - second ||
        (first < second + length && second < first + length)) return 0;
    for (i = 0; i != length; ++i) destination[i] = input[i];
    return 1;
}

uint32_t j2p_guest_unmap_scope(J2pGuestSpace *space, J2pScope scope) {
    uint32_t i, keep = 0, removed = 0;
    if (!space || space->count > 16) return 0;
    for (i = 0; i != space->count; ++i) {
        if (same_scope(scope, space->regions[i].scope)) ++removed;
        else space->regions[keep++] = space->regions[i];
    }
    space->count = keep;
    return removed;
}
