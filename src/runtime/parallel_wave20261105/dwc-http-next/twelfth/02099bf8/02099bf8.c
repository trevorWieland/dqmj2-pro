#include "context.h"
u32 native_main_02099bf8(char*time){
s64 current,remote;
unsigned long length;
int i;
RTCDate date;
RTCTime clock;
char text[32];
length=native_fn_0201d69c(time);
if(length==native_fn_0201d69c(native_data_020df1fc)&&time[7]==' '&&time[11]==' '&&time[16]==' '&&time[19]==':'&&time[22]==':'&&time[25]==' '){
if(native_fn_0200f540(&date,&clock)==0){
current=native_fn_0200fc74(&date,&clock);
if(current!=-1){
native_fn_0201d6b8(text,time);
text[7]=0;text[11]=0;text[16]=0;text[19]=0;text[22]=0;text[25]=0;
native_data_020ec9b0=0;
date.year=native_fn_0201f274(text+12);
if(native_data_020ec9b0!=34){
date.year-=2000;
date.month=13;
for(i=0;i<12;i++){if(native_fn_0201d800(native_data_020df1cc[i],text+8)==0){date.month=i+1;break;}}
if(date.month<=12){
native_data_020ec9b0=0;
date.day=native_fn_0201f274(text+5);
if(native_data_020ec9b0!=34){
native_data_020ec9b0=0;
clock.hour=native_fn_0201f274(text+17);
if(native_data_020ec9b0!=34){
native_data_020ec9b0=0;
clock.minute=native_fn_0201f274(text+20);
if(native_data_020ec9b0!=34){
native_data_020ec9b0=0;
clock.second=native_fn_0201f274(text+23);
if(native_data_020ec9b0!=34){
remote=native_fn_0200fc74(&date,&clock);
if(remote!=-1){native_data_021d1990.diff=current-remote;native_data_021d1990.base=current;native_data_021d1990.valid=1;return 1;}
}
}
}
}
}
}
}
}
}
return 0;
}
