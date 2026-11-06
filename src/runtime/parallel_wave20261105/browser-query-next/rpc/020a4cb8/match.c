typedef unsigned int u32;
typedef unsigned short u16;
typedef void(*Callback)(u32,u32,u32);
void native_fn_020072d0(void*,u32);
void native_fn_020072ec(void*,u32);
u32 native_fn_0200a41c(u32,u32);
void native_fn_0200a3d0(u32,Callback);
u16 native_fn_020a4dcc(u32,u32,u32);
int native_fn_020a49b0(u32,u32,u32,void*);
void native_fn_020004fc(u32);
int native_main_020a4cb8(u32 address,u32 length,void*buffer){native_fn_020072d0(buffer,length);while(!native_fn_0200a41c(4,1)){}native_fn_0200a3d0(4,(Callback)native_fn_020a4dcc);for(;;){if(native_fn_020a49b0(1,address,(u16)length,buffer)==1)break;native_fn_020004fc(0x40000);}native_fn_020072d0(buffer,length);return 1;}
