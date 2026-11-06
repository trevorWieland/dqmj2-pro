#include "context.h"
u32 native_main_02096094(u32 prefix){int i,shift=(int)(32-prefix);u32 mask=0xffffffff;for(i=0;i<shift;i++)mask<<=1;return SOC_HtoNl(mask);}
