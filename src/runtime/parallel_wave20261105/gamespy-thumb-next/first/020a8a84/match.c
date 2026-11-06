#include "context.h"
void native_main_020a8a84(HashTable table, TableMapFn fn, void *clientData)
{
    int i;
    
    assert(fn);
    
    for (i = 0 ; i < table->nbuckets ; i++)
        native_fn_020a87dc(table->buckets[i], fn, clientData);
    
}
