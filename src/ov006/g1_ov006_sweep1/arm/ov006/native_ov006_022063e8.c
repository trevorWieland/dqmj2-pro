/* ov006 row 0x022063e8: 180 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa4 -> native_data4_0221c398 (image word 0x0221c398)
 *   pool +0xa8 -> native_data_0220bc04 (image word 0x0220bc04)
 *   pool +0xac -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0xb0 -> native_data_0220e950 (image word 0x0220e950)
 *   2 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022063e8; the literal pool and
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

extern u8 native_data4_0221c398[];
extern void native_fn_02008d78(void);
extern u8 native_data_0220bc04[];
extern void native_fn_021e6530(void);
extern void native_fn_02046af4(void);
extern void native_fn_020629e0(void);
extern u8 native_data_0220e950[];
extern void native_fn_020211c0(void);
extern void native_fn_02021294(void);
extern void native_fn_021e75ec(void);
extern void native_fn_021e7b8c(void);
extern void native_fn_021e775c(void);


asm u32 native_ov006_022063e8 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #76
    ldr r0, =native_data4_0221c398
    mov r1, #0
    mov r2, #128
    bl native_fn_02008d78
    ldr r0, =native_data_0220bc04
    bl native_fn_021e6530
    ldr r2, =native_data4_0221c398
    mov r1, r0
    str r2, [sp]
    mov r12, #255
    ldr r0, =0x021c9698
    mov r2, #32
    mov r3, #16
    str r12, [sp, #0x4]
    bl native_fn_02046af4
    bl native_fn_020629e0
    rsb r3, r0, #100
    ldr r2, =native_data_0220e950
    add r0, sp, #12
    mov r1, #32
    bl native_fn_020211c0
    ldr r0, =native_data4_0221c398
    add r1, sp, #12
    bl native_fn_02021294
    mov r0, #2
    bl native_fn_021e75ec
    mov r0, #2
    bl native_fn_021e7b8c
    mov r0, #30
    str r0, [sp]
    mov r2, #1
    ldr r1, =native_data4_0221c398
    str r2, [sp, #0x4]
    mov r3, #0
    mov r0, #2
    str r3, [sp, #0x8]
    bl native_fn_021e775c
    add sp, sp, #76
    ldmia sp!, {pc}
}
