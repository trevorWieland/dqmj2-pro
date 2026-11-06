typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {void *data;u32 size;} Resource;
extern u32 data_ov003_021e0690[];
extern u32 data_ov003_021e07a8[];
extern u32 data_ov003_021e07ac[];
extern char data_ov003_021e032c[];
extern char data_ov003_021e0340[];
extern void *func_ov003_021dad9c(void);
extern u32 func_ov003_021dada8(void);
extern void func_02048e74(void *,u32);
extern void func_02048fcc(void *);
extern u32 func_0202a250(void);
extern void *func_0203cc2c(void *,u32);
extern void func_0204518c(Resource *,void *,u32);
extern void func_02008e0c(void *,void *,u32);
extern void func_02045994(u32,void *,u32,u32);
extern void func_0202a498(u32,void *);
extern void func_ov003_021daf90(void);
extern u32 func_02041944(void);
extern void func_02041538(u32,u32,u32);
extern u32 func_02041814(void);
extern void func_ov003_021db034(void);
extern void func_02041510(u32,u32,u32);
extern void func_ov003_021db248(void);
extern void func_0205e814(u32,u32,u32);
extern void func_ov003_021dff60(void *);
extern void func_ov003_021df6ac(void *);
extern void func_ov003_021df4b4(u32);
extern void func_ov003_021dfccc(void);
extern void func_ov003_021deda4(void *,u32,void *,u32,u32,u32,u32);
extern u32 func_020c35fc(void);
extern void func_ov003_021df3b4(void *,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021dfd18(u32);
extern u32 func_02062378(void);
extern void func_020620b4(u32);
extern void func_02062358(u32);

void native_ov003_021dacec(void) {
    if(data_ov003_021e0690[1]) {func_0202a498(2,(void *)data_ov003_021e0690[1]);data_ov003_021e0690[1]=0;}
}

void native_ov003_021dad1c(u32 kind,u32 bank) {
    Resource section;
    u32 heap=func_0202a250();
    void *resource=func_0203cc2c(data_ov003_021e032c,heap);
    func_0204518c(&section,resource,kind);func_02008e0c(section.data,(void *)data_ov003_021e0690[1],section.size);func_02045994(bank,(void *)data_ov003_021e0690[1],0,2048);func_0202a498(heap,resource);
}

void native_ov003_021dadc4(void) {
    func_02048e74(data_ov003_021e07ac,0);func_02048fcc(func_ov003_021dad9c());
    switch(func_ov003_021dada8()) {
    case 1:*(u32 *)func_ov003_021dad9c()=1;break;
    case 4:*(u32 *)func_ov003_021dad9c()=2;break;
    case 6:*(u32 *)func_ov003_021dad9c()=3;break;
    default:*(u32 *)func_ov003_021dad9c()=0;break;
    }
    data_ov003_021e07a8[2]=0;
}

u32 native_ov003_021dae50(void) {
    u32 *pending;
    u32 result;
    u32 redraw;
    pending=data_ov003_021e07ac;
    result=data_ov003_021e07a8[1];
    redraw=0;
    switch(data_ov003_021e07a8[2]) {
    case 0:func_ov003_021daf90();if(func_02041944()) func_02041538(0,2,10);redraw=1;pending[1]=1;break;
    case 1:redraw=1;if(func_02041814()!=1) func_ov003_021db034();break;
    case 2:func_02041510(1,2,10);result=9;break;
    case 3:result=1;redraw=1;break;
    case 4:result=4;redraw=1;break;
    case 5:result=6;redraw=1;break;
    case 6:func_ov003_021db248();redraw=1;break;
    case 7:func_02041510(1,2,10);func_02041538(1,2,10);func_0205e814(0,0,10);result=8;break;
    }
    if(redraw) {func_ov003_021dff60(func_ov003_021dad9c());func_ov003_021df6ac(func_ov003_021dad9c());}
    return result;
}

void native_ov003_021daf7c(void) {func_ov003_021df4b4(1);func_ov003_021dfccc();}

void native_ov003_021daf90(void) {
    void *context=func_ov003_021dad9c();
    u32 *selected=func_ov003_021dad9c();
    void *second;
    func_ov003_021deda4(context,5,data_ov003_021e0340,2,5,28,*selected);
    second=func_ov003_021dad9c();
    func_ov003_021df3b4(second,func_020c35fc(),16,2,21,28,2);func_ov003_021dfd18(1);
    if(func_02062378()!=34) {func_020620b4(34);func_02062358(1);}
}
