#ifndef J2P_NITROFS_20261106_H
#define J2P_NITROFS_20261106_H
#include "resource_bridge_20261106.h"

typedef struct J2pNitroFS J2pNitroFS;
typedef struct { uint32_t id, start, bytes; } J2pNitroEntry;
J2pNitroFS *j2p_nitrofs_mount(const char *, uint32_t, J2pScope);
void j2p_nitrofs_unmount(J2pNitroFS *);
int j2p_nitrofs_lookup(J2pNitroFS *, J2pScope, const char *, J2pNitroEntry *);
int j2p_nitrofs_file_id(J2pNitroFS *, J2pScope, uint32_t, J2pNitroEntry *);
int j2p_nitrofs_read(J2pNitroFS *, J2pScope, uint32_t, uint32_t, J2pGuestSpace *, uint32_t, uint32_t);
int j2p_nitrofs_card_read_at(void *, uint32_t, unsigned char *, uint32_t);
const char *j2p_nitrofs_container(J2pNitroFS *, J2pScope);
uint32_t j2p_nitrofs_metric(J2pNitroFS *, uint32_t);
J2pResourceContext *j2p_nitrofs_resource_create(J2pNitroFS *, J2pGuestSpace *, J2pScope, uint32_t, uint32_t, uint32_t);
#endif
