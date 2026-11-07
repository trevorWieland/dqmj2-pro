#ifndef J2P_RESOURCE_BRIDGE_20261106_H
#define J2P_RESOURCE_BRIDGE_20261106_H
#include "card_reader_20261106.h"

typedef struct J2pResourceContext J2pResourceContext;
J2pResourceContext *j2p_resource_create(J2pGuestSpace *, J2pScope, const char *, const char *,
                                      uint32_t, uint32_t, uint32_t, uint32_t, uint32_t);
void j2p_resource_destroy(J2pResourceContext *);
uint32_t j2p_resource_load(J2pResourceContext *, uint32_t, uint32_t, uint32_t);
int j2p_resource_release(J2pResourceContext *, uint32_t);
uint32_t j2p_resource_metric(J2pResourceContext *, uint32_t);
#endif
