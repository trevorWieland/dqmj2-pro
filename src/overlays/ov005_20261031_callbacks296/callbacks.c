typedef void (*OpaqueCallback)(void);
typedef struct { OpaqueCallback entries[3]; } CallbackRecord;
extern void native_fn_ov005_021e1600(void);
extern void native_fn_ov005_021e19b8(void);
extern void native_fn_ov005_021e1a6c(void);
extern const CallbackRecord native_data_ov005_021e6ea4[2] = {
    {{native_fn_ov005_021e1600,native_fn_ov005_021e19b8,native_fn_ov005_021e1a6c}},
    {{0,0,0}}
};
