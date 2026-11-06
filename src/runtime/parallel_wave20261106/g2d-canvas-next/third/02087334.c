#include "context.h"
void native_main_02087334(RawContext*raw){
 u8 x,y;int mode;
 if(raw->state!=5){x=(u8)((raw->byte5e-3)*8);y=(u8)((raw->byte5f-2)*8+4);mode=0;}
 else{x=(u8)((raw->byte5e-2)*8);y=(u8)((raw->byte33-raw->byte5d+raw->byte35-3)*8+4);mode=15;}
 native_fn_main_02087e58(raw->word44,mode,x,(u8)(y+2),12,10);
}
