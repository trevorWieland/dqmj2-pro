/* ov006 row 0x021fcb50: 192 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (2 loads, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xac -> native_data2_0221c10c (image word 0x0221c10c)
 *   pool +0xb0 -> native_fn_021f57f4+1 (image word 0x021f57f5)
 *   pool +0xb4 -> native_data_0220b8b4 (image word 0x0220b8b4)
 *   pool +0xb8 -> native_fn_021fcfa0+1 (image word 0x021fcfa1)
 *   pool +0xbc -> native_fn_021fcc10+1 (image word 0x021fcc11)
 *   branch +0x08 -> +0x10
 *   branch +0x0c -> +0x3a
 *   branch +0x16 -> +0x1e
 *   branch +0x1a -> +0x2e
 *   branch +0x1c -> +0xa4
 *   branch +0x2c -> +0xa4
 *   branch +0x46 -> +0x92
 *   branch +0x52 -> +0x64
 *   branch +0x94 -> +0x9a
 *   test +0x06 cmp r0, #0x0
 *   test +0x0a cmp r0, #0x1
 *   test +0x14 cmp r0, #0x0
 *   test +0x18 cmp r0, #0x1
 *   test +0x44 cmp r0, #0x4
 *   test +0x50 cmp r0, #0xff
 *   test +0x92 cmp r0, #0x2
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fcb50; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 192 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void ov006_context_byte_16_021f2390(void);
extern void native_fn_021f5334(void);
extern void native_fn_021ff6d4(void);
extern u8 native_data2_0221c10c[];
extern void native_fn_021f23f4(void);
extern void native_fn_021f57f4(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021ff0bc(void);
extern void native_fn_021f23b8(void);
extern void native_fn_021f5328(void);
extern u8 native_data_0220b8b4[];
extern void native_fn_02200344(void);
extern void native_fn_021fcf44(void);
extern void native_fn_021fcfa0(void);
extern void native_fn_021ff0d0(void);
extern void native_fn_021fd0a4(void);
extern void native_fn_021fcc10(void);


asm u32 native_ov006_021fcb50 (register u32 a0)
{
    push {r3, r4, r5, lr}
    bl ov006_context_byte_16_021f2390
    cmp r0, #0x0
    beq ov006_021fcb50_L10
    cmp r0, #0x1
    beq ov006_021fcb50_L3a
    pop {r3, r4, r5, pc}
ov006_021fcb50_L10:
    bl native_fn_021f5334
    cmp r0, #0x0
    beq ov006_021fcb50_L1e
    cmp r0, #0x1
    beq ov006_021fcb50_L2e
    b ov006_021fcb50_La4
ov006_021fcb50_L1e:
    mov r0, #0x7
    bl native_fn_021ff6d4
    ldr r0, =native_data2_0221c10c
    mov r1, #0x2
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x1d]
    b ov006_021fcb50_La4
ov006_021fcb50_L2e:
    bl native_fn_021f23f4
    ldr r0, =native_fn_021f57f4+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, r4, r5, pc}
ov006_021fcb50_L3a:
    ldr r0, =native_data2_0221c10c
    mov r2, #0x1
    ldr r1, [r0, #0x4]
    strb r2, [r1, #0x1d]
    ldrb r0, [r0, #0]
    cmp r0, #0x4
    blo ov006_021fcb50_L92
    sub r5, r0, #0x4
    add r0, r5, #0x0
    bl native_fn_021ff0bc
    cmp r0, #0xff
    bne ov006_021fcb50_L64
    mov r0, #0x9
    bl native_fn_021ff6d4
    mov r0, #0x0
    mvn r0, r0
    bl native_fn_021f23b8
    pop {r3, r4, r5, pc}
ov006_021fcb50_L64:
    mov r0, #0x6
    bl native_fn_021ff6d4
    bl native_fn_021f5328
    add r4, r0, #0x0
    ldr r3, =native_data_0220b8b4
    add r0, r5, #0x1
    str r0, [sp]
    ldrsb r3, [r3, r4]
    mov r0, #0x46
    mov r1, #0x0
    mov r2, #0x1
    bl native_fn_02200344
    bl native_fn_021fcf44
    bl native_fn_021f23f4
    ldr r0, =native_fn_021fcfa0+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, r4, r5, pc}
ov006_021fcb50_L92:
    cmp r0, #0x2
    bhi ov006_021fcb50_L9a
    bl native_fn_021ff0d0
ov006_021fcb50_L9a:
    mov r0, #0x6
    bl native_fn_021ff6d4
    bl native_fn_021fd0a4
ov006_021fcb50_La4:
    ldr r0, =native_fn_021fcc10+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, r4, r5, pc}
}
