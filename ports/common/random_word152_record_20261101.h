#ifndef J2P_RANDOM_WORD152_RECORD_20261101_H
#define J2P_RANDOM_WORD152_RECORD_20261101_H
#include <stddef.h>

typedef struct J2pRandomWordRecord {
    unsigned char unknown_0[12];
    unsigned int field_c;
} J2pRandomWordRecord;

extern J2pRandomWordRecord native_data_020f6028;
extern unsigned int native_rng_state;
_Static_assert(sizeof(J2pRandomWordRecord) == 16, "Measured record view");
_Static_assert(_Alignof(J2pRandomWordRecord) == 4, "Measured record alignment");
_Static_assert(offsetof(J2pRandomWordRecord, field_c) == 12, "Measured word field");
#endif
