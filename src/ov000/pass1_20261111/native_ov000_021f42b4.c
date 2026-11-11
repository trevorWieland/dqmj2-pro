/* Selected-object tail check.
 *
 * Queries the current object, offsets 512 bytes into it and compares the signed
 * byte at 108 with 42. The image adds 512 with a separate `add` and then folds
 * the 108 into the load, so the 512 is a byte offset to a sub-object and the 108
 * a field inside it.
 * Unknowns: what the sub-object is and what value 42 marks.
 */
typedef signed char s8;
typedef int s32;
typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u8 pad[108];
    s8 field;
} Sub;

extern u8 *native_fn_02061944(void);

u32 native_ov000_021f42b4(void)
{
    Sub *sub = (Sub *)(native_fn_02061944() + 512);
    u32 result = 0;

    if (sub->field != 42)
        result = 1;
    return result;
}
