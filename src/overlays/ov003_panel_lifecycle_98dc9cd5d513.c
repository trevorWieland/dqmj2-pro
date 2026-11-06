typedef unsigned char u8;
typedef unsigned int u32;
extern u8 data_ov003_021e057c[];
extern u32 data_ov003_021e0580[];
extern void func_020c39d0(u32);
extern void func_02061260(u32);
extern void func_02061bf0(void);
extern void func_ov003_021d95a0(void);
extern u32 *func_02062a50(u32);
extern u32 *func_02062a88(u32);
extern u32 func_020c3828(u32);
extern u32 func_020c3904(u32);
extern void func_ov003_021d9dc0(void);
extern void func_ov003_021d9c60(void);
extern void func_ov003_021d9e40(void);

void native_ov003_021d8d68(void) {
    u8 index;
    u32 *record;
    func_020c39d0(2);
    func_02061260(0);
    func_02061bf0();
    func_ov003_021d95a0();
    for(index=0;index<3;index++) {
        record=func_02062a50(index);
        if(!record) data_ov003_021e0580[index]=-1;
        else data_ov003_021e0580[index]=record[5];
    }
    data_ov003_021e057c[0]=0;
    data_ov003_021e057c[1]=1;
    data_ov003_021e057c[2]=0;
}

void native_ov003_021d8f80(void) {
    u8 index;
    u32 *record;
    func_020c39d0(2);
    func_02061260(0);
    func_02061bf0();
    func_ov003_021d95a0();
    for(index=0;index<3;index++) {
        record=func_02062a88(index);
        if(!record) data_ov003_021e0580[index]=-1;
        else data_ov003_021e0580[index]=record[5];
    }
    data_ov003_021e057c[0]=0;
    data_ov003_021e057c[1]=1;
    data_ov003_021e057c[2]=0;
}

void native_ov003_021d9198(void) {
    u8 index;
    
    func_020c39d0(2);
    func_02061260(0);
    func_02061bf0();
    func_ov003_021d95a0();
    for(index=0;index<3;index++) {
        data_ov003_021e0580[index]=func_020c3828(index);
    }
    data_ov003_021e057c[0]=0;
    data_ov003_021e057c[1]=0;
    data_ov003_021e057c[2]=0;
}

void native_ov003_021d939c(void) {
    u8 index;
    
    func_020c39d0(2);
    func_02061260(0);
    func_02061bf0();
    func_ov003_021d95a0();
    for(index=0;index<3;index++) {
        data_ov003_021e0580[index]=func_020c3904(index);
    }
    data_ov003_021e057c[0]=0;
    data_ov003_021e057c[1]=0;
    data_ov003_021e057c[2]=0;
}

void native_ov003_021d8f6c(void) {
    func_ov003_021d9dc0();
    func_ov003_021d9c60();
    func_ov003_021d9e40();
}

void native_ov003_021d9184(void) {
    func_ov003_021d9dc0();
    func_ov003_021d9c60();
    func_ov003_021d9e40();
}

void native_ov003_021d9388(void) {
    func_ov003_021d9dc0();
    func_ov003_021d9c60();
    func_ov003_021d9e40();
}

void native_ov003_021d958c(void) {
    func_ov003_021d9dc0();
    func_ov003_021d9c60();
    func_ov003_021d9e40();
}
