/* ov006 row 0x021f6808: 112 bytes.
 *
 * What it does: 44 instructions; 8 call(s) to 0x021f2390, 0x021ff6d4, 0x020a4660, +5 more; loops (back edge at +0x04); returns through pop {pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x68 -> constant 0x0221c0a8 (image word 0x0221c0a8)
 *   pool +0x6c -> native_fn_021f6878+1 (image word 0x021f6879)
 *   branch +0x0a -> +0x14
 *   branch +0x0e -> +0x1c
 *   branch +0x1a -> +0x5c
 *   branch +0x28 -> +0x4c
 *   branch +0x38 -> +0x4c
 *   test +0x08 cmp r0, #0x0
 *   test +0x0c cmp r0, #0x1
 *   test +0x26 cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f6808; the literal pool and
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

extern void native_fn_021f2390(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_020a4660(void);
extern void native_fn_021f23b8(void);
extern void native_fn_021f69e0(void);
extern void native_fn_021f6878(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f6808 (register u32 a0)
{
    push {lr}
    sub sp, #0x14
    bl native_fn_021f2390
    cmp r0, #0x0
    beq ov006_021f6808_L14
    cmp r0, #0x1
    beq ov006_021f6808_L1c
    add sp, #0x14
    pop {pc}
ov006_021f6808_L14:
    mov r0, #0x7
    bl native_fn_021ff6d4
    b ov006_021f6808_L5c
ov006_021f6808_L1c:
    add r0, sp, #0x0
    bl native_fn_020a4660
    ldr r0, =0x0221c0a8
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f6808_L4c
    ldr r3, [sp]
    mov r0, #0x0
    ldr r2, [sp, #0x4]
    mov r1, #0x0
    eor r1, r2
    eor r0, r3
    orr r0, r1
    bne ov006_021f6808_L4c
    mov r0, #0x9
    bl native_fn_021ff6d4
    mov r0, #0x0
    mvn r0, r0
    bl native_fn_021f23b8
    add sp, #0x14
    pop {pc}
ov006_021f6808_L4c:
    mov r0, #0x6
    bl native_fn_021ff6d4
    bl native_fn_021f69e0
    ldr r0, =0x0221c0a8
    mov r1, #0x1
    strb r1, [r0, #0x1]
ov006_021f6808_L5c:
    ldr r0, =native_fn_021f6878+1
    bl native_fn_021f52cc
    add sp, #0x14
    pop {pc}
    mov r8, r8
}
