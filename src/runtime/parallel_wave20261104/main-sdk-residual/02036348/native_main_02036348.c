#include "context.h"
void native_main_02036348 (NNSG2dCharCanvas * pCC, void * charBase, int areaWidth, int areaHeight, NNSG2dCharaColorMode colorMode)
{
    OBJ1DParam p;
    const ObjectSize * pObj = GetMaxObjectSize(areaWidth, areaHeight);
    ((void) 0); ;
    ((void) 0); ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    p.baseWidthShift = pObj->widthShift;
    p.baseHeightShift = pObj->heightShift;
    native_fn_020361d0(
        pCC,
        charBase, areaWidth, areaHeight, colorMode,
        &native_data_main_020d90d0.field_0024, p.packed
        );
}
