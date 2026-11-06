typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {volatile s8 timer;u8 pad[23];u32 current,phase,next,previous;} State;
typedef struct {void (*start)(void);u32 (*step)(void);void (*finish)(void);} Mode;
typedef struct {u16 unused,buttons;} Input;
extern State data_ov003_021e0690;
extern u32 data_ov003_021e06a8[];
extern u8 data_ov003_021e06b8[];
extern Mode data_ov003_021e0160[];
extern u32 func_0202a1e0(u32);
extern void func_ov003_021da898(void);
extern void func_02048e8c(void);
extern void func_ov003_021daa44(void);
extern void func_ov003_021daac4(void);
extern void func_020414c8(u32);
extern void func_020418b0(u32);
extern u32 func_020c3a00(void);
extern void func_020c39f0(u32);
extern void func_02048e74(void *,u32);
extern void *func_ov003_021dad9c(void);
extern void func_02048fcc(void *);
extern u32 func_02027400(void);
extern void func_ov003_021d79e4(u32);
extern void func_02041538(u32,u32,u32);
extern void func_ov003_021dff60(void);
extern u32 func_02041814(void);
extern u32 func_02062520(void);
extern u32 func_020653d0(void);
extern void func_ov003_021dea38(u32,u32,u32,u32,u32,int);
extern void func_ov003_021df6ac(void);
extern Input *func_0202a634(void);
extern void func_ov003_021df668(u32);
extern void func_ov003_021d7fa4(void);
extern void func_ov003_021d7878(u32);
extern u32 func_020c39e0(void);
extern void func_020c39d0(u32);
extern u32 func_020273c8(void);
extern void func_02045738(u32);
extern void func_0206258c(u32);
extern void func_020c40f4(u32);
extern void func_02041898(u32);
extern void func_020414b0(u32);
extern void func_0204176c(void);
extern void func_ov003_021de710(void);
extern void func_ov003_021dfbf4(void);
extern void func_ov003_021dacec(void);
extern void func_ov003_021daa0c(void);

typedef struct {u32 root;s8 kind;u8 limit;s8 flag;u8 padding;} Object;
extern Object *func_02049ad0(s8);
extern void func_0205fd80(u32);
extern void func_02048f3c(u32,u32);
extern void func_02048f2c(u32,u32);
extern void func_02048f1c(u32,u32);
extern void func_02048f4c(u32,u32);
extern void func_02049940(u32);
extern void func_020848d4(u32);
extern void func_0204617c(u32,u32);
extern u8 data_ov003_021e0698[];

void native_ov003_021da3fc(void) {
    u32 old=func_0202a1e0(2);
    u32 mode;
    func_ov003_021da898();func_02048e8c();func_ov003_021daa44();func_0202a1e0(old);func_ov003_021daac4();
    func_020414c8(63);func_020418b0(2);
    if(func_020c3a00()==2) {mode=0;func_020c39f0(1);}
    else if(func_020c3a00()==3) {mode=2;func_020c39f0(1);}
    else if(func_020c3a00()==4) mode=5;
    else mode=0;
    func_02048e74(data_ov003_021e06a8,mode);
    func_02048fcc(func_ov003_021dad9c());
    data_ov003_021e0690.previous=12;
    if(func_02027400()==2 && func_020c3a00()==0) {
        data_ov003_021e0690.phase=4;data_ov003_021e0690.timer=5;func_020c39f0(1);return;
    }
    if(func_020c3a00()==0) {func_ov003_021d79e4(33);func_020c39f0(1);}
    func_02041538(0,2,10);
}

void native_ov003_021da86c(void) {
    if(func_020c3a00()==1) func_020c39f0(0);
    func_ov003_021de710();func_ov003_021dfbf4();func_ov003_021dacec();func_ov003_021daa0c();
}

void native_ov003_021daa0c(void) {
    func_02049940(1);func_020848d4(1);func_020848d4(2);func_0204617c(1,2);func_0204617c(2,2);
}

void native_ov003_021daa44(void) {
    s8 index;
    Object *object;
    func_0205fd80(1);
    for(index=0;index<36;index++) {
        object=func_02049ad0(index);object->kind=12;object->limit=127;object->root=0;object->flag=-1;
    }
    func_02048f3c(2,1);func_02048f2c(0,1);func_02048f1c(1,1);func_02048f4c(3,1);
}

void *native_ov003_021dad9c(void) {return data_ov003_021e06b8;}

u32 native_ov003_021dada8(void) {return data_ov003_021e0690.previous;}

void *native_ov003_021dadb8(void) {return data_ov003_021e0698;}
