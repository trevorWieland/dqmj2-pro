#include "context.h"
BOOL native_main_0202e260(NNSG3dVisAnmResult*pResult,const NNSG3dAnmObj*pAnmObj,u32 nodeID){
 BOOL rval=0;const NNSG3dAnmObj*p;NNSG3dVisAnmResult tmp;p=pAnmObj;pResult->isVisible=0;
 do{if(nodeID<p->numMapData){u32 dataIdx=p->mapData[nodeID];if(dataIdx&0x0100){NNSG3dFuncAnmVis func=(NNSG3dFuncAnmVis)p->funcAnm;if(func){(*func)(&tmp,p,dataIdx&0x00ff);pResult->isVisible|=tmp.isVisible;rval=1;}}}p=p->next;}while(p);
 return rval;
}
