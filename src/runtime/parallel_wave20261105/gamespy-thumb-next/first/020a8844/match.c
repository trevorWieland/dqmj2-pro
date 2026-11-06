#include "context.h"
void *native_main_020a8844(const void *key, void *base, int count, int size,
                     ArrayCompareFn comparator)
{
    int i;
    for (i = 0; i < count; i++)
    {
        if (comparator(key, (char *)base + size*i) == 0)
            return (char *)base + size*i;
    }
    return NULL;
}
