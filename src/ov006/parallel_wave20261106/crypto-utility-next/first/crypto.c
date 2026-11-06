#include "context.h"
void native_ov006_021ed86c(Stream*c,const u8*key,u32 keyLength,u32 size){u32 i,j,k;u8 temp,b;u8*s=c->state;c->y=0;c->x=0;c->size=size;for(i=0;i<size;i++)s[i]=(u8)i;j=0;k=0;for(i=0;i<size;i++){temp=s[i];j=(j+key[k]+temp)%c->size;b=s[j];s[j]=temp;s[i]=b;k++;if(k>=keyLength)k=0;}}
void native_ov006_021ed8d0(Stream*c,u8*out,const u8*in,u32 size){u32 i;for(i=0;i<size;i++){u8 key=(u8)native_ov006_021ed8fc(c);out[i]=in[i]^key;}}
u32 native_ov006_021ed8fc(Stream*c){u32 size=c->size;u8*s=c->state;u8 x=(u8)((c->x+1)%size);u8 a=s[x];u8 y=(u8)((a+c->y)%size);u8 b=s[y];c->x=x;c->y=y;s[y]=a;s[x]=b;return s[(a+b)%c->size];}
u32 native_ov006_021ed964(u32 crc,const u8*in,s32 length,u32 initialized,u32*table){s32 i;if(initialized==0)native_ov006_021ed99c(initialized,table);for(i=0;i<length;i++)crc=(crc>>8)^table[(crc^in[i])&255];return crc;}
void native_ov006_021f08fc(const u8*a,const u8*b,u8*out){out[0]=a[0]^b[0];out[1]=a[1]^b[1];out[2]=a[2]^b[2];out[3]=a[3]^b[3];out[4]=a[4]^b[4];out[5]=a[5]^b[5];out[6]=a[6]^b[6];out[7]=a[7]^b[7];}
