#include "context.h"
void native_ov006_021f1e40 (unsigned char *output, UINT4 *input, unsigned int len)
{
  unsigned int i, j;
  for (i = 0, j = 0; j < len; i++, j += 4) {
    output[j] = (unsigned char)(input[i] & 0xff);
    output[j+1] = (unsigned char)((input[i] >> 8) & 0xff);
    output[j+2] = (unsigned char)((input[i] >> 16) & 0xff);
    output[j+3] = (unsigned char)((input[i] >> 24) & 0xff);
  }
}
void native_ov006_021f1e6c (UINT4 *output, unsigned char *input, unsigned int len)
{
  unsigned int i, j;
  for (i = 0, j = 0; j < len; i++, j += 4)
    output[i] = ((UINT4)input[j]) | (((UINT4)input[j+1]) << 8) |
      (((UINT4)input[j+2]) << 16) | (((UINT4)input[j+3]) << 24);
}
void native_ov006_021f1e98(POINTER output,POINTER input,unsigned int len){unsigned int i;for(i=0;i<len;i++)output[i]=input[i];}
void native_ov006_021f1eb0(POINTER output,int value,unsigned int len){unsigned int i;for(i=0;i<len;i++)((char*)output)[i]=(char)value;}
