#include "card_reader_20261106.h"

static uint32_t load32(const unsigned char *p) {
    return p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

static void store32(unsigned char *p, uint32_t value) {
    unsigned i;
    for (i = 0; i != 4; ++i) p[i] = (unsigned char)(value >> (8 * i));
}

int j2p_card_read_polling(J2pGuestSpace *space, J2pScope scope, void *cache_object,
                        J2pReadAt reader, void *reader_context, uint32_t maximum_blocks) {
    unsigned char *cache = cache_object;
    unsigned char *backend;
    unsigned char block[512];
    uint32_t ordinal;
    if (scope.program != J2P_PROGRAM_HOST || scope.processor != J2P_CPU_ARM9 ||
        scope.module != J2P_MODULE_MAIN || !scope.generation || !cache || !reader) return -1;
    backend = j2p_guest_resolve(space, scope, 0x020e5500, 0x120, 1);
    if (!backend) return -1;
    for (ordinal = 0; ordinal != maximum_blocks; ++ordinal) {
        uint32_t source = load32(backend + 0x1c);
        uint32_t destination = load32(backend + 0x20);
        uint32_t length = load32(backend + 0x24);
        uint32_t base = source & ~UINT32_C(511);
        int cached = source != base || (destination & 3) || length < 512;
        uint32_t count = cached ? 512 - (source - base) : 512;
        unsigned char *target;
        uint32_t i;
        if (cached && count > length) count = length;
        target = count ? j2p_guest_resolve(space, scope, destination, count, 1) : 0;
        if (count && !target) return -1;
        if (!reader(reader_context, base, block, 512)) return -3;
        if (cached) {
            int result;
            store32(cache + 8, base);
            for (i = 0; i != 512; ++i) cache[0x20 + i] = block[i];
            result = j2p_card_cache_copy(space, scope, cache);
            if (result < 0) return -1;
            if (!result) return 0;
        } else {
            for (i = 0; i != 512; ++i) target[i] = block[i];
            store32(backend + 0x1c, load32(backend + 0x1c) + 512);
            store32(backend + 0x20, load32(backend + 0x20) + 512);
            store32(backend + 0x24, load32(backend + 0x24) - 512);
            if (!load32(backend + 0x24)) return 0;
        }
    }
    return -2;
}
