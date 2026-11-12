/* ov006 row 0x021edce4: 112 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02219b4c (image word 0x02219b4c)
 *   pool +0x64 -> constant 0x5d588b65 (image word 0x5d588b65)
 *   pool +0x68 -> constant 0x00269ec3 (image word 0x00269ec3)
 *   pool +0x6c -> constant 0x00007fff (image word 0x00007fff)
 *   branch +0x0a -> +0x42
 *   branch +0x20 -> +0x32
 *   test +0x08 cmp r0, #0x0
 *   test +0x1e cmp r0, #0x0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021edce4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021edbac(void);
extern void native_fn_0200f48c(void);


asm u32 native_ov006_021edce4 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0xc
    ldr r0, =0x02219b4c
    ldr r0, [r0, #0x8]
    cmp r0, #0x0
    bne ov006_021edce4_L42
    mov r4, #0x0
    add r0, sp, #0x0
    add r1, r4, #0x0
    mov r2, #0xc
    bl native_fn_021edbac
    add r0, sp, #0x0
    blx native_fn_0200f48c
    cmp r0, #0x0
    bne ov006_021edce4_L32
    ldr r0, [sp]
    lsl r0, r0, #0xa
    add r1, r4, r0
    ldr r0, [sp, #0x4]
    lsl r0, r0, #0x3
    add r1, r1, r0
    ldr r0, [sp, #0x8]
    add r4, r1, r0
ov006_021edce4_L32:
    ldr r0, =0x02219b4c
    ldr r1, =0x5d588b65
    str r4, [r0, #0x18]
    str r1, [r0, #0x1c]
    ldr r1, =0x00269ec3
    str r1, [r0, #0x20]
    mov r1, #0x1
    str r1, [r0, #0x8]
ov006_021edce4_L42:
    ldr r0, =0x02219b4c
    ldr r2, [r0, #0x1c]
    ldr r1, [r0, #0x18]
    ldr r3, [r0, #0x20]
    mul r1, r2
    add r1, r3, r1
    str r1, [r0, #0x18]
    ldr r0, =0x00007fff
    lsr r1, r1, #0x10
    mul r0, r1
    lsr r0, r0, #0x10
    lsl r0, r0, #0x10
    lsr r0, r0, #0x10
    add sp, #0xc
    pop {r3, r4, pc}
}
