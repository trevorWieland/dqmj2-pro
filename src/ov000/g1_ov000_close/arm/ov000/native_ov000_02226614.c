/* ov000 row 0x02226614: 356 bytes.
 *
 * What it does: 87 instructions and 13 call(s), then a 7-entry dispatch through an inline branch table at 0x02226630 (dispatch word at 0x02226628)
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

extern void native_fn_02227ccc(void);
extern void native_fn_022250c4(void);
extern void native_fn_02224fa4(void);
extern void native_fn_022251f8(void);
extern void native_fn_01ffa5ac(void);
extern void native_fn_02062520(void);


asm u32 native_ov000_02226614 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, [pc, #0x150]
    ldr r4, [pc, #0x150]
    ldrsb r0, [r0, #24]
    cmp r0, #27
    addls pc, pc, r0, lsl #2
    ldmia sp!, {r4, pc}
    dcd 0xea00001a
    dcd 0xea000019
    dcd 0xea000018
    dcd 0xea000017
    dcd 0xea00001e
    dcd 0xea00001d
    dcd 0xea00001c
    ldmia sp!, {r4, pc}
    ldmia sp!, {r4, pc}
    b L_022266c0
    b L_022266ec
    b L_022266e0
    b L_022266ec
    b L_022266ec
    b L_022266ec
    b L_022266e0
    ldmia sp!, {r4, pc}
    ldmia sp!, {r4, pc}
    ldmia sp!, {r4, pc}
    ldmia sp!, {r4, pc}
    b L_02226720
    ldmia sp!, {r4, pc}
    b L_022266f8
    b L_022266f8
    b L_02226714
    b L_02226714
    b L_02226714
    b L_02226754
    bl native_fn_02227ccc
    cmp r0, #0
    mov r0, #0
    beq L_022266b8
    bl native_fn_022250c4
    ldmia sp!, {r4, pc}
L_022266b8:
    bl native_fn_02224fa4
    ldmia sp!, {r4, pc}
L_022266c0:
    bl native_fn_02227ccc
    cmp r0, #0
    mov r0, #1
    beq L_022266d8
    bl native_fn_022250c4
    ldmia sp!, {r4, pc}
L_022266d8:
    bl native_fn_02224fa4
    ldmia sp!, {r4, pc}
L_022266e0:
    mov r0, #19
    bl native_fn_022251f8
    ldmia sp!, {r4, pc}
L_022266ec:
    mov r0, #65
    bl native_fn_022251f8
    ldmia sp!, {r4, pc}
L_022266f8:
    mov r3, #127
    add r0, r4, #404
    mov r1, #68
    mov r2, #20
    strb r3, [r4, #0x194]
    bl native_fn_01ffa5ac
    ldmia sp!, {r4, pc}
L_02226714:
    mov r0, #66
    bl native_fn_022251f8
    ldmia sp!, {r4, pc}
L_02226720:
    bl native_fn_02062520
    cmp r0, #0
    ldmeqia sp!, {r4, pc}
    ldr r1, [pc, #0x3c]
    add r0, r4, #143
    ldrb r2, [r1, #0x20]
    add r0, r0, #256
    mov r1, #1
    add r2, r2, #21
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_01ffa5ac
    ldmia sp!, {r4, pc}
L_02226754:
    mov r3, #1
    add r0, r4, #404
    mov r1, #68
    mov r2, #64
    strb r3, [r4, #0x194]
    bl native_fn_01ffa5ac
    ldmia sp!, {r4, pc}
    dcd 0x022468b8
    dcd 0x02246c84
}
