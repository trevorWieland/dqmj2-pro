/* ov000 row 0x02201428: 192 bytes.
 *
 * What it does: 47 instructions and 2 call(s), then a 6-entry dispatch through an inline branch table at 0x0220144c (dispatch word at 0x02201444)
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

extern void native_fn_02215698(void);
extern void native_fn_0204b53c(void);


asm u32 native_ov000_02201428 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    mov r4, r0
    bl native_fn_02215698
    ldr r1, [pc, #0xa4]
    ldr r2, [r1]
    cmp r2, #5
    addls pc, pc, r2, lsl #2
    b L_022014b0
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea00000a
    dcd 0xea000009
    mov r2, #16
    mov r1, #40
    strh r2, [sp]
    strh r1, [sp, #2]
    b L_022014b8
    mov r2, #16
    mov r1, #64
    strh r2, [sp]
    strh r1, [sp, #2]
    b L_022014b8
    mov r2, #16
    strh r2, [sp]
    ldrb r1, [r1, #0x5e8]
    cmp r1, #0
    moveq r1, #80
    streqh r1, [sp, #2]
    movne r1, #64
    strneh r1, [sp, #2]
    b L_022014b8
L_022014b0:
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
L_022014b8:
    ldrsh r12, [sp, #2]
    ldr r3, [r4]
    ldr r2, [r4, #0x4]
    add r1, sp, #0
    sub r2, r3, r2
    add r2, r12, r2, lsl #4
    add r0, r0, #16
    strh r2, [sp, #2]
    bl native_fn_0204b53c
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
    dcd 0x02237778
}
