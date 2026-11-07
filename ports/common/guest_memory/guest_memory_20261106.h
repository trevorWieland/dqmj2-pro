#ifndef J2P_GUEST_MEMORY_20261106_H
#define J2P_GUEST_MEMORY_20261106_H
#include <stdint.h>

typedef struct { uint32_t program, processor, module, generation; } J2pScope;
typedef struct { J2pScope scope; uint32_t base, length; uint8_t *bytes; } J2pGuestRegion;
typedef struct { uint32_t count; J2pGuestRegion regions[16]; } J2pGuestSpace;
enum { J2P_PROGRAM_HOST = 0, J2P_PROGRAM_DWC_CHILD = 1, J2P_CPU_ARM7 = 7, J2P_CPU_ARM9 = 9, J2P_MODULE_MAIN = 1 };

int j2p_guest_map(J2pGuestSpace *, J2pScope, uint32_t, void *, uint32_t);
void *j2p_guest_resolve(J2pGuestSpace *, J2pScope, uint32_t, uint32_t, uint32_t);
int j2p_guest_copy(J2pGuestSpace *, J2pScope, uint32_t, const void *, uint32_t);
uint32_t j2p_guest_unmap_scope(J2pGuestSpace *, J2pScope);
int j2p_card_cache_copy(J2pGuestSpace *, J2pScope, void *);

_Static_assert(sizeof(J2pScope) == 16, "Scope wire identity must use four 32-bit fields");
#endif
