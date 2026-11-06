#include "context.h"
void *native_main_020a8a3c(HashTable table, const void *elemKey)
{
    int hash, itempos;
    if(table==NULL)return NULL;
    
    hash = table->hashfn(elemKey, table->nbuckets);
    itempos = native_fn_020a8764(table->buckets[hash], elemKey, table->compfn, 0,
                          0);
    if (itempos == NOT_FOUND)
        return NULL;
    else
        return native_fn_020a8644(table->buckets[hash], itempos);
}
