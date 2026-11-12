/* ov000 row 0x021f8f70: 348 bytes.
 *
 * What it does: 86 instructions and 17 call(s), then a 11-entry dispatch through an inline branch table at 0x021f9050 (dispatch word at 0x021f9048)
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
extern void native_fn_02049ad0(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_0204a04c(void);
extern void native_fn_021f8d14(void);
extern void native_fn_021f9948(void);
extern void native_fn_021f8e4c(void);
extern void native_fn_021f99b0(void);
extern void native_fn_02063b60(void);
extern void native_fn_02085270(void);
extern void native_fn_02085418(void);
extern void native_fn_02086b14(void);


asm u32 native_ov000_021f8f70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_02215698
    mov r4, r0
    mov r0, #0
    bl native_fn_02049ad0
    add r1, r4, #1024
    ldrsb r2, [r1, #154]
    ldr r0, [r0]
    ldr r12, [pc, #0x130]
    cmp r2, #1
    ldr r4, [r0, #0x4]
    ldrb r5, [r12]
    bne L_021f8ff8
    ldrsb r2, [r1, #144]
    ldrsb r0, [r1, #145]
    add r0, r2, r0, lsl #2
    and r0, r0, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    mov r3, r0
    ldr r0, [pc, #0x100]
    cmp r3, #127
    strb r3, [r0]
    mov r0, r4
    mov r1, #5
    bne L_021f8fe8
    mov r2, #0
    mov r3, #31
    bl native_fn_0204a04c
    b L_021f9034
L_021f8fe8:
    mov r2, #7
    bl native_fn_0204a04c
    bl native_fn_021f8d14
    b L_021f9034
L_021f8ff8:
    cmp r2, #0
    mov r1, #5
    bne L_021f9024
    mov lr, #127
    mov r0, r4
    mov r2, #7
    mov r3, #12
    strb lr, [r12]
    bl native_fn_0204a04c
    bl native_fn_021f8d14
    b L_021f9034
L_021f9024:
    mov r0, r4
    mov r2, #2
    mov r3, #36
    bl native_fn_0204a04c
L_021f9034:
    ldr r0, [pc, #0x8c]
    ldrb r0, [r0]
    cmp r5, r0
    beq L_021f909c
    cmp r5, #10
    addls pc, pc, r5, lsl #2
    b L_021f909c
    dcd 0xea000011
    dcd 0xea000010
    dcd 0xea00000f
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000000
    dcd 0xeaffffff
    mov r0, r5
    bl native_fn_021f9948
    mov r1, #0
    bl native_fn_021f8e4c
    mov r0, r5
    bl native_fn_021f99b0
    mov r1, #0
    bl native_fn_02063b60
L_021f909c:
    add r0, r4, #60
    mov r1, #0
    mov r2, #8
    bl native_fn_02085270
    mov r0, r4
    mov r1, #3
    bl native_fn_02085418
    mov r0, r4
    mov r1, #25
    bl native_fn_02086b14
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x02236f14
}
