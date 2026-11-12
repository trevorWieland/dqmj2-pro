#include "context.h"

/*
 * 0x020973C8 (16 B, Thumb, p032/2.0-base)
 *
 * Read the word at +0x24 of the first argument, swap it into place of the
 * second, and tail-call the Thumb helper 0x02096FFC with the third argument
 * passed through. The pool word is the Thumb-tagged pointer 0x02096FFD, so
 * the call is through an absolute function pointer, not a direct BL.
 *
 * Unknowns: the record at +0x24, and the helper's contract.
 */

typedef struct {
    u8 pad[0x24];
    u32 f24;
} RecordView;

extern u32 native_fn_02096ffc();

void native_main_020973c8(RecordView *record, s32 b, s32 c)
{
    native_fn_02096ffc(b, record->f24, c);
}
