/* ov000 row 0x02211e08: 256 bytes.
 *
 * What it does: 61 instructions; 7 call(s) to 0x021d8a50, 0x0202859c, 0x02211ee4, +4 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf4 -> constant 0x0224157c (image word 0x0224157c)
 *   pool +0xf8 -> constant 0x02240ddc (image word 0x02240ddc)
 *   pool +0xfc -> constant 0x057e4000 (image word 0x057e4000)
 *   branch +0x10 -> +0x1c
 *   branch +0x18 -> +0x24
 *   branch +0x48 -> +0xdc
 *   branch +0x5c -> +0xdc
 *   branch +0xa0 -> +0xdc
 *   branch +0xc0 -> +0xd8
 *   back edge +0xe8 -> +0x40
 *   test +0x08 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x58 cmpne r0, #0
 *   test +0xbc cmp r0, r4
 *   test +0xe0 cmp r7, #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02211e08; the literal pool and
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

extern void native_fn_021d8a50(void);
extern void native_fn_0202859c(void);
extern void native_fn_0203caa4(void);
extern void native_fn_022115cc(void);
extern void native_fn_0203cac8(void);


asm u32 native_ov000_02211e08 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r8, #0
    cmp r0, #0
    mov r0, r8
    bne ov000_02211e08_L1c
    bl native_fn_021d8a50
    b ov000_02211e08_L24
ov000_02211e08_L1c:
    mov r1, r8
    bl native_fn_0202859c
ov000_02211e08_L24:
    mov r7, #0
    ldr r9, =0x0224157c
    ldr r6, =0x02240ddc
    ldr r11, =0x057e4000
    mov r10, r0
    mvn r4, #0
    mov r5, r7
ov000_02211e08_L40:
    ldrsh r0, [r9]
    cmp r0, #0
    ble ov000_02211e08_Ldc
    ldrb r0, [r9, #0xa]
    cmp r0, #0
    ldrneb r0, [r9, #0x9]
    cmpne r0, #0
    beq ov000_02211e08_Ldc
    ldr r1, [r10, #0x4]
    ldr r0, [r9, #0x88]
    ldr r12, [r10]
    sub r2, r1, r0
    smull r0, r1, r2, r2
    ldr r2, [r9, #0x84]
    ldr r3, [r10, #0x8]
    sub r2, r12, r2
    smlal r0, r1, r2, r2
    ldr r2, [r9, #0x8c]
    sub r2, r3, r2
    smlal r0, r1, r2, r2
    mov r0, r0, lsr #12
    orr r0, r0, r1, lsl #20
    subs r0, r0, r11
    rscs r0, r5, r1, asr #12
    bge ov000_02211e08_Ldc
    mov r1, #1
    add r0, r9, #20
    bl native_fn_0203caa4
    ldrsh r0, [r9]
    ldrsh r1, [r9, #2]
    bl native_fn_022115cc
    cmp r0, r4
    beq ov000_02211e08_Ld8
    mov r1, #96
    mla r2, r0, r1, r6
    mov r1, #1
    add r0, r2, #4
    bl native_fn_0203cac8
ov000_02211e08_Ld8:
    add r8, r8, #1
ov000_02211e08_Ldc:
    add r7, r7, #1
    cmp r7, #24
    add r9, r9, #360
    blt ov000_02211e08_L40
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
