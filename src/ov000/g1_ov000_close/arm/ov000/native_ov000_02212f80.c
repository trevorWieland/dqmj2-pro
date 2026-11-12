/* ov000 row 0x02212f80: 336 bytes.
 *
 * What it does: 84 instructions; 9 call(s) to 0x02212804, 0x0204106c, 0x02212e84, +6 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x18 -> +0x144
 *   branch +0x6c -> +0x144
 *   branch +0x80 -> +0xa0
 *   branch +0xb0 -> +0xcc
 *   branch +0xdc -> +0xf8
 *   branch +0x10c -> +0x120
 *   test +0x14 cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xd8 cmp r0, #0
 *   test +0x108 cmp r0, #0
 *   12 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02212f80; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02212804(void);
extern void native_fn_0204106c(void);
extern void native_fn_02212e84(void);
extern void native_fn_02041268(void);
extern void native_fn_02212ec0(void);
extern void native_fn_02041474(void);
extern void native_fn_02212efc(void);
extern void native_fn_02041448(void);
extern void native_fn_021db15c(void);


asm u32 native_ov000_02212f80 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #36
    mov r5, r0
    ldrb r0, [r5, #0x105]
    mov r4, #0
    cmp r0, #0
    beq ov000_02212f80_L144
    add r0, r5, #112
    ldmia r0, {r0, r1, r2}
    add lr, sp, #24
    add r3, sp, #12
    add r12, r5, #136
    stmia lr, {r0, r1, r2}
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, r5, #124
    add r3, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldrb r0, [r5, #0x106]
    bl native_fn_02212804
    mov r6, r0
    mov r0, r5
    add r1, r6, #4
    mov r2, r4
    bl native_fn_0204106c
    cmp r0, #0
    beq ov000_02212f80_L144
    mov r0, r6
    mov r1, r4
    bl native_fn_02212e84
    cmp r0, #0
    beq ov000_02212f80_La0
    mov r2, r4
    mov r0, r5
    mov r3, r2
    add r1, r6, #96
    bl native_fn_02041268
    ldr r0, [r6, #0x5c]
    strb r0, [r5, #0x102]
ov000_02212f80_La0:
    mov r0, r6
    mov r1, #0
    bl native_fn_02212ec0
    cmp r0, #0
    beq ov000_02212f80_Lcc
    mov r0, r5
    add r1, r6, #160
    mov r2, #0
    bl native_fn_02041474
    ldr r0, [r6, #0x9c]
    strb r0, [r5, #0x103]
ov000_02212f80_Lcc:
    mov r0, r6
    mov r1, #0
    bl native_fn_02212efc
    cmp r0, #0
    beq ov000_02212f80_Lf8
    mov r0, r5
    add r1, r6, #192
    mov r2, #0
    bl native_fn_02041448
    ldr r0, [r6, #0xbc]
    strb r0, [r5, #0x104]
ov000_02212f80_Lf8:
    add r0, sp, #24
    add r1, r5, #112
    mvn r2, #0
    bl native_fn_021db15c
    cmp r0, #0
    bne ov000_02212f80_L120
    add r0, sp, #24
    add r3, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_02212f80_L120:
    add r0, sp, #12
    add r3, r5, #136
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #0
    add r3, r5, #124
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r4, #1
ov000_02212f80_L144:
    mov r0, r4
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, pc}
}
