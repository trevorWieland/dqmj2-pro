typedef unsigned char u8;typedef unsigned int u32;typedef u32 size_t;
typedef enum{bt_int,bt_float,bt_string}BucketType;
typedef struct bucketset_s{void*buckets;}*bucketset_t;
typedef struct bucket_s{char*name;BucketType type;int nvals;union{int ival;double fval;char*sval;}vals;}bucket_t;
#define NULL ((void*)0)
#define assert(x) ((void)0)
#define AVG(cur,new,num) (((cur*num)+new)/(++num))
extern bucketset_t native_data_021d2504;
#define g_buckets native_data_021d2504
char*native_fn_020a8ea0(const char*);void native_fn_020a89a4(void*,const void*);void*native_fn_020a8a3c(void*,const void*);void*native_fn_020a927c(u32);void native_fn_020a929c(void*);
u32 native_fn_0201d69c(const char*);char*native_fn_0201d6b8(char*,const char*);char*native_fn_0201d7d0(char*,const char*);
void*native_fn_020b2fe4(bucket_t*,void*);void*native_fn_020b3030(bucket_t*);bucket_t*native_fn_020b3048(bucketset_t,char*);char*native_fn_020b2fc0(char*);
void*native_fn_020b2f9c(int);void*native_fn_020b2fac(double);void*native_fn_020b2ebc(bucketset_t,char*,void*);
#define goastrdup native_fn_020a8ea0
#define TableEnter native_fn_020a89a4
#define TableLookup native_fn_020a8a3c
#define gsimalloc native_fn_020a927c
#define gsifree native_fn_020a929c
#define strlen native_fn_0201d69c
#define strcpy native_fn_0201d6b8
#define strcat native_fn_0201d7d0
#define DoSet native_fn_020b2fe4
#define DoGet native_fn_020b3030
#define DoFind native_fn_020b3048
#define stripchars native_fn_020b2fc0
#define bint native_fn_020b2f9c
#define bfloat native_fn_020b2fac
#define BucketConcat native_fn_020b2ebc
