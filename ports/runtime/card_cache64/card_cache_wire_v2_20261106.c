#include "guest_memory_20261106.h"

static uint32_t load_le32(const unsigned char *bytes) {
    return bytes[0] | ((uint32_t)bytes[1] << 8) | ((uint32_t)bytes[2] << 16) | ((uint32_t)bytes[3] << 24);
}

static void store_le32(unsigned char *bytes, uint32_t value) {
    bytes[0] = (unsigned char)value;
    bytes[1] = (unsigned char)(value >> 8);
    bytes[2] = (unsigned char)(value >> 16);
    bytes[3] = (unsigned char)(value >> 24);
}

int j2p_card_cache_copy(J2pGuestSpace *space, J2pScope scope, void *cache_object) {
    unsigned char *cache = cache_object;
    unsigned char *backend;
    uint32_t source, base;
    if (scope.program != J2P_PROGRAM_HOST || scope.processor != J2P_CPU_ARM9 ||
        scope.module != J2P_MODULE_MAIN || !scope.generation) return -1;
    backend = j2p_guest_resolve(space, scope, 0x020e5500, 0x120, 1);
    if (!backend || !cache) return -1;
    source = load_le32(backend + 0x1c);
    base = source & ~UINT32_C(511);
    if (base == load_le32(cache + 8)) {
        uint32_t offset = source - base;
        uint32_t count = 512 - offset;
        uint32_t length = load_le32(backend + 0x24);
        if (count > length) count = length;
        if (!j2p_guest_copy(space, scope, load_le32(backend + 0x20), cache + 0x20 + offset, count)) return -1;
        store_le32(backend + 0x1c, load_le32(backend + 0x1c) + count);
        store_le32(backend + 0x20, load_le32(backend + 0x20) + count);
        store_le32(backend + 0x24, load_le32(backend + 0x24) - count);
    }
    return load_le32(backend + 0x24) != 0;
}
