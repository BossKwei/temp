#include <iostream>
#include <chrono>
#include <thread>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <tuple>
#include <cassert>
#include <functional>
#include <cmath>
#include <queue>
#include <bitset>
#include <unordered_map>
#include <mutex>
#include <memory>
#include <condition_variable>


std::vector<std::string> split(const std::string &s, char sep)
{
    std::vector<std::string> output;
    std::string::size_type prev_pos = 0, pos = 0;

    while ((pos = s.find(sep, pos)) != std::string::npos)
    {
        std::string substring(s.substr(prev_pos, pos - prev_pos));
        output.push_back(substring);
        prev_pos = ++pos;
    }
    output.push_back(s.substr(prev_pos, pos - prev_pos)); // Last word

    return output;
}

template <typename T>
void print_vector1(const std::vector<T> &result)
{
    for (auto &x : result)
    {
        std::cout << x << " ";
    }
    std::cout << std::endl;
}

template <typename T>
void print_vector2(const std::vector<std::vector<T>> &result)
{
    for (auto &line : result)
    {
        for (auto &x : line)
        {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }
}