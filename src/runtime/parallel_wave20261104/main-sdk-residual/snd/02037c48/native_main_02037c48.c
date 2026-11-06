#include "context_00.h"
void native_main_02037c48 (NNSSndHeapHandle heap, int level)
{
    NNSSndHeapSection * section;
    void * object = ((void *)0) ;
    BOOL result;
    BOOL doCallback = 0 ;
    ((void) 0) ;
    ((void) 0) ;
    if (level == 0) {
        native_fn_02037ad8(heap);
        return;
    }
    while (level < heap->sectionList.numObjects) {
        section = (NNSSndHeapSection *)native_fn_0202bba0(&heap->sectionList, ((void *)0) );
        while ((object = native_fn_0202bba0(&section->blockList, object)) != ((void *)0) ) {
            NNSSndHeapBlock * block = (NNSSndHeapBlock *)object;
            if (block->callback != ((void *)0) ) {
                block->callback(block->buffer, block->size, block->data1, block->data2);
                doCallback = 1 ;
            }
        }
        native_fn_0202bb28(&heap->sectionList, section);
    }
    result = native_fn_0202b834(heap->handle, (u32)level);
    ((void) 0) ;
    if (doCallback) native_fn_02037da8();
    result = native_fn_0202b7e4(heap->handle, heap->sectionList.numObjects);
    ((void) 0) ;
    result = native_fn_02037d6c(heap);
    ((void) 0) ;
}
