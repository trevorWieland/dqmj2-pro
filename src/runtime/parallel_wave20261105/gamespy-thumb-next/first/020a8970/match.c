#include "context.h"
int native_main_020a8970(HashTable table)
{
    int i, count = 0;
    if(table==NULL)return count;
    
    for (i = 0 ; i < table->nbuckets ; i++)
        count += native_fn_020a8640(table->buckets[i]);
    
    return count;
}
