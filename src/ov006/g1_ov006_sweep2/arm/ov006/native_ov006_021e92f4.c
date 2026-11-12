/* ov006 row 0x021e92f4: 116 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x6c -> native_data_02207dc8 (image word 0x02207dc8)
 *   pool +0x70 -> native_data_02207dd8 (image word 0x02207dd8)
 *   branch +0x1c -> +0x2c
 *   test +0x10 cmp r5, #4
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e92f4; the literal pool and
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

extern void native_fn_021e92b4(void);
extern u8 native_data_02207dc8[];
extern void native_fn_021e92bc(void);
extern void native_fn_021e7b8c(void);
extern void native_fn_021e7a40(void);
extern u8 native_data_02207dd8[];
extern void native_fn_021e791c(void);


asm u32 native_ov006_021e92f4 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r5, r0
    bl native_fn_021e92b4
    cmp r5, #4
    mov r4, r0
    ldrhs r5, =native_data_02207dc8
    bhs ov006_021e92f4_L2c
    mov r0, r5
    bl native_fn_021e92bc
    mov r5, r0
ov006_021e92f4_L2c:
    mov r0, r4
    bl native_fn_021e7b8c
    mov r1, r5
    mov r0, #0
    bl native_fn_021e7a40
    mov r3, #0
    str r3, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldr r1, =native_data_02207dd8
    mov r0, r4
    mov r2, #2
    str r3, [sp, #0x8]
    bl native_fn_021e791c
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
