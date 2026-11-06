#include "context.h"
void * native_main_020a8ab0(HashTable table, TableMapFn2 fn, void *clientData)
{
    int i;
    void * pcurr;
    
    assert(fn);
    
    for (i = 0 ; i < table->nbuckets ; i++)
    {
        pcurr = native_fn_020a87fc(table->buckets[i], fn, clientData);
        if(pcurr)
            return pcurr;
    }

    return NULL;
}
