/* ov006 row 0x021f0554: 56 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x30 -> constant 0x0221aad0 (image word 0x0221aad0)
 *   pool +0x34 -> native_data_0220d480 (image word 0x0220d480)
 *   branch +0x12 -> +0x1a
 *   branch +0x18 -> +0x1e
 *   test +0x10 cmp r4, #0x1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f0554; the literal pool and
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

extern void native_fn_021f0170(void);
extern void native_fn_021ef334(void);
extern u8 native_data_0220d480[];
extern void native_fn_021f2170(void);


asm u32 native_ov006_021f0554 (register u32 a0)
{
    push {r4, lr}
    bl native_fn_021f0170
    add r4, r0, #0x0
    ldr r0, =0x0221aad0
    str r4, [r0, #0x78]
    bl native_fn_021ef334
    cmp r4, #0x1
    bne ov006_021f0554_L1a
    mov r1, #0x6
    ldr r0, =0x0221aad0
    b ov006_021f0554_L1e
ov006_021f0554_L1a:
    ldr r0, =0x0221aad0
    mov r1, #0x7
ov006_021f0554_L1e:
    str r1, [r0, #0x38]
    mov r1, #0x0
    ldr r0, =native_data_0220d480
    mvn r1, r1
    str r1, [r0, #0xc]
    bl native_fn_021f2170
    pop {r4, pc}
    mov r8, r8
}
