// clang-format off
#include <array>
#include <iostream>
#include <memory>
#include <random>
#include <vector>
#include <chrono>
/*
#undef __CUDACC__
#undef __CUDACC_VER__
#undef __CUDA_ARCH__
#include <Eigen/Eigen>
*/
#include <cuda_runtime.h>
#include <utils/helper_cuda.h>
// clang-format on

namespace {
template <typename T> T *create2DArrayCPU(size_t n_rows, size_t n_cols) {
  T *ptr = new T[n_rows * n_cols];
  return ptr;
}

template <typename T> T *create2DArrayGPU(size_t n_rows, size_t n_cols) {
  T *ptr = nullptr;
  checkCudaErrors(cudaMalloc(ptr, sizeof(T) * n_rows * n_cols));
  return ptr;
}

} // namespace

template <typename T> class MatCPU {
public:
  MatCPU(size_t height, size_t width)
      : data_(height * width, T(0)), height_(height), width_(width) {}
  MatCPU(const std::vector<T> &data, size_t height, size_t width)
      : data_(data), height_(height), width_(width) {}
  MatCPU(std::vector<T> &&data, size_t height, size_t width)
      : data_(data), height_(height), width_(width) {}

  T &at(size_t y, size_t x) { return data_[y * width() + x]; }
  const T &at(size_t y, size_t x) const { return data_[y * width() + x]; }

  static MatCPU<float> randn(size_t n_rows, size_t n_cols) {
    size_t n = n_rows * n_cols;
    std::vector<float> data(n);
    std::default_random_engine generator;
    std::uniform_real_distribution<float> distribution(0.0, 1.0);
    for (size_t i = 0; i < n; i += 1) {
      data[i] = distribution(generator);
    }
    return MatCPU<float>(std::move(data), n_rows, n_cols);
  }

  friend MatCPU<T> operator*(const MatCPU<T> &A, const MatCPU<T> &B) {
    MatCPU<T> C(A.height(), B.width());
    for (size_t y = 0; y < C.height(); y += 1) {
      for (size_t x = 0; x < C.width(); x += 1) {
        assert(A.width() == B.height());
        for (size_t i = 0; i < A.width(); i += 1) {
          C.at(y, x) += A.at(y, i) * B.at(i, x);
        }
      }
    }
    return C;
  }

  size_t height() const { return height_; }
  size_t width() const { return width_; }

private:
  std::vector<T> data_;
  size_t height_, width_;
};

/*
void test_cpu_matmul() {
  MatCPU<float> A = MatCPU<float>::randn(1024, 512);
  MatCPU<float> B = MatCPU<float>::randn(512, 256);
  MatCPU<float> C = A * B;
  //
  Eigen::MatrixXf eA(1024, 512);
  for (size_t y = 0; y < A.height(); y += 1) {
    for (size_t x = 0; x < A.width(); x += 1) {
      eA(y, x) = A.at(y, x);
    }
  }
  Eigen::MatrixXf eB(512, 1024);
  for (size_t y = 0; y < B.height(); y += 1) {
    for (size_t x = 0; x < B.width(); x += 1) {
      eB(y, x) = B.at(y, x);
    }
  }
  Eigen::MatrixXf eC = eA * eB;
  //
  for (size_t y = 0; y < C.height(); y += 1) {
    for (size_t x = 0; x < C.width(); x += 1) {
      assert(eC(y, x) == C.at(y, x));
    }
  }
  std::cout << "[PASS] test_matmul()" << std::endl;
}
*/

namespace {
#define ERROR_ALLOW 1e-3
#define BLOCK_SIZE 32
#define GRID_SIZE 64
const dim3 threadsPerBlock(BLOCK_SIZE, BLOCK_SIZE, 1);
const dim3 blocksPerGrid(GRID_SIZE, GRID_SIZE, 1);
#define HANDLE_ERROR(x) checkCudaErrors(x)

/*********************************************/
/***************without cache*****************/
/*********************************************/
__global__ void matrixMul_kernel_1(const float *A, const float *B, float *C,
                                   uint32_t hA, uint32_t wA, uint32_t hB,
                                   uint32_t wB) {
  for (uint32_t y = blockIdx.y * blockDim.y + threadIdx.y; y < hA;
       y += gridDim.y * blockDim.y) {
    for (uint32_t x = blockIdx.x * blockDim.x + threadIdx.x; x < wB;
         x += gridDim.x * blockDim.x) {
      //
      uint32_t iC = y * wB + x;
      C[iC] = 0.0f;

      //
      for (uint32_t offset = 0; offset < wA; offset++) {
        uint32_t iA = y * wA + offset;
        uint32_t iB = offset * wB + x;
        C[iC] += A[iA] * B[iB];
      }
    }
  }
}

void matrixMul_gpu_1(const float *A, const float *B, float *C, uint32_t hA,
                     uint32_t wA, uint32_t hB, uint32_t wB) {
  uint32_t sizeA = hA * wA * sizeof(float);
  uint32_t sizeB = hB * wB * sizeof(float);
  uint32_t sizeC = hA * wB * sizeof(float);

  // allocate device memory
  float *dev_A = NULL, *dev_B = NULL, *dev_C = NULL;
  HANDLE_ERROR(cudaMalloc(&dev_A, sizeA));
  HANDLE_ERROR(cudaMalloc(&dev_B, sizeB));
  HANDLE_ERROR(cudaMalloc(&dev_C, sizeC));

  // copy from host to device
  HANDLE_ERROR(cudaMemcpy(dev_A, A, sizeA, cudaMemcpyHostToDevice));
  HANDLE_ERROR(cudaMemcpy(dev_B, B, sizeB, cudaMemcpyHostToDevice));

  // real timer
  clock_t before = clock();
  matrixMul_kernel_1<<<blocksPerGrid, threadsPerBlock>>>(dev_A, dev_B, dev_C,
                                                         hA, wA, hB, wB);
  HANDLE_ERROR(cudaGetLastError());
  HANDLE_ERROR(cudaDeviceSynchronize());
  printf("gpu duration: %ld\n", clock() - before);

  // copy from device to host
  HANDLE_ERROR(cudaMemcpy(C, dev_C, sizeC, cudaMemcpyDeviceToHost));

  // free memory
  HANDLE_ERROR(cudaFree(dev_A));
  HANDLE_ERROR(cudaFree(dev_B));
  HANDLE_ERROR(cudaFree(dev_C));
}

/*********************************************/
/*****************with cache******************/
/*********************************************/
__global__ void matrixMul_kernel_2(const float *A, const float *B, float *C,
                                   uint32_t hA, uint32_t wA, uint32_t hB,
                                   uint32_t wB) {
  for (uint32_t y = blockIdx.y * blockDim.y + threadIdx.y; y < hA;
       y += gridDim.y * blockDim.y) {
    for (uint32_t x = blockIdx.x * blockDim.x + threadIdx.x; x < wB;
         x += gridDim.x * blockDim.x) {

      //
      float value = 0.0f;
      for (uint32_t offset = 0; offset < wA; offset++) {
        uint32_t iA = y * wA + offset;
        uint32_t iB = offset * wB + x;
        value += A[iA] * B[iB];
      }
      uint32_t iC = y * wB + x;
      C[iC] = value;
    }
  }
}

void matrixMul_gpu_2(const float *A, const float *B, float *C, uint32_t hA,
                     uint32_t wA, uint32_t hB, uint32_t wB) {
  uint32_t sizeA = hA * wA * sizeof(float);
  uint32_t sizeB = hB * wB * sizeof(float);
  uint32_t sizeC = hA * wB * sizeof(float);

  // allocate device memory
  float *dev_A = NULL, *dev_B = NULL, *dev_C = NULL;
  HANDLE_ERROR(cudaMalloc(&dev_A, sizeA));
  HANDLE_ERROR(cudaMalloc(&dev_B, sizeB));
  HANDLE_ERROR(cudaMalloc(&dev_C, sizeC));

  // copy from host to device
  HANDLE_ERROR(cudaMemcpy(dev_A, A, sizeA, cudaMemcpyHostToDevice));
  HANDLE_ERROR(cudaMemcpy(dev_B, B, sizeB, cudaMemcpyHostToDevice));

  // real JIT
  clock_t before = clock();
  matrixMul_kernel_2<<<blocksPerGrid, threadsPerBlock>>>(dev_A, dev_B, dev_C,
                                                         hA, wA, hB, wB);
  HANDLE_ERROR(cudaGetLastError());
  HANDLE_ERROR(cudaDeviceSynchronize());
  printf("gpu duration: %ld\n", clock() - before);

  // copy from device to host
  HANDLE_ERROR(cudaMemcpy(C, dev_C, sizeC, cudaMemcpyDeviceToHost));

  // free memory
  HANDLE_ERROR(cudaFree(dev_A));
  HANDLE_ERROR(cudaFree(dev_B));
  HANDLE_ERROR(cudaFree(dev_C));
}

/*********************************************/
/****************with shared******************/
/*********************************************/
__global__ void matrixMul_kernel_3(const float *A, const float *B, float *C,
                                   uint32_t hA, uint32_t wA, uint32_t hB,
                                   uint32_t wB) {
  // slide window on C
  for (uint32_t gy = blockIdx.y * blockDim.y + threadIdx.y; gy < hA;
       gy += gridDim.y * blockDim.y) {
    for (uint32_t gx = blockIdx.x * blockDim.x + threadIdx.x; gx < wB;
         gx += gridDim.x * blockDim.x) {
      float value = 0.0f;
      // slide window on A and B
      for (uint32_t offset = 0; offset < wA; offset += BLOCK_SIZE) {
        __shared__ float sA[BLOCK_SIZE * BLOCK_SIZE];
        __shared__ float sB[BLOCK_SIZE * BLOCK_SIZE];
        sA[threadIdx.y * BLOCK_SIZE + threadIdx.x] =
            A[gy * wA + (offset + threadIdx.x)];
        sB[threadIdx.y * BLOCK_SIZE + threadIdx.x] =
            B[(offset + threadIdx.y) * wB + gx];
        __syncthreads();
        for (uint32_t i = 0; i < BLOCK_SIZE; i += 1) {
          value += sA[threadIdx.y * BLOCK_SIZE + i] *
                   sB[i * BLOCK_SIZE + threadIdx.x];
        }
        __syncthreads();
      }
      C[gy * wB + gx] = value;
    }
  }
}

void matrixMul_gpu_3(const float *A, const float *B, float *C, uint32_t hA,
                     uint32_t wA, uint32_t hB, uint32_t wB) {
  uint32_t sizeA = hA * wA * sizeof(float);
  uint32_t sizeB = hB * wB * sizeof(float);
  uint32_t sizeC = hA * wB * sizeof(float);

  // allocate device memory
  float *dev_A = NULL, *dev_B = NULL, *dev_C = NULL;
  HANDLE_ERROR(cudaMalloc(&dev_A, sizeA));
  HANDLE_ERROR(cudaMalloc(&dev_B, sizeB));
  HANDLE_ERROR(cudaMalloc(&dev_C, sizeC));

  // copy from host to device
  HANDLE_ERROR(cudaMemcpy(dev_A, A, sizeA, cudaMemcpyHostToDevice));
  HANDLE_ERROR(cudaMemcpy(dev_B, B, sizeB, cudaMemcpyHostToDevice));

  // real JIT
  clock_t before = clock();
  matrixMul_kernel_3<<<blocksPerGrid, threadsPerBlock>>>(dev_A, dev_B, dev_C,
                                                         hA, wA, hB, wB);
  HANDLE_ERROR(cudaGetLastError());
  HANDLE_ERROR(cudaDeviceSynchronize());
  printf("gpu duration: %ld\n", clock() - before);

  // copy from device to host
  HANDLE_ERROR(cudaMemcpy(C, dev_C, sizeC, cudaMemcpyDeviceToHost));

  // free memory
  HANDLE_ERROR(cudaFree(dev_A));
  HANDLE_ERROR(cudaFree(dev_B));
  HANDLE_ERROR(cudaFree(dev_C));
}

__global__ void matrixMul_kernel_4(const float *A, const float *B, float *C,
                                   uint32_t hA, uint32_t wA, uint32_t hB,
                                   uint32_t wB) {
  // slide window on C
  for (uint32_t gy = blockIdx.y * blockDim.y + threadIdx.y; gy < hA;
       gy += gridDim.y * blockDim.y) {
    for (uint32_t gx = blockIdx.x * blockDim.x + threadIdx.x; gx < wB;
         gx += gridDim.x * blockDim.x) {
      // slide window on A and B
      for (uint32_t offset = 0; offset < wA; offset += BLOCK_SIZE) {
        __shared__ float sA[BLOCK_SIZE * BLOCK_SIZE];
        __shared__ float sB[BLOCK_SIZE * BLOCK_SIZE];
        sA[threadIdx.y * BLOCK_SIZE + threadIdx.x] =
            A[gy * wA + (offset + threadIdx.x)];
        sB[threadIdx.y * BLOCK_SIZE + threadIdx.x] =
            B[(offset + threadIdx.y) * wB + gx];
        __syncthreads();
        for (uint32_t i = 0; i < BLOCK_SIZE; i += 1) {
          C[gy * wB + gx] += sA[threadIdx.y * BLOCK_SIZE + i] *
                             sB[i * BLOCK_SIZE + threadIdx.x];
        }
        __syncthreads();
      }
    }
  }
}

void matrixMul_gpu_4(const float *A, const float *B, float *C, uint32_t hA,
                     uint32_t wA, uint32_t hB, uint32_t wB) {
  uint32_t sizeA = hA * wA * sizeof(float);
  uint32_t sizeB = hB * wB * sizeof(float);
  uint32_t sizeC = hA * wB * sizeof(float);

  // allocate device memory
  float *dev_A = NULL, *dev_B = NULL, *dev_C = NULL;
  HANDLE_ERROR(cudaMalloc(&dev_A, sizeA));
  HANDLE_ERROR(cudaMalloc(&dev_B, sizeB));
  HANDLE_ERROR(cudaMalloc(&dev_C, sizeC));

  // copy from host to device
  HANDLE_ERROR(cudaMemcpy(dev_A, A, sizeA, cudaMemcpyHostToDevice));
  HANDLE_ERROR(cudaMemcpy(dev_B, B, sizeB, cudaMemcpyHostToDevice));

  // real JIT
  clock_t before = clock();
  matrixMul_kernel_4<<<blocksPerGrid, threadsPerBlock>>>(dev_A, dev_B, dev_C,
                                                         hA, wA, hB, wB);
  HANDLE_ERROR(cudaGetLastError());
  HANDLE_ERROR(cudaDeviceSynchronize());
  printf("gpu duration: %ld\n", clock() - before);

  // copy from device to host
  HANDLE_ERROR(cudaMemcpy(C, dev_C, sizeC, cudaMemcpyDeviceToHost));

  // free memory
  HANDLE_ERROR(cudaFree(dev_A));
  HANDLE_ERROR(cudaFree(dev_B));
  HANDLE_ERROR(cudaFree(dev_C));
}

/*********************************************/
/*********************cpu*********************/
/*********************************************/
void matrixMul_cpu(const float *A, const float *B, float *C, size_t hA,
                   size_t wA, size_t hB, size_t wB) {
  if (wA != hB) {
    fprintf(stderr, "matrix error, wA: %ld, hB: %ld\n", wA, hB);
    return;
  }

  clock_t before = clock();
  for (size_t rA = 0; rA < hA; rA++) {
    for (size_t cB = 0; cB < wB; cB++) {
      //
      size_t iC = (rA * wB) + cB;
      C[iC] = 0.0f;

      //
      for (size_t offset = 0; offset < wA; offset++) {
        size_t iA = rA * wA + offset;
        size_t iB = (offset * wB) + cB;

        C[iC] += A[iA] * B[iB];
      }
    }
  }
  printf("cpu duration: %ld\n", clock() - before);
}

float *randMatrix(size_t height, size_t width) {
  size_t size = height * width * sizeof(float);
  float *dst = (float *)malloc(size);

  for (size_t i = 0; i < height * width; i++) {
    dst[i] = (float)rand() / RAND_MAX;
  }

  return dst;
}

bool allClose(float *A, float *B, size_t height, size_t width) {
  for (size_t row = 0; row < height; row++) {
    for (size_t col = 0; col < width; col++) {
      size_t idx = row * width + col;
      if (!isfinite(A[idx]) or !isfinite(B[idx])) {
        fprintf(stderr, "infinite error, idx: %ld\n", idx);
        return false;
      }
      if (fabs(A[idx] - B[idx]) > ERROR_ALLOW) {
        fprintf(stderr, "inequal error, %f != %f, (x, y): (%ld, %ld)\n", A[idx],
                B[idx], col, row);
        return false;
      }
    }
  }
  return true;
}

}; // namespace

void do_benchmark() {
  size_t hA = 8192, wA = 8192, hB = 8192, wB = 8192;

  float *A = randMatrix(hA, wA);
  float *B = randMatrix(hB, wB);
  float *C1 = randMatrix(hA, wB), *C2 = randMatrix(hA, wB),
        *C3 = randMatrix(hA, wB), *C4 = randMatrix(hA, wB),
        *C5 = randMatrix(hA, wB);

  // matrixMul_cpu(A, B, C1, hA, wA, hB, wB);
  matrixMul_gpu_1(A, B, C2, hA, wA, hB, wB);
  matrixMul_gpu_2(A, B, C3, hA, wA, hB, wB);
  matrixMul_gpu_3(A, B, C4, hA, wA, hB, wB);
  matrixMul_gpu_4(A, B, C5, hA, wA, hB, wB);
  // allClose(C1, C2, hA, wB);
  // allClose(C2, C3, hA, wB);
  // allClose(C3, C4, hA, wB);

  free(A);
  free(B);
  free(C1);
  free(C2);
  free(C3);
  free(C4);
  free(C5);

  printf("all down\n");
}

int main() {
  for (size_t i = 0; i < 16; i += 1) {
    do_benchmark();
  }
  return 0;
}

/*
int main() {
  test_cpu_matmul();
  return 0;
}
*/