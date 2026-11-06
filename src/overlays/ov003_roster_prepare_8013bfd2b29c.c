typedef unsigned char u8;
typedef unsigned int u32;
extern void func_02064978(void);
extern void func_020443d4(u32);
extern void func_02044454(u32);
extern u32 func_020c361c(void);
extern u32 func_020c363c(void);
extern u32 func_020c365c(void);
extern u32 func_020c369c(void);
extern void func_020652dc(u32);
extern void func_02065304(u32);
extern void func_02065630(u32);
extern void func_02065648(u32);
extern void func_0206532c(u32);
extern void func_020445c4(u32);
extern void func_0206534c(int);
extern void func_020652c4(u32);
extern void func_020656d0(u32);
extern void func_02008d78(void *,u32,u32);
extern void func_020c36b8(void *);
extern void func_020c3724(void *);
extern u8 *func_02062a50(u32);
extern u8 *func_02062a88(u32);
extern u8 *func_020c3838(u32);
extern u8 *func_020c3914(u32);
extern void *func_020649ac(u32);
extern void *func_020649d4(u32);
extern void *func_020649c0(u32);
extern void *func_020649e8(u32);
extern void func_ov003_021db4a8(void *,void *);
extern void func_020443c4(u32);

void native_ov003_021db290(void) {
    u32 flags=0;
    u32 ids[3];
    u8 *record;
    u8 index;
    func_02064978();func_020443d4(5);func_02044454(0);
    switch(func_020c361c()) {case 1:flags|=0x00800000;break;case 2:flags|=0x01000000;break;}
    if(func_020c363c()==1) flags|=0x02000000;
    if(func_020c365c()==2) flags|=0x04000000;else if(func_020c365c()==1) flags|=1;
    switch(func_020c369c()) {case 1:flags|=0x08000000;break;case 2:flags|=0x10000000;break;}
    func_02044454(flags|0x46);func_020652dc(104);func_02065304(0);func_02065630(0);func_02065648(45);func_0206532c(3);func_020445c4(1);func_0206534c(-1);func_020652c4(0);func_020656d0(1);
    func_02008d78(ids,0,12);func_020c36b8(ids);
    for(index=0;index<3;index++) {record=func_02062a50(index);if(record) ids[index]=*(u32 *)(record+20);func_ov003_021db4a8(func_020649ac(index),record);}
    func_020c36b8(ids);func_02008d78(ids,0,12);func_020c3724(ids);
    {u8 *record1;
    for(index=0;index<3;index++) {record1=func_02062a88(index);if(record1) ids[index]=*(u32 *)(record1+20);func_ov003_021db4a8(func_020649d4(index),record1);}
    }
    func_020c3724(ids);
    {u8 *record2;
    for(index=0;index<3;index++) {record2=func_020c3838(index);if(!*(u32 *)(record2+20)) record2=0;func_ov003_021db4a8(func_020649c0(index),record2);}
    }
    {u8 *record3;
    for(index=0;index<3;index++) {record3=func_020c3914(index);if(!*(u32 *)(record3+20)) record3=0;func_ov003_021db4a8(func_020649e8(index),record3);}
    }
    func_020443c4(12);
}
