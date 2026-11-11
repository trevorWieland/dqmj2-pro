/* 0x02046e68 (main, ARM, 52 B) -- advance the text command cursor by one command.

   The text walker (native_main_02047ac0) asks this for the byte length of the command
   at the cursor: native_02046e9c decodes the command into the halfword table slot at
   native_data_020fae64[cursor] and returns how many input bytes it consumed, and this
   wrapper advances the halfword cursor at native_data_020fb2e4 afterwards. The return
   value is native_02046e9c's length.

   The cursor is reached through a const pointer on purpose: the image materialises
   the address once, keeps it in r4 across the call and re-reads it with `ldrh r1, [r4]`.
   Without the const qualifier mwccarm rematerialises the literal after the call and the
   body grows to 56 B. Reproduces under the pinned 2.0/base (p001) and under the
   src/main rule (2.0/sp1p5, p002). */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

extern u16 native_data_020fae64[];
extern u16 native_data_020fb2e4;
extern u32 native_fn_02046e9c(u16 *, const u8 *);

u32 native_main_02046e68(const u8 *command)
{
    u16 *const cursor = &native_data_020fb2e4;
    u32 length = native_fn_02046e9c(&native_data_020fae64[*cursor], command);

    (*cursor)++;
    return length;
}
