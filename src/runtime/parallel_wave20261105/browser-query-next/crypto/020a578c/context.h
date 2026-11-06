typedef unsigned char u8;
typedef unsigned int u32;
typedef struct{u8 cards[256],rotor,ratchet,avalanche,last_plain,last_cipher;} GOACryptState;
u8 native_fn_020a5660(GOACryptState*,int,u8*,u8,u8*,u32*);
void native_fn_020a56d4(GOACryptState*);
u8 native_fn_020a578c(GOACryptState*,u8);
#define keyrand native_fn_020a5660
#define GOAHashInit native_fn_020a56d4
#define GOAEncryptByte native_fn_020a578c
#define GOADecryptByte native_fn_020a578c
