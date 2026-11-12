/* ov000 row 0x0220d9f4: 260 bytes.
 *
 * What it does: 65 instructions; 4 call(s) to 0x0220ce54, 0x02209c68, 0x02042c0c, +1 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x24
 *   branch +0x2c -> +0x90
 *   branch +0x3c -> +0x7c
 *   branch +0x78 -> +0x90
 *   branch +0x98 -> +0xfc
 *   branch +0xb4 -> +0xdc
 *   test +0x10 cmp r1, #0
 *   test +0x28 cmp r0, #10
 *   test +0x94 cmp r0, #20
 *   test +0xb0 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220d9f4; the literal pool and
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

extern void native_fn_0220ce54(void);
extern void native_fn_02209c68(void);
extern void native_fn_02042c0c(void);
extern void native_fn_0221089c(void);


asm u32 native_ov000_0220d9f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r1, [r5, #0x279]
    mov r4, #0
    cmp r1, #0
    bne ov000_0220d9f4_L24
    bl native_fn_0220ce54
    mov r0, #10
    strb r0, [r5, #0x279]
ov000_0220d9f4_L24:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne ov000_0220d9f4_L90
    ldrb r0, [r5, #0x2c2]
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    beq ov000_0220d9f4_L7c
    ldr r2, [r5, #0x2a8]
    ldr r1, [r5, #0x70]
    ldr r0, [r5, #0x2b8]
    sub r1, r2, r1
    smull r3, r2, r1, r1
    ldr lr, [r5, #0x2b0]
    ldr r12, [r5, #0x78]
    mov r1, r0, asr #31
    sub r12, lr, r12
    smlal r3, r2, r12, r12
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    subs r0, r3, r0
    rscs r0, r1, r2, asr #12
    bge ov000_0220d9f4_L90
ov000_0220d9f4_L7c:
    add r0, r5, #512
    mov r1, #31
    strh r1, [r0, #122]
    mov r0, #20
    strb r0, [r5, #0x279]
ov000_0220d9f4_L90:
    ldrb r0, [r5, #0x279]
    cmp r0, #20
    bne ov000_0220d9f4_Lfc
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    bgt ov000_0220d9f4_Ldc
    mov r0, r5
    mov r1, #10
    bl native_fn_02209c68
    mov r0, #0
    strb r0, [r5, #0x1e2]
    add r0, r5, #512
    mov r1, #31
    strh r1, [r0, #122]
    mov r4, #1
ov000_0220d9f4_Ldc:
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    mov r0, r5
    and r1, r1, #255
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #0
    bl native_fn_0221089c
ov000_0220d9f4_Lfc:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
