typedef unsigned int u32;
typedef void*(*MallocCB)(u32);
typedef void(*FreeCB)(void*);
typedef void*(*ReallocCB)(void*,u32);
typedef struct{u32 uninterpreted[2];MallocCB malloc;FreeCB free;ReallocCB realloc;} HeapView;
extern HeapView native_data_021d2374;
