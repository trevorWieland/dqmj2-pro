typedef unsigned int u32;
typedef u32 (*HandleContract)(void *);

static HandleContract handle_contract;

void set_handle_contract(HandleContract callback) {
    handle_contract = callback;
}

u32 native_fn_02029688(void *record) {
    return handle_contract(record);
}
