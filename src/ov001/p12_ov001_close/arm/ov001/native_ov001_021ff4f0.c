/* ov001 row 0x021ff4f0: 296 bytes.
 *
 * What it does: 71 instructions; 10 call(s) to 0x02202360, 0x021fd544, 0x022044c8, +7 more; loops (back edge at +0x68); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (71 instructions, 10 calls, 3 branches, 5 back edges, 3 literal slots).
 *
 *   pool +0x11c -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x120 -> native_data_0222e044 (image word 0x0222e044)
 *   pool +0x124 -> native_data_0222ed34 (image word 0x0222ed34)
 *   branch +0x38 -> +0x4c
 *   branch +0x48 -> +0xcc
 *   branch +0xe4 -> +0x100
 *   test +0x34 cmp r2, #0
 *   test +0x8c cmp r1, r0
 *   test +0xe0 cmp r0, #0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff4f0; the literal pool and
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

extern void native_fn_02202360(void);
extern u8 native_data_0222e044[];
extern void native_fn_021fd544(void);
extern u8 native_data_0222ed34[];
extern void native_fn_022044c8(void);
extern void native_fn_021fd7c4(void);
extern void native_fn_021fe2b8(void);
extern void native_fn_021fe3dc(void);
extern void native_fn_021fd858(void);
extern void native_fn_02204590(void);
extern void native_fn_0220451c(void);
extern void native_fn_022023c4(void);


asm u32 native_ov001_021ff4f0 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_02202360
    ldr r2, =native_data_0222e044
    ldr r1, =0x02239c10
    ldrh r3, [r2, #8]
    ldrh r12, [r2, #6]
    ldrb r2, [r1]
    mov r4, r0
    strh r12, [sp, #8]
    strh r3, [sp, #10]
    cmp r2, #0
    beq ov001_021ff4f0_L4c
    mov r0, #0
    strb r0, [r1]
    str r0, [r4]
    b ov001_021ff4f0_Lcc
ov001_021ff4f0_L4c:
    mov r12, #6
    mov r0, #1
    str r12, [sp]
    mov r1, r0
    mov r2, #9
    mov r3, #3
    str r12, [sp, #0x4]
    bl native_fn_021fd544
    ldr r0, =0x02239c10
    ldr r1, =native_data_0222ed34
    ldrsb r2, [r0, #12]
    mvn r0, #0
    mov r3, #72
    strb r2, [r4, #0x10]
    ldrsb r1, [r1, #1]
    add r2, sp, #8
    cmp r1, r0
    moveq r0, #0
    streq r0, [r4]
    ldr r0, =0x02239c10
    strne r1, [r4]
    ldrsb r1, [r0, #12]
    add r0, r4, #24
    bl native_fn_022044c8
    mov r0, #0
    mov r3, r0
    mov r1, #21
    mov r2, #10
    bl native_fn_021fd7c4
    mov r0, #2
    mov r1, #1
    bl native_fn_021fe2b8
ov001_021ff4f0_Lcc:
    mov r0, #1
    mov r1, #0
    bl native_fn_021fe3dc
    bl native_fn_021fd858
    ldr r0, [r4, #0x34]
    cmp r0, #0
    beq ov001_021ff4f0_L100
    add r0, r4, #24
    mov r1, #123
    bl native_fn_02204590
    ldr r1, [r4]
    add r0, r4, #24
    bl native_fn_0220451c
ov001_021ff4f0_L100:
    ldr r1, =native_data_0222ed34
    mov r2, #1
    mov r0, #143
    strb r2, [r1, #0x2]
    bl native_fn_022023c4
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
}
