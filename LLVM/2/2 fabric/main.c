#include <stdio.h>

int factorial_naive(int n) {
    if (n == 1) {
        return 1;
    }
    return n * factorial_naive(n - 1);
}

int factorial_tail(int n, int result) {
    if (n == 1) {
        return result;
    }
    return factorial_tail(n - 1, n * result);
}

int main() {
    printf("naive: %d\n", factorial_naive(3));
    printf("naive: %d\n", factorial_tail(3, 1));
    return 0;
}
