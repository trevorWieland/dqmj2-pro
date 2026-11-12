/* ov006 row 0x021e6114: 100 bytes.
 *
 * What it does: 23 instructions; 6 call(s) to 0x021e6954, 0x021e3f28, 0x021e57d0, +3 more; loops (back edge at +0x24); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> native_data_0220d108 (image word 0x0220d108)
 *   pool +0x60 -> constant 0x02218d70 (image word 0x02218d70)
 *   branch +0x0c -> +0x54
 *   branch +0x1c -> +0x2c
 *   branch +0x28 -> +0x54
 *   branch +0x3c -> +0x4c
 *   branch +0x48 -> +0x54
 *   test +0x08 cmp r0, #0
 *   test +0x18 cmp r0, #0
 *   test +0x38 cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e6114; the literal pool and
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

extern void native_fn_021e6954(void);
extern u8 native_data_0220d108[];
extern void native_fn_021e3f28(void);
extern void native_fn_021e57d0(void);
extern void native_fn_021e3cd8(void);


asm u32 native_ov006_021e6114 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021e6954
    cmp r0, #0
    beq ov006_021e6114_L54
    ldr r0, =native_data_0220d108
    ldr r0, [r0]
    cmp r0, #0
    bge ov006_021e6114_L2c
    mov r0, #102
    bl native_fn_021e3f28
    b ov006_021e6114_L54
ov006_021e6114_L2c:
    bl native_fn_021e57d0
    ldr r1, =0x02218d70
    ldr r1, [r1]
    cmp r1, r0
    bne ov006_021e6114_L4c
    mov r0, #100
    bl native_fn_021e3f28
    b ov006_021e6114_L54
ov006_021e6114_L4c:
    mov r0, #103
    bl native_fn_021e3f28
ov006_021e6114_L54:
    bl native_fn_021e3cd8
    ldmia sp!, {r3, pc}
}
