// -----
// cuda: grid -> block -> thread, __shared__
// cl:   kernel -> work_group -> work_item, __local
// -----
// size_t tid = get_local_id(0);
// size_t tid = threadIdx.x;
// -----
// size_t gid = get_global_id(0);
// size_t gid = blockIdx.x * blockDim.x + threadIdx.x;
// -----
// size_t window = get_local_size(0);
// size_t window = blockDim.x;
// -----
// size_t stride = get_global_size(0);
// size_t stride = gridDim.x * blockDim.x;
// -----

kernel void vectorAdd(global float *A) {
    int gid = get_global_id(0);
    A[gid] = A[gid] + 1.0;
}
