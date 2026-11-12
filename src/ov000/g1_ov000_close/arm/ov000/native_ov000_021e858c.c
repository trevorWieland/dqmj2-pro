/* ov000 row 0x021e858c: 108 bytes.
 *
 * What it does: 27 instructions and 5 call(s), then a 5-entry dispatch through an inline branch table at 0x021e85b0 (dispatch word at 0x021e85a8)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e801c(void);
extern void native_fn_021e805c(void);
extern void native_fn_021e8224(void);
extern void native_fn_021e84d4(void);
extern void native_fn_021e8548(void);


asm u32 native_ov000_021e858c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_021e801c
    cmp r0, #0
    beq L_021e85f0
    ldrb r0, [r4, #0x2a9]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021e85e8
    dcd 0xea00000c
    dcd 0xea000002
    dcd 0xea000004
    dcd 0xea000009
    dcd 0xea000005
    mov r0, r4
    bl native_fn_021e805c
    b L_021e85f0
    mov r0, r4
    bl native_fn_021e8224
    b L_021e85f0
    mov r0, r4
    bl native_fn_021e84d4
    b L_021e85f0
L_021e85e8:
    mov r0, r4
    bl native_fn_021e8548
L_021e85f0:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
