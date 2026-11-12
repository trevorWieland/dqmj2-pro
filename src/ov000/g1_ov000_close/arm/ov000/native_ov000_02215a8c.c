/* ov000 row 0x02215a8c: 316 bytes.
 *
 * What it does: 77 instructions and 12 call(s), then a 15-entry dispatch through an inline branch table at 0x02215acc (dispatch word at 0x02215ac4)
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

extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0204820c(void);
extern void native_fn_0202a498(void);
extern void native_fn_0204518c(void);
extern void native_fn_02048308(void);
extern u8 native_data_0222f994[];
extern u8 native_data_0222f9a4[];


asm u32 native_ov000_02215a8c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #44
    mov r3, #0
    add r2, sp, #12
    strh r3, [sp]
    mov r1, #8
L_02215aa4:
    strb r3, [r2]
    strb r3, [r2, #0x1]
    strb r3, [r2, #0x2]
    strb r3, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne L_02215aa4
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_02215b68
    dcd 0xea00000d
    dcd 0xea000024
    dcd 0xea000023
    dcd 0xea000022
    dcd 0xea000021
    dcd 0xea000020
    dcd 0xea00001f
    dcd 0xea00001e
    dcd 0xea00001d
    dcd 0xea00001c
    dcd 0xea00001b
    dcd 0xea00001a
    dcd 0xea000019
    dcd 0xea000018
    dcd 0xea000017
    ldr r1, [pc, #0xb0]
    add r0, sp, #12
    bl native_fn_0201d444
    add r0, sp, #12
    bl native_fn_0202a8e0
    movs r4, r0
    addeq sp, sp, #44
    ldmeqia sp!, {r3, r4, pc}
    add r0, sp, #12
    mov r1, #2
    bl native_fn_0203cc2c
    mov r2, r4
    mov r1, #0
    mov r4, r0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #44
    ldmia sp!, {r3, r4, pc}
L_02215b68:
    ldr r0, [pc, #0x54]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #4
    mov r1, r4
    mov r2, #0
    bl native_fn_0204518c
    ldr r0, [sp, #0x4]
    ldr r2, [sp, #0x8]
    mov r1, #0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #44
    ldmia sp!, {r3, r4, pc}
    dcd native_data_0222f994
    dcd native_data_0222f9a4
}
