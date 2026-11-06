#include "context.h"
void native_main_0208bd24(u8*srcAddr,u8*dstAddr,u8*buf1,u32 size1,u8*buf2,u32 size2){
 u32 size,new_putpnt;u16 blocklen;
 if(G.buf==NULL||G.buflen==0)return;
 size=size1+size2;
 if(size<8||size>1508)return;
 if(buf1[0]!=native_data_020de7b4[0]||buf1[1]!=native_data_020de7b4[1]||buf1[2]!=native_data_020de7b4[2]||buf1[6]!=8||(buf1[7]!=0&&buf1[7]!=6))return;
 blocklen=(size+9)&~1;
 new_putpnt=G.putpnt+blocklen;
 if(G.putpnt<G.getpnt&&G.getpnt<=new_putpnt)return;
 if(new_putpnt==G.buflen){new_putpnt=0;if(G.getpnt==0)return;}
 else if(new_putpnt>G.buflen){new_putpnt=blocklen;if(G.getpnt<=blocklen)return;}
 if(G.putpnt+blocklen>G.buflen){if(G.buflen-G.putpnt>=2)*(u16*)(G.buf+G.putpnt)=0;G.putpnt=0;}
 *(u16*)(G.buf+G.putpnt)=blocklen;
 native_fn_02008e0c(dstAddr,G.buf+G.putpnt+2,6);
 native_fn_02008e0c(srcAddr,G.buf+G.putpnt+8,6);
 native_fn_02008e0c(buf1+6,G.buf+G.putpnt+14,size1-6);
 if(buf2!=NULL&&size2!=0)native_fn_02008e0c(buf2,G.buf+G.putpnt+8+size1,size2);
 G.putpnt=new_putpnt;
}
