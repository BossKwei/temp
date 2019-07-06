#include <array>
#include <chrono>
#include <deque>
#include <functional>
#include <iostream>
#include <numeric>
#include <thread>

template <typename T> class YieldWrapper {
  class iterator {
  public:
    iterator(YieldWrapper<T> &parent) : parent_(parent) {}
    bool operator!=(const iterator &other) const {
      return not parent_.isFinish();
    }
    iterator &operator++() {
      parent_.step();
      return *this;
    }
    T operator*() { return parent_.result(); }

  private:
    YieldWrapper<T> &parent_;
  };

  void step() {
    counter_ += 1;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    if (counter_ == 13) {
      finish_ = true;
    }
  }

  T result() { return counter_; }

public:
  YieldWrapper() : finish_(false), counter_(0) {}
  iterator begin() { return iterator(*this); }
  iterator end() { return iterator(*this); }
  bool isFinish() { return finish_; }

private:
  bool finish_;
  size_t counter_;
};

void increase() {}

int main() {
  for (auto x : YieldWrapper<int>()) {
    std::cout << x << std::endl;
  }
  return 0;
}
