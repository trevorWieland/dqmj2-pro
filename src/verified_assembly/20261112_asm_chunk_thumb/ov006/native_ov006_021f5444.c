/* ov006 row 0x021f5444: 164 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (3 loads, 5 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x88 -> constant 0x0001e2a4 (image word 0x0001e2a4)
 *   pool +0x8c -> native_data3_0221c090 (image word 0x0221c090)
 *   pool +0x90 -> constant 0x0001e298 (image word 0x0001e298)
 *   pool +0x94 -> native_data_0220d9d8 (image word 0x0220d9d8)
 *   pool +0x98 -> native_data2_0221c098 (image word 0x0221c098)
 *   pool +0x9c -> native_fn_021f5568+1 (image word 0x021f5569)
 *   pool +0xa0 -> constant 0x0001e29c (image word 0x0001e29c)
 *   branch +0x6a -> +0x70
 *   test +0x68 cmp r0, #0x0
 *   6 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5444; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 164 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02203c08(void);
extern u8 native_data3_0221c090[];
extern u8 native_data_0220d9d8[];
extern u8 native_data2_0221c098[];
extern void native_fn_021f5418(void);
extern void native_fn_021f5368(void);
extern void native_fn_02201df4(void);
extern void native_fn_02201fbc(void);
extern void native_fn_02008430(void);
extern void native_fn_021f5568(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f5444 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x1c
    add r4, r0, #0x0
    ldr r0, =0x0001e2a4
    mov r1, #0x20
    bl native_fn_02203c08
    ldr r3, =native_data3_0221c090
    ldr r1, =0x0001e298
    str r0, [r3, #0]
    str r4, [r0, r1]
    add r0, r1, #0x0
    ldr r4, [r3, #0]
    mov r2, #0x0
    add r0, #0x8
    strb r2, [r4, r0]
    ldr r0, [r3, #0]
    add r1, #0x9
    ldr r4, =native_data_0220d9d8
    strb r2, [r0, r1]
    ldmia r4!, {r0, r1}
    add r3, sp, #0x0
    stmia r3!, {r0, r1}
    ldmia r4!, {r0, r1}
    stmia r3!, {r0, r1}
    ldmia r4!, {r0, r1}
    stmia r3!, {r0, r1}
    ldr r0, [r4, #0]
    add r1, r2, #0x0
    str r0, [r3, #0]
    ldr r0, =native_data2_0221c098
    ldr r0, [r0, #0]
    bl native_fn_021f5418
    str r0, [sp, #0x4]
    ldr r0, =native_data2_0221c098
    mov r1, #0x1
    ldr r0, [r0, #0]
    bl native_fn_021f5418
    str r0, [sp, #0x8]
    bl native_fn_021f5368
    add r1, sp, #0x0
    strb r0, [r1, #0x18]
    ldr r0, =native_data3_0221c090
    add r1, sp, #0x0
    ldr r0, [r0, #0]
    bl native_fn_02201df4
    bl native_fn_02201fbc
    cmp r0, #0x0
    bne ov006_021f5444_L70
    blx native_fn_02008430
ov006_021f5444_L70:
    mov r0, #0x0
    ldr r1, =native_fn_021f5568+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data3_0221c090
    ldr r2, [r1, #0]
    ldr r1, =0x0001e29c
    str r0, [r2, r1]
    add sp, #0x1c
    pop {r3, r4, pc}
}
