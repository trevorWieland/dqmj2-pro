/* ov000 row 0x021e1fa0: 188 bytes.
 *
 * What it does: 45 instructions; 5 call(s) to 0x021d8528, 0x021e0ba4, 0x021d8528, +2 more; loops (back edge at +0x30); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb4 -> constant 0x022322c4 (image word 0x022322c4)
 *   pool +0xb8 -> constant 0x022322d4 (image word 0x022322d4)
 *   branch +0x28 -> +0x54
 *   branch +0x38 -> +0x4c
 *   branch +0x58 -> +0x80
 *   branch +0x68 -> +0x78
 *   test +0x24 cmp r2, #256
 *   test +0x34 cmp r4, #0
 *   test +0x54 cmp r2, #512
 *   test +0x64 cmp r4, #0
 *   test +0x80 cmp r2, #768
 *   test +0x8c tst r2, #768
 *   test +0x90 cmpne r1, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1fa0; the literal pool and
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

extern void native_fn_021d8528(void);
extern void native_fn_021e0ba4(void);
extern void native_fn_021d84e8(void);


asm u32 native_ov000_021e1fa0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r2, =0x022322c4
    mov r4, r0
    ldr r3, [r2, #0x4]
    mov r0, #0
    ldrh r2, [r3]
    and r2, r2, #768
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    cmp r2, #256
    bne ov000_021e1fa0_L54
    sub r0, r0, #16384
    bl native_fn_021d8528
    cmp r4, #0
    beq ov000_021e1fa0_L4c
    mov r0, #16384
    rsb r0, r0, #0
    mov r1, #0
    bl native_fn_021e0ba4
ov000_021e1fa0_L4c:
    mov r0, #1
    ldmia sp!, {r4, pc}
ov000_021e1fa0_L54:
    cmp r2, #512
    bne ov000_021e1fa0_L80
    mov r0, #16384
    bl native_fn_021d8528
    cmp r4, #0
    beq ov000_021e1fa0_L78
    mov r0, #16384
    mov r1, #0
    bl native_fn_021e0ba4
ov000_021e1fa0_L78:
    mov r0, #2
    ldmia sp!, {r4, pc}
ov000_021e1fa0_L80:
    cmp r2, #768
    ldmneia sp!, {r4, pc}
    ldrh r2, [r3, #2]
    tst r2, #768
    cmpne r1, #0
    ldmeqia sp!, {r4, pc}
    ldr r2, =0x022322d4
    mov r1, r0
    ldr r0, [r2, #0x8c]
    add r0, r0, #737280
    bl native_fn_021d84e8
    mov r0, #1
    ldmia sp!, {r4, pc}
}
