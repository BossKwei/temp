#include <stdio.h>


int add(int a, int b) {
  return a + b;
}

int main(int argc, char **argv) {
  printf("%d\n", add(1, 2));
  return 0;
}
