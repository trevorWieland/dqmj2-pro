#include "context_00.h"
void native_main_0201a618 (dst_string * p, const char * s, int n)
{
    if (n > 0) {
        size_t i, k = p->len;
        if (k > (size_t) n)
            k = (size_t) n;
        for (i = 0; i < k; ++i)
            p->cur[i] = s[i];
        p->len -= k;
        p->cur += n;
    }
}
