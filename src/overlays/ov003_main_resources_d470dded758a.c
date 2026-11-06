typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {void *data;u32 size;} Resource;
extern s32 data_ov003_021e0698[];
extern u32 data_ov003_021e0690[];
extern char data_ov003_021e0304[];
extern char data_ov003_021e0318[];
extern u8 data_ov003_021e06b8[];
extern void func_02002d00(u32);
extern void func_020038a8(u32);
extern void func_02003950(u32);
extern void func_020039c0(u32);
extern void func_02003a40(u32);
extern void func_020489f0(u32);
extern void func_02046150(u32,u32,u32);
extern void func_020848d0(void);
extern void func_02008c58(u32,u32,u32);
extern void func_02045738(u32);
extern u32 func_0202a250(void);
extern u32 func_02048f6c(u32);
extern u32 func_02048f5c(u32);
extern u32 func_02048f7c(u32);
extern u32 func_02048f8c(u32);
extern void *func_0203cc2c(const char *,u32);
extern void func_0204518c(Resource *,void *,u32);
extern void func_0204820c(void *,u32,u32);
extern void func_02048308(void);
extern void func_ov003_021dac44(void *,u32,s32 *);
extern void func_0202a498(u32,void *);
extern void func_ov003_021de6b4(void);
extern void func_0201d444(void *,const char *,...);
extern void func_0205ff80(void *);
extern void func_ov003_021de768(void *);
extern void func_ov003_021de7d8(void *);
extern void func_0205ff9c(void);
extern void func_ov003_021de840(s32);
extern void func_ov003_021df928(void);
extern void func_02045680(u32);
extern void func_ov003_021deb78(void *,u32);
extern void func_02045490(u32,void *,u32,u32);
extern void *func_0202a44c(u32,u32,u32);
extern void func_02008e0c(void *,void *,u32);
extern void func_02045994(u32,void *,u32,u32);

void native_ov003_021da898(void) {
    func_02002d00(0);func_020038a8(4);func_02003950(256);func_020039c0(0);func_02003a40(0);
    *(volatile u32 *)0x04001000=(*(volatile u32 *)0x04001000&0xFFCFFFEF)|16;
    func_020489f0(1);func_02046150(1,0,2);func_02046150(2,2,2);func_020848d0();
    *(volatile u16 *)0x04001008=(*(volatile u16 *)0x04001008&0x43)|0x108;
    *(volatile u16 *)0x0400100A=(*(volatile u16 *)0x0400100A&0x43)|4;
    *(volatile u16 *)0x0400100C=(*(volatile u16 *)0x0400100C&0x43)|0x218;
    *(volatile u16 *)0x0400100E=(*(volatile u16 *)0x0400100E&0x43)|0x310;
    func_02008c58(0,0x06200000,0x20000);func_02008c58(0,0x06600000,0x20000);func_02008c58(0,0x05000400,0x400);func_02008c58(0,0x07000400,0x400);
    *(volatile u16 *)0x0400100C&=~3;
    *(volatile u16 *)0x04001008=(*(volatile u16 *)0x04001008&~3)|1;
    *(volatile u16 *)0x0400100A=(*(volatile u16 *)0x0400100A&~3)|2;
    *(volatile u16 *)0x0400100E=(*(volatile u16 *)0x0400100E&~3)|3;
    func_02045738(1);
    *(volatile u32 *)0x04001000=(*(volatile u32 *)0x04001000&~0x1F00)|0x1F00;
}

void native_ov003_021daac4(void) {
    u16 zero=0;
    Resource section;
    char filename[32]={0};
    u32 heap=func_0202a250();
    void *resource;
    u32 bank;
    data_ov003_021e0698[func_02048f6c(1)]=32;
    data_ov003_021e0698[func_02048f5c(1)]=32;
    data_ov003_021e0698[func_02048f7c(1)]=32;
    data_ov003_021e0698[func_02048f8c(1)]=0;
    resource=func_0203cc2c(data_ov003_021e0304,heap);
    func_0204518c(&section,resource,0);func_0204820c(section.data,0,section.size);func_0204820c(&zero,0,2);func_02048308();
    bank=func_02048f8c(1);
    func_ov003_021dac44(resource,bank,&data_ov003_021e0698[func_02048f8c(1)]);
    func_0202a498(heap,resource);func_ov003_021de6b4();
    func_0201d444(filename,data_ov003_021e0318);func_0205ff80(filename);func_ov003_021de768(data_ov003_021e0698);func_ov003_021de7d8(data_ov003_021e0698);func_0205ff9c();
    func_ov003_021de840(data_ov003_021e0698[func_02048f6c(1)]>>5);func_ov003_021df928();
    func_02045680(func_02048f7c(1));func_ov003_021deb78(data_ov003_021e06b8,0);
}

void native_ov003_021dac44(void *resource,u32 bank,s32 *cursor) {
    Resource section;
    func_0204518c(&section,resource,1);func_02045490(bank,section.data,*cursor,section.size);*cursor=*cursor+section.size;
    data_ov003_021e0690[1]=(u32)func_0202a44c(2,2048,4);
    func_0204518c(&section,resource,2);func_02008e0c(section.data,(void *)data_ov003_021e0690[1],section.size);func_02045994(bank,(void *)data_ov003_021e0690[1],0,2048);
}
