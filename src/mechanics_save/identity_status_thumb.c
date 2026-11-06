typedef unsigned int u32;
extern const char native_sdk_version[];
extern void native_sdk_version_register(const char *);
extern int native_sdk_query(void *);
extern int native_sdk_pending(void);
extern void native_sdk_finalize(void *);
extern void native_sdk_callbacks(void (*)(void), void (*)(void), void (*)(void), void (*)(void));
extern void native_sdk_callback0(void);
extern void native_sdk_callback1(void);
extern void native_sdk_callback2(void);
extern void native_sdk_callback3(void);
extern int native_identity_kind(void *);
extern u32 native_identity_flags(void *);
extern int native_identity_flags_set(void *, u32);
int saved_sdk_bootstrap_status(void *input) {
    int pending = 0;
    int query;
    native_sdk_version_register(native_sdk_version);
    query = native_sdk_query(input);
    if (native_sdk_pending()) {
        native_sdk_finalize(input);
        pending = 1;
    }
    if (query < 0) {
        if (pending) pending = 2;
        else pending = 3;
    } else {
        if (pending) pending = 1;
        else pending = 0;
    }
    native_sdk_callbacks(native_sdk_callback0, native_sdk_callback1, native_sdk_callback2, native_sdk_callback3);
    return pending;
}
void saved_identity_mark_flag4(void *identity) {
    if (native_identity_kind(identity) == 3) { u32 flags = native_identity_flags(identity) | 4; native_identity_flags_set(identity, flags); }
}
