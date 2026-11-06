#include "context.h"
int native_main_020a89f0(HashTable table, const void *delElem)
{
    int hash, itempos;
    if(table==NULL)return 0;
    
    hash = table->hashfn(delElem, table->nbuckets);
    itempos = native_fn_020a8764(table->buckets[hash], delElem, table->compfn, 0,0);
    if (itempos == NOT_FOUND)
        return 0;
    else
        native_fn_020a8720(table->buckets[hash], itempos);
    return 1;
}
