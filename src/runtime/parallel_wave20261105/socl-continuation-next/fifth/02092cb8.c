#include "context.h"
#define F(b,c,d) (((c)^(d))&(b))^(d)
#define G(b,c,d) (((b)^(c))&(d))^(c)
#define H(b,c,d) ((b)^(c)^(d))
#define I(b,c,d) ((~(d)|(b))^(c))
#define ROTATE(v,s) (((v)<<(s))|((v)>>(32-(s))))
#define STEP(f,a,b,c,d,s) { (a)=(b)+ROTATE((a)+((f(b,c,d))+x[native_data_020de898[i]]+native_data_020de918[i]),s); i++; }
void native_main_02092cb8(Md5View *context,u8 *input)
{
    u32 x[16];
    u32 a=context->state[0],b=context->state[1],c=context->state[2],d=context->state[3];
    int i,j;
    native_fn_02092ca8(x,input,64);
    i=0;
    for(j=0;j<4;j++){STEP(F,a,b,c,d,7);STEP(F,d,a,b,c,12);STEP(F,c,d,a,b,17);STEP(F,b,c,d,a,22);}
    for(j=0;j<4;j++){STEP(G,a,b,c,d,5);STEP(G,d,a,b,c,9);STEP(G,c,d,a,b,14);STEP(G,b,c,d,a,20);}
    for(j=0;j<4;j++){STEP(H,a,b,c,d,4);STEP(H,d,a,b,c,11);STEP(H,c,d,a,b,16);STEP(H,b,c,d,a,23);}
    for(j=0;j<4;j++){STEP(I,a,b,c,d,6);STEP(I,d,a,b,c,10);STEP(I,c,d,a,b,15);STEP(I,b,c,d,a,21);}
    context->state[0]+=a;
    context->state[1]+=b;
    context->state[2]+=c;
    context->state[3]+=d;
}
