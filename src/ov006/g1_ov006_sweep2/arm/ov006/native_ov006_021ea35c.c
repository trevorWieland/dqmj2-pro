/* ov006 row 0x021ea35c: 120 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x0221928c (image word 0x0221928c)
 *   pool +0x74 -> native_data_02208558 (image word 0x02208558)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ea35c; the literal pool and
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

extern void native_fn_02067af4(void);
extern void native_fn_021ea2d0(void);
extern void native_fn_021ea2ac(void);
extern void native_fn_021e7f08(void);
extern void native_fn_021e7ed8(void);
extern u8 native_data_02208558[];
extern void native_fn_021e767c(void);
extern void native_fn_021e7b64(void);


asm u32 native_ov006_021ea35c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r4, r0
    bl native_fn_02067af4
    mov r6, r0
    mov r0, r4
    bl native_fn_021ea2d0
    mov r5, r0
    mov r0, r6
    bl native_fn_021ea2ac
    ldr r2, =0x0221928c
    add r1, r5, r5, lsl #2
    add r5, r0, r1
    ldrb r6, [r2, r4]
    add r2, r5, #10
    mov r0, #7
    mov r1, #9
    bl native_fn_021e7f08
    add r2, r5, #10
    add r0, r6, #7
    mov r1, #9
    bl native_fn_021e7ed8
    add r0, r4, #44
    ldr r1, =native_data_02208558
    add r1, r1, r6, lsl #2
    bl native_fn_021e767c
    add r0, r4, #44
    bl native_fn_021e7b64
    ldmia sp!, {r4, r5, r6, pc}
}
