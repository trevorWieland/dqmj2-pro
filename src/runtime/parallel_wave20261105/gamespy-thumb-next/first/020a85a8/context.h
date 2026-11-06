typedef unsigned int size_t;
typedef void (*ArrayElementFreeFn)(void *);
typedef int (*ArrayCompareFn)(const void *,const void *);
typedef void (*ArrayMapFn)(void *,void *);
typedef int (*ArrayMapFn2)(void *,void *);
typedef struct DArrayImplementation {int count,capacity,elemsize,growby;ArrayElementFreeFn elemfreefn;void *list;} *DArray;
#define NULL ((void *)0)
#define DEF_GROWBY 8
#define NOT_FOUND -1
#define assert(x) ((void)0)
void *native_fn_020a927c(size_t);
void *native_fn_020a928c(void *,size_t);
void native_fn_020a929c(void *);
void *native_fn_0201b19c(void *,const void *,size_t);
void *native_fn_0201b1bc(void *,const void *,size_t);
void *native_fn_020a8644(DArray,int);
void native_fn_020a8594(DArray,int);
void native_fn_020a85a8(DArray);
void native_fn_020a85c4(DArray,const void *,int);
DArray native_fn_020a85dc(int,int,ArrayElementFreeFn);
void native_fn_020a866c(DArray,const void *,int);
void *native_fn_020a8884(const void *,void *,int,int,ArrayCompareFn,int *);

