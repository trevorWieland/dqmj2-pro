#include "context.h"
void native_main_020a89a4(HashTable table, const void *newElem)
{
    int hash, itempos;
    if(table==NULL)return;
    
    hash = table->hashfn(newElem, table->nbuckets);
    itempos = native_fn_020a8764(table->buckets[hash], newElem, table->compfn, 0,0);
    if (itempos == NOT_FOUND)
        native_fn_020a865c(table->buckets[hash], newElem);
    else
        native_fn_020a8734(table->buckets[hash], newElem, itempos);
}
