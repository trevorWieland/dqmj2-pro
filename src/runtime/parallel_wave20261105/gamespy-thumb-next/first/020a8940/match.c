#include "context.h"
void native_main_020a8940(HashTable table)
{
    int i;
    if(table==NULL)return;
    
    assert(table);
    
    for (i = 0 ; i < table->nbuckets ; i++)
        native_fn_020a8614(table->buckets[i]);
    native_fn_020a929c(table->buckets);
    native_fn_020a929c(table);
}
