#include "context.h"

/* Three-word vector copied through the shared buffer. */
typedef struct {
    u32 a;
    u32 b;
    u32 c;
} Vector;

extern u8 native_data_0221c094[];

/* Publish the caller's three words into the shared buffer. */
void native_main_021f57cc(const Vector *source)
{
    Vector *target = *(Vector **)native_data_0221c094;

    *target = *source;
}

