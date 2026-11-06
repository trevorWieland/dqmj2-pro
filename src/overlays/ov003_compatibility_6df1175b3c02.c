typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {u8 name[20];u32 id;s16 species;u8 variant;u8 remainder[105];} Record;
typedef struct {u32 unused;u16 low:4;u16 family:4;u16 high:8;} Species;
extern Species *func_020449d4(s16);
extern u32 func_020c365c(void);
extern u32 func_ov003_021db7fc(Record *,Record *);
extern u32 func_ov003_021db978(Record *,Record *);
extern u32 func_ov003_021db6ec(Record **,Record **);
extern u32 func_ov003_021db868(Record **,Record **);
extern Record *func_02062a50(u32);
extern Record *func_02062a88(u32);
extern u32 func_020c3828(u32);
extern u32 func_020c3904(u32);
extern Record *func_02062a10(u32);
extern void func_02008e0c(void *,void *,u32);
extern void func_0207b460(s16,u8,void *,void *);
extern void func_0207b1c4(void *,void *,void *);
extern void func_0207c078(s16,u8,void *,void *);

u32 native_ov003_021db7fc(Record *a,Record *b) {
    Species *first;
    Species *second;
    u8 af,bf;
    if(a && b && a->id && b->id) {
        first=func_020449d4(a->species);second=func_020449d4(b->species);
        af=first->family;bf=second->family;
        if(af==bf) return 1;
    }
    return 0;
}

u32 native_ov003_021db978(Record *a,Record *b) {
    if(a && b && a->id && b->id && a->species==b->species && a->variant==b->variant) return 1;
    return 0;
}

u32 native_ov003_021db6ec(Record **a,Record **b) {
    int i,j;
    if(func_020c365c()!=2) {
        for(i=0;i<3;i++) for(j=0;j<3;j++) if(func_ov003_021db7fc(a[i],b[j])) return 1;
        if(func_ov003_021db7fc(a[0],a[1]) || func_ov003_021db7fc(a[1],a[2]) || func_ov003_021db7fc(a[0],a[2]) || func_ov003_021db7fc(b[0],b[1]) || func_ov003_021db7fc(b[1],b[2]) || func_ov003_021db7fc(b[0],b[2])) return 1;
        return 0;
    } else {
        if(func_ov003_021db7fc(a[0],a[1]) || func_ov003_021db7fc(a[1],a[2]) || func_ov003_021db7fc(a[0],a[2])) return 1;
        return 0;
    }
}

u32 native_ov003_021db868(Record **a,Record **b) {
    int i,j;
    if(func_020c365c()!=2) {
        for(i=0;i<3;i++) for(j=0;j<3;j++) if(func_ov003_021db978(a[i],b[j])) return 1;
        if(func_ov003_021db978(a[0],a[1]) || func_ov003_021db978(a[1],a[2]) || func_ov003_021db978(a[0],a[2]) || func_ov003_021db978(b[0],b[1]) || func_ov003_021db978(b[1],b[2]) || func_ov003_021db978(b[0],b[2])) return 1;
        return 0;
    } else {
        if(func_ov003_021db978(a[0],a[1]) || func_ov003_021db978(a[1],a[2]) || func_ov003_021db978(a[0],a[2])) return 1;
        return 0;
    }
}

u32 native_ov003_021db57c(u32 mode) {
    Record *primary[3];
    Record *secondary[3];
    u8 index;
    for(index=0;index<3;index++) {primary[index]=0;primary[index]=func_02062a50(index);}
    for(index=0;index<3;index++) {secondary[index]=0;secondary[index]=func_02062a88(index);}
    switch(mode) {
    case 0:if(func_ov003_021db6ec(primary,secondary)) return 1;break;
    case 1:if(func_ov003_021db868(primary,secondary)) return 1;break;
    }
    for(index=0;index<3;index++) {primary[index]=0;primary[index]=func_02062a10(func_020c3828(index));}
    for(index=0;index<3;index++) {secondary[index]=0;secondary[index]=func_02062a10(func_020c3904(index));}
    switch(mode) {
    case 0:if(func_ov003_021db6ec(primary,secondary)) return 1;break;
    case 1:if(func_ov003_021db868(primary,secondary)) return 1;break;
    }
    return 0;
}

void native_ov003_021db4a8(u8 *target,u8 *record) {
    if(!record) {*(s16 *)(target+46)=-1;*(u32 *)target=-1;return;}
    func_02008e0c(record,target+182,20);
    *(u32 *)target=*(s16 *)(record+24);*(s16 *)(target+46)=*(s16 *)(record+24);target[48]=record[26];*(u32 *)(target+4)=*(u32 *)(record+20);target[177]=record[27];target[178]=record[30];target[175]=record[28];
    func_02008e0c(record+122,target+214,10);func_02008e0c(record+64,target+224,58);func_02008e0c(record+32,target+284,32);
    func_0207b460(*(s16 *)(target+46),target[48],record+122,target+74);func_0207b1c4(record+122,target+74,target+12);func_0207c078(*(s16 *)(target+46),target[48],target+74,target+138);
}
