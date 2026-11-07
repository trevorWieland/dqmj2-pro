#include "matrix_20261106.h"

_Static_assert(sizeof(J2pMatrixOwner) == 24 && sizeof(J2pMatrixSeed) == 284 &&
    sizeof(J2pMatrixCommand) == 96 && sizeof(J2pMatrixState) == 4384, "Owned fixed-width matrix layout");

static int owner_valid(const J2pMatrixOwner *p) {
    return p->scope.program == 0 && p->scope.processor == 9 && p->scope.module == 1 &&
        p->scope.generation != 0 && p->model_set != 0;
}

static int owner_equal(const J2pMatrixOwner *a, const J2pMatrixOwner *b) {
    return a->scope.program == b->scope.program && a->scope.processor == b->scope.processor &&
        a->scope.module == b->scope.module && a->scope.generation == b->scope.generation &&
        a->model_set == b->model_set && a->model_index == b->model_index;
}

static int overlap(const void *a_ptr, uint32_t a_size, const void *b_ptr, uint32_t b_size) {
    uintptr_t a = (uintptr_t)a_ptr, b = (uintptr_t)b_ptr;
    return a_size > UINTPTR_MAX - a || b_size > UINTPTR_MAX - b || (a < b + b_size && b < a + a_size);
}

static void identity(int32_t out[16]) {
    uint32_t i;
    for (i = 0; i != 16; ++i) out[i] = i % 5 ? 0 : 4096;
}

static void copy_matrix(int32_t out[16], const int32_t in[16]) {
    uint32_t i;
    for (i = 0; i != 16; ++i) out[i] = in[i];
}

static int narrow(int64_t value, int32_t *out) {
    if (value < INT32_MIN || value > INT32_MAX) return 0;
    *out = (int32_t)value;
    return 1;
}

static int dot(const int32_t *a, uint32_t a_stride, const int32_t *b, uint32_t b_stride,
               uint32_t count, int32_t *out) {
    uint32_t i;
    uint64_t magnitude_sum = 0;
    int64_t total = 0, shifted;
    for (i = 0; i != count; ++i) {
        int64_t product = (int64_t)a[i * a_stride] * b[i * b_stride];
        uint64_t magnitude = product < 0 ? (uint64_t)(-product) : (uint64_t)product;
        if (magnitude > (uint64_t)INT64_MAX - magnitude_sum) return 0;
        magnitude_sum += magnitude;
        total += product;
    }
    shifted = total / 4096;
    if (total < 0 && total % 4096) --shifted;
    return narrow(shifted, out);
}

static int transform(int32_t out[16], const int32_t current[16], uint32_t opcode, const int32_t args[16]) {
    int32_t incoming[16];
    uint32_t row, col;
    if (opcode == 0x15) { identity(out); return 1; }
    if (opcode == 0x16) { copy_matrix(out, args); return 1; }
    if (opcode == 0x1b) {
        copy_matrix(out, current);
        for (row = 0; row != 3; ++row) for (col = 0; col != 4; ++col)
            if (!dot(args + row, 1, current + row * 4 + col, 1, 1, out + row * 4 + col)) return 0;
        return 1;
    }
    if (opcode == 0x1c) {
        copy_matrix(out, current);
        for (col = 0; col != 4; ++col) {
            int32_t shifted;
            if (!dot(args, 1, current + col, 4, 3, &shifted) ||
                !narrow((int64_t)current[12 + col] + shifted, out + 12 + col)) return 0;
        }
        return 1;
    }
    identity(incoming);
    if (opcode == 0x18) copy_matrix(incoming, args);
    else if (opcode == 0x17 || opcode == 0x19) {
        for (row = 0; row != 4; ++row) {
            for (col = 0; col != 3; ++col) incoming[row * 4 + col] = args[row * 3 + col];
            incoming[row * 4 + 3] = row == 3 ? 4096 : 0;
        }
        if (opcode == 0x17) { copy_matrix(out, incoming); return 1; }
    } else if (opcode == 0x1a) {
        for (row = 0; row != 3; ++row) for (col = 0; col != 3; ++col)
            incoming[row * 4 + col] = args[row * 3 + col];
    } else return 0;
    for (row = 0; row != 4; ++row) for (col = 0; col != 4; ++col)
        if (!dot(incoming + row * 4, 1, current + col, 4, 4, out + row * 4 + col)) return 0;
    return 1;
}

static uint32_t parameters(uint32_t opcode) {
    switch (opcode) {
    case 0x10: case 0x13: case 0x14: return 1;
    case 0x15: return 0;
    case 0x16: case 0x18: return 16;
    case 0x17: case 0x19: return 12;
    case 0x1a: return 9;
    case 0x1b: case 0x1c: return 3;
    default: return UINT32_MAX;
    }
}

static int execute(J2pMatrixState *state, const J2pMatrixCommand *command) {
    uint32_t opcode = command->opcode, i, targets[2], count = 1;
    int32_t result[16];
    if (parameters(opcode) == UINT32_MAX) return -2;
    if (command->count != parameters(opcode)) return -1;
    if (opcode == 0x10) {
        if (command->arguments[0] < 0 || command->arguments[0] > 3) return -2;
        state->mode = (uint32_t)command->arguments[0];
        return 1;
    }
    if (opcode == 0x13 || opcode == 0x14) {
        uint32_t slot = (uint32_t)command->arguments[0];
        if ((state->mode != 1 && state->mode != 2) || slot >= 31) return -2;
        if (opcode == 0x13) {
            copy_matrix(state->position_stack[slot], state->matrices[1]);
            copy_matrix(state->vector_stack[slot], state->matrices[2]);
            state->valid_slots |= 1U << slot;
        } else {
            if (!(state->valid_slots & (1U << slot))) return -3;
            copy_matrix(state->matrices[1], state->position_stack[slot]);
            copy_matrix(state->matrices[2], state->vector_stack[slot]);
        }
        return 1;
    }
    targets[0] = state->mode == 0 ? 0 : state->mode == 3 ? 3 : 1;
    if (state->mode == 2 && opcode != 0x1b) { targets[1] = 2; count = 2; }
    for (i = 0; i != count; ++i) {
        if (!transform(result, state->matrices[targets[i]], opcode, command->arguments)) return -4;
        copy_matrix(state->matrices[targets[i]], result);
    }
    return 1;
}

int j2p_matrix_init(const J2pMatrixOwner *current, const J2pMatrixSeed *seed, J2pMatrixState *output) {
    J2pMatrixState value = {0};
    uint32_t i;
    if (!current || !seed || !output || overlap(output, sizeof(*output), current, sizeof(*current)) ||
        overlap(output, sizeof(*output), seed, sizeof(*seed)) || !owner_valid(current) || !owner_equal(current, &seed->owner)) return -1;
    if (seed->mode > 3) return -2;
    value.owner = *current;
    value.mode = seed->mode;
    for (i = 0; i != 4; ++i) copy_matrix(value.matrices[i], seed->matrices[i]);
    *output = value;
    return 1;
}

int j2p_matrix_apply(const J2pMatrixOwner *current, J2pMatrixState *state, const J2pMatrixCommand *commands, uint32_t count) {
    J2pMatrixState next;
    uint32_t i;
    if (!current || !state || count > 10000 || (count && !commands) ||
        overlap(state, sizeof(*state), current, sizeof(*current)) ||
        (count && overlap(state, sizeof(*state), commands, count * (uint32_t)sizeof(*commands))) ||
        !owner_valid(current) || !owner_equal(current, &state->owner) || state->mode > 3 || (state->valid_slots & UINT32_C(0x80000000))) return -1;
    if (!count) return 1;
    next = *state;
    for (i = 0; i != count; ++i) {
        int status;
        if (!owner_equal(current, &commands[i].owner)) return -1;
        status = execute(&next, &commands[i]);
        if (status != 1) return status;
    }
    *state = next;
    return 1;
}
