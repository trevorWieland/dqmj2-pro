/* ov000 row 0x021edd04: 576 bytes.
 *
 * What it does: 143 instructions and 22 call(s), then a 5-entry dispatch through an inline branch table at 0x021edd28 (dispatch word at 0x021edd20)
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

extern void native_fn_021efa9c(void);
extern void native_fn_021effec(void);
extern void native_fn_021efe60(void);
extern void native_fn_021ef17c(void);
extern void native_fn_021ef154(void);
extern void native_fn_021ef3a0(void);
extern void native_fn_02062d04(void);
extern void native_fn_021ee1b0(void);
extern void native_fn_021f02a4(void);
extern void native_fn_020c49e8(void);
extern void native_fn_021ef8e0(void);
extern void native_fn_021f015c(void);
extern void native_fn_02026144(void);


asm u32 native_ov000_021edd04 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    ldr r1, [pc, #0x22c]
    mov r9, r0
    ldr r0, [r1, #0x4]
    ldrsb r4, [r0, #32]
    cmp r4, #4
    addls pc, pc, r4, lsl #2
    b L_021edf34
    dcd 0xea000081
    dcd 0xea000002
    dcd 0xea00001a
    dcd 0xea000071
    dcd 0xea000077
    ldrb r0, [r0, #0x518]
    cmp r0, #0
    beq L_021edf34
    bl native_fn_021efa9c
    cmp r0, #0
    bne L_021edf34
    bl native_fn_021effec
    mov r0, #1
    bl native_fn_021efe60
    mov r0, #1
    bl native_fn_021ef17c
    mov r0, #1
    bl native_fn_021ef154
    mov r0, #1
    bl native_fn_021ef3a0
    ldr r0, [pc, #0x1c0]
    mov r2, #0
    ldr r1, [r0, #0x4]
    strb r2, [r1, #0x101]
    ldrb r1, [r9]
    orr r1, r1, #7
    strb r1, [r9]
    ldr r0, [r0, #0x4]
    strb r2, [r0, #0x518]
    b L_021edf34
    ldrb r0, [r0, #0x518]
    cmp r0, #0
    beq L_021edf34
    bl native_fn_021efa9c
    cmp r0, #0
    bne L_021edf34
    ldr r0, [pc, #0x180]
    mov r5, #1
    ldr r1, [r0, #0x4]
    ldr r0, [r1, #0x10]
    add r0, r1, r0, lsl #2
    ldr r0, [r0, #0x104]
    bl native_fn_02062d04
    cmp r0, #0
    bne L_021edeac
    mov r0, #2
    bl native_fn_021ee1b0
    ldr r0, [pc, #0x154]
    ldr r1, [r0, #0x4]
    ldrb r0, [r1, #0x504]
    cmp r0, #0
    moveq r4, #0
    moveq r5, r4
    beq L_021edeac
    ldr r6, [r1, #0x10]
    ldr r7, [r1, #0x14]
    bl native_fn_021f02a4
    bl native_fn_020c49e8
    mov r0, r5
    mov r1, #6
    mov r2, #28
    bl native_fn_021ef8e0
    ldr r0, [pc, #0x118]
    mov r8, #20
    ldr r2, [r0, #0x4]
    mov r3, #28
    ldrb r1, [r2, #0x504]
    cmp r1, #6
    movlo r0, r1
    movhs r0, #6
    and r0, r0, #255
    stmia sp, {r0, r1}
    add r0, r2, #16
    mov r1, #1
    mov r2, #7
    str r8, [sp, #0x8]
    bl native_fn_021f015c
    ldr r0, [pc, #0xdc]
    ldr r8, [r0, #0x4]
    ldrh r1, [r8, #30]
    cmp r1, r6
    ble L_021ede80
    str r7, [r8, #0x14]
    ldr r0, [r0, #0x4]
    str r6, [r0, #0x10]
    b L_021edeac
L_021ede80:
    ldrh r6, [r8, #28]
    sub r0, r1, #1
    mov r1, r6
    bl native_fn_02026144
    mul r1, r6, r0
    ldr r0, [pc, #0xa4]
    str r1, [r8, #0x14]
    ldr r1, [r0, #0x4]
    ldrh r0, [r1, #30]
    sub r0, r0, #1
    str r0, [r1, #0x10]
L_021edeac:
    bl native_fn_021effec
    ldr r0, [pc, #0x88]
    mov r2, #0
    ldr r1, [r0, #0x4]
    cmp r5, #0
    strb r2, [r1, #0x101]
    ldr r0, [r0, #0x4]
    strb r2, [r0, #0x518]
    beq L_021edee0
    mov r0, #1
    bl native_fn_021efe60
    mov r0, #1
    bl native_fn_021ef17c
L_021edee0:
    mov r0, #1
    bl native_fn_021ef154
    mov r0, #1
    bl native_fn_021ef3a0
    ldrb r0, [r9]
    orr r0, r0, #7
    strb r0, [r9]
    b L_021edf34
    ldrb r0, [r0, #0x518]
    cmp r0, #0
    beq L_021edf34
    bl native_fn_021efa9c
    cmp r0, #0
    moveq r4, #1
    b L_021edf34
    ldrb r0, [r0, #0x518]
    cmp r0, #0
    beq L_021edf34
    bl native_fn_021efa9c
    cmp r0, #0
    moveq r4, #1
L_021edf34:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    dcd 0x02236bc4
}
