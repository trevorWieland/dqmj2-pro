#include "context_00.h"
void native_main_02037ad8 (NNSSndHeapHandle heap)
{
    NNSSndHeapSection * section = ((void *)0) ;
    void * object;
    BOOL result;
    BOOL doCallback = 0 ;
    ((void) 0) ;
    while ((section = (NNSSndHeapSection *)native_fn_0202bba0(&heap->sectionList, ((void *)0) )) != ((void *)0) ) {
        object = ((void *)0) ;
        while ((object = native_fn_0202bba0(&section->blockList, object)) != ((void *)0) ) {
            NNSSndHeapBlock * block = (NNSSndHeapBlock *)object;
            if (block->callback != ((void *)0) ) {
                block->callback(block->buffer, block->size, block->data1, block->data2);
                doCallback = 1 ;
            }
        }
        native_fn_0202bb28(&heap->sectionList, section);
    }
    native_fn_0202b7b8(heap->handle, ((1 << 0) | (1 << 1)) );
    if (doCallback) native_fn_02037da8();
    result = native_fn_02037d6c(heap);
    ((void) 0) ;
}
