template <typename T, size_t N>
std::shared_ptr<std::array<T, N>> linspace(T start, T end) {
  auto buffer = std::make_shared<std::array<T, N>>();
  T increasement = (end - start) / N;
  for (auto &item : *buffer) {
    item = start;
    start += increasement;
  }
  return buffer;
}

template <typename T, size_t N>
std::shared_ptr<std::array<T, N>> zeros() {
  auto buffer = std::make_shared<std::array<T, N>>();
  for (auto &x : *buffer) {
    x = T(0.0);
  }
  return buffer;
}

template <typename T, size_t N>
std::shared_ptr<std::array<T, N>> randn(T mean = T(0.0), T std = T(1.0)) {
  auto clock = std::chrono::system_clock::now().time_since_epoch();
  std::default_random_engine generator(clock.count());
  std::normal_distribution<T> distribution(mean, std);

  auto buffer = std::make_shared<std::array<T, N>>();
  for (auto &x : *buffer) {
    x = distribution(generator);
  }
  return buffer;
}
