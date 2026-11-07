#ifndef J2P_CARD_READER_20261106_H
#define J2P_CARD_READER_20261106_H
#include "guest_memory_20261106.h"

typedef int (*J2pReadAt)(void *, uint32_t, unsigned char *, uint32_t);
int j2p_card_read_polling(J2pGuestSpace *, J2pScope, void *, J2pReadAt, void *, uint32_t);
void *j2p_readonly_open(const char *);
int j2p_readonly_read_at(void *, uint32_t, unsigned char *, uint32_t);
int j2p_readonly_close(void *);
#endif
