/* ov000 row 0x021f097c: 724 bytes.
 *
 * What it does: 179 instructions and 22 call(s), then a 8-entry dispatch through an inline branch table at 0x021f09cc (dispatch word at 0x021f09c4)
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

extern void native_fn_0202a634(void);
extern void native_fn_021f1018(void);
extern void native_fn_02062520(void);
extern void native_fn_021f0c50(void);
extern void native_fn_02041538(void);
extern void native_fn_021f1338(void);
extern void native_fn_021f1428(void);
extern void native_fn_021f10e4(void);
extern void native_fn_021f10ec(void);
extern void native_fn_021f1be0(void);
extern void native_fn_021f2a64(void);
extern void native_fn_021f1080(void);
extern void native_fn_021f1850(void);
extern void native_fn_021f2008(void);
extern void native_fn_021f26b4(void);
extern void native_fn_021f2a20(void);
extern void native_fn_021f11b0(void);
extern void native_fn_020c4318(void);
extern void native_fn_021f1298(void);
extern void native_fn_020d3708(void);


asm u32 native_ov000_021f097c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r7, #4
    bl native_fn_0202a634
    ldr r4, [pc, #0x2b4]
    mov r8, r0
    ldr r0, [r4, #0x8]
    ldr r5, [pc, #0x2ac]
    ldrsb r0, [r0, #32]
    mov r11, #0
    mov r10, #2
    str r0, [sp, #0x8]
    mov r6, #1
L_021f09b0:
    ldr r1, [r4, #0x8]
    mov r9, #0
    add r3, r1, #4096
    ldrb r0, [r3, #0x91d]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_021f0c20
    dcd 0xea000006
    dcd 0xea00000b
    dcd 0xea000020
    dcd 0xea00006d
    dcd 0xea00006f
    dcd 0xea00007b
    dcd 0xea000082
    dcd 0xea00008c
    bl native_fn_021f1018
    str r6, [r4, #0x4]
    ldr r0, [r4, #0x8]
    add r0, r0, #4096
    strb r6, [r0, #0x91d]
    b L_021f0c20
    ldr r0, [r4, #0x4]
    cmp r0, #0
    beq L_021f0a1c
    bl native_fn_02062520
    cmp r0, #0
    beq L_021f0c20
L_021f0a1c:
    bl native_fn_021f0c50
    ldr r0, [r4, #0x8]
    add r0, r0, #4096
    strb r10, [r0, #0x91d]
    ldr r0, [r4, #0x4]
    cmp r0, #0
    beq L_021f0a4c
    mov r0, #0
    mov r1, r10
    mov r2, #10
    bl native_fn_02041538
    str r11, [r4, #0x4]
L_021f0a4c:
    mov r0, #1
    str r0, [r4]
    mov r9, r0
    b L_021f0c20
    ldrh r0, [r8, #2]
    tst r0, #2
    beq L_021f0a9c
    mov r0, r5
    bl native_fn_021f1338
    ldr r2, [r4, #0x8]
    ldrsb r1, [r2, #32]
    cmp r0, r1
    beq L_021f0b60
    add r1, r2, #4096
    strb r0, [r1, #0x91f]
    ldr r0, [r4, #0x8]
    add r1, r0, #4096
    mov r0, #3
    strb r0, [r1, #0x91d]
    b L_021f0b60
L_021f0a9c:
    tst r0, #1
    beq L_021f0ad8
    mov r0, r5
    bl native_fn_021f1428
    ldr r2, [r4, #0x8]
    ldrsb r1, [r2, #32]
    cmp r0, r1
    beq L_021f0b60
    add r1, r2, #4096
    strb r0, [r1, #0x91f]
    ldr r0, [r4, #0x8]
    add r1, r0, #4096
    mov r0, #3
    strb r0, [r1, #0x91d]
    b L_021f0b60
L_021f0ad8:
    tst r0, #2048
    beq L_021f0b00
    bl native_fn_021f10e4
    cmp r0, #0
    beq L_021f0b60
    ldr r0, [r4, #0x8]
    add r1, r0, #4096
    mov r0, #4
    strb r0, [r1, #0x91d]
    b L_021f0b60
L_021f0b00:
    tst r0, #4
    beq L_021f0b58
    ldrsb r0, [r1, #32]
    cmp r0, #2
    cmpne r0, #4
    cmpne r0, #6
    bne L_021f0b58
    bl native_fn_021f10ec
    ldr r1, [r4, #0x8]
    ldrb r0, [r1, #0x20]
    add r1, r1, #4096
    ldrb r1, [r1, #0x921]
    bl native_fn_021f1be0
    mov r0, #0
    bl native_fn_021f2a64
    ldr r0, [r4, #0x8]
    add r1, r0, #4096
    mov r0, #4
    strb r0, [r1, #0x91d]
    mov r0, #1
    str r0, [r4]
    b L_021f0b60
L_021f0b58:
    mov r0, r5
    bl native_fn_021f1080
L_021f0b60:
    ldr r0, [r4]
    cmp r0, #1
    bne L_021f0b80
    bl native_fn_021f1850
    bl native_fn_021f2008
    bl native_fn_021f26b4
    mov r0, #0
    str r0, [r4]
L_021f0b80:
    ldr r0, [r4, #0x8]
    mov r1, #3
    add r0, r0, #16
    bl native_fn_021f2a20
    b L_021f0c20
    bl native_fn_021f11b0
    mov r7, r0
    b L_021f0c20
    bl native_fn_020c4318
    cmp r0, #0
    beq L_021f0c20
    bl native_fn_021f1298
    cmp r0, #0
    bne L_021f0c20
    ldr r1, [r4, #0x8]
    mov r0, #1
    add r2, r1, #4096
    mov r1, #2
    strb r1, [r2, #0x91d]
    bl native_fn_021f2a64
    b L_021f0c20
    bl native_fn_020c4318
    cmp r0, #0
    beq L_021f0c20
    ldr r0, [r4, #0x8]
    add r1, r0, #4096
    mov r0, #3
    strb r0, [r1, #0x91d]
    b L_021f0c20
    add r1, r1, #6400
    ldrsh r0, [r1, #20]
    str r0, [sp]
    ldrb r0, [r3, #0x916]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #12]
    ldrsh r2, [r1, #16]
    ldrb r1, [r3, #0x90e]
    ldrb r3, [r3, #0x912]
    bl native_fn_020d3708
    mov r7, #9
L_021f0c20:
    cmp r9, #0
    bne L_021f09b0
    ldr r1, [pc, #0x18]
    mov r0, r7
    ldr r1, [r1, #0x8]
    add r2, r1, #4096
    ldr r1, [sp, #0x8]
    strb r1, [r2, #0x920]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02236d98
    dcd 0x02236d98
}
