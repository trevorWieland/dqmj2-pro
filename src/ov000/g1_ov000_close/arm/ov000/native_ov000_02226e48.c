/* ov000 row 0x02226e48: 508 bytes.
 *
 * What it does: 124 instructions and 10 call(s), then a 5-entry dispatch through an inline branch table at 0x02226e74 (dispatch word at 0x02226e6c)
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

extern void native_fn_01ffadd8(void);
extern void native_fn_01ffaf98(void);
extern void native_fn_02223c94(void);
extern void native_fn_022249e0(void);
extern void native_fn_022249b0(void);
extern void native_fn_02223c6c(void);
extern void native_fn_01ffb34c(void);
extern void native_fn_0204b61c(void);
extern void native_fn_01ffa804(void);
extern void native_fn_02064488(void);
extern u8 native_data_0222feb4[];


asm u32 native_ov000_02226e48 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r0, [pc, #0x1e4]
    ldr r1, [pc, #0x1e4]
    ldrsb r6, [r0, #24]
    ldr r4, [pc, #0x1e0]
    mov r5, #0
    add r0, r6, r6, lsl #2
    ldrsb r0, [r1, r0]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_02226e94
    dcd 0xea000006
    dcd 0xea000002
    dcd 0xea000003
    dcd 0xea000003
    dcd 0xea000002
    bl native_fn_01ffadd8
    b L_02226e94
    bl native_fn_01ffaf98
L_02226e94:
    ldr r0, [pc, #0x19c]
    ldrsb r0, [r0, #24]
    cmp r0, #16
    bgt L_02226ef4
    cmp r0, #0
    addge pc, pc, r0, lsl #2
    b L_02226f44
    b L_02226f00
    b L_02226f00
    b L_02226f44
    b L_02226f44
    b L_02226f00
    b L_02226f44
    b L_02226f44
    b L_02226f44
    b L_02226f00
    b L_02226f44
    b L_02226f0c
    b L_02226f44
    b L_02226f44
    b L_02226f0c
    b L_02226f0c
    b L_02226f44
    b L_02226f00
L_02226ef4:
    cmp r0, #24
    beq L_02226f34
    b L_02226f44
L_02226f00:
    mov r0, #127
    strb r0, [r4, #0x18c]
    b L_02226f44
L_02226f0c:
    mov r0, #1
    bl native_fn_02223c94
    mov r0, #1
    bl native_fn_022249e0
    mov r2, #127
    ldr r0, [pc, #0x110]
    mov r1, #0
    strb r2, [r4, #0x18c]
    strb r1, [r0, #0x1c]
    b L_02226f44
L_02226f34:
    bl native_fn_022249b0
    bl native_fn_02223c6c
    mov r0, #127
    strb r0, [r4, #0x18c]
L_02226f44:
    ldr r0, [pc, #0xec]
    ldrsb r2, [r0, #26]
    cmp r2, #21
    bgt L_02226f9c
    subs r1, r2, #10
    addpl pc, pc, r1, lsl #2
    b L_02226f90
    b L_02226ffc
    b L_0222700c
    b L_0222700c
    b L_02226ffc
    b L_02226ffc
    b L_02226fa8
    b L_0222700c
    b L_0222700c
    b L_0222700c
    b L_0222700c
    b L_0222700c
    b L_02226fdc
L_02226f90:
    cmp r2, #3
    beq L_02226fa8
    b L_0222700c
L_02226f9c:
    cmp r2, #30
    beq L_02226fbc
    b L_0222700c
L_02226fa8:
    ldr r0, [pc, #0x88]
    mov r1, #2
    strb r2, [r0, #0x18]
    str r1, [r0, #0x14]
    b L_02227020
L_02226fbc:
    mov r1, #8
    str r1, [r0, #0x14]
    bl native_fn_01ffb34c
    mov r1, #0
    bl native_fn_0204b61c
    bl native_fn_01ffa804
    mov r5, #0
    b L_02227020
L_02226fdc:
    mov r0, #1
    bl native_fn_02064488
    ldr r0, [pc, #0x4c]
    mov r1, #2
    ldrsb r2, [r0, #26]
    strb r2, [r0, #0x18]
    str r1, [r0, #0x14]
    b L_02227020
L_02226ffc:
    mov r1, #127
    strb r1, [r0, #0x21]
    mov r1, #30
    str r1, [r0, #0x4]
L_0222700c:
    ldr r0, [pc, #0x24]
    mov r1, #2
    ldrsb r2, [r0, #26]
    strb r2, [r0, #0x18]
    str r1, [r0, #0x14]
L_02227020:
    ldr r1, [pc, #0x10]
    mov r2, #29
    strb r6, [r1, #0x19]
    mov r0, r5
    strb r2, [r1, #0x1a]
    ldmia sp!, {r4, r5, r6, pc}
    dcd 0x022468b8
    dcd native_data_0222feb4
    dcd 0x02246aa8
}
