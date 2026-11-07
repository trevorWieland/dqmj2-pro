#include "g3d_file_blocks_20261106.h"

static uint32_t half(const unsigned char *p) { return p[0] | ((uint32_t)p[1] << 8); }
static uint32_t word(const unsigned char *p) { return half(p) | (half(p + 2) << 16); }

int j2p_g3d_file_block(J2pGuestSpace *space, J2pScope scope, uint32_t file, uint32_t available,
                      uint32_t selector, uint32_t *block, uint32_t *bytes) {
    const unsigned char *input;
    uint32_t signature, total, header, count, offsets[2], sizes[2], kinds[2], i, selected;
    uint64_t address;
    if (!block || !bytes || block == bytes) return -1;
    *block = 0;
    *bytes = 0;
    if (scope.program != J2P_PROGRAM_HOST || scope.processor != J2P_CPU_ARM9 ||
        scope.module != J2P_MODULE_MAIN || !scope.generation || selector > 1 || available < 16) return -1;
    input = j2p_guest_resolve(space, scope, file, available, 1);
    if (!input) return -1;
    signature = word(input);
    total = word(input + 8);
    header = half(input + 12);
    count = half(input + 14);
    if ((signature != UINT32_C(0x30444d42) && signature != UINT32_C(0x30585442)) ||
        half(input + 4) != 0xfeff || !count || count > 2 || header < 16 || (header & 3) ||
        total > available || total < header || count * 4 > total - header ||
        (signature == UINT32_C(0x30585442) && count != 1)) return -1;
    for (i = 0; i != count; ++i) {
        offsets[i] = word(input + header + i * 4);
        if ((offsets[i] & 3) || offsets[i] < header + count * 4 || total - (header + count * 4) < 8 ||
            offsets[i] > total - 8) return -1;
        kinds[i] = word(input + offsets[i]);
        sizes[i] = word(input + offsets[i] + 4);
        if (sizes[i] < 8 || (uint64_t)offsets[i] + sizes[i] > total) return -1;
    }
    if (count == 2 && offsets[1] < (uint64_t)offsets[0] + sizes[0]) return -1;
    if (signature == UINT32_C(0x30444d42)) {
        if (kinds[0] != UINT32_C(0x304c444d) || (count == 2 && kinds[1] != UINT32_C(0x30584554))) return -1;
        if (selector == J2P_G3D_TEXTURE_BLOCK && count == 1) return 0;
        selected = selector == J2P_G3D_TEXTURE_BLOCK ? 1 : 0;
    } else {
        if (kinds[0] != UINT32_C(0x30584554)) return -1;
        if (selector == J2P_G3D_MODEL_BLOCK) return 0;
        selected = 0;
    }
    address = (uint64_t)file + offsets[selected];
    if (address > UINT32_MAX) return -1;
    *block = (uint32_t)address;
    *bytes = sizes[selected];
    return 1;
}
