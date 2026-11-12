/* Tail-call thunk to the identity-profile pointer getter.
   Unknowns: the profile block role and the caller contract. */
#include "context.h"
extern void *native_data_02063ea4(void);
void *saved_identity_profile_pointer(void) { return native_data_02063ea4(); }