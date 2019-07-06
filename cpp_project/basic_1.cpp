#include "utils.hpp"


void test_chrono() {
    auto before = std::chrono::system_clock::now();

    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    auto after = std::chrono::system_clock::now();

    std::chrono::duration<double> diff = after - before;

    std::cout << diff.count() << std::endl;
}


void test_next_permutation() {
    std::string s = "aba";
    std::sort(s.begin(), s.end());
    do {
        std::cout << s << '\n';
    } while (std::next_permutation(s.begin(), s.end()));
}


std::vector<std::vector<int>> permute_1(std::vector<int> &nums) {
    std::vector<std::vector<int>> result;
    std::sort(nums.begin(), nums.end());
    do {
        result.push_back(nums);
    } while (std::next_permutation(nums.begin(), nums.end()));
    return result;
}


void test_permute() {
    std::vector<int> input = {1, 2, 3};

    //
    auto result_1 = permute_1(input);
    std::cout << "permute_1():" << std::endl;
    print_vector2(result_1);

}

void test_loop_1() {
    std::vector<int> input = {1, 2, 3};
    for (auto &x : input) {
        if (x == 2) {
            x = 9;
        }
    }
    print_vector1(input);
}


void test_tuple() {
    std::tuple<int, int> pair = std::make_tuple(1, 2);
    int a, b;
    std::tie(a, b) = pair;
    std::cout << a << " " << b << std::endl;
}


std::size_t check_prime(std::size_t n) {
    if (n < 3) {
        return n;
    }

    for (std::size_t i = 2; i < n / 2; i += 1) {
        if (n % i == 0) {
            return i;
        }
    }
    return 0;
}


void bench_cpu() {
    for (std::size_t i = 2; i < 5 * 105943; i += 1) {
        check_prime(i);
    }
}


void test_thread() {
    auto before = std::chrono::system_clock::now();

    std::vector<std::thread> works;
    for (std::size_t i = 0; i < 4; i += 1) {
        works.emplace_back(bench_cpu);
    }
    for (auto &work : works) {
        work.join();
    }

    auto after = std::chrono::system_clock::now();

    std::chrono::duration<double> diff = after - before;

    std::cout << diff.count() << std::endl;
}


std::vector<std::vector<int>> subsets(std::vector<int>& nums) {
}


int searchInsert(std::vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (target < nums[mid]) {
            right = mid - 1;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            return mid;
        }
    }
    return left;
}


void test_dict_1() {
    std::unordered_map<int, size_t> table = {};

    table[2] = 2;
    table[3] = 3;

    auto aa = table[2];

    for (auto &x : table) {
        std::cout << x.first << " " << x.second << std::endl;
    }
}
