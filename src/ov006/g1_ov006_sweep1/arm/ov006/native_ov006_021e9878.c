/* ov006 row 0x021e9878: 164 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x98 -> native_data_02208440 (image word 0x02208440)
 *   pool +0x9c -> native_data2_02219284 (image word 0x02219284)
 *   pool +0xa0 -> native_data_022083de (image word 0x022083de)
 *   branch +0x1c -> +0x90
 *   branch +0x24 -> +0x90
 *   branch +0x44 -> +0x90
 *   branch +0x4c -> +0x78
 *   branch +0x58 -> +0x88
 *   branch +0x74 -> +0x88
 *   test +0x20 cmp r5, #0
 *   test +0x34 cmp r5, r0
 *   test +0x40 cmpne r5, r0
 *   test +0x48 cmp r5, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9878; the literal pool and
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

extern u8 native_data_02208440[];
extern void native_fn_021e8fc0(void);
extern void native_fn_021e8000(void);
extern u8 native_data2_02219284[];
extern void native_fn_021e5750(void);
extern u8 native_data_022083de[];
extern void native_fn_021e9dc8(void);
extern void native_fn_021eb9a4(void);


asm u32 native_ov006_021e9878 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r1, =native_data_02208440
    mov r2, r5
    mov r0, #5
    bl native_fn_021e8fc0
    movs r4, r0
    bne ov006_021e9878_L90
    cmp r5, #0
    beq ov006_021e9878_L90
    bl native_fn_021e8000
    mov r5, r0
    mvn r0, #0
    cmp r5, r0
    ldrne r0, =native_data2_02219284
    ldrne r0, [r0]
    cmpne r5, r0
    beq ov006_021e9878_L90
    cmp r5, #3
    bne ov006_021e9878_L78
    bl native_fn_021e5750
    movs r1, r0
    beq ov006_021e9878_L88
    ldr r0, =native_data_022083de
    bl native_fn_021e9dc8
    mov r0, #4
    mov r1, #1
    mov r2, #0
    bl native_fn_021eb9a4
    b ov006_021e9878_L88
ov006_021e9878_L78:
    mov r1, #0
    mov r2, r1
    mov r0, #5
    bl native_fn_021eb9a4
ov006_021e9878_L88:
    ldr r0, =native_data2_02219284
    str r5, [r0]
ov006_021e9878_L90:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
